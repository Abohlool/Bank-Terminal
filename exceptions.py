class InputError(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.msg = message


class TransactionError(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.msg = message


class WrongInformationError(ValueError):
    def __init__(self, message):
        super().__init__(self, message)
        self.msg = message


class CorrectInput(ValueError):
    pass


class Back(ValueError):
    pass


class Exit(ValueError):
    pass
