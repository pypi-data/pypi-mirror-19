import datetime
import logging
from typing import Any, Generator, Iterable, List, Optional


class Logger(object):

    def __init__(self, name: str, level: str) -> None:
        super().__init__()
        self._logger = logging.getLogger(name)
        self._level = level
        self._parts = []

    def __lshift__(self, part: Any) -> 'Logger':
        self._parts.append(str(part))
        return self

    def __del__(self) -> None:
        msg = ' '.join(self._parts)
        log = getattr(self._logger, self._level)
        log(msg)


def DEBUG(name: str) -> Logger:
    return Logger(name, 'debug')


def INFO(name: str) -> Logger:
    return Logger(name, 'info')


def WARNING(name: str) -> Logger:
    return Logger(name, 'warning')


def ERROR(name: str) -> Logger:
    return Logger(name, 'error')


def CRITICAL(name: str) -> Logger:
    return Logger(name, 'critical')


def EXCEPTION(name: str) -> Logger:
    return Logger(name, 'exception')


def setup(log_name_list: Iterable[str], file_path: str = None) -> List[logging.Logger]:
    formatter = logging.Formatter('{asctime}|{threadName:_<10.10}|{levelname:_<8}|{message}', style='{')
    handler = create_handler(file_path, formatter)
    loggers = [create_logger(name, handler) for name in log_name_list]
    return loggers


def create_handler(path: Optional[str], formatter: logging.Formatter) -> logging.Handler:
    if path:
        # alias
        TRFHandler = logging.handlers.TimedRotatingFileHandler
        # rotate on Sunday
        handler = TRFHandler(path, when='w6', atTime=datetime.time())
    else:
        handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    return handler


def create_logger(name: str, handler: logging.Handler) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
