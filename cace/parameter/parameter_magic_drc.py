# Copyright 2024 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys

from ..common.common import run_subprocess, get_magic_rcfile, get_layout_path
from .parameter import Parameter, ResultType, Argument, Result
from .parameter_manager import register_parameter
from ..logging import (
    dbg,
    verbose,
    info,
    subproc,
    rule,
    success,
    warn,
    err,
)


@register_parameter('magic_drc')
class ParameterMagicDRC(Parameter):
    """
    Run magic drc
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self.add_result(Result('drc_errors'))

        self.add_argument(Argument('args', [], False))
        self.add_argument(Argument('gds_flatten', False, False))

    def is_runnable(self):
        netlist_source = self.runtime_options['netlist_source']

        if netlist_source == 'schematic':
            info('Netlist source is schematic capture. Not running DRC.')
            self.result_type = ResultType.SKIPPED
            return False

        return True

    def implementation(self):

        self.cancel_point()

        # Acquire a job from the global jobs semaphore
        with self.jobs_sem:

            """
            Run magic to get a DRC report
            """

            projname = self.datasheet['name']
            paths = self.datasheet['paths']

            info('Running magic to get layout DRC report.')

            rcfile = get_magic_rcfile()

            # Get the path to the layout, prefer magic
            (layout_filepath, is_magic) = get_layout_path(
                projname, self.paths, check_magic=True
            )

            # Check if layout exists
            if not os.path.isfile(layout_filepath):
                err('No layout found!')
                self.result_type = ResultType.ERROR
                return

            # Run magic to get the bounds of the design geometry
            # Get triplet of area, width, and height

            magic_input = ''

            if is_magic:
                magic_input += f'path search +{os.path.abspath(os.path.dirname(layout_filepath))}\n'
                magic_input += f'load {os.path.basename(layout_filepath)}\n'
            else:
                if self.get_argument('gds_flatten'):
                    magic_input += 'gds flatglob *\n'
                else:
                    magic_input += 'gds flatglob guard_ring_gen*\n'
                    magic_input += 'gds flatglob vias_gen*\n'
                magic_input += f'gds read {os.path.abspath(layout_filepath)}\n'
                magic_input += f'load {projname}\n'

            magic_input += 'drc on\n'
            magic_input += 'catch {drc style drc(full)}\n'
            magic_input += 'select top cell\n'
            magic_input += 'drc check\n'
            magic_input += 'drc catchup\n'
            magic_input += 'set dcount [drc list count total]\n'
            magic_input += 'puts stdout "drc = $dcount"\n'
            magic_input += 'set outfile [open "magic_drc.out" w+]\n'
            magic_input += 'set drc_why [drc listall why]\n'
            magic_input += 'puts stdout $drc_why\n'
            magic_input += 'foreach x $drc_why {\n'
            magic_input += '   puts $outfile $x\n'
            magic_input += '   puts stdout $x\n'
            magic_input += '}\n'

            returncode = self.run_subprocess(
                'magic',
                ['-dnull', '-noconsole', '-rcfile', rcfile]
                + self.get_argument('args'),
                input=magic_input,
                cwd=self.param_dir,
            )

        if self.step_cb:
            self.step_cb(self.param)

        magrex = re.compile('drc[ \t]+=[ \t]+([0-9.]+)[ \t]*$')

        stdoutfilepath = os.path.join(self.param_dir, 'magic_stdout.out')
        drcfilepath = os.path.join(self.param_dir, 'magic_drc.out')

        if not os.path.isfile(drcfilepath):
            err('No output file generated by magic!')
            err(f'Expected file: {drcfilepath}')
            self.result_type = ResultType.ERROR
            return

        info(
            f"Magic DRC report at '[repr.filename][link=file://{os.path.abspath(drcfilepath)}]{os.path.relpath(drcfilepath)}[/link][/repr.filename]'…"
        )

        drccount = None
        with open(stdoutfilepath, 'r') as stdout_file:

            for line in stdout_file.readlines():
                lmatch = magrex.match(line)
                if lmatch:
                    drccount = int(lmatch.group(1))

        if drccount != None:
            self.result_type = ResultType.SUCCESS
            self.get_result('drc_errors').values = [drccount]

        # Increment progress bar
        if self.step_cb:
            self.step_cb(self.param)
