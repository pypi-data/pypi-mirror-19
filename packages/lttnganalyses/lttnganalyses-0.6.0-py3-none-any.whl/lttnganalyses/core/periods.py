# The MIT License (MIT)
#
# Copyright (C) 2016 - Julien Desfossez <jdesfossez@efficios.com>
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

from .analysis import Analysis, PeriodData


class _PeriodData(PeriodData):
    def __init(self):
        self._period_event = None

    @property
    def period_event(self):
        return self._period_event


class PeriodAnalysis(Analysis):
    def __init__(self, state, conf):
        super().__init__(state, conf, {})
        # This is a special case where we keep a global state instead of a
        # per-period state, since we are accumulating statistics about
        # all the periods.
        self._all_period_stats = {}
        self._all_period_list = []
        self._all_total_duration = 0
        self._all_min_duration = None
        self._all_max_duration = None
        # Internal map between currently active periods and their
        # corresponding PeriodEvent object.
        self._current_periods = {}

    def _create_period_data(self):
        return _PeriodData()

    @property
    def all_count(self):
        return len(self._all_period_list)

    @property
    def all_period_stats(self):
        return self._all_period_stats

    @property
    def all_period_list(self):
        return self._all_period_list

    @property
    def all_min_duration(self):
        return self._all_min_duration

    @property
    def all_max_duration(self):
        return self._all_max_duration

    @property
    def all_total_duration(self):
        return self._all_total_duration

    def update_global_stats(self, period_event):
        if self._all_min_duration is None or period_event.duration < \
                self._all_min_duration:
            self._all_min_duration = period_event.duration

        if self._all_max_duration is None or period_event.duration > \
                self._all_max_duration:
            self._all_max_duration = period_event.duration
        self._all_total_duration += period_event.duration

    # beginning of a new period
    def _begin_period_cb(self, period_data):
        # Only track real periods, not the dummy ones created
        # when no --period argument was passed.
        if period_data.period.definition is None:
            return

        period = period_data.period
        definition = period.definition

        if definition.name not in self._all_period_stats:
            if definition.name is None:
                name = ""
            else:
                name = definition.name
            self._all_period_stats[name] = \
                PeriodStats.new_from_period(period_data.period)

        if period.parent is not None:
            parent = self._current_periods[period.parent]
        else:
            parent = None

        period_data._period_event = PeriodEvent(
            period.begin_evt.timestamp, definition.name, parent)

        self._all_period_list.append(period_data._period_event)
        self._current_periods[period] = period_data._period_event

    def _end_period_cb(self, period_data, completed,
                       begin_captures, end_captures):
        period = period_data.period

        if period.definition is None:
            return

        if completed is False:
            # We should eventually warn the user here or keep
            # the event as uncomplete or in a separate table.
            self._all_period_list.remove(period_data._period_event)
            return

        if period.definition.name is None:
            name = ""
        else:
            name = period.definition.name

        period_data._period_event.finish(
            self.last_event_ts, begin_captures, end_captures)
        self._all_period_stats[name].update_stats(
            period_data._period_event)
        self.update_global_stats(period_data._period_event)

        if period.parent is not None:
            parent = self._current_periods[period.parent]
            parent.add_child(period_data._period_event)

        del self._current_periods[period]


class PeriodStats():
    def __init__(self, name):
        self.name = name
        self.period_list = []
        self.min_duration = None
        self.max_duration = None
        self.total_duration = 0

    @classmethod
    def new_from_period(cls, period):
        if period.definition.name is None:
            return cls("")
        return cls(period.definition.name)

    @property
    def count(self):
        return len(self.period_list)

    def update_stats(self, period_event):
        if self.min_duration is None or period_event.duration < \
                self.min_duration:
            self.min_duration = period_event.duration

        if self.max_duration is None or period_event.duration > \
                self.max_duration:
            self.max_duration = period_event.duration
        self.total_duration += period_event.duration
        self.period_list.append(period_event)


class PeriodEvent():
    def __init__(self, start_ts, name, parent):
        self._start_ts = start_ts
        self._name = name
        self._parent = parent
        self._end_ts = None
        self._begin_captures = None
        self._end_captures = None
        # Only during the aggregation phase, store the list
        # of children we want to output.
        self._children = []

    @property
    def start_ts(self):
        return self._start_ts

    @property
    def end_ts(self):
        return self._end_ts

    @property
    def name(self):
        if self._name is None:
            return ""
        return self._name

    @property
    def duration(self):
        return self._end_ts - self._start_ts

    @property
    def begin_captures(self):
        return str(self._begin_captures)

    @property
    def end_captures(self):
        return str(self._end_captures)

    def filtered_captures(self, period_group_by):
        # List of tuple (field, value) for all the captured fields
        # present in the _period_group_by dict.
        _captures = []
        if self._name not in period_group_by.keys():
            return _captures
        if self._begin_captures is not None:
            for c in sorted(self._begin_captures.keys()):
                if c in period_group_by[self._name]:
                    _captures.append(('%s.%s' % (self._name, c),
                                     self._begin_captures[c]))
        if self._end_captures is not None:
            for c in sorted(self._end_captures.keys()):
                if c in period_group_by[self._name]:
                    _captures.append(('%s.%s' % (self._name, c),
                                     self._end_captures[c]))
        return _captures

    def full_captures(self):
        _captures = []
        if self._begin_captures is not None:
            for c in self._begin_captures.keys():
                _captures.append(('%s.%s' % (self._name, c),
                                 self._begin_captures[c]))
        if self._end_captures is not None:
            for c in self._end_captures.keys():
                _captures.append(('%s.%s' % (self._name, c),
                                 self._end_captures[c]))
        return _captures

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    def finish(self, end_ts, begin_captures, end_captures):
        self._end_ts = end_ts
        self._begin_captures = begin_captures
        self._end_captures = end_captures

    def add_child(self, child_period_event):
        self._children.append(child_period_event)
