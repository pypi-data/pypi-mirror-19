# The MIT License (MIT)
#
# Copyright (C) 2015 - Julien Desfossez <jdesfossez@efficios.com>
#               2016 - Philippe Proulx <pproulx@efficios.com>
#               2015 - Antoine Busque <abusque@efficios.com>
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

import argparse
import json
import os
import re
import sys
import subprocess
import traceback
from babeltrace import TraceCollection
from . import mi, progressbar, period_parsing
from .. import __version__
from ..core import analysis, period as core_period
from ..common import (
    format_utils, parse_utils, trace_utils, version_utils
)
from ..linuxautomaton import automaton


class Command:
    _MI_BASE_TAGS = ['linux-kernel', 'lttng-analyses']
    _MI_AUTHORS = [
        'Julien Desfossez',
        'Antoine Busque',
        'Philippe Proulx',
    ]
    _MI_URL = 'https://github.com/lttng/lttng-analyses'
    _VERSION = version_utils.Version.new_from_string(__version__)
    _BT_INTERSECT_VERSION = version_utils.Version(1, 4, 0)
    _DEBUG_ENV_VAR = 'LTTNG_ANALYSES_DEBUG'

    def __init__(self, mi_mode=False):
        self._analysis = None
        self._analysis_conf = None
        self._args = None
        self._babeltrace_version = None
        self._handles = None
        self._traces = None
        self._period_ticks = 0
        self._mi_mode = mi_mode
        self._debug_mode = os.environ.get(self._DEBUG_ENV_VAR)
        self._run_step('create automaton', self._create_automaton)
        self._run_step('setup MI', self._mi_setup)

    @property
    def mi_mode(self):
        return self._mi_mode

    def _run_step(self, action_title, fn):
        try:
            fn()
        except KeyboardInterrupt:
            self._print('Cancelled by user')
            sys.exit(0)
        except Exception as e:
            self._gen_error('Cannot {}: {}'.format(action_title, e))

    def run(self):
        self._run_step('parse arguments', self._parse_args)
        self._run_step('open trace', self._open_trace)
        self._run_step('create analysis', self._create_analysis)

        if not self._mi_mode or not self._args.test_compatibility:
            self._run_step('run analysis', self._run_analysis)

        self._run_step('close trace', self._close_trace)

    def _mi_error(self, msg, code=None):
        print(json.dumps(mi.get_error(msg, code)))

    def _non_mi_msg(self, msg, color):
        if self._args.color:
            try:
                import termcolor

                msg = termcolor.colored(msg, color, attrs=['bold'])
            except ImportError:
                pass

        print(msg, file=sys.stderr)

    def _non_mi_error(self, msg):
        self._non_mi_msg(msg, 'red')

    def _non_mi_warn(self, msg):
        self._non_mi_msg(msg, 'yellow')

    def _error(self, msg, exit_code=1):
        if self._debug_mode:
            traceback.print_exc()

        if self._mi_mode:
            self._mi_error(msg)
        else:
            self._non_mi_error(msg)

        if exit_code is not None:
            sys.exit(exit_code)

    def _warn(self, msg):
        if not self._mi_mode:
            self._non_mi_warn(msg)

    def _gen_error(self, msg, exit_code=1):
        self._error('Error: {}'.format(msg), exit_code)

    def _cmdline_error(self, msg, exit_code=1):
        self._error('Command line error: {}'.format(msg), exit_code)

    def _print(self, msg):
        if not self._mi_mode:
            print(msg)

    def _mi_create_result_table(self, table_class_name, begin, end,
                                subtitle=None):
        return mi.ResultTable(self._mi_table_classes[table_class_name],
                              begin, end, subtitle)

    def _mi_setup(self):
        self._mi_table_classes = {}

        for tc_tuple in self._MI_TABLE_CLASSES:
            table_class = mi.TableClass(tc_tuple[0], tc_tuple[1], tc_tuple[2])
            self._mi_table_classes[table_class.name] = table_class

        self._mi_clear_result_tables()

    def _mi_print_metadata(self):
        tags = self._MI_BASE_TAGS + self._MI_TAGS
        infos = mi.get_metadata(version=self._VERSION, title=self._MI_TITLE,
                                description=self._MI_DESCRIPTION,
                                authors=self._MI_AUTHORS, url=self._MI_URL,
                                tags=tags,
                                table_classes=self._mi_table_classes.values())
        print(json.dumps(infos))

    def _mi_append_result_table(self, result_table):
        if not result_table or not result_table.rows:
            return

        tc_name = result_table.table_class.name
        self._mi_get_result_tables(tc_name).append(result_table)

    def _mi_append_result_tables(self, result_tables):
        if not result_tables:
            return

        for result_table in result_tables:
            self._mi_append_result_table(result_table)

    def _mi_clear_result_tables(self):
        self._result_tables = {}

    def _mi_get_result_tables(self, table_class_name):
        if table_class_name not in self._result_tables:
            self._result_tables[table_class_name] = []

        return self._result_tables[table_class_name]

    def _mi_print(self):
        results = []

        for result_tables in self._result_tables.values():
            for result_table in result_tables:
                results.append(result_table.to_native_object())

        obj = {
            'results': results,
        }

        print(json.dumps(obj))

    def _create_summary_result_tables(self):
        pass

    def _open_trace(self):
        self._babeltrace_version = trace_utils.read_babeltrace_version()
        if self._babeltrace_version >= self._BT_INTERSECT_VERSION:
            traces = TraceCollection(intersect_mode=self._args.intersect_mode)
        else:
            if self._args.intersect_mode:
                self._print('Warning: intersect mode not available - '
                            'disabling')
                self._print('         Use babeltrace {} or later to '
                            'enable'.format(
                                trace_utils.BT_INTERSECT_VERSION))
                self._args.intersect_mode = False
            traces = TraceCollection()
        handles = traces.add_traces_recursive(self._args.path, 'ctf')
        if handles == {}:
            self._gen_error('Failed to open ' + self._args.path, -1)
        self._handles = handles
        self._traces = traces
        self._ts_begin = traces.timestamp_begin
        self._ts_end = traces.timestamp_end
        self._process_date_args()
        self._read_tracer_version()
        if not self._args.skip_validation:
            self._check_lost_events()
        if not self._check_period_args():
            self._gen_error('Invalid period parameters')

    def _close_trace(self):
        for handle in self._handles.values():
            self._traces.remove_trace(handle)

    def _read_tracer_version(self):
        # TODO: associate the version of the tracer with each trace, not
        # globally. Waiting for bug #1085 to be fixed in Babeltrace.
        kernel_path = None
        # remove the trailing /
        while self._args.path.endswith('/'):
            self._args.path = self._args.path[:-1]
        for root, _, _ in os.walk(self._args.path):
            if root.endswith('kernel'):
                kernel_path = root
                break

        # If we don't have a kernel folder, we don't need to check the version
        # of the tracer for now.
        if kernel_path is None:
            return

        try:
            ret, metadata = subprocess.getstatusoutput(
                'babeltrace -o ctf-metadata "%s"' % kernel_path)
        except subprocess.CalledProcessError:
            self._gen_error('Cannot run babeltrace on the trace, cannot read'
                            ' tracer version')

        # fallback to reading the text metadata if babeltrace failed to
        # output the CTF metadata
        if ret != 0:
            try:
                metadata = subprocess.getoutput(
                    'cat "%s"' % os.path.join(kernel_path, 'metadata'))
            except subprocess.CalledProcessError:
                self._gen_error('Cannot read the metadata of the trace, cannot'
                                'extract tracer version')

        major_match = re.search(r'tracer_major = "*(\d+)"*', metadata)
        minor_match = re.search(r'tracer_minor = "*(\d+)"*', metadata)
        patch_match = re.search(r'tracer_patchlevel = "*(\d+)"*', metadata)

        if not major_match or not minor_match or not patch_match:
            self._gen_error('Malformed metadata, cannot read tracer version')

        self.state.tracer_version = version_utils.Version(
            int(major_match.group(1)),
            int(minor_match.group(1)),
            int(patch_match.group(1)),
        )

    def _read_babeltrace_version(self):
        try:
            output = subprocess.check_output('babeltrace')
        except subprocess.CalledProcessError:
            self._gen_error('Could not run babeltrace to verify version')

        output = output.decode(sys.stdout.encoding)
        first_line = output.splitlines()[0]
        version_string = first_line.split()[-1]

        self._babeltrace_version = \
            version_utils.Version.new_from_string(version_string)

    def _check_lost_events(self):
        msg = 'Checking the trace for lost events...'
        self._print(msg)

        if self._mi_mode and self._args.output_progress:
            mi.print_progress(0, msg)

        try:
            subprocess.check_output('babeltrace "%s"' % self._args.path,
                                    shell=True)
        except subprocess.CalledProcessError:
            self._gen_error('Cannot run babeltrace on the trace, cannot verify'
                            ' if events were lost during the trace recording')

    def _pre_analysis(self):
        pass

    def _mi_post_analysis(self):
        if not self._mi_mode:
            return

        if self._period_ticks > 1:
            self._create_summary_result_tables()

        self._mi_print()

    def _post_analysis(self):
        self._mi_post_analysis()

    def _pb_setup(self):
        if self._args.no_progress:
            return

        ts_end = self._ts_end

        if self._analysis_conf.end_ts is not None:
            ts_end = self._analysis_conf.end_ts

        if self._mi_mode:
            cls = progressbar.MiProgress
        else:
            cls = progressbar.FancyProgressBar

        self._progress = cls(self._ts_begin, ts_end, self._args.path,
                             self._args.progress_use_size)

    def _pb_update(self, event):
        if self._args.no_progress:
            return

        self._progress.update(event)

    def _pb_finish(self):
        if self._args.no_progress:
            return

        self._progress.finalize()

    def _run_analysis(self):
        self._pre_analysis()
        self._pb_setup()

        if self._args.intersect_mode:
            if not self._traces.has_intersection:
                self._gen_error('Trace has no intersection. '
                                'Use --no-intersection to override')

        first_event = True
        for event in self._traces.events:
            if first_event is True:
                self._analysis.begin_analysis(event)
                first_event = False
            self._pb_update(event)
            self._analysis.process_event(event)
            if self._analysis.ended:
                break
            self._automaton.process_event(event)

        self._pb_finish()
        self._analysis.end_analysis()
        self._post_analysis()

    def _print_date(self, begin_ns, end_ns):
        time_range_str = format_utils.format_time_range(
            begin_ns, end_ns, print_date=True, gmt=self._args.gmt
        )
        date = 'Timerange: {}'.format(time_range_str)

        self._print(date)

    def _format_timestamp(self, timestamp):
        return format_utils.format_timestamp(
            timestamp, print_date=self._args.multi_day, gmt=self._args.gmt
        )

    def _uniform_freq_min(self, category='default'):
        return self._analysis_conf.uniform_min[category]

    def _uniform_freq_max(self, category='default'):
        return self._analysis_conf.uniform_max[category]

    def _uniform_freq_step(self, category='default'):
        return self._analysis_conf.uniform_step[category]

    def _find_uniform_freq_values(self, durations, ratio=1000,
                                  category='default'):
        if category not in self._analysis_conf.uniform_step.keys():
            self._analysis_conf.uniform_min[category] = None
            self._analysis_conf.uniform_max[category] = None
            self._analysis_conf.uniform_step[category] = None

        if self._args.min is not None:
            self._analysis_conf.uniform_min[category] = self._args.min
        else:
            if len(durations) == 0:
                self._analysis_conf.uniform_min[category] = 0
            else:
                if self._analysis_conf.uniform_min[category] is None or \
                        min(durations) / ratio < \
                        self._analysis_conf.uniform_min[category]:
                    self._analysis_conf.uniform_min[category] = \
                        min(durations) / ratio
        if self._args.max is not None:
            self._analysis_conf.uniform_max[category] = self._args.max
        else:
            if len(durations) == 0:
                self._analysis_conf.uniform_max[category] = 0
            else:
                if self._analysis_conf.uniform_max[category] is None or \
                        max(durations) / ratio > \
                        self._analysis_conf.uniform_max[category]:
                    self._analysis_conf.uniform_max[category] = \
                        max(durations) / ratio

        # ns to µs
        self._analysis_conf.uniform_step[category] = (
            (self._analysis_conf.uniform_max[category] -
                self._analysis_conf.uniform_min[category]) /
            self._args.freq_resolution)

        return self._analysis_conf.uniform_min[category], \
            self._analysis_conf.uniform_max[category], \
            self._analysis_conf.uniform_step[category]

    def _check_period_args(self):
        # FIXME
        return True

        if len(self._analysis_conf.period_defs) > 0:
            name = self._analysis_conf.period_begin_ev_name
            if not trace_utils.check_event_exists(self._handles, name):
                self._gen_error("Event %s not found in the trace" % name)
                return False
        if self._analysis_conf.period_end_ev_name is not None:
            name = self._analysis_conf.period_end_ev_name
            if not trace_utils.check_event_exists(self._handles, name):
                self._gen_error("Event %s not found in the trace" % name)
                return False

        ev_name = self._analysis_conf.period_begin_ev_name
        for field in self._analysis_conf.period_begin_key_fields:
            if not ev_name:
                break
            if not trace_utils.check_field_exists(self._handles,
                                                  ev_name, field):
                self._gen_error("Field %s not found in event %s" %
                                (field, ev_name))
                return False
        ev_name = self._analysis_conf.period_end_ev_name
        for field in self._analysis_conf.period_end_key_fields:
            if not ev_name:
                break
            if not trace_utils.check_field_exists(self._handles,
                                                  ev_name, field):
                self._gen_error("Field %s not found in event %s" %
                                (field, ev_name))
                return False
        return True

    def _validate_transform_period_args(self, analysis_conf):
        args = self._args

        # validate period arguments
        if (args.period_begin is not None or args.period_end is not None or
           args.period_key_value is not None or
           args.period_begin_key is not None or
           args.period_end_key is not None) and (args.period or
                                                 args.period_captures):
            self._cmdline_error('Do not use another period option when using '
                                'one or more --period or --period-captures '
                                'options')

        registry = self._analysis_conf.period_def_registry
        name_to_begin_captures_exprs = {}
        name_to_end_captures_exprs = {}

        # parse period definition expressions
        if args.period:
            # period captures first
            if args.period_captures:
                for arg in args.period_captures:
                    try:
                        res = period_parsing.parse_period_captures_arg(arg)
                    except period_parsing.MalformedExpression as e:
                        self._cmdline_error('Malformed period captures '
                                            'expression: {}'.format(e))
                    except Exception as e:
                        self._cmdline_error('Cannot parse period captures '
                                            'expression: {}'.format(e))

                    if res.name in name_to_begin_captures_exprs:
                        fmt = 'Duplicate period name "{}" in ' \
                              '--period-captures argument'
                        self._cmdline_error(fmt.format(res.name))

                    name_to_begin_captures_exprs[res.name] = \
                        res.begin_captures_exprs
                    name_to_end_captures_exprs[res.name] = \
                        res.end_captures_exprs

            for period_arg in args.period:
                try:
                    res = period_parsing.parse_period_def_arg(period_arg)
                except period_parsing.MalformedExpression as e:
                    self._cmdline_error('Malformed period definition '
                                        'expression: {}'.format(e))
                except Exception as e:
                    self._cmdline_error('Cannot parse period definition '
                                        'expression: {}'.format(e))

                begin_captures_exprs = {}
                end_captures_exprs = {}

                if res.period_name is not None:
                    begin_captures_exprs = name_to_begin_captures_exprs.get(
                        res.period_name, {})
                    end_captures_exprs = name_to_end_captures_exprs.get(
                        res.period_name, {})

                try:
                    registry.add_period_def(res.parent_name, res.period_name,
                                            res.begin_expr, res.end_expr,
                                            begin_captures_exprs,
                                            end_captures_exprs)
                except core_period.IllegalExpression as e:
                    self._cmdline_error('Illegal period definition '
                                        'expression: {}'.format(e))
                except core_period.InvalidPeriodDefinition as e:
                    self._cmdline_error('Cannot add period: {}'.format(e),
                                        None)
                    self._error('Period argument: {}'.format(period_arg))
        elif (args.period_begin is not None or args.period_end is not None):
            self._warn('''Warning: The following period options are deprecated:

  --period-begin
  --period-end
  --period-begin-key
  --period-end-key
  --period-key-value

Please consider using the --period option.''')

            # create new-style expression from old-style arguments
            if args.period_begin is None:
                # ignore incomplete period definition
                return

            if not args.period_begin_key:
                args.period_begin_key = 'cpu_id'

            if not args.period_end:
                args.period_end = args.period_begin

            if not args.period_end_key:
                args.period_end_key = args.period_begin_key

            begin_exprs = []
            end_exprs = []

            # conditions for matching the event name
            begin_event_name_expr = core_period.EventScope(
                core_period.EventName())
            begin_event_name_str_expr = core_period.String(args.period_begin)
            end_event_name_expr = core_period.EventScope(
                core_period.EventName())
            end_event_name_str_expr = core_period.String(args.period_end)
            begin_event_name_eq_expr = core_period.Eq(
                begin_event_name_expr, begin_event_name_str_expr)
            begin_exprs.append(begin_event_name_eq_expr)
            end_event_name_eq_expr = core_period.Eq(end_event_name_expr,
                                                    end_event_name_str_expr)
            end_exprs.append(end_event_name_eq_expr)
            begin_field_names = args.period_begin_key.split(',')
            end_field_names = args.period_end_key.split(',')

            # conditions for begin field values
            if args.period_key_value:
                parts = args.period_key_value.split(',')
                value_exprs = []

                for part in parts:
                    try:
                        value_exprs.append(core_period.Number(float(part)))
                    except:
                        value_exprs.append(core_period.String(part))

                for field_name, value_expr in zip(begin_field_names,
                                                  value_exprs):
                    event_field_name = core_period.EventFieldName(field_name)
                    dyn_scope = core_period.DynamicScope(
                        core_period.DynScope.AUTO, event_field_name)
                    evt_scope = core_period.EventScope(dyn_scope)
                    begin_scope = core_period.BeginScope(evt_scope)
                    eq_expr = core_period.Eq(begin_scope, value_expr)
                    begin_exprs.append(eq_expr)

            # conditions for equal end and begin fields
            for begin_field_name, end_field_name in zip(begin_field_names,
                                                        end_field_names):
                # begin scope
                event_field_name = core_period.EventFieldName(begin_field_name)
                dyn_scope = core_period.DynamicScope(core_period.DynScope.AUTO,
                                                     event_field_name)
                evt_scope = core_period.EventScope(dyn_scope)
                begin_scope = core_period.BeginScope(evt_scope)

                # end event scope
                event_field_name = core_period.EventFieldName(end_field_name)
                dyn_scope = core_period.DynamicScope(core_period.DynScope.AUTO,
                                                     event_field_name)
                end_evt_scope = core_period.EventScope(dyn_scope)
                eq_expr = core_period.Eq(end_evt_scope, begin_scope)
                end_exprs.append(eq_expr)

            begin_expr = core_period.create_conjunction_from_exprs(begin_exprs)
            end_expr = core_period.create_conjunction_from_exprs(end_exprs)
            registry.add_period_def(None, None, begin_expr, end_expr, {}, {})

        # check that --period-captures name existing periods
        for name in name_to_begin_captures_exprs:
            if not registry.has_period_def(name):
                fmt = 'Cannot find period named "{}" for --period-captures ' \
                      'argument'
                self._cmdline_error(fmt.format(name))

    def _validate_transform_common_args(self):
        args = self._args
        refresh_period_ns = None
        if args.refresh is not None:
            try:
                refresh_period_ns = parse_utils.parse_duration(args.refresh)
            except ValueError as e:
                self._cmdline_error(str(e))

        self._analysis_conf = analysis.AnalysisConfig()
        self._analysis_conf.refresh_period = refresh_period_ns
        self._validate_transform_period_args(self._analysis_conf)

        if args.refresh is not None and not \
                self._analysis_conf.period_def_registry.is_empty:
            self._cmdline_error('Cannot specify --period* and --refresh '
                                'arguments at the same time')

        if args.cpu:
            self._analysis_conf.cpu_list = args.cpu.split(',')
            self._analysis_conf.cpu_list = [int(cpu) for cpu in
                                            self._analysis_conf.cpu_list]

        if args.debug:
            self._debug_mode = True

        # convert min/max args from µs to ns, if needed
        if hasattr(args, 'min') and args.min is not None:
            args.min *= 1000
            self._analysis_conf.min_duration = args.min
        if hasattr(args, 'max') and args.max is not None:
            args.max *= 1000
            self._analysis_conf.max_duration = args.max

        if hasattr(args, 'procname'):
            if args.procname:
                self._analysis_conf.proc_list = args.procname.split(',')

        if hasattr(args, 'tid'):
            if args.tid:
                self._analysis_conf.tid_list = args.tid.split(',')
                self._analysis_conf.tid_list = [int(tid) for tid in
                                                self._analysis_conf.tid_list]

        if hasattr(args, 'freq'):
            if args.freq_series:
                # implies uniform buckets
                args.freq_uniform = True

        if hasattr(args, 'freq') and args.freq_uniform:
            self._analysis_conf.uniform_min = {}
            self._analysis_conf.uniform_max = {}
            self._analysis_conf.uniform_step = {}

        if self._mi_mode:
            # print MI version if required
            if args.mi_version:
                print(mi.get_version_string())
                sys.exit(0)

            # print MI metadata if required
            if args.metadata:
                self._mi_print_metadata()
                sys.exit(0)

        # validate path argument (required at this point)
        if not args.path:
            self._cmdline_error('Please specify a trace path')

        if type(args.path) is list:
            args.path = args.path[0]

    def _validate_transform_args(self):
        pass

    def _parse_args(self):
        ap = argparse.ArgumentParser(description=self._DESC)

        # common arguments
        ap.add_argument('-r', '--refresh', type=str,
                        help='Refresh period, with optional units suffix '
                        '(default units: s)')
        ap.add_argument('--gmt', action='store_true',
                        help='Manipulate timestamps based on GMT instead '
                             'of local time')
        ap.add_argument('--skip-validation', action='store_true',
                        help='Skip the trace validation')
        ap.add_argument('--begin', type=str, help='start time: '
                                                  'hh:mm:ss[.nnnnnnnnn]')
        ap.add_argument('--end', type=str, help='end time: '
                                                'hh:mm:ss[.nnnnnnnnn]')
        ap.add_argument('--period', action='append', help='Period definition')
        ap.add_argument('--period-captures', action='append',
                        help='Period captures definition')
        ap.add_argument('--period-begin', type=str,
                        help='Analysis period start marker event name')
        ap.add_argument('--period-end', type=str,
                        help='Analysis period end marker event name '
                        '(requires --period-begin)')
        ap.add_argument('--period-begin-key', type=str,
                        help='Optional, list of event field names used to '
                        'match period markers (default: cpu_id)')
        ap.add_argument('--period-end-key', type=str,
                        help='Optional, list of event field names used to '
                        'match period marker. If none specified, use the same '
                        ' --period-begin-key')
        ap.add_argument('--period-key-value', type=str,
                        help='Optional, define a fixed key value to which a'
                        ' period must correspond to be considered.')
        ap.add_argument('--cpu', type=str,
                        help='Filter the results only for this list of '
                        'CPU IDs')
        ap.add_argument('--timerange', type=str, help='time range: '
                                                      '[begin,end]')
        ap.add_argument('--progress-use-size', action='store_true',
                        help='use trace size to approximate progress')
        ap.add_argument('--no-intersection', action='store_false',
                        dest='intersect_mode',
                        help='disable stream intersection mode')
        ap.add_argument('-V', '--version', action='version',
                        version='LTTng Analyses v{}'.format(self._VERSION))
        ap.add_argument('--debug', action='store_true',
                        help='Enable debug mode (or set {} environment '
                             'variable)'.format(self._DEBUG_ENV_VAR))
        ap.add_argument('--no-color', action='store_false', dest='color',
                        help='Disable colored output')

        # MI mode-dependent arguments
        if self._mi_mode:
            ap.add_argument('--mi-version', action='store_true',
                            help='Print MI version')
            ap.add_argument('--metadata', action='store_true',
                            help='Print analysis\' metadata')
            ap.add_argument('--test-compatibility', action='store_true',
                            help='Check if the provided trace is supported '
                                 'and exit')
            ap.add_argument('path', metavar='<path/to/trace>',
                            help='trace path', nargs='*')
            ap.add_argument('--output-progress', action='store_true',
                            help='Print progress indication lines')
        else:
            ap.add_argument('--no-progress', action='store_true',
                            help='Don\'t display the progress bar')
            ap.add_argument('path', metavar='<path/to/trace>',
                            help='trace path')

        # Used to add command-specific args
        self._add_arguments(ap)

        self._args = ap.parse_args()

        if self._mi_mode:
            # Compatiblity checking does not need to read the whole
            # trace, the caller should make sure there are no lost
            # events. At worst, they will be detected when the analysis
            # is actually run.
            if self._args.test_compatibility:
                self._args.skip_validation = True
            self._args.no_progress = True

            if self._args.output_progress:
                self._args.no_progress = False

        self._validate_transform_common_args()
        self._validate_transform_args()

    @staticmethod
    def _add_proc_filter_args(ap):
        ap.add_argument('--procname', type=str,
                        help='Filter the results only for this list of '
                        'process names')
        ap.add_argument('--tid', type=str,
                        help='Filter the results only for this list of TIDs')

    @staticmethod
    def _add_min_max_args(ap):
        ap.add_argument('--min', type=float,
                        help='Filter out durations shorter than min usec')
        ap.add_argument('--max', type=float,
                        help='Filter out durations longer than max usec')

    @staticmethod
    def _add_freq_args(ap, help=None):
        if not help:
            help = 'Output the frequency distribution'

        ap.add_argument('--freq', action='store_true', help=help)
        ap.add_argument('--freq-resolution', type=int, default=20,
                        help='Frequency distribution resolution '
                        '(default 20)')
        ap.add_argument('--freq-uniform', action='store_true',
                        help='Use a uniform resolution across distributions')
        ap.add_argument('--freq-series', action='store_true',
                        help='Consolidate frequency distribution histogram '
                        'as a single one')

    @staticmethod
    def _add_log_args(ap, help=None):
        if not help:
            help = 'Output the events in chronological order'

        ap.add_argument('--log', action='store_true', help=help)

    @staticmethod
    def _add_top_args(ap, help=None):
        if not help:
            help = 'Output the top results'

        ap.add_argument('--limit', type=int, default=10,
                        help='Limit to top X (default = 10)')
        ap.add_argument('--top', action='store_true', help=help)

    @staticmethod
    def _add_stats_args(ap, help=None):
        if not help:
            help = 'Output statistics'

        ap.add_argument('--stats', action='store_true', help=help)

    def _add_arguments(self, ap):
        pass

    def _process_date_args(self):
        def parse_date(date):
            try:
                ts = parse_utils.parse_trace_collection_date(
                    self._traces, date, self._args.gmt, self._handles
                )
            except ValueError as e:
                self._cmdline_error(str(e))

            return ts

        self._args.multi_day = trace_utils.is_multi_day_trace_collection(
            self._traces, self._handles)
        begin_ts = None
        end_ts = None

        if self._args.timerange:
            try:
                begin_ts, end_ts = (
                    parse_utils.parse_trace_collection_time_range(
                        self._traces, self._args.timerange,
                        self._args.gmt, self._handles)
                )
            except ValueError as e:
                self._cmdline_error(str(e))
        else:
            if self._args.begin:
                begin_ts = parse_date(self._args.begin)
            if self._args.end:
                end_ts = parse_date(self._args.end)

                # We have to check if timestamp_begin is None, which
                # it always is in older versions of babeltrace. In
                # that case, the test is simply skipped and an invalid
                # --end value will cause an empty analysis
                if self._ts_begin is not None and \
                   end_ts < self._ts_begin:
                    self._cmdline_error(
                        '--end timestamp before beginning of trace')

        self._analysis_conf.begin_ts = begin_ts
        self._analysis_conf.end_ts = end_ts

    def _create_analysis(self):
        notification_cbs = {
            analysis.AnalysisCallbackType.TICK_CB: self._analysis_tick_cb
        }

        self._analysis = self._ANALYSIS_CLASS(self.state, self._analysis_conf)
        self._analysis.register_notification_cbs(notification_cbs)

    def _create_automaton(self):
        self._automaton = automaton.Automaton()
        self.state = self._automaton.state

    def _analysis_tick_cb(self, period, end_ns):
        # No event was processed, just exit
        if end_ns is None:
            return
        self._analysis_tick(period, end_ns)

        if period is not None:
            # increment the number of effective ticks associated to
            # an existing period
            self._period_ticks += 1

    def _analysis_tick(self, period, end_ns):
        raise NotImplementedError()
