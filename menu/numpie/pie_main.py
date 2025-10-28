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

from .numpadpie import get_menu, get_menu_pie

def draw_object_mode(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "Animation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Transform", '', 'BSMAX_MT_pie_view3d_transform')
	get_menu	(pie, "Add", '', 'VIEW3D_MT_add')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_mesh(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "Selection Mode", '', 'BSMAX_MT_pie_view3d_edit_mode')
	get_menu_pie(pie, "Transform", '', 'BSMAX_MT_pie_view3d_transform')
	get_menu_pie(pie, "Add", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_surface(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')
	
def draw_edit_curve(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_curves(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_meta(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_lattice(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_armature(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_pointcloud(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_gpencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_sculpt(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_sculpt_curves(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')


def draw_vertex_paint(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_weight_paint(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_texture_paint(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_edit_grease_pencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_sculpt_grease_pencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_paint_grease_pencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_weight_grease_pencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_vertex_grease_pencil(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')

def draw_pose(pie):
	get_menu_pie(pie, "Relation", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "Selection", '', 'BSMAX_MT_pie_view3d_Selection')
	get_menu_pie(pie, "Editor", '', 'BSMAX_MT_pie_view3d_edit_modeor')
	get_menu_pie(pie, "Edit", '', 'BSMAX_MT_pie_view3d_edit_mode')
	
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu_pie(pie, "???", '', 'BSMAX_MT_pie_template')
	get_menu	(pie, "???", '', 'BSMAX_MT_pie_template')
	
	get_menu_pie(pie, "View", '', 'VIEW3D_MT_view_pie')


def draw_switch(mode, pie):
	if mode == 'OBJECT': draw_object_mode(pie)
	elif mode == 'EDIT_MESH': draw_edit_mesh(pie)
	elif mode == 'EDIT_SURFACE': draw_edit_surface(pie)
	elif mode == 'EDIT_CURVE': draw_edit_curve(pie)
	elif mode == 'EDIT_CURVES': draw_edit_curves(pie)
	elif mode == 'EDIT_META': draw_edit_meta(pie)
	elif mode == 'EDIT_LATTICE': draw_edit_lattice(pie)
	elif mode == 'EDIT_ARMATURE': draw_edit_armature(pie)
	elif mode == 'EDIT_POINTCLOUD': draw_edit_pointcloud(pie)
	elif mode == 'EDIT_GPENCIL': draw_edit_gpencil(pie)
	elif mode == 'EDIT_GREASE_PENCIL': draw_edit_grease_pencil(pie)
	elif mode == 'SCULPT': draw_sculpt(pie)
	elif mode == 'SCULPT_CURVES': draw_sculpt_curves(pie)
	elif mode == 'SCULPT_GREASE_PENCIL': draw_sculpt_grease_pencil(pie)
	elif mode == 'PAINT_VERTEX': draw_vertex_paint(pie)
	elif mode == 'PAINT_WEIGHT': draw_weight_paint(pie)
	elif mode == 'PAINT_TEXTURE': draw_texture_paint(pie)
	elif mode == 'PAINT_GREASE_PENCIL': draw_paint_grease_pencil(pie)
	elif mode == 'WEIGHT_GREASE_PENCIL': draw_weight_grease_pencil(pie)
	elif mode == 'VERTEX_GREASE_PENCIL': draw_vertex_grease_pencil(pie)
	elif mode == 'POSE': draw_pose(pie)


class VIEW3D_MT_PIE_View3D_Main(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_object_main"
	bl_label = "View3D Object"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_switch(context.mode, pie)


def register_pie_main():
	bpy.utils.register_class(VIEW3D_MT_PIE_View3D_Main)

def unregister_pie_main():
	bpy.utils.unregister_class(VIEW3D_MT_PIE_View3D_Main)

if __name__ == '__main__':
	register_pie_main()