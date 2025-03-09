"""unbrowsed exceptions."""


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, suggested_method):
        super().__init__(
            f"Found {count} elements with '{text}'. "
            f"Use {suggested_method} if multiple matches are expected."
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, text, suggested_method):
        super().__init__(
            f"No elements found with '{text}'. "
            f"Use {suggested_method} if expecting no matches."
        )
