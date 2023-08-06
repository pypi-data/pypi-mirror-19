# utility functions
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


from __future__ import print_function
import sys
import re


def error(msg):
    print('[Error]:', msg, file=sys.stderr)
    sys.exit(1)


def digitBoundary(digit, bmin, bmax):
    if bmin < digit < bmax:
        return digit
    else:
        return bmax if digit > bmax else bmin


def fmap(func, iterable, funcargs=None):
    if funcargs is not None:
        for elem in iterable:
            func(elem, *funcargs)
    else:
        for elem in iterable:
            func(elem)


def isFloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def digitFromString(string):
    res = re.search(r'\d+(?:\.\d+)*', string)

    return res.group() if res else None


def debug(vlist, ptsnum):
    ptsnum = str(ptsnum)
    if ptsnum.isdigit():
        with open('/dev/pts/' + ptsnum, 'w') as f:
            print('Debug::::::', vlist, file=f)
    else:
        print('Debug::::::', vlist)
