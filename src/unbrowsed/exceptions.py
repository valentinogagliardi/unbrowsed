"""unbrowsed exceptions."""


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, alt_method):
        super().__init__(
            f"Found {count} elements with '{text}'. "
            f"Use {alt_method} if multiple matches are expected."
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, text, alt_method):
        super().__init__(
            f"No elements found with '{text}'. "
            f"Use {alt_method} if expecting no matches."
        )
