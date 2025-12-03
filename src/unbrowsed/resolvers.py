"""unbrowsed resolvers."""

from typing import Optional
from selectolax.lexbor import LexborNode
from unbrowsed.types import ImplicitRoleMapping


class AccessibleNameResolver:

    def __init__(self, element):
        self.element = element

    def resolve(self) -> Optional[str]:
        node = self.element
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

            return node.text(deep=True, strip=True)

        if title := node.attributes.get("title"):
            if title.strip():
                return title.strip()

        return None


class AccessibleDescriptionResolver:
    def __init__(self, element):
        self.element = element

    def resolve(self) -> Optional[str]:
        node = self.element
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
        element: LexborNode,
        target_role: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.element = element
        self.target_role = target_role.lower()
        self.name = name
        self.description = description

    def get_implicit_role_mapping(self) -> ImplicitRoleMapping:
        return {
            "a": self.get_a_role,
            "address": "group",
            "article": "article",
            "aside": "complementary",
            "b": "generic",
            "body": "generic",
            "button": "button",
            "fieldset": "group",
            "footer": self.get_footer_role,
            "form": "form",
            "h1": "heading",
            "h2": "heading",
            "h3": "heading",
            "h4": "heading",
            "h5": "heading",
            "h6": "heading",
            "header": "banner",
            "html": "document",
            "img": self.get_img_role,
            "input": {
                "checkbox": "checkbox",
                "radio": "radio",
                "text": "textbox",
                "search": "searchbox",
                "button": "button",
                "password": "textbox",
            },
            "main": "main",
            "meter": "meter",
            "nav": "navigation",
            "ol": "list",
            "p": "paragraph",
            "select": self.get_select_role,
            "td": self.get_td_role,
            "textarea": "textbox",
            "ul": "list",
        }

    def matches(self) -> bool:

        explicit_role = self.element.attributes.get("role")
        implicit_role = self.get_implicit_role_handler()

        role_matches = False
        if (explicit_role and explicit_role.lower() == self.target_role) or (
            implicit_role and implicit_role.lower() == self.target_role
        ):
            role_matches = True

        if not role_matches:
            return False

        if self.name is not None:
            node_name = AccessibleNameResolver(self.element).resolve()
            if node_name != self.name:
                return False

        if self.description is not None:
            node_description = AccessibleDescriptionResolver(
                self.element
            ).resolve()
            if node_description != self.description:
                return False

        return True

    def get_implicit_role_handler(self):
        tag = self.element.tag
        handler = self.get_implicit_role_mapping().get(tag)  # type: ignore

        if callable(handler):
            return handler()
        if isinstance(handler, dict):
            input_type = self.element.attributes.get("type", "")
            return handler.get(input_type)
        return handler if isinstance(handler, str) else None

    def get_td_role(self) -> str:
        """
        Determine the implicit role of a <td> element.
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td#technical_summary
        """
        ancestor = self.element.parent
        while ancestor and ancestor.tag != "table":
            ancestor = ancestor.parent

        table_role = ancestor.attributes.get("role")  # type: ignore

        if not table_role:
            return "cell"

        table_role = table_role.lower()
        if table_role == "table":
            return "cell"
        elif table_role in ["grid", "treegrid"]:
            return "gridcell"

        return ""

    def get_img_role(self) -> str:
        """
        Determine the implicit role of an <img> element.
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#technical_summary
        """
        if "alt" in self.element.attributes:
            alt = self.element.attributes.get("alt")
            if alt == "":
                return "presentation"
            return "img"
        if "alt" not in self.element.attributes and not (
            AccessibleNameResolver(self.element).resolve()
            or AccessibleDescriptionResolver(self.element).resolve()
        ):
            return "presentation"
        return "img"

    def get_select_role(self) -> str:
        """
        Determine the implicit role of a <select> element.
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#technical_summary
        """
        if "multiple" in self.element.attributes:
            return "listbox"
        if (
            "size" in self.element.attributes
            and self.element.attributes.get("size", None) is not None
        ):
            if int(self.element.attributes.get("size")) > 1:  # type: ignore
                return "listbox"
        return "combobox"

    def get_a_role(self) -> str:
        """
        Determine the implicit role of an <a> element.
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#technical_summary
        """
        if "href" in self.element.attributes:
            return "link"
        return "generic"

    def get_footer_role(self) -> str:
        """
        Determine the implicit role of a <footer> element.
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/footer#technical_summary
        """
        parent = self.element.parent

        if parent is not None:
            if parent.tag in [
                "article",
                "aside",
                "main",
                "nav",
                "section",
            ] or parent.css_first(
                ":is([role='article'],"
                "[role='complementary'],"
                "[role='main'],"
                "[role='navigation'],"
                "[role='region'])"
            ):
                return "generic"

        return "contentinfo"
