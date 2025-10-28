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

# from .numpadpie import get_menu, get_menu_pie


class VIEW3D_MT_PIE_View3D_Object_Create(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_object_create"
	bl_label = "Create"

	def draw(self, context):
		pie = self.layout.menu_pie()
		pie.menu("BSMAX_MT_create_light_pi", text="Light/Prop", icon="OUTLINER_OB_LIGHT")
		pie.menu("BSMAX_MT_curve_create_menu", icon='OUTLINER_OB_CURVE')
		pie.menu("BSMAX_MT_create_menu", text="Armature/Lattice")
		pie.prop(context.scene.primitive_setting, 'draw_mode', text='', icon='VIEW3D')
		pie.menu("BSMAX_MT_create_menu", text="Others")
		pie.menu("BSMAX_MT_mesh_create_menu", icon='OUTLINER_OB_MESH')
		pie.menu("BSMAX_MT_forcefield_cecreate_menu", icon='OUTLINER_OB_FORCE_FIELD')
		pie.menu("BSMAX_MT_empty_create_menu", text="Empty/Image")