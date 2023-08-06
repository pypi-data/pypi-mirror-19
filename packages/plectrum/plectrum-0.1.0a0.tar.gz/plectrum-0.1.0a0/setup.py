# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import os
import re

from setuptools import setup, find_packages


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(ROOT_PATH, 'resource')
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')

PACKAGE_NAME = 'plectrum'

# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Compute dependencies.
INSTALL_REQUIRES = [
    'prompt_toolkit >= 1.0.9, < 2',
    'ordered-set >= 2, < 3'
]
DOC_REQUIRES = [
    'sphinx >= 1.2.2, < 2',
    'sphinx_rtd_theme >= 0.1.6, < 1',
    'lowdown >= 0.1.0, < 1',
]
TEST_REQUIRES = [
    'pytest-runner >= 2.7, < 3',
    'pytest >= 2.3.5, < 3',
    'pytest-cov >= 2, < 3',
    'pytest-mock >= 0.11, < 1'
]

# Readthedocs requires Sphinx extensions to be specified as part of
# INSTALL_REQUIRES in order to build properly.
if os.environ.get('READTHEDOCS', None) == 'True':
    INSTALL_REQUIRES.extend(DOC_REQUIRES)


# Execute setup.
setup(
    name='plectrum',
    version=VERSION,
    description='Interactively select items from a list in a terminal.',
    long_description=open(README_PATH).read(),
    url='https://gitlab.com/4degrees/plectrum',
    keywords='terminal, gui, selector',
    author='Martin Pengelly-Phillips',
    author_email='martin@4degrees.ltd.uk',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'doc': DOC_REQUIRES,
        'test': TEST_REQUIRES,
        'dev': DOC_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False,
)
