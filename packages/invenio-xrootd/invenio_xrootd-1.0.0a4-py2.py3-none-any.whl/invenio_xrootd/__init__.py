# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

r"""XRootD file storage support for Invenio.

This modules provide an Invenio file storage interface for XRootD. By default
Invenio already has support for XRootD via
`PyFilesytem <http://docs.pyfilesystem.org/en/latest/>`_  and the
`XRootDPyFS <http://xrootdpyfs.readthedocs.io/>`_ package. This module
adds optimization and performance improvements such as efficient checksum
calculations.

Using this module is as simple as configuring your Invenio instance to
use the storage factory:

.. code-block:: python

   # config.py
   FILES_REST_STORAGE_FACTORY = \
       'invenio_xrootd:xrootd_storage_factory'

The module also provides a file storage interface for CERN EOS disk storage
system via XRootD protocol.

Using the EOS file storage module is as easy as configuring:

.. code-block:: python

   # config.py
   FILES_REST_STORAGE_FACTORY = \
       'invenio_xrootd:eos_storage_factory'

Overwriting reported checksum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XRootD v3.x only has support for reporting adler32 as the used checksum
algorithm, even though the server might be providing e.g. an MD5 checksum. If
this is the case, you can overwrite the reported checksum using the
configuration variable ``XROOTD_CHECKSUM_ALGO``:

.. code-block:: python

   # config.py
   XROOTD_CHECKSUM_ALGO = 'md5'

Kerberos authentication
~~~~~~~~~~~~~~~~~~~~~~~
If your XRootD server requires Kerberos authentication (e.g. CERN EOS), then
you can run a tool such as
`k5start <https://www.eyrie.org/~eagle/software/kstart/k5start.html>`_ on each
client node in order to obtain a Kerberos ticket and continue keeping the
ticket valid. The XRootD python bindings will transparently use this Kerberos
ticket to authenticate against your server.
"""

from __future__ import absolute_import, print_function

from .errors import SizeRequiredError
from .storage import EOSFileStorage, XRootDFileStorage, eos_storage_factory, \
    xrootd_storage_factory
from .version import __version__

__all__ = (
    '__version__',
    'eos_storage_factory',
    'EOSFileStorage',
    'SizeRequiredError',
    'xrootd_storage_factory',
    'XRootDFileStorage',
)
