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
# 2024/03/03

from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class


def get_utility_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")


class SCENE_OP_BsMax_Utilities_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Utilities'
	bl_idname = 'VIEW3D_PT_BsMax_ttilities'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'UTILITIES'
	
	def draw(self, ctx):
		get_utility_panel(self.layout, ctx)


def register_utility_panel():
	register_class(SCENE_OP_BsMax_Utilities_Panel)


def unregister_utility_panel():
	unregister_class(SCENE_OP_BsMax_Utilities_Panel)


if __name__ == "__main__":
	register_utility_panel()