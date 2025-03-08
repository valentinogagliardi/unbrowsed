class TextMatch:
    """Wrapper class for text matching."""

    def __init__(self, text: str, exact=True):
        self.text = text.strip()
        self.exact = exact

    def __eq__(self, other: str):
        if not self.exact:
            return self.text.lower() in other.lower()
        return self.text == other