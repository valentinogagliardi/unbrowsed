"""unbrowsed resolvers."""

from typing import Optional
from selectolax.lexbor import LexborNode


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
