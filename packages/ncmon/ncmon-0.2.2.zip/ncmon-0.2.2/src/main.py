# ncmon main
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

import os
import sys
import getopt
import threading
import Queue
import time
import random
import operator
import itertools
import weakref

## ncmon modules

from ncmon.proginfo  import *
from ncmon.constants import *
from ncmon.utils     import *

import ncmon.cursesgraphic as cursesgraphic
import ncmon.rules as rules

from cursesgraphic import CursesBase, CursesDrawer, CursesWindow
from ncmon.mixins  import ParentRouter, OptionSetter, Drawable, Stoppable
from ncmon.parser  import Parser


class Config:
    """
    Initializes the parser and does some checking.
    """

    global_opts = {}
    number_of_bars = 0

    cfile = os.environ['HOME'] + '/.ncmonrc'

    @classmethod
    def init(cls):
        """ 
        Parses configiguration file and returns data.
        """

        parser = Parser(cls.cfile, rules.annidation_structure, rules.rules)
        data = parser.parse()

        gopts = data['tree']['options']
        Config.global_opts = gopts if gopts is not None else {}

        start_point = data['tree']['sub_entries']

        bnum = len([key for key in start_point])

        if bnum > MAX_BARS:
            error('Too many bars, maximum is %s, quitting.' % MAX_BARS)

        cls.number_of_bars = bnum
        return start_point


class Bar(Drawable):
    """
    Represents a single line (of text) whose width is equal to
    the screen one. It's also a container of BarEntry elements,
    and has some methods which operate on all elements.
    """
    # instance counter
    index = 0

    def __init__(self, data):
        Drawable.__init__(self)

        self.row = self.__class__.index
        self.starts_at = 1

        lcname = self.__class__.__name__.lower()
        key = lcname + str(self.row)
        opts = data[key]['options']
        self.initOptions(opts)

        entries = data[key]['sub_entries']
        if len(entries) > MAX_ENTRIES:
            error('Too many entries, maximum is %s, quitting.' % MAX_ENTRIES)

        self.sub_drawables = [BarEntry(self, entries[e]) for e in entries]

        self.__class__.index += 1

    def getAspect(self):
        return (self.row, self.starts_at, self.string,
                self.color_pair, self.font)


    def initOptions(self, opts):
        """
        Default options values. Must be initialized because
        all other classes which have instance of this class
        as parent will route requests here.
        """

        self.bg = opts.get('bg', 'trans')
        self.fg = opts.get('fg', 'white')
        self.color_pair = [self.bg, self.fg]
        self.font = opts.get('font', 'normal')
        self.string = opts.get('fillchar', ' ')

    def getTotlen(self):
        return sum([elem.strlen for elem in self.sub_drawables])

    def getMaxdelay(self):
        return max([entry.delay for entry in self.sub_drawables])

    def __len__(self):
        return len(self.sub_drawables)

    def __iter__(self):
        return iter(self.sub_drawables)

    def __getitem__(self, idx):
        return self.sub_drawables[idx]

    def __str__(self):
        return str([str(elem) for elem in self.sub_drawables])


