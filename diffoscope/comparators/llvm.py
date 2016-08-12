# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016 Ximin Luo <infinity0@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <http://www.gnu.org/licenses/>.

from diffoscope import tool_required
from diffoscope.comparators.binary import File
from diffoscope.comparators.utils import Command
from diffoscope.difference import Difference


class LlvmBcAnalyzer(Command):
    @tool_required('llvm-bcanalyzer')
    def cmdline(self):
        return ['llvm-bcanalyzer', '-dump', self.path]

class LlvmBcDisassembler(Command):
    @tool_required('llvm-dis')
    def cmdline(self):
        return ['llvm-dis', '-o', '-', self.path]

class LlvmBitCodeFile(File):
    @staticmethod
    def recognizes(file):
        return file.magic_file_type and file.magic_file_type.startswith('LLVM IR bitcode')

    def compare_details(self, other, source=None):
        return [Difference.from_command(LlvmBcAnalyzer,   self.path, other.path),
                Difference.from_command(LlvmBcDisassembler, self.path, other.path)]
