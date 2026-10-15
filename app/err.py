import logging

logger = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 500

    def __init__(self, msg: str, *, log: bool = True):
        self.msg = msg
        super().__init__(msg)

        if log:
            logger.warning("%s: %s", self.__class__.__name__, msg)


class NotFound(AppError):
    status_code = 404


class EmailAlreadyExists(AppError):
    status_code = 409


class InsufficientStock(AppError):
    status_code = 400