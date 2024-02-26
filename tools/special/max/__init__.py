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

# from .menu import register_menu,unregister_menu
from .modifier import register_modifier,unregister_modifier
from .side_panel import register_side_panel, unregister_side_panel
from .edit_curve import register_edit_curve, unregister_edit_curve
from .edit_mesh import register_edit_mesh, unregister_edit_mesh

def register_max(preferences):
	register_modifier()
	if preferences.side_panel == '3DsMax':
		register_side_panel()
		register_edit_curve()
		register_edit_mesh()

def unregister_max():
	unregister_modifier()
	unregister_side_panel()
	unregister_edit_curve()
	unregister_edit_mesh()
