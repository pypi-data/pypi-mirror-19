
==========================
Incident Command Utilities
==========================

This is a simple toolkit of utilities that make my on-call life easier.

Tools
=====

scan-hipchat-room
-----------------
::

   scan-hipchat-room START END ROOM [ROOM...]

**START**
   The earliest time to fetch messages from.  IOW, the starting date.

**END**
   The latest time to fetch messages from.  IOW, the ending date.

**ROOM**
   One or more room names to fetch messages from.

This utility writes the JSON formatted messages to the standard output stream.


Environment Variables
=====================

HIPCHAT_TOKEN
-------------
API token to use when talking to the `HipChat API`_.

.. _HipChat API: https://developer.atlassian.com/hipchat/guide/hipchat-rest-api


