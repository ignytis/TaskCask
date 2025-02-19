from abc import ABC, abstractmethod
from functools import cmp_to_key
from typing import Type

from .types import BaseEvent
from ..utils.reflection import get_all_subclasses

_listeners: dict[Type["BaseListener"], list["BaseListener"]] = {}


class BaseListener(ABC):
    @classmethod
    @abstractmethod
    def get_priority(cls) -> int:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, e: BaseEvent) -> int:
        raise NotImplementedError()

    @classmethod
    def register_listeners(cls) -> None:
        global _listeners
        _listeners[cls] = []
        for sub_cls in get_all_subclasses(cls):
            _listeners[cls].append(sub_cls())

        _listeners[cls] = sorted(_listeners[cls], key=cmp_to_key(lambda a, b: a.get_priority() - b.get_priority()))

    @classmethod
    def process_event(cls, e: BaseEvent):
        for listener in _listeners[cls]:
            listener.handle(e)


class BaseTaskPreExecuteListener(BaseListener):
    pass


class BaseTaskPostExecuteListener(BaseListener):
    pass
