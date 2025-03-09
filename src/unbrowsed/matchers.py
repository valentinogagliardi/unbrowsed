"""unbrowsed matchers."""

from selectolax.lexbor import LexborNode

IMPLICIT_ROLES = {
    "a": lambda node: "link" if "href" in node.attributes else None,
    "button": "button",
    "img": "img",
    "input": {
        "checkbox": "checkbox",
        "radio": "radio",
        "text": "textbox",
    },
    "textarea": "textbox",
    "select": "combobox",
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
}


class RoleMatcher:
    """Matcher for ARIA roles."""

    def __init__(self, target_role: str):
        self.target_role = target_role.lower()

    def matches(self, node: LexborNode) -> bool:
        implicit_role = RoleMatcher.get_implicit_role(node)
        return implicit_role and implicit_role.lower() == self.target_role

    @staticmethod
    def get_implicit_role(node: LexborNode):
        tag = node.tag
        if not tag:
            return None
        handler = IMPLICIT_ROLES.get(tag)

        if callable(handler):
            return handler(node)
        if isinstance(handler, dict):
            if tag == "input":
                input_type = node.attributes.get("type", "")
                return handler.get(input_type)
        return handler if isinstance(handler, str) else None


class TextMatch:
    """Wrapper class for text matching."""

    def __init__(self, text: str, exact=True) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        self.text = text.strip()
        self.exact = exact

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        if not self.exact:
            return self.text.lower() in other.lower()
        return self.text == other
