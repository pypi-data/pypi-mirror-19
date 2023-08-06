# setup.py : basicconfigparser setup
# Written by Francesco Palumbo aka phranz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
import sys


setup(
    name                = 'basicconfigparser',
    version             = '0.1',
    author              = 'Francesco Palumbo',
    author_email        = 'franzopal@gmail.com',
    url                 = 'https://github.com/phr4nz/basicconfigparser',
    license             = 'GPL3',
    description         = 'A basic configuration file parser module for Python. ',
    long_description    = 'A basic configuration file parser module for Python. ' 
                          'It is a simple function which takes a file path ' 
                          'a dictionary of rules (regex based) an optional key value '
                          'separator (default is \'=\'), an optional character to identify'
                          ' lines which start with a comment (default \'#\'),'
                          ' and returns a dictionary containing parsed data. '
                          'No sections or others things are required. '
                          'The eventually rised exceptions contain error line number.',
    py_modules          = ['basicconfigparser'],
    data_files          = [('/usr/share/doc/basicconfigparser-0.1', ['LICENSE']),
                           ('/usr/share/doc/basicconfigparser-0.1', ['README'])],

    classifiers         = ['Intended Audience :: Developers',
                           'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                           'Operating System :: POSIX :: Linux',
                           'Programming Language :: Python']
)
