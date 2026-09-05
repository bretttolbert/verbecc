import warnings


class NonApiWarning():
    @staticmethod
    def warn() -> None:
        # stacklevel=2 shows the line of code that CALLED this function, rather than this line itself
        warnings.warn(
            "This method is not part of the public API and may change or be removed without notice.",
            category=UserWarning,
            stacklevel=2
        )
