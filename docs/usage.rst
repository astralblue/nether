=====
Usage
=====

What Is Nether?
===============

Nether is the “underworld” substrate where JSON/CBOR documents are published,
filtered, then retrieved in real time.

Subscribing to Documents
========================

Let's say we are interested in all documents that have a value greater than or
equal to 100 at the ``foo.bar`` key, for example this JSON document::

    {"foo":{"bar":120,"baz":150},"quux":200}

Nether uses `asyncio`, so let's import the usual prerequisites first:

>>> from asyncio import Queue, ensure_future, get_event_loop

Then we create a portal into Nether:

>>> from nether import AsyncioPortal
>>> loop = get_event_loop()
>>> portal = AsyncioPortal(loop=loop)

Then plug into it an `~asyncio.Queue` via which to receive the matching docs:

>>> foobar100_queue = Queue()
>>> portal.subscribe("""doc['foo']['bar'] >= 100""", via=foobar100_queue)

Then consume the documents out of the queue from an async method:

>>> from pprint import pprint
>>> async def print_queue(queue):
...     while True:
...         msg = await queue.get()
...         pprint(msg.doc)
...         if msg.doc['quux'] < 100:
...             return

Publishing Documents
====================

Publishing documents is even easier.  Simply put them into the portal's publish
queue:

>>> async def publish_docs(queue):
...     await queue.put({"foo": {"bar": 100, "baz": 150}, "quux": 200})
...     await queue.put({"foo": {"bar": 50, "baz": 25}, "quux": 0})
...     await queue.put({"quux": 30})
...     await queue.put({"foo": {"bar": 250, "baz": 300}, "quux": 20})
>>> ensure_future(enqueue_docs(portal.publish_queue), loop)
>>> loop.run_until_complete()
{'foo': {'bar': 100, 'baz': 150}, 'quux': 200}
{'foo': {'bar': 250, 'baz': 300}, 'quux': 20}

Network Topology
================

Nether portals on the same subnet discover each other using the mDNS service
name “nether”, then connect to each discovered neighbor using unicast.
