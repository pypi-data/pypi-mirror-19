Fake Listener and Auth Server Reference Implementation
======================================================

Requirements
------------

1. Python >= 3.5 (new asyncio syntax)
2. PyCryptodome

Installation
------------
::

   pip install c3-reference

Running the Listener Simulation / Traffic Generator
---------------------------------------------------

Start listener with 1 beacon, send reports to UDP 127.0.0.1:9999 :

::

      listener

Listener simulating 500 beacons, send reports to google.com:35309 :

::

      listener -nb 500 --server google.com --port 35309


Running the reference Authentication Server
-------------------------------------------

::

      authserver

The auth server listens on 0.0.0.0:9999 and decodes and verifies any
rx'd packets from the listener simulation *or* real listeners.
