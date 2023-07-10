from typing import Union


class AnovaPrecisionOvenError(Exception):
    def __init(self, msg: str):
        super().__init__(msg)

class APIError(AnovaPrecisionOvenError):
    def __init__(self, error: str):
        super().__init__("Anova api error: {}".format(error))

class AccessDeniedError(AnovaPrecisionOvenError):
    def __init__(
        self, 
        resource: str,
        error: Union[str, None] = None,
        message: Union[str, None] = None,
    ):
        self.resource: str = resource
        self.error: Union[str, None] = error
        self.message: Union[str, None] = message
        msg = "Access denied for resource {}".format(resource)
        if error is not None:
            if message is not None:
                msg = "{}: {}: {}".format(msg, error, message)
            else:
                msg = "{}: {}".format(msg, error)
        super().__init__(msg)

class OvenUnreachableError(AnovaPrecisionOvenError):
    def __init__(self, reason: Union[str, None] = None):
        msg = "Oven is unreachable"
        self.reason: Union[str, None] = reason
        if reason is not None:
            msg = "{}: {}".format(msg, reason)
        super().__init__(msg)