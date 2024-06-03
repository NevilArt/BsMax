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

from .command_panel import register_command_panel, unregister_command_panel

from .create_panel import register_create_panel, unregister_create_panel
from .modifier_panel import register_modifier_panel,unregister_modifier_panel
from .hierarcy_panel import register_hierarchy_panel, unregister_hierarchy_panel
from .motion_panel import register_motion_panel, unregister_motion_panel
from .display_panel import register_display_panel, unregister_display_panel
from .utility_panel import register_utility_panel, unregister_utility_panel


from .edit_curve import register_edit_curve, unregister_edit_curve
from .edit_mesh import register_edit_mesh, unregister_edit_mesh

def register_max(preferences):
	if preferences.side_panel == '3DSMAX':
		register_command_panel()
		register_create_panel()
		register_modifier_panel()
		register_hierarchy_panel()
		register_motion_panel()
		register_display_panel()
		register_utility_panel()

		register_edit_curve()
		register_edit_mesh()


def unregister_max():
	unregister_command_panel()
	unregister_create_panel()
	unregister_modifier_panel()
	unregister_hierarchy_panel()
	unregister_motion_panel()
	unregister_display_panel()
	unregister_utility_panel()

	unregister_edit_curve()
	unregister_edit_mesh()