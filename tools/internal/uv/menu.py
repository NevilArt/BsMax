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
from bsmax.state import version

class UV_MT_Edit(Menu):
	bl_idname = "UV_MT_edit"
	bl_label = "Edit"

	def draw(self, ctx):
		layout=self.layout
		if ctx.space_data.show_uvedit:
			layout.operator("uv.turn",text="-90",icon="LOOP_BACK").ccw = False
			layout.operator("uv.turn",text="+90",icon="LOOP_FORWARDS").ccw = True
			layout.separator()
			layout.operator("uv.cylinder_project",text="Cylinder Project",icon="MESH_CYLINDER")
			layout.operator("uv.cube_project",text="Cube Project",icon="MESH_CUBE")
			layout.operator("uv.sphere_project",text="Sphere Project",icon="MESH_UVSPHERE")
			# layout.lable(text="Plane Project")

def uv_edit_menu(self, ctx):
	self.layout.menu("UV_MT_edit")

mnu = bpy.types.MASK_MT_editor_menus if version() < 283 else bpy.types.IMAGE_MT_editor_menus

def register_menu():
	bpy.utils.register_class(UV_MT_Edit)
	mnu.append(uv_edit_menu)

def unregister_menu():
	mnu.remove(uv_edit_menu)
	bpy.utils.unregister_class(UV_MT_Edit)