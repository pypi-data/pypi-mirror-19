Installation
============

Install from PyPI::

    pip install invenio-xrootd

.. note::

   Invenio-XRootD is dependent on
   `XRootDPyFS <http://xrootdpyfs.readthedocs.io/>`_ and the XRootD Python
   bindings which are compatible with Python 2.7 only, and which can be
   somewhat difficult to install. Please consult the XRootDPyFS installation
   guide for further details.


Running tests
-------------
The easiest way of running the tests is via Docker due to the difficulties in
installing the Python XRootD bindings locally:

.. code-block:: console

   $ docker build -t xrootd . && docker run -h xrootdhost -it xrootd
