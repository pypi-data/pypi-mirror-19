# parser.py : a parser module used by ncmon
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
from collections import OrderedDict

import os
import re


### TODO: reimplement without loading the whole file into memory

class NoRulesProvided(Exception):
    pass


class NoTagsProvided(Exception):
    pass


class InvalidOption(Exception):
    pass


class MissMandatory(Exception):
    pass


class FileTooLarge(Exception):
    pass


class EntryIsEmpty(Exception):
    pass


class _TagList:
    """
    Represents a list of tag from the "roots" (first element)
    to the "leaves" (last element). Conceptually, the recursion starts at
    "roots" and ends at "leaves", so order matters.
    """
    sep = '/'

    def __init__(self, ilist):
        ilist.insert(0, 'global')
        self.ltag = tuple(ilist)
        self.pos = 1
        self.length = len(self.ltag)
        self.occurrences = {tag: 0 for tag in self.ltag}

    def setPosByTag(self, tag):
        self.pos = self.ltag.index(tag)

    def newOccur(self):
        self.occurrences[self.ltag[self.pos]] += 1

    def getNoccurs(self):
        return self.occurrences[self.ltag[self.pos]]

    def getNoccursByTag(self, tag):
        return self.occurrences[tag]

    def resetNoccurs(self):
        self.occurrences[self.ltag[self.pos]] = 0

    def last(self):
        return self.ltag[-1]

    def current(self):
        return self.ltag[self.pos]

    def maxReached(self):
        if (self.pos + 1) == self.length:
            return True
        else:
            return False

    def first(self):
        return self.ltag[1]

    def goInner(self):
        self.pos += 1
        if self.pos >= self.length - 1:
            self.pos = self.length - 1
            return self.last()
        else:
            return self.current()

    def getPrevs(self):
        if self.pos == 1:
            return ''
        else:
            return self.ltag[1:self.pos]

    def goOuter(self):
        self.pos -= 1
        if self.pos <= 0:
            self.pos = 0
            return self.first()
        else:
            return self.current()

    def contains(self, tag):
        if tag in self.ltag:
            return True
        else:
            return False

    def __iter__(self):
        return iter(self.ltag)


class Parser(object):
    """
    Represents a parser that take a text file in input and,
    for the given taglist, recursively parses the file.
    """

    def __init__(self, cfile, tlist, rules=None):
        self._taglist = _TagList(tlist)
        self._cfile = cfile
        self._maxfsize = 20480
        self._data = OrderedDict()
        self._validator = Validator(self._taglist, rules) if rules else None

    def setSep(self, sep):
        self._taglist.sep = sep

    def getOpts(self, string, curtag):
        blist = [line for line in string.strip(' ')
                 .strip('\n')
                 .split('\n')]

        opts = []

        for line in blist:
            if line.startswith('<'):
                break
            if line != '':
                opts.append(line)

        if opts:
            optdict = {}
            for opt in opts:
                k, v = opt.strip(' ').split('=', 1)
                k = k.strip()
                v = v.strip()
                optdict[k] = v
            return optdict
        else:
            if curtag != 'global':
                raise EntryIsEmpty('<%s> is empty!' % curtag)

    def getMatched(self, string, curdata):
        tagl = self._taglist
        curtag = tagl.current()
        miter = re.finditer(r'^<{tag}>\s*\n(.+?)^</{tag}>$'.format(tag=curtag),
                            string, re.MULTILINE | re.DOTALL)

        if miter is not None:
            for match in miter:
                tagl.newOccur()
                tag = curtag + str(tagl.getNoccurs() - 1)
                curdata[tag] = OrderedDict({'options': []})
                saved_curtag = curtag
                string = match.group(1)
                curdata[tag]['options'] = self.getOpts(string, curtag)
                curdata[tag]['tag_name'] = curtag
                curdata[tag]['sub_entries'] = OrderedDict()
                if not tagl.maxReached():
                    tagl.goInner()
                    self.getMatched(string, curdata[tag]['sub_entries'])
                tagl.setPosByTag(saved_curtag)
        tagl.resetNoccurs()

    def parse(self):
        if not os.path.isfile(self._cfile):
            raise IOError('No such file %s' % self._cfile)

        if int(os.path.getsize(self._cfile)) > self._maxfsize:
            raise FileTooLarge('Config file is too big!')

        clist = self.preproc()
        string = ''.join(clist)
        del(clist)
        self._data['tree'] = OrderedDict()
        data = self._data['tree']
        data['options'] = self.getOpts(string, 'global')
        data['tag_name'] = 'global'
        data['sub_entries'] = OrderedDict()
        self.getMatched(string, data['sub_entries'])
        re.purge()

        if self._validator is not None:
            self._validator.validate(self._data)
        return self._data

    def setMaxfsize(self, fsize):
        self._maxfsize = fsize

    def preproc(self):
        clist = []
        with open(self._cfile, 'r') as f:
            for line in f:
                line = line.strip(' ').replace('\t', '')
                if line.startswith('\n'):
                    continue
                elif line.startswith('#'):
                    continue
                else:
                    clist.append(line)
        return clist

    def printData(self, data, snum=0):
        spaces = snum * ' '
        for key in data:
            if key == 'sub_entries':
                self.printData(data[key], snum + 4)
            elif key == 'options':
                for k, v in data[key].items():
                    print(spaces + (4 * ' ') + k, '=', v)
            elif key == 'tag_name':
                continue
            else:
                print(spaces + '[' + key + ']')
                self.printData(data[key], snum)


