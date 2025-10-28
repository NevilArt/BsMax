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
from bpy.props import EnumProperty
from bpy.utils import register_class, unregister_class

from .numpadpie import get_menu, get_menu_pie

def draw_object_mode(pie, quick):
	if quick:
		pie.operator('object.select_all', text="All").action='SELECT'
		pie.operator('object.select_all', text="Deselect").action='DESELECT'
		pie.operator('object.select_all', text="Invert").action='INVERT'
		return
	
	#Submenu Come Here
	pie.operator('object.select_all', text="All").action='SELECT'
	pie.operator('object.select_all', text="Deselect").action='DESELECT'
	pie.operator('object.select_all', text="Invert").action='INVERT'

def draw_edit_mesh(pie, quick):
	pie.operator('mesh.select_mode', text="Vertex").type='VERT'
	pie.operator('mesh.select_mode', text="Edge").type='EDGE'
	pie.operator('mesh.select_mode', text="Face").type='FACE'

def draw_edit_surface(pie, quick):
	pass
	
def draw_edit_curve(pie, quick):
	pass

def draw_edit_curves(pie, quick):
	pass

def draw_edit_meta(pie, quick):
	pass

def draw_edit_lattice(pie, quick):
	pass

def draw_edit_armature(pie, quick):
	pass

def draw_edit_pointcloud(pie, quick):
	pass

def draw_edit_gpencil(pie, quick):
	pass

def draw_sculpt(pie, quick):
	pass


def draw_switch(mode, pie, quick=False):
	if mode == 'OBJECT':
		draw_object_mode(pie, quick)

	elif mode == 'EDIT_MESH':
		draw_edit_mesh(pie, quick)
	
	elif mode == 'EDIT_SURFACE':
		draw_edit_surface(pie, quick)

	elif mode == 'EDIT_CURVE':
		draw_edit_curve(pie, quick)
	
	elif mode == 'EDIT_CURVES':
		draw_edit_curves(pie, quick)

	elif mode == 'EDIT_META': 
		draw_edit_meta(pie, quick)

	elif mode == 'EDIT_LATTICE':
		draw_edit_lattice(pie, quick)

	elif mode == 'EDIT_ARMATURE':
		draw_edit_armature(pie, quick)
	
	elif mode == 'EDIT_POINTCLOUD':
		draw_edit_pointcloud(pie, quick)

	elif mode == 'EDIT_GPENCIL':
		draw_edit_gpencil(pie, quick)
	
	elif mode == 'SCULPT':
		draw_sculpt(pie, quick)

	elif mode == 'PAINT_VERTEX':
		pass

	elif mode == 'PAINT_WEIGHT':
		pass

	elif mode == 'PAINT_TEXTURE':
		pass

	elif mode == 'EDIT_GREASE_PENCIL':
		pass

	elif mode == 'SCULPT_GREASE_PENCIL':
		pass

	elif mode == 'PAINT_GREASE_PENCIL':
		pass

	elif mode == 'WEIGHT_GREASE_PENCIL':
		pass

	elif mode == 'VERTEX_GREASE_PENCIL':
		pass

	elif mode == 'EDIT_ARMATURE':
		pass

	elif mode == 'POSE':
		pass


class VIEW3D_MT_PIE_View3D_Selection(Menu):
	bl_idname = 'BSMAX_MT_pie_view3d_Selection'
	bl_label = "Select"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_switch(context.mode, pie)


# class VIEW3D_MT_PIE_View3D_Selection_sub(Menu):
# 	bl_idname = 'BSMAX_MT_pie_view3d_Selection_sub'
# 	bl_label = "Select"

# 	def draw(self, context):
# 		pie = self.layout.menu_pie()
# 		draw_switch(context.mode, pie)


class VIEW3D_MT_PIE_View3D_Selection_Quick(Menu):
	bl_idname = 'BSMAX_MT_pie_view3d_Selection_quick'
	bl_label = "Select"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_switch(context.mode, pie, quick=True)


classes = {
	VIEW3D_MT_PIE_View3D_Selection,
	VIEW3D_MT_PIE_View3D_Selection_Quick
}


def register_pie_selection():
	for cls in classes:
		register_class(cls)

def unregister_pie_selection():
	for cls in classes:
		unregister_class(cls)

if __name__ == '__main__':
	register_pie_selection()
