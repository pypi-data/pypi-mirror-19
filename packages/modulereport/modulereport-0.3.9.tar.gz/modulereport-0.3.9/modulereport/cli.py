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
modulereport.cli
-----------------------------------

Main entry for the `modulereport` CLI.

"""

import sys
import argparse

from modulereport import __version__
from modulereport.modulesimported import show_import_report
from modulereport.utils.environment import python_version


def main(argv=sys.argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("pathname", help="path to python file to analyze for imports")
    parser.add_argument("-s, --skipreport", help="skip list of all modules", action="store_false", dest='fullreport', default=True)
    parser.add_argument("-l, --loaded", help="show loaded modules", action="store_true", dest='showloaded', default=False)
    parser.add_argument("-m, --missing", help="show missing modules", action="store_true", dest='shownotloaded', default=False)
    parser.add_argument('-V', action='version',
                        version='%(prog)s: version {version} (Python {pyversion})'.format(version=__version__, pyversion=python_version()))

    args = parser.parse_args()
    try:
        show_import_report(args.pathname, args.showloaded, args.shownotloaded, args.fullreport)
    except IOError:
        print("Cannot find python script: '%s'" % args.pathname)

    return 0
