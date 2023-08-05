
CHANGES
=======

0.30
----

*   Added ``Signal.afire()`` method that returns awaitable to support
    coroutine-based signal handlers
*   Dropped Python 2.6 and 3.2 support

0.22
----

*   Added `Watchman` class as a testing helper

0.21
----

*   Removed distribute dependency
*   Improved tests

0.20
----

*   Changed handler subscription mechanism from subscription by reference to
    subscription by weak reference

0.11
----

*   Fixed logger loose on program termination

0.1
---

*   Initial release
