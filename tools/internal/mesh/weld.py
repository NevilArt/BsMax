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
# 2024/03/16

import bpy

from bpy.types import Operator, Menu
from bpy.props import FloatProperty, BoolProperty
from bpy.utils import register_class, unregister_class

from bsmax.graphic import Rubber_Band

# TARGET WELD
# Original Coded from Stromberg90 updated by Nevil
# https://github.com/Stromberg90/Scripts/tree/master/Blender


#TODO Target weld for edge mode same as vertex by face orient order

def select_vert(ctx, event, started):
	coord = (event.mouse_region_x, event.mouse_region_y)
	result = bpy.ops.view3d.select(extend=started, location=coord)
	if result == {'PASS_THROUGH'}:
		bpy.ops.mesh.select_all(action='DESELECT')


class Mesh_OT_Target_Weld(Operator):
	bl_idname = "mesh.target_weld"
	bl_label = "Target Weld"
	bl_options = {'REGISTER', 'UNDO'}
	
	start, end, handle = None, None, None
	drag, picked = False, False

	rb = Rubber_Band()

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if not event.type in {'LEFTMOUSE','RIGHTMOUSE', 'MOUSEMOVE','ESC'}:
			return {'PASS_THROUGH'}

		elif event.type == 'MOUSEMOVE':
			if self.start != None:
				self.end = event.mouse_region_x, event.mouse_region_y
				sx, sy = self.start
				ex, ey = self.end
				self.rb.create(sx, sy, ex, ey)

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				if self.start == None:
					self.start = event.mouse_region_x, event.mouse_region_y
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend=False, location=coord)

			if event.value =='RELEASE':
				self.end = event.mouse_region_x, event.mouse_region_y

				if self.start != None:
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend=True,location=coord)
					# bm = bmesh.from_edit_mesh(mesh)
					# bm.verts[index].co

				select_vert(ctx, event, self.start != None)
				if ctx.object.data.total_vert_sel == 2:
					self.start = self.end = None
					bpy.ops.mesh.merge(type='LAST')
					bpy.ops.mesh.select_all(action='DESELECT')
					self.rb.create(0, 0, 0, 0)

			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			self.rb.unregister()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def execute(self,ctx):
		return{"FINISHED"}

	def invoke(self, ctx, event):
		if ctx.space_data.type == 'VIEW_3D':
			self.rb.register()
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'CANCELLED'}


class VIEW3D_MT_edit_mesh_weld(Menu):
	bl_label = "Weld"
	def draw(self, ctx):
		self.layout.operator_enum("mesh.merge", "type")
		self.layout.operator("mesh.remove_doubles", text="Weld by distance")


class Mesh_OT_Weld(Operator):
	bl_idname = "mesh.weld"
	bl_label = "Weld"
	bl_options = {'REGISTER', 'UNDO'}

	threshold: FloatProperty(
		name='Merge Distance',
		min=0.00001, max=10, unit='LENGTH',
		default=0.001
	)
	use_unselected: BoolProperty()
	use_sharp_edge: BoolProperty()

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'threshold')
		layout.prop(self, 'use_unselected')
		layout.prop(self, 'use_sharp_edge')

	def execute(self,ctx):
		bpy.ops.mesh.remove_doubles(
			threshold=self.threshold,
			use_unselected=self.use_unselected,
			use_sharp_edge_from_normals=self.use_sharp_edge
		)
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)


classes = (
	Mesh_OT_Target_Weld,
	VIEW3D_MT_edit_mesh_weld,
	Mesh_OT_Weld
)


def register_weld():
	for c in classes:
		register_class(c)


def unregister_weld():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_weld()