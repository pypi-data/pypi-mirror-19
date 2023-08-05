Fake Listener and Auth Server Reference Implementation
======================================================

Installation
------------

pip install pycryptodome

*or*

easy\_install pycryptodome

Running the fake listener
-------------------------

Start listener with 1 beacon, send reports to UDP 127.0.0.1:9999 :

::

      python listener.py

Listener simulating 500 beacons, send reports to google.com:35309 :

::

      python listener.py -nb 500 --server google.com --port 35309

Running the auth server
-----------------------

::

      python authserver.py

The auth server listens on 127.0.0.1:9999 and decodes and verifies any
rx'd packets.
