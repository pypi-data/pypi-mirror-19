#
# This file is part of Flap.
#
# Flap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flap.  If not, see <http://www.gnu.org/licenses/>.
#

from re import compile, DOTALL
from flap.substitutions.commons import Substitution


class EndInput(Substitution):
    """
    Discard whatever comes after an `\endinput` command.
    """

    def prepare_pattern(self):
        return compile(r"\\endinput.+\Z", DOTALL)

    def replacements_for(self, fragment, match):
        return []


