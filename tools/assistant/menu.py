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

import bpy
from bpy.types import Menu
from bsmax.state import is_object_mode

class BsMax_MT_View3D_tools(Menu):
	bl_idname = "BSMAX_MT_view3dtools"
	bl_label = "Tools"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.menu("BSMAX_MT_animationtools",icon='ARMATURE_DATA')
		layout.menu("BSMAX_MT_rendertools",icon='RENDER_ANIMATION')
		layout.menu("BSMAX_MT_riggtools",icon='TOOL_SETTINGS')

def tools_menu(self, ctx):
	self.layout.menu("BSMAX_MT_view3dtools")

def register_menu():
	bpy.utils.register_class(BsMax_MT_View3D_tools)
	bpy.types.VIEW3D_MT_editor_menus.append(tools_menu)

def unregister_menu():
	bpy.utils.unregister_class(BsMax_MT_View3D_tools)
	bpy.types.VIEW3D_MT_editor_menus.remove(tools_menu)