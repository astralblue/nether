# -*- coding: utf-8 -*-

from asyncio import (AbstractEventLoop, Queue,
                     get_event_loop, run_coroutine_threadsafe)
from asyncio.tasks import ensure_future

from zeroconf import ServiceBrowser, Zeroconf


class AsyncioPortal:
    def __init__(self, *args, **kwargs):
        """
        Create and return a new Nether portal.

        :param loop:
            the `asyncio` event loop in which this portal runs.  If `None`
            (default), use the main event loop as returned by
            `~asyncio.get_event_loop()`.
        :param `~zeroconf.Zeroconf` zeroconf:
            the Zeroconf engine to use for discovering services.  If `None`
            (default), create a new instance and use it.
        :return:
            the newly created Nether portal.
        :rtype:
            `Portal`
        """
        try:
            loop = kwargs.pop('loop')
        except KeyError:
            loop = get_event_loop()
        if not isinstance(loop, AbstractEventLoop):
            raise TypeError("{!r} is not an asyncio event loop".format(loop))
        try:
            zeroconf = kwargs.pop('zeroconf')
        except KeyError:
            zeroconf = Zeroconf()
        if not isinstance(zeroconf, Zeroconf):
            raise TypeError('zeroconf {!r} is not an instance of Zeroconf'
                            .format(zeroconf))
        super().__init__(*args, **kwargs)
        self.__loop = loop
        self.__browser = ServiceBrowser(zeroconf, '_nether._tcp.local.',
                                        [self])
        self.__publish_queue = Queue()
        self.__task = ensure_future(self.__run(), loop=loop)

    @property
    def loop(self):
        """Event loop in which this portal runs."""
        return self.__loop

    @property
    def publish_queue(self):
        """`asyncio.Queue()` to use for publishing documents."""
        return self.__publish_queue

    def __add_zeroconf_service(self, zeroconf, typ, nam):
        info = zeroconf.get_service_info(typ, nam)
        run_coroutine_threadsafe(self.__add_service(info))

    def remove_service(self, zeroconf, typ, nam):
        run_coroutine_threadsafe(self.__remove_service(info))

    async def __run(self):
        pass

    def close(self):
        """Close the portal."""
        # TODO implement

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class _PortalZeroconfListener:
    def __init__(self, *args, **kwargs):
        portal = kwargs.pop('portal')
        if not isinstance(portal, Portal):
            raise TypeError('portal {!r} is not an instance of Portal'
                            .format(portal))
        super().__init__(*args, **kwargs)
        self.__portal = portal

    def add_service(self, zeroconf, typ, nam):
        run_coroutine_threadsafe(
            self.__portal.__add_zeroconf_service(typ, nam))

    def remove_service(self, zeroconf, typ, nam):
        run_coroutine_threadsafe(
            self.__portal.__remove_zeroconf_service(typ, nam))
