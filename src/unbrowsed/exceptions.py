"""unbrowsed exceptions."""


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, alt_method):
        self.text = text
        self.count = count
        self.alt_method = alt_method
        super().__init__(
            f"Found {count} elements with '{text}'. "
            f"Use {alt_method} if multiple matches are expected."
        )

    def __reduce__(self):
        return (
            MultipleElementsFoundError,
            (self.text, self.count, self.alt_method),
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, text, alt_method):
        self.text = text
        self.alt_method = alt_method
        super().__init__(
            f"No elements found with '{text}'. "
            f"Use {alt_method} if expecting no matches."
        )

    def __reduce__(self):
        return (
            NoElementsFoundError,
            (self.text, self.alt_method),
        )
