"""unbrowsed resolvers."""

from typing import Optional
from selectolax.lexbor import LexborNode
from unbrowsed.types import ImplicitRoleMapping


class AccessibleNameResolver:

    @staticmethod
    def resolve(node: LexborNode) -> Optional[str]:
        labelledby = node.attributes.get("aria-labelledby")
        if labelledby:
            root = node
            while root.parent:
                root = root.parent

            name_texts = []
            for id_ref in labelledby.split():
                if element := root.css_first(f"#{id_ref}"):
                    text = element.text(deep=True, strip=True)
                    if text:
                        name_texts.append(text)

            if name_texts:
                return " ".join(name_texts)

        if aria_label := node.attributes.get("aria-label"):
            aria_label = aria_label.strip()
            if aria_label:
                return aria_label

        if node.tag == "fieldset":
            if legend := node.css_first("legend"):
                return legend.text(deep=True, strip=True)

        if node.tag in ["input", "textarea", "select"] and node.attributes.get(
            "id"
        ):
            element_id = node.attributes.get("id")
            root = node
            while root.parent:
                root = root.parent

            if label := root.css_first(f"label[for='{element_id}']"):
                return label.text(deep=True, strip=True)

        if node.tag == "img" and node.attributes.get("alt"):
            return node.attributes.get("alt", "").strip()  # type: ignore

        if node.tag in ["button", "a", "h1", "h2", "h3", "h4", "h5", "h6"]:

            if (
                node.tag == "a"
                and (img := node.css_first("img"))
                and img.attributes.get("alt")
            ):
                alt_text = img.attributes.get(
                    "alt", ""
                ).strip()  # type: ignore
                node_text = node.text(deep=True, strip=True)
                if node_text:
                    return f"{alt_text} {node_text}"
                return alt_text

            content = node.text(deep=True, strip=True)
            if content:
                return content

        if title := node.attributes.get("title"):
            if title.strip():
                return title.strip()

        return None


class AccessibleDescriptionResolver:
    @staticmethod
    def resolve(node: LexborNode) -> Optional[str]:
        describedby = node.attributes.get("aria-describedby")
        if not describedby:
            return None

        root = node
        while root.parent:
            root = root.parent

        description_texts = []
        for id_ref in describedby.split():
            if element := root.css_first(f"#{id_ref}"):
                text = element.text(deep=True, strip=True)
                if text:
                    description_texts.append(text)

        if description_texts:
            return " ".join(description_texts)

        return None


class RoleResolver:

    def __init__(
        self,
        target_role: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.target_role = target_role.lower()
        self.name = name
        self.description = description

    @staticmethod
    def get_implicit_role_mapping() -> ImplicitRoleMapping:
        return {
            "a": RoleResolver.get_a_role,
            "article": "article",
            "aside": "complementary",
            "address": "group",
            "b": "generic",
            "button": "button",
            "fieldset": "group",
            "form": "form",
            "img": RoleResolver.get_img_role,
            "input": {
                "checkbox": "checkbox",
                "radio": "radio",
                "text": "textbox",
                "search": "searchbox",
                "button": "button",
                "password": "textbox",
            },
            "textarea": "textbox",
            "select": RoleResolver.get_select_role,
            "nav": "navigation",
            "main": "main",
            "meter": "meter",
            "header": "banner",
            "footer": "contentinfo",
            "h1": "heading",
            "h2": "heading",
            "h3": "heading",
            "h4": "heading",
            "h5": "heading",
            "h6": "heading",
            "ul": "list",
            "ol": "list",
            "td": RoleResolver.get_td_role,
        }

    def matches(self, node: LexborNode) -> bool:

        explicit_role = node.attributes.get("role")
        implicit_role = RoleResolver.get_implicit_role(node)

        role_matches = False
        if (explicit_role and explicit_role.lower() == self.target_role) or (
            implicit_role and implicit_role.lower() == self.target_role
        ):
            role_matches = True

        if not role_matches:
            return False

        if self.name is not None:
            node_name = AccessibleNameResolver.resolve(node)
            if node_name != self.name:
                return False

        if self.description is not None:
            node_description = AccessibleDescriptionResolver.resolve(node)
            if node_description != self.description:
                return False

        return True

    @staticmethod
    def get_implicit_role(node: LexborNode):
        if not hasattr(node, "tag"):
            return
        tag = node.tag
        if not tag:
            return
        handler = RoleResolver.get_implicit_role_mapping().get(
            tag  # type: ignore
        )

        if callable(handler):
            return handler(node)
        if isinstance(handler, dict):
            input_type = node.attributes.get("type", "")
            return handler.get(input_type)
        return handler if isinstance(handler, str) else None

    @staticmethod
    def get_td_role(node: LexborNode) -> str:
        """Determine the role of a td element."""
        ancestor = node.parent
        while ancestor and ancestor.tag != "table":
            ancestor = ancestor.parent

        if not ancestor:
            return ""

        table_role = ancestor.attributes.get("role")

        if not table_role:
            return "cell"

        table_role = table_role.lower()
        if table_role == "table":
            return "cell"
        elif table_role in ["grid", "treegrid"]:
            return "gridcell"

        return ""

    @staticmethod
    def get_img_role(node: LexborNode) -> str:
        """Determine the role of an img element."""
        if "alt" in node.attributes:
            alt = node.attributes.get("alt")
            if alt == "":
                return "presentation"
            return "img"
        if "alt" not in node.attributes and not (
            AccessibleNameResolver.resolve(node)
            or AccessibleDescriptionResolver.resolve(node)
        ):
            return "presentation"
        return "img"

    @staticmethod
    def get_select_role(node: LexborNode) -> str:
        """Determine the role of a select element."""
        if "multiple" in node.attributes:
            return "listbox"
        if (
            "size" in node.attributes
            and node.attributes.get("size", None) is not None
        ):
            if int(node.attributes.get("size")) > 1:  # type: ignore
                return "listbox"
        return "combobox"

    @staticmethod
    def get_a_role(node: LexborNode) -> str:
        """Determine the role of an element"""
        if "href" in node.attributes:
            return "link"
        return "generic"
