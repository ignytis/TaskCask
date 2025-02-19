from unittest import TestCase

from taskcask.events.listeners import BaseListener
from taskcask.events.types import BaseEvent


class MockEvent(BaseEvent):
    val: list[int] = []


class MockAbstractEventListener(BaseListener):
    pass


class MockEventListenerA(MockAbstractEventListener):
    def handle(self, e: MockEvent):
        e.val.append("b")

    def get_priority(cls) -> int:
        return 10


class MockEventListenerB(MockAbstractEventListener):
    def handle(self, e: MockEvent):
        e.val.append("c")

    def get_priority(cls) -> int:
        return 50


class MockEventListenerC(MockAbstractEventListener):
    def handle(self, e: MockEvent):
        e.val.append("a")

    def get_priority(cls) -> int:
        return 2


class MockEventListenerD:
    """An irrelevant listener"""
    def handle(self, e: MockEvent):
        e.val.append("d")

    def get_priority(cls) -> int:
        return 1


class ListenersTest(TestCase):
    def test_listener_exec_order(self) -> None:
        MockAbstractEventListener.register_listeners()

        e = MockEvent()
        MockAbstractEventListener.process_event(e)
        self.assertEqual(["a", "b", "c"], e.val)