class BarEntry(ParentRouter, OptionSetter, Drawable):
    """
    Represents a visual bar entry (text:command)
    """


    entries_events = []

    def __init__(self, parent, entry):
        Drawable.__init__(self)
        ParentRouter.__init__(self, parent)
        OptionSetter.__init__(self, entry['options'])

        if [self.bg, self.fg] != self.color_pair:
            self.color_pair = [self.bg, self.fg]

        self.delay = digitBoundary(int(self.delay), MIN_DELAY, MAX_DELAY)
        alerts = entry['sub_entries']

        if len(alerts) > MAX_ALERTS:
            error('Too many alerts, maximum is %s, quitting.' % MAX_ALERTS)

        self.alerts = None

        if alerts:
            self.alerts = [Alert(self, alerts[a]) for a in alerts]

        if 'event' in self.__dict__:
            self.__class__.entries_events.append({self.event: self}) 

            del self.__dict__['event']

        self.len_changed     = False
        self.alert_triggered = False
        self.last_output = 'None'
        self.output = 'None'
        self.string = 'None'
        self.prev_strlen = 0
        self.genOutput()

    def getAspect(self):
        o = self

        if self.alerts:
            if self.alert_triggered:
                o = self.switchAspect()

        return (o.row, o.starts_at, o.string,
                o.color_pair, o.font)
            
    def switchAspect(self):
        return next(self.display_list)

    def changeAspect(self, reset=False):
        if reset:
            if 'color_pair' in self.__dict__:
                del self.__dict__['color_pair']

        if self.alerts:
            for a in self.alerts:
                a.changeAspect(reset=reset)

    def loadAlerts(self):
        '''
        When there are alerts, cycle indefinitely (till alerts stops)
        between them and original entry.
        '''

        dlist = [alert for alert in self.alerts if alert.check()]
        self.alert_triggered = True if len(dlist) else False
        dlist.append(self)

        self.display_list = itertools.cycle(dlist)

    def genOutput(self):
        self.updated = False

        self.output = os.popen(self.command)\
                        .read(MAX_OUTPUT)\
                        .replace('\n', ' ')\
                        .rstrip()

        if not self.output:
            self.output = self.__dict__.get('default', '[NONE]')

        self.string = self.text + self.output
        self.strlen = len(self.string)

        self.len_changed = True if self.strlen != self.prev_strlen else False

        if self.last_output != self.output:
            if self.alerts:
                self.loadAlerts()

            self.updated = True

        self.prev_strlen = self.strlen
        self.last_output = self.output

    def __str__(self):
        return self.string


class Alert(ParentRouter, OptionSetter, Drawable):
    """
    Alert for each entry (at most MAX_ALERTS per entry).
    """

    opdict = {
        '=' : operator.eq,
        '>' : operator.gt,
        '<' : operator.lt,
        '|' : operator.contains,
    }

    def __init__(self, parent, alert):
        Drawable.__init__(self)
        ParentRouter.__init__(self, parent)
        OptionSetter.__init__(self, alert['options'])

        ## invert parent bg, fg (parent route)
        altbg = self.__dict__.get('bg', self.fg)
        altfg = self.__dict__.get('fg', self.bg)

        self.color_pair = [altbg, altfg]
        self.operator   = self.cmpvalue[:1]
        self.triggered  = False
        self.last_triggered = False


        if not self.operator in self.__class__.opdict:
            error('Bad operator in config file.')

        self.cmpvalue = self.cmpvalue[1:]

        if 'action' in self.__dict__:
            self.action_every = digitBoundary(int(self.action_every),
                                              MIN_DELAY,
                                              MAX_DELAY) if 'action_every' in self.__dict__ else 2

            self.repeat = digitBoundary(int(self.repeat),
                                        0,
                                        MAX_DELAY) if 'repeat' in self.__dict__ else 1

            self.action = Action(self.action, times=self.repeat, every=self.action_every)

        if 'stop_action' in self.__dict__:
            self.stop_action = Action(self.stop_action)

    def changeAspect(self, reset):
        if 'color_pair' in self.__dict__:
            del self.__dict__['color_pair']

        self.color_pair = list(reversed(self.color_pair))

    def check(self):
        self.triggered = False

        outv = self.output
        cmpv = self.cmpvalue

        if isFloat(cmpv):

            if not isFloat(outv):
                outv = digitFromString(outv)
                
                if not outv:
                    return False
                
            if isFloat(outv):
                outv = float(outv)
                cmpv = float(cmpv)


        if self.__class__.opdict[self.operator](outv, cmpv):
            self.triggered = True
        
            if not self.last_triggered:
                if 'action' in self.__dict__:
                    self.action()
         
        else:
            if self.last_triggered:
                if 'action' in self.__dict__:
                    self.action(stop=True)

                if 'stop_action' in self.__dict__:
                    self.stop_action()

        self.last_triggered = self.triggered
   
        return self.triggered