class Validator:
    """
    Input validation.
    """

    def __init__(self, tlist, rules):
        self._rules = rules
        self._taglist = tlist

    @staticmethod
    def checkLiteral(options, rulk, rulv):
        optvalue = options[rulk]
        errmsg = '"%s = %s" is a wrong type!' % (rulk, optvalue)
        rule_values = rulv.split('|')
        found = False
        for rule in rule_values:
            if optvalue == rule:
                found = True
                break
        if not found:
            raise InvalidOption(errmsg)

    @staticmethod
    def checkType(options, rulk, rulv):
        optvalue = options[rulk]
        errmsg = '"%s = %s" is invalid!' % (rulk, optvalue)
        if rulv == '<string>':
            if not len(optvalue):
                errmsg = '"%s = %s" is empty!' % (rulk, optvalue)
                raise InvalidOption(errmsg)
        elif rulv == '<digit>':
            if not optvalue.isdigit():
                raise InvalidOption(errmsg)

    def check(self, options, tag):
        for rulk, rulv in self._rules[tag].items():
            mandatory = False
            if rulk.startswith('!'):
                mandatory = True
                rulk = rulk[1:]

            if not options:
                if mandatory:
                    raise MissMandatory('%s is mandatory!' % rulk)
                return

            if rulk in options:
                if '|' in rulv:
                    self.checkLiteral(options, rulk, rulv)
                else:
                    self.checkType(options, rulk, rulv)
            else:
                if mandatory:
                    raise MissMandatory('%s is mandatory!' % rulk)

    def validate(self, data):
        for entry in data:
            opts = data[entry]['options']
            tag = data[entry]['tag_name']
            self.check(opts, tag)
            self.validate(data[entry]['sub_entries'])


if __name__ == '__main__':
    import sys
    colors = 'red|white|yellow|cyan|blue|black|magenta|green'
    rules = {
        'global': {},
        'bar': {
            'bg': colors,
            'fg': colors,
        },
        'entry': {
            'bg': colors,
            'fg': colors,
            '!text': '<string>',
            '!command': '<string>',
            '!delay': '<digit>',
        },
        'alert': {
            'bg': colors,
            'fg': colors,
            '!cmpvalue': '<string>',
            'beep': 'on|off',
        },
    }

    try:
        parser = Parser(sys.argv[1], ['bar', 'entry', 'alert', ], rules)
        data = parser.parse()
        parser.printData(data)
    except IndexError:
        pass
