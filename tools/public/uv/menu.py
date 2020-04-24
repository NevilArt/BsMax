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

class BsMax_MT_UV_Edit(Menu):
	bl_idname = "BSMAX_MT_uvedit"
	bl_label = "Edit"

	def draw(self, ctx):
		layout=self.layout
		if ctx.space_data.show_uvedit:
			layout.operator("uv.turn",text="-90",icon="LOOP_BACK").ccw = False
			layout.operator("uv.turn",text="+90",icon="LOOP_FORWARDS").ccw = True
			#layout.separator()
		# elif ctx.space_data.show_uvedit:# image editor
		# 	layout.operator("image.turn",text="-90",icon="LOOP_BACK").ccw = False
		# 	layout.operator("image.turn",text="+90",icon="LOOP_FORWARDS").ccw = True

def uv_edit_menu(self, ctx):
	self.layout.menu("BSMAX_MT_uvedit")

mnu = bpy.types.MASK_MT_editor_menus if bpy.app.version[1] < 83 else bpy.types.IMAGE_MT_editor_menus

def register_menu():
	bpy.utils.register_class(BsMax_MT_UV_Edit)
	mnu.append(uv_edit_menu)

def unregister_menu():
	mnu.remove(uv_edit_menu)
	bpy.utils.unregister_class(BsMax_MT_UV_Edit)