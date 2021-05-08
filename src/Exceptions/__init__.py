class PepperBotBaseException(Exception):
    pass


class EmptySelectionException(PepperBotBaseException):
    pass


class PermissionError(PepperBotBaseException):
    pass


class NotRunnableError(PepperBotBaseException):
    # todo 定义的所有Exception，都应有trace
    pass


class CatchException(PepperBotBaseException):
    pass
