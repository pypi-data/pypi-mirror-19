# parser rules
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



## Rules provided to the parser in order to validate input

_colors = 'trans|red|white|yellow|cyan|blue|black|magenta|green|random'

annidation_structure = ['bar', 'entry', 'alert',]

rules = {
    'global': {
        'fifo': '<string>',
    },
    'bar': {
        'bg': _colors,
        'fg': _colors,
        'font': 'normal|bold',
    },
    'entry': {
        'bg': _colors,
        'fg': _colors,
        'font': 'normal|bold',
        'default': '<string>',
        'event': '<string>',
        '!text': '<string>',
        '!command': '<string>',
        '!delay': '<digit>',
    },
    'alert': {
        'bg': _colors,
        'fg': _colors,
        'font': 'normal|bold',
        'action': '<string>',
        'action_every': '<digit>',
        'repeat': '<digit>',
        '!cmpvalue': '<string>',
    },
}
