# The MIT License (MIT)
#
# Copyright (C) 2015 - Julien Desfossez <jdesfossez@efficios.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class StateProvider:
    def __init__(self, state, cbs):
        self._state = state
        self._cbs = cbs

    def process_event(self, ev):
        name = ev.name

        if name in self._cbs:
            self._cbs[name](ev)
        # for now we process all the syscalls at the same place
        elif 'syscall_entry' in self._cbs and \
                (name.startswith('sys_') or name.startswith('syscall_entry_')):
            self._cbs['syscall_entry'](ev)
        elif 'syscall_exit' in self._cbs and \
                (name.startswith('exit_syscall') or
                 name.startswith('syscall_exit_')):
            self._cbs['syscall_exit'](ev)
