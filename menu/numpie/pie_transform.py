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
from bpy.utils import register_class, unregister_class

# from .numpadpie import get_menu, get_menu_pie

# Piemenu Order by Index
#			4
#		5		6
#	1				2
#		7		8
#			3

def draw_transform(context, pie) -> None:
	pie.separator()
	pie.separator()
	pie.operator('object.rotate', text="Rotate")
	pie.operator('transform.translate', text="Rotate")
	pie.operator('transform.translate', text="Move")
	pie.operator('transform.translate', text="Scale")
	pie.operator('object.move', text="Move")
	pie.operator('object.scale', text="Scale")


def draw_transform_quick(context, pie) -> None:
	pie.separator()
	pie.separator()
	pie.operator('object.rotate', text="Rotate")
	pie.operator('transform.translate', text="Rotate")
	pie.operator('transform.translate', text="Move")
	pie.operator('transform.translate', text="Scale")
	pie.operator('object.move', text="Move")
	pie.operator('object.scale', text="Scale")


class VIEW3D_MT_PIE_View3D_Transform(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_transform"
	bl_label = "Transform"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_transform(context, pie)


class VIEW3D_MT_PIE_View3D_Transform_Quick(Menu):
	bl_idname = "BSMAX_MT_pie_view3d_transform_quick"
	bl_label = "Transform"

	def draw(self, context):
		pie = self.layout.menu_pie()
		draw_transform_quick(context, pie)


classes = {
	VIEW3D_MT_PIE_View3D_Transform,
	VIEW3D_MT_PIE_View3D_Transform_Quick
}

def register_pie_transform():
	for cls in classes:
		register_class(cls)

def unregister_pie_transform():
	for cls in classes:
		unregister_class(cls)

if __name__ == '__main__':
	register_pie_transform()
