# setup.py : ncmon setup
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

sys.path.append('src')

from proginfo import *

setup(
    name            = PRGNAME,
    version         = VERSION,
    author          = AUTHOR,
    author_email    = EMAIL,
    url             = REPO,
    license         = LICENSE,
    description     = DESCRIPTION,
    package_dir     = {PRGNAME: 'src'},
    packages        = [PRGNAME],
    data_files      = [('/usr/share/doc/' + PRGNAME + '-' + VERSION, ['LICENSE']),
                       ('/usr/share/man/man1', ['man/' + PRGNAME + '.1']),
                       ('/usr/share/doc/' + PRGNAME + '-' + VERSION, ['conf/ncmonrc.sample']),
                       ('/usr/bin/', ['src/' + PRGNAME]), ]
)
