# mixins
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


import threading
import weakref


class ParentRouter:
    """
    Classes inheriting from this one will make their instances route attribute requests
    to the provided "parent" instance if their instances have no such attribute.
    """
    def __init__(self, parent):
        self.parent = weakref.proxy(parent)

    def __getattr__(self, attr):
        return getattr(self.parent, attr)


class OptionSetter:
    """
    Classes inheriting from this one will make all their
    instances add options to __dict__
    """
    def __init__(self, options):
        for opt in options:
            self.__dict__[opt] = options[opt]


class Drawable:
    """
    Helper to track drawables
    """

    instances = []

    def __init__(self):
        self.__class__.instances.append(weakref.proxy(self))

    def getAspect(self):
        raise NotImplementedError    

    def changeAspect(self, reset=False):
        raise NotImplementedError    

    @classmethod
    def enumerate(cls):
        for drawable in cls.instances:
            yield drawable


class Stoppable:
    """
    Stoppable threads.
    """
    def __init__(self):
        self.killev = threading.Event()

    def stop(self):
        self.killev.set()
        self.join()
