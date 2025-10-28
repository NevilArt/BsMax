############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
# 2025/10/16

from .numpadpie import register_numpadpie, unregister_numpadpie
from .operators import register_operators, unregister_operators
from .pie_main import register_pie_main, unregister_pie_main
from .pie_editor import register_pie_editor, unregister_pie_editor
from .pie_edit import register_pie_edit, unregister_pie_edit
from .pie_selection import register_pie_selection, unregister_pie_selection
from .pie_transform import register_pie_transform, unregister_pie_transform
from .keymaps import register_keymaps, unregister_keymaps

def register_numpie_main():
	register_numpadpie()
	register_operators()
	register_pie_main()
	register_pie_edit()
	register_pie_editor()
	register_pie_selection()
	register_pie_transform()
	register_keymaps()

def unregister_numpie_main():
	unregister_keymaps()
	unregister_pie_main()
	unregister_pie_transform()
	unregister_pie_selection()
	unregister_pie_editor()
	unregister_pie_edit()
	unregister_operators()
	unregister_numpadpie()
