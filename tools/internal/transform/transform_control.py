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

from bpy.types import Operator, Menu
from bpy.props import BoolProperty

from bsmax.actions import freeze_transform



class Object_OT_Freeze_Transform(Operator):
	""" Copy selected objects transform to Delta transform and reset transform values """
	bl_idname = "object.freeze_transform"
	bl_label = "Freeze Transform"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	location: BoolProperty(name="Location", default=True)
	rotation: BoolProperty(name="Rotation", default=True)
	scale: BoolProperty(name="Scale", default=True)
	
	def execute(self, ctx):
		freeze_transform(ctx.selected_objects,
			location=self.location,
			rotation=self.rotation,
			scale=self.scale)
		return{"FINISHED"}



class Object_OT_Transform_To_Zero(Operator):
	""" Clare transform """
	bl_idname = "object.transform_to_zero"
	bl_label = "Transform To Zero"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	location: BoolProperty(name="Location", default=True)
	rotation: BoolProperty(name="Rotation", default=True)
	scale: BoolProperty(name="Scale", default=True)
	
	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			if self.location:
				bpy.ops.object.location_clear(clear_delta=False)
			if self.rotation:
				bpy.ops.object.rotation_clear(clear_delta=False)
			if self.scale:
				bpy.ops.object.scale_clear(clear_delta=False)

		elif ctx.mode == 'POSE':
			if self.location:
				bpy.ops.pose.loc_clear()
			if self.rotation:
				bpy.ops.pose.rot_clear()
			if self.scale:
				bpy.ops.pose.scale_clear()

		return{"FINISHED"}



class Object_OT_Transform_Copy(Operator):
	""" Copy Transform to buffer """
	bl_idname = "object.transform_copy"
	bl_label = "Copy Transform"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT' and ctx.active_object

	def execute(self, ctx):
		string = 'BSMAXTRANSFORMCLIPBOARD\n'
		for matrix in ctx.object.matrix_world:
			for m in matrix:
				string += str(m) + '\n'
		ctx.window_manager.clipboard = string
		return{"FINISHED"}



class Object_OT_Transform_Paste(Operator):
	""" Paste transform from buffer """
	bl_idname = "object.transform_paste"
	bl_label = "Paste Transform"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT' and ctx.active_object

	def matrix_from_clipboard(self, ctx):
		string = ctx.window_manager.clipboard
		lines = string.splitlines()
		if len(lines) == 17:
			if not lines[0] == 'BSMAXTRANSFORMCLIPBOARD':
				return None
			matrix = ctx.object.matrix_world.copy()

			m = []
			for line in lines[1:]:
				m.append(float(line))

			matrix[0][0] = m[0]
			matrix[0][1] = m[1]
			matrix[0][2] = m[2]
			matrix[0][3] = m[3]

			matrix[1][0] = m[4]
			matrix[1][1] = m[5]
			matrix[1][2] = m[6]
			matrix[1][3] = m[7]

			matrix[2][0] = m[8]
			matrix[2][1] = m[9]
			matrix[2][2] = m[10]
			matrix[2][3] = m[11]

			matrix[3][0] = m[12]
			matrix[3][1] = m[13]
			matrix[3][2] = m[14]
			matrix[3][3] = m[15]

			return matrix

		return None
	
	def execute(self, ctx):
		matrix_world = self.matrix_from_clipboard(ctx)

		if matrix_world:
			ctx.object.matrix_world = matrix_world

		return{"FINISHED"}



#TODO for now is ok but nedd to moveto better place if add more items
class Object_MT_Object_Copy(Menu):
	bl_idname = "OBJECT_MT_object_copy"
	bl_label = "Copy"

	def draw(self, ctx):
		layout=self.layout
		layout.operator("view3d.copybuffer", text="Object")
		layout.operator("object.transform_copy", text="Transform")



class Object_MT_Object_Paste(Menu):
	bl_idname = "OBJECT_MT_object_paste"
	bl_label = "Paste"

	def draw(self, ctx):
		layout=self.layout
		layout.operator("view3d.pastebuffer", text="Object")
		layout.operator("object.transform_paste", text="Transform")



classes = [
			Object_OT_Freeze_Transform,
			Object_OT_Transform_To_Zero, 
			Object_OT_Transform_Copy,
			Object_OT_Transform_Paste,
			Object_MT_Object_Copy,
			Object_MT_Object_Paste
		]

def register_transform_control():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_transform_control():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_transform_control()