#!/usr/bin/env python3
#
# Copyright Bertil Kronlund, 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module Reporter setup.

"""
import re
import os
import codecs

from codecs import open
from os import path

from setuptools import setup


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'docs/shortdescription.rst'), encoding='utf-8') as description_file:
    SHORT_DESCRIPTION = description_file.read().replace('.. :shortdescription:', '')

with open(path.join(here, 'docs/longdescription.rst'), encoding='utf-8') as long_description_file:
    LONG_DESCRIPTION = long_description_file.read().replace('.. :longdescription:', '')

# The full canonical version information, including alpha/beta/rc/git tags.
FULL_VERSION = find_version('modulereport/__init__.py')
# Short X.Y version.
MAJOR_MINOR_VERSION = FULL_VERSION.rsplit(u".", 1)[0]

# TODO: put package requirements here
INSTALL_REQUIRES = []

TESTS_REQUIRE = ['green>=2.5', 'coverage>=4.2', 'flake8>=3.0', 'check-manifest>=0.31']

setup(
    name='modulereport',
    packages=[
        'modulereport',
    ],
    package_dir={'modulereport': 'modulereport'},
    entry_points={
        'console_scripts': [
            'modulereport = modulereport.cli:main',
        ]
    },
    version=FULL_VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Bertil Kronlund',
    author_email='bertil.kronlund@gmail.com',
    url='https://github.com/berrak/modulereport',
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    license='Apache License, Version 2.0',
    zip_safe=False,
        classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
    ],
    keywords=('modulereport', 'import'),
)
