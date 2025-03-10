"""unbrowsed exceptions."""


class MultipleElementsFoundError(AssertionError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __reduce__(self):
        return (
            MultipleElementsFoundError,
            (self.message,),
        )


class NoElementsFoundError(AssertionError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __reduce__(self):
        return (
            NoElementsFoundError,
            (self.message,),
        )
