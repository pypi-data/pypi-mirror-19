# curses things
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


from ncmon.utils  import *
from ncmon.mixins import Stoppable

import collections
import threading
import Queue
import weakref
import curses
import random

wrapper = curses.wrapper

class CursesBase:
    """
    Auxiliary class to group some curses thingies.
    """

    tfont = {
        'normal': curses.A_NORMAL,
        'bold'  : curses.A_BOLD,
    }

    colors = {
        'trans'     : -1,
        'black'     : curses.COLOR_BLACK,
        'red'       : curses.COLOR_RED,
        'green'     : curses.COLOR_GREEN,
        'yellow'    : curses.COLOR_YELLOW,
        'blue'      : curses.COLOR_BLUE,
        'magenta'   : curses.COLOR_MAGENTA,
        'cyan'      : curses.COLOR_CYAN,
        'white'     : curses.COLOR_WHITE,
    }

    ## dict of initialized color pair numbers:
    ## key='[bgcolor, 'fgcolor'] value=pair_number
    pn_dict = {}

    available_pair_numbers = []
    screen = None

    last_width = 1
    width  = 1
    height = 1

    KEY_RESIZE = curses.KEY_RESIZE

    @classmethod
    def refresh(cls):
        cls.screen.refresh()

    @classmethod
    def init(cls, screen):
        cls.screen = screen
        curses.curs_set(0)
        curses.use_default_colors()

        cls.resetAvailPnums()
        cls.updateCoords()

    @classmethod
    def resetAvailPnums(cls, reset_dict=False):
        if reset_dict:
            cls.pn_dict = {}

        cls.available_pair_numbers = list(range(1, curses.COLOR_PAIRS))

    @classmethod
    def updateCoords(cls):
        cls.height, cls.width = cls.screen.getmaxyx()
        cls.width -= 2

    @classmethod
    def randomColors(cls):
        cdict = cls.colors
        klist = cdict.keys()
        bg    = random.choice(klist)

        klist.remove(bg)
        fg = random.choice(klist)
        return [bg, fg]

    @classmethod
    def randomColor(cls):
        return random.choice(cls.colors.keys())

    @classmethod
    def givePairNumber(cls, cpair):
        """
        Takes a two element list composed by
        a background and a foreground color (by name),
        takes the corresponding int value of each color,
        and initializes curses color pair returning the
        pair number. (Note: only in this method there is
        the "conversion" color_name -> color_number.)
        """

        strid = str(cpair)
        
        if strid in cls.pn_dict:
            pnum = cls.pn_dict[strid]
        else:
            try:
                pnum = cls.available_pair_numbers.pop()
            except IndexError:
                pnum = 1

            cls.pn_dict[strid] = pnum

            npair = [cls.colors[cls.randomColor()]
                     if col == 'random' else cls.colors[col] for col in cpair]

            bg, fg = npair
            curses.init_pair(pnum, fg, bg)

        return pnum

    @classmethod
    def clear(cls):
        cls.screen.clear()

    @staticmethod
    def close():
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()


class CursesWindow(CursesBase):
    """
    A curses window consisting of a single line of text.
    Due to the impossibility to write to last character of a
    curses window for historical reasons, the (logical) width of the window (writable
    space) has been decremented by 2.
    """
    def __init__(self, row):
        if not self.__class__.screen:
            return

        self.win = curses.newwin(1, self.__class__.width + 2, row, 1)
        self.hidden = False

    def draw(self, row, startpos, string, cpair, font):
        width  = self.__class__.width
        height = self.__class__.height

        if startpos > width:
            return

        pnum = self.__class__.givePairNumber(cpair)
        cnum = curses.color_pair(pnum)

        if len(string) == 1:
            string *= (width - 1)

        # if text goes beyond the end of the window, cut it.
        if((startpos + len(string)) > width):
            string = string[:width - startpos]

        tfont = self.tfont[font]
        self.win.addstr(0, startpos, string, cnum | tfont)

    def resize(self, h, w):
        self.win.resize(h, w)

    def refresh(self):
        self.win.refresh()

    def noutrefresh(self):
        self.win.noutrefresh()

    def clear(self):
        self.win.clear()


