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
modulereport.modulesimported
------------------------------------

A simple example to list modules imported in your
Python script using ModuleFinder (standard Python module).

"""

from os.path import basename
from modulefinder import ModuleFinder


def show_import_report(pathname=None, show_loaded=False, show_not_imported=False, fullreport=False):

    filename = basename(pathname)

    finder = ModuleFinder()
    finder.run_script(pathname)

    if show_loaded or show_not_imported or fullreport:
        print('-'*50)
    else:
        print("Missing options what to do. Use 'modulereport --help'")
    if show_loaded:
        print("Loaded modules for: " + filename)
        print('-'*50)
        for name, mod in finder.modules.items():
            line = "{pyname}: {modlist}".format(pyname=name, modlist=','.join(list(mod.globalnames.keys())[:3]))
            print(line)
        print('-'*50)

    if show_not_imported:
        print("Modules missing for: " + filename)
        print('-'*50)
        print('\n'.join(finder.badmodules.keys()))
        print('-'*50)

    if fullreport:
        print("Full report:")
        print('-'*50)
        finder.report()
