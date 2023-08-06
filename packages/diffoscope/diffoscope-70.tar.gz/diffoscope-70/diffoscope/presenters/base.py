# -*- coding: utf-8 -*-
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2017 Chris Lamb <lamby@debian.org>
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
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.


class Presenter(object):
    def __init__(self):
        self.depth = 0

    def visit(self, difference):
        self.visit_difference(difference)

        self.depth += 1

        for x in difference.details:
            self.visit(x)

        self.depth -= 1

    def visit_difference(self, difference):
        raise NotImplementedError()

    @classmethod
    def indent(cls, val, prefix):
        # As an optimisation, output as much as possible in one go to avoid
        # unnecessary splitting, interpolating, etc.
        #
        # We don't use textwrap.indent as that unnecessarily calls
        # str.splitlines, etc.
        return prefix + val.rstrip().replace('\n', '\n{}'.format(prefix))
