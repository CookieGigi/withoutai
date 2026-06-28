from typing import Self

import structlog

from configuration import Config


class LoggerService:
    _config: Config
    _logger: structlog.BoundLogger

    def __init__(self, config: Config) -> None:
        self._logger = structlog.getLogger(service=config.name)
        self._config = config

    def bind(self, **kwargs) -> Self:
        cls = type(self)
        new = cls.__new__(cls)
        new._logger = self._logger.bind(**kwargs)
        new._config = self._config
        return new

    def unbind(self, *keys: str) -> Self:
        cls = type(self)
        new = cls.__new__(cls)
        new._logger = self._logger.unbind(*keys)
        new._config = self._config
        return new

    def debug(self, event: str, **kwargs):
        self._logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs):
        self._logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs):
        self._logger.warning(event, **kwargs)

    def error(self, event: str, exc_info: bool = False, **kwargs):
        self._logger.error(event, exc_info=exc_info, **kwargs)

    def exception(self, event: str, **kwargs):
        self._logger.exception(event, **kwargs)