class CursesDrawer(threading.Thread, Stoppable):
    """
    Every Bar instance has a Drawer obj responsible for handling a type of window
    (CursesWindow in this case) for each bar instance. A drawer knows how to display
    an object which has specified attributes.
    """
    def __init__(self, drawables):

        threading.Thread.__init__(self)
        Stoppable.__init__(self)

        self.windows = [CursesWindow(n) for n in range(len(drawables))]

        self.qproc   = Queue.Queue()
        self.daemon  = True

        CursesBase.updateCoords()
        CursesBase.refresh()

        fmap(self.setPositions, drawables)
        fmap(self.drawAndDisplay, drawables, (True,))

        curses.doupdate()

    def run(self):
        while True:
            task, params = self.qproc.get()

            task(*params) if len(params) else task()

            self.qproc.task_done()
    
    def resize(self, drawables):
        CursesBase.updateCoords()

        for drawable in drawables:
            curwin = self.windows[drawable.row]

            if CursesBase.height > drawable.row:
                if curwin.hidden:
                    self.windows[drawable.row] = CursesWindow(drawable.row)
                
                if CursesBase.last_width != CursesBase.width:
                    self.setPositions(drawable)
                    self.clear(drawable)

                self.draw(drawable)
                self.display(drawable, noref=True)

            else:
                curwin.hidden = True
                
        curses.doupdate()
        CursesBase.last_width = CursesBase.width

    def clear(self, drawable):
        self.windows[drawable.row].clear()

    def draw(self, drawobj):
        row, starts_at, string, color_pair, font = drawobj.getAspect()

        self.windows[row].draw(row, starts_at, string,
                               color_pair, font)

        if isinstance(drawobj, collections.Iterable):
            fmap(self.draw, drawobj)

    def setAndClear(self, drawable):
        self.setPositions(drawable)
        self.clear(drawable)

    def drawAndDisplay(self, drawable, noref=False):
        self.draw(drawable)
        self.display(drawable, noref=noref)

    @staticmethod   
    def setPositions(drawable):
        '''
        Assigns a starting positions to every entry.
        '''
        width = CursesBase.width

        strlen = drawable.getTotlen()
        enum = len(drawable)

        if enum == 1:
            enum = 2

        if width >= strlen:
            nspaces = width - strlen
            spacing = (nspaces / (enum - 1))
            res = nspaces % (enum - 1)
        else:
            spacing = 0
            res = 0

        count = 0
        for d in drawable:
            d.starts_at = count

            count += len(d.string) + spacing

            if(res != 0):
                count += res - (res - 1)
                res -= 1

    def changeColor(self, drawables, randomall=False):
        CursesBase.resetAvailPnums(reset_dict=True)

        rcols = CursesBase.randomColors

        for drawable in drawables:
            drawable.color_pair = rcols()

            for d in drawable:
                if randomall:
                    d.color_pair = rcols()

                d.changeAspect(reset=(not randomall))

            self.draw(drawable)
            self.display(drawable, noref=True)

        curses.doupdate()

    def display(self, drawobj, noref=False):
        if noref:
            self.windows[drawobj.row].noutrefresh()
        else:
            self.windows[drawobj.row].refresh()

    def qChCol(self, drawables, randomall=False):
        self.qproc.put((self.changeColor, (drawables, randomall)))

    def qResize(self, drawables):
        self.qproc.put((self.resize, (drawables,)))

    def qSetAndClear(self, drawable):
        self.qproc.put((self.setAndClear, (drawable,)))

    def qDrawAndDisplay(self, drawable):
        self.qproc.put((self.drawAndDisplay, (drawable,)))