class Action(object):
    """
    Command to execute whan an alert condition is triggered.
    """

    __slots__ = ['command', 'times', 'every', 'killev']

    def __init__(self, command, times=1, every=0):

        self.every   = every
        self.times   = times
        self.command = command
        self.killev  = threading.Event()

    def run(self):
        count = 0
        times = self.times
        kev   = self.killev
        every = self.every

        kev.clear()

        while True:
            os.system(self.command)
            count += 1

            if kev.wait(float(every)) or count == times:
                sys.exit()

    def __call__(self, stop=False):
        if stop:
            self.killev.set()
            return

        if self.times == 1:
            threading.Thread(target=os.system, args=(self.command,)).start()
        else:
            t = threading.Thread(target=self.run)
            t.daemon = True
            t.start()
     

class BarThread(threading.Thread, Stoppable):
    """
    A thread for each bar.
    """

    def __init__(self, bar, wakeev, qpoll, drawer):
        threading.Thread.__init__(self)
        Stoppable.__init__(self)

        self.bar    = bar
        self.wake   = wakeev
        self.daemon = True
        self.drawer = drawer
        self.qpoll  = qpoll

    def run(self):
        maxdelay = self.bar.getMaxdelay()
        counter  = 0
        qpoll    = self.qpoll
        drawer   = self.drawer
        wake     = self.wake
        bar      = self.bar
        kev      = self.killev


        while True:
            if kev.is_set():
                sys.exit()

            # assume that if event times out there is no FifoPoller intromission
            isasync = wake.wait(float(TIME_SPAN))
            wake.clear()

            update    = False
            changed   = False

            if isasync:
                entry = qpoll.get()
                entry.genOutput()

                changed = entry.len_changed
                update  = entry.updated

                qpoll.task_done()

            else:
                for entry in bar:
                    if entry.alert_triggered:
                        update = True

                    if not (counter % entry.delay) and counter:
                        entry.genOutput()

                        if not update:
                            update = entry.updated

                        if not changed:
                            changed = entry.len_changed

                counter = (counter + TIME_SPAN) if counter < maxdelay else 0

            if changed:
                drawer.qSetAndClear(bar)  

            if update:
                drawer.qDrawAndDisplay(bar)


class FifoPoller(threading.Thread, Stoppable):
    """
    A fifo poller waiting for events from a named pipe.
    """

    def __init__(self, fifo, wakes, qpolls):
        import stat
        if os.path.exists(fifo):
            if not stat.S_ISFIFO(os.stat(fifo).st_mode):
                CursesBase.close()
                error('%s is not a named pipe!' % fifo)
        else:
            try:
                os.mkfifo(fifo)

            except OSError:
                CursesBase.close()
                error("cannot create %s, check permissions." % fifo)

        self.events = {}

        self.fifo_opened = False
        self.fifo   = fifo
        self.wakes  = wakes
        self.qpolls = qpolls

        threading.Thread.__init__(self)
        Stoppable.__init__(self)

        self.daemon = True

    def openfifo(self):
        try:
            self.fdin = os.open(self.fifo, os.O_RDONLY | os.O_NONBLOCK)
        except OSError:
            pass

    def register(self, entries_events):
        
        if not self.fifo_opened:
            self.openfifo()
            self.fifo_opened = True

        for k, v in [e.items()[0] for e in entries_events]:
            self.events[k] = v

    def run(self):
        import errno

        evs    = self.events
        qpolls = self.qpolls
        wakes  = self.wakes
        kev    = self.killev

        while True:
            if kev.is_set():
                sys.exit()
            
            try:
                data = os.read(self.fdin, MAX_EVENT_LEN)
            except OSError as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    data = None

            if data:
                data = data.strip()

                if data in evs:
                    entry = evs[data]

                    qpolls[entry.row].put_nowait(entry)
                    wakes[entry.row].set()
            else:
                time.sleep(0.1)


