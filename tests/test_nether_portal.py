from asyncio import Queue, get_event_loop, new_event_loop
from unittest.mock import patch

from pytest import fixture, raises

from nether.portal.asyncio import AsyncioPortal


class TestAsyncioPortal:
    @fixture
    def loop(self):
        return new_event_loop()

    @fixture
    def portal(self):
        portal = AsyncioPortal()
        yield portal
        portal.close()

    def test_takes_and_avails_event_loop(self, loop):
        assert AsyncioPortal(loop=loop).loop is loop

    def test_no_loop_means_default_event_loop(self):
        assert AsyncioPortal().loop is get_event_loop()

    def test_with_asyncio_raises_typeerror_for_invalid_loop(self):
        loop = object()
        with raises(TypeError) as e:
            AsyncioPortal(loop=loop)
        assert (str(e.value) ==
                "{!r} is not an asyncio event loop".format(loop))

    def test_publish_queue_returns_asyncio_queue(self, portal):
        assert isinstance(portal.publish_queue, Queue)

    def test_context_manager(self):
        portal = AsyncioPortal()
        with patch.object(portal, 'close', side_effect=portal.close) as close:
            with portal as portal_entered:
                assert portal is portal_entered
        assert close.called
