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


class ClassCommandDefinitionError(PepperBotBaseException):
    """未按照commandClass规范定义命令类，导致的异常"""

    pass


class PatternFormotError(PepperBotBaseException):
    pass


class PatternValidateError(PepperBotBaseException):
    pass


class ClassCommandOnFinish(PepperBotBaseException):

    pass


class ClassCommandOnExit(PepperBotBaseException):

    pass


class ClassCommandOnTimeout(PepperBotBaseException):

    pass


class EventHandlerDefineError(PepperBotBaseException):

    pass


class InitializationError(PepperBotBaseException):
    pass

class EventHandleError(PepperBotBaseException):
    pass 

class BackendApiError(PepperBotBaseException):
    pass