class Program:
    """
    Auxiliary class for main starting/stopping.
    """


    bar_list = []

    @classmethod
    def init(cls, cfile):
        data = Config.init()

        fifo = Config.global_opts.get('fifo', False)

        qpolls = [Queue.Queue() if fifo else None
                  for i in range(Config.number_of_bars)]

        wakeevs = [threading.Event()
                   for i in range(Config.number_of_bars)]

        cls.bar_list = [Bar(data)
                        for i in range(Config.number_of_bars)]

        cls.drawer = CursesDrawer(cls.bar_list)
        cls.drawer.start()

        bts = [BarThread(bar, wev, qp, cls.drawer)
               for bar, wev, qp in zip(cls.bar_list, wakeevs, qpolls)]

        fpoller = None
        if fifo and BarEntry.entries_events:
            fpoller = FifoPoller(fifo, wakeevs, qpolls) 
            fpoller.register(BarEntry.entries_events)
            

        for bt in bts: bt.start()

        if fpoller is not None:
            fpoller.start()


    @classmethod
    def restart(cls):
        cls.stop()
        CursesBase.close()
        pt = sys.executable
        os.execl(pt, pt, *sys.argv)

    @classmethod
    def terminate(cls):
        cls.stop()
        sys.exit()

    @classmethod
    def stop(cls):
        try:
            for t in threading.enumerate():
                t.stop()
        except AttributeError:
            pass

        CursesBase.clear()
        CursesBase.refresh()

    @classmethod
    def resize(cls):
        cls.drawer.qResize(cls.bar_list)

    @classmethod
    def changeColor(cls, randomall=False):
        cls.drawer.qChCol(cls.bar_list, randomall=randomall)

    @staticmethod
    def mainLoop(stdscr):
        CursesBase.init(stdscr)
        Program.init(Config.cfile)

        dkey = {ord('q'): sys.exit,
                ord('r'): Program.restart,
                ord('c'): Program.changeColor,
                ord('C'): lambda: Program.changeColor(randomall=True),
                CursesBase.KEY_RESIZE: Program.resize, }
        try:
            while True:
                action = dkey.get(stdscr.getch(), None)

                if action is not None:
                    action()

        except KeyboardInterrupt:
            sys.exit()

    @staticmethod
    def parseCmdline():
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hf:')
        except getopt.GetoptError as e:
            error(e)

        for opt, value in opts:
            if opt == '-f':
                Config.cfile = value

                if not os.path.isfile(Config.cfile):
                    error('\'%s\' doesn\'t exist!' % Config.cfile)

            elif opt == '-h':
                print(
                      '''\r--------------------------------------------------------------------
                      \r[{prgname} - {description}] Version {version} 
                      \r--------------------------------------------------------------------
                      \rUsage:
                      \r    {prgname} [Options]

                      \rOptions:
                      \r    -f <config>   use <config> as configuration file
                      \r    -h            print this help
                    
                      \rDefault <config> location:
                      \r    ~/.ncmonrc

                      \rSample <config>:
                      \r    /usr/share/doc/ncmon-{version}/ncmonrc.sample

                      \rRepository:
                      \r    <{repo}>
                      \r 
                      \rLicense: 
                      \r    {license}

                      \rContacts:
                      \r    Please report bugs and comments to <{author_email}>

                      \rWritten by {author}
                      \r--------------------------------------------------------------------
                      \rThis program is free software: you can redistribute it and/or modify
                      \rit under the terms of the GNU General Public License as published by
                      \rthe Free Software Foundation, either version 3 of the License, or
                      \r(at your option) any later version.

                      \rThis program is distributed in the hope that it will be useful,
                      \rbut WITHOUT ANY WARRANTY; without even the implied warranty of
                      \rMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                      \rGNU General Public License for more details.

                      \rYou should have received a copy of the GNU General Public License
                      \ralong with this program.  If not, see <http://www.gnu.org/licenses/>.
                      \r--------------------------------------------------------------------'''
                    .format(prgname=PRGNAME, license=LICENSE, author=AUTHOR, 
                            author_email=EMAIL, version=VERSION, repo=REPO, 
                            description=DESCRIPTION))

                sys.exit()
