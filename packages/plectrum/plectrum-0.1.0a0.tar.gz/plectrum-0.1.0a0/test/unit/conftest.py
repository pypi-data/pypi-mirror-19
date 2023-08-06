# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import uuid
import shutil
import os
import tempfile

import pytest


@pytest.fixture()
def unique_name():
    '''Return a unique name.'''
    return 'unique-{0}'.format(uuid.uuid4())


@pytest.fixture()
def temporary_file(request):
    '''Return a temporary file path.'''
    file_handle, path = tempfile.mkstemp()
    os.close(file_handle)

    def cleanup():
        '''Remove temporary file.'''
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


@pytest.fixture()
def temporary_directory(request):
    '''Return a temporary directory path.'''
    path = tempfile.mkdtemp()

    def cleanup():
        '''Remove temporary directory.'''
        shutil.rmtree(path)

    request.addfinalizer(cleanup)

    return path
