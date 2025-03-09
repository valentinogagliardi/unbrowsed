"""unbrowsed matchers."""


class TextMatch:
    """Wrapper class for text matching."""

    def __init__(self, text: str, exact=True) -> None:
        self.text = text.strip()
        self.exact = exact

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        if not self.exact:
            return self.text.lower() in other.lower()
        return self.text == other
