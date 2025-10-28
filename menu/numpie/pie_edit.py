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

import bpy

from bpy.types import Menu

def draw_edit_menu_pie(context, pie):
	type = context.object.type
	
	# All items has object mode
	pie.operator("object.mode_set", text="Object Mode").mode='OBJECT'

	if type in {
		'MESH', 'SURFACE', 'CURVE', 'CURVES', 'META',
		'LATTICE', 'ARMATURE', 'POINTCLOUD', 'GREASEPENCIL'}:
		
		pie.operator("object.mode_set", text="Edit Mode").mode='EDIT'
	
	if type == 'MESH':
		pie.operator("object.mode_set", text="Sculpt Mode").mode='SCULPT'

	elif type == 'CURVES':
		pie.operator("object.mode_set", text="Sculpt Mode").mode='SCULPT_CURVES'

	elif type == 'GREASEPENCIL':
		pie.operator("object.mode_set", text="Sculpt Mode").mode='SCULPT_GREASE_PENCIL'

	if type == 'MESH':
		pie.operator("object.mode_set", text="Vertext Paint").mode='VERTEX_PAINT'
		pie.operator("object.mode_set", text="Weight Paint").mode='WEIGHT_PAINT'
		pie.operator("object.mode_set", text="Texture Paint").mode='TEXTURE_PAINT'
	
	elif type == 'GREASEPENCIL':
		pie.operator("object.mode_set", text="Draw Mode").mode='PAINT_GREASE_PENCIL'
		pie.operator("object.mode_set", text="Weight Paint").mode='WEIGHT_GREASE_PENCIL'
		pie.operator("object.mode_set", text="Vertext Paint").mode='VERTEX_GREASE_PENCIL'
		
	elif type == 'ARMATURE':
		pie.separator()
		pie.operator("object.mode_set", text="Pose Mode").mode='POSE'


class VIEW3D_MT_PIE_View3D_Edit_Mode(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_edit_mode"
	bl_label = "Mode"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_edit_menu_pie(context, pie)


def register_pie_edit():
	bpy.utils.register_class(VIEW3D_MT_PIE_View3D_Edit_Mode)

def unregister_pie_edit():
	bpy.utils.unregister_class(VIEW3D_MT_PIE_View3D_Edit_Mode)

if __name__ == '__main__':
	register_pie_edit()