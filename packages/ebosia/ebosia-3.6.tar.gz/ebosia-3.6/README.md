Eventbus
========

A library for dealing with getting arbitrary events moving throughout the system

Changelog
=========

3.6
---
3.5 is a bad tag, don't use it, don't download it. It has a pdb.set_trace in the setup.py...

3.5
---
Add async publishing and a bridge to allow async code to correct call ebosia.sync.publish. It's wild and wacky, but it should work

3.4
---
Fix bug with nesting event publishes inside event subscriptions when testing

3.3
---
Automatically serialize UUIDs and datetimes. This means that you can be less careful about what you push through ebosia. No
I don't currently support a custom formatter, sorry, send me a PR

3.2
---
Allow more control when subscribing like specifying the durability and exclusivity. This can be useful for making exchanges
and queues that last longer than the connection to the client

3.1
---
Allow eventbus fixture's published() function to not specify the payload. This is nice if your code emits very large or very complex events
and you don't want to have to fully check that payload in every test

3.0
---
Rename the package to ebosia so that I can publish on PyPI

2.3
---
Fix synchronous subscription. I had broken it in some previous update

2.2
---
Allow publishing enums as event topics. This modifies the default JSON serializer a bit so that it attempts to
convert anything passed through to a string which is nice for items coming out of a database

2.1
---
Automatically retry on connection failure when synchronously publishing. Also fix the sync-emitter script. And include it on installation

2.0
---
Update kombo package to 3.0.34

1.9
---
Make heartbeat default to 60 seconds but configurable to whatever you want

1.8
---

Add default heartbeat for async connections of 60 seconds.

1.7
---

Add reconnect logic for async subscribers. Subscribers now need to supply `on_reconnect` when calling `connect`. `on_reconnect` should be a coroutine that sets up the subscriptions whenever a reconnection is made

1.6
---

Make the connection stateful in the global state. Whenever a connection is made we'll keep it in a global location so that clients can get it via ebosia.get(). This means a client doesn't need to pass the connection around everywhere
