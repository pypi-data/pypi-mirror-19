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

"""Storage tests."""

from __future__ import absolute_import, print_function

from os.path import exists

import pytest

from invenio_xrootd import EOSFileStorage, SizeRequiredError, \
    XRootDFileStorage, eos_storage_factory, xrootd_storage_factory


def test_version():
    """Test version import."""
    from invenio_xrootd import __version__
    assert __version__


def test_init(file_url):
    """Test checksum overwrite."""
    assert XRootDFileStorage(file_url).checksum_algo is None
    assert EOSFileStorage(file_url).checksum_algo is None


def test_init_app(app, file_url):
    """Test checksum overwrite."""
    assert XRootDFileStorage(file_url).checksum_algo == 'md5'
    assert EOSFileStorage(file_url).checksum_algo == 'md5'


def test_factory(file_instance_mock):
    """Test factory functions."""
    assert isinstance(
        xrootd_storage_factory(fileinstance=file_instance_mock),
        XRootDFileStorage
    )
    assert isinstance(
        eos_storage_factory(fileinstance=file_instance_mock),
        EOSFileStorage
    )


def test_checksum_fallback(xrd_storage, eos_storage, file_md5):
    """Test checksum."""
    assert xrd_storage.checksum() == 'md5:{0}'.format(file_md5)
    assert eos_storage.checksum() == 'md5:{0}'.format(file_md5)


def test_checksum_xrd(xrd_storage_mocked, file_md5):
    """Test checksum."""
    assert xrd_storage_mocked.checksum() == 'adler32:{0}'.format(file_md5)


def test_checksum_xrd_overwrite(app, xrd_storage_mocked, file_md5):
    """Test checksum."""
    assert xrd_storage_mocked.checksum() == 'md5:{0}'.format(file_md5)


def test_checksum_ospath(xrd_storage_ospath, file_md5):
    """Test checksum overwrite."""
    assert xrd_storage_ospath.checksum() == 'md5:{0}'.format(file_md5)


def test_get_fs(xrd_storage, file_path, file_url):
    """Test checksum overwrite."""
    assert not exists(file_path)
    xrd_storage.initialize(10)
    assert exists(file_path)


def test_get_fs_ospath(xrd_storage_ospath, file_path):
    """Test checksum overwrite."""
    assert not exists(file_path)
    xrd_storage_ospath.initialize(10)
    assert exists(file_path)


def test_eos_initialize(eos_storage, file_path, file_url):
    """Test checksum overwrite."""
    assert not exists(file_path)
    eos_storage.initialize(size=10)
    assert exists(file_path)
    # Check parameter passing
    eos_storage.initialize(10)
    # Size required.
    pytest.raises(
        SizeRequiredError,
        eos_storage.initialize
    )


def test_eos_save(eos_storage, file_path, file_url, BytesIO):
    """Test checksum overwrite."""
    assert not exists(file_path)
    pytest.raises(
        SizeRequiredError,
        eos_storage.save,
        BytesIO(b'test')
    )
    assert not exists(file_path)
    eos_storage.save(BytesIO(b'test'), size=4)
    assert exists(file_path)


def test_eos_default_bookingsize(app, eos_storage, file_path, file_url,
                                 BytesIO):
    """Test checksum overwrite."""
    max_len = app.config['MAX_CONTENT_LENGTH']
    assert eos_storage.default_booking_size == max_len
    assert eos_storage.save(BytesIO(b'test'))
    assert exists(file_path)
    eos_storage.save(BytesIO(b'a' * (max_len + 1)), size=max_len + 1)
    assert exists(file_path)
