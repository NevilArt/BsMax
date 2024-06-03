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
# 2024/06/02

import bpy

from bpy.types import Operator, Menu
from bpy.utils import register_class, unregister_class


class View3D_OT_perespective(Operator):
	bl_idname = 'view3d.perespective'
	bl_label = "Perespective"

	mode: bpy.props.StringProperty(default='Toggle') # type: ignore
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		r3d = ctx.area.spaces[0].region_3d
		if self.mode == 'Toggle':
			if r3d.view_perspective == 'CAMERA':
				view_matrix = ctx.area.spaces.active.region_3d.view_matrix
				r3d.view_perspective = 'PERSP'
				ctx.area.spaces.active.region_3d.view_matrix = view_matrix

			elif r3d.view_perspective == 'PERSP':
				r3d.view_perspective = 'ORTHO'

			elif r3d.view_perspective == 'ORTHO':
				r3d.view_perspective = 'PERSP'

		elif self.mode == 'Perspective':
			r3d.view_perspective = 'PERSP'

		elif self.mode == 'Orthographic':
			r3d.view_perspective = 'ORTHO'

		return{'FINISHED'}


class Object_OT_Viewport_Display(Operator):
	bl_idname = 'object.viewoport_display'
	bl_label = "Object Viewport Dispaly"

	@classmethod
	def poll(self, ctx):
		return ctx.object

	def draw(self, ctx):
		layout = self.layout
		layout.prop(ctx.object, 'show_name', text="Name")
		layout.prop(ctx.object, 'show_axis', text="Axix")
		layout.prop(ctx.object, 'show_wire', text="Wireframe")
		layout.prop(ctx.object, 'show_all_edges', text="All Edges")
		layout.prop(ctx.object, 'show_texture_space', text="Texture Space")
		layout.prop(ctx.object.display, 'show_shadows', text="Shadow")
		layout.prop(ctx.object, 'show_in_front', text="In Front")
		layout.prop(ctx.object, 'color', text="Color")
		layout.prop(ctx.object, 'display_type', text="Display As")

		row = layout.row()
		row.prop(ctx.object, 'show_bounds', text="Bounds")
		row.prop(ctx.object, 'display_bounds_type', text="")
		layout.label(text="'Hold Alt for Apply Selection'")

	def execute(self, _):
		return {'FINISHED'}

	def cancel(self, _):
		return None
	
	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self, width=150)
	

class View3D_MT_Import_Float(Menu):
	bl_idname = 'VIEW3D_MT_import_float'
	bl_label = "Import"

	def draw(self, ctx):
		layout = self.layout
		layout.operator('wm.link', text="Link", icon='LINK_BLEND')
		layout.operator(
			'wm.append', text="Append", icon='APPEND_BLEND'
		)
		if ctx.mode == 'OBJECT':
			layout.menu('TOPBAR_MT_file_import', icon='IMPORT')


def import_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.menu('VIEW3D_MT_import_float', text="Import", icon='IMPORT')


classes = {
	View3D_OT_perespective,
	Object_OT_Viewport_Display,
	View3D_MT_Import_Float
}


def register_view3d():
	for cls in classes:
		register_class(cls)

	bpy.types.VIEW3D_MT_add.append(import_menu)


def unregister_view3d():
	bpy.types.VIEW3D_MT_add.remove(import_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_view3d()