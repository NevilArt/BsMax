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
from bpy.types import Operator

class Object_OT_Freeze_Transform(Operator):
	bl_idname = "object.freeze_transform"
	bl_label = "Freeze Transform"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_location = obj.location
			obj.location = [0,0,0]
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
		self.report({'OPERATOR'},'bpy.ops.object.freeze_transform()')
		return{"FINISHED"}

class Object_OT_Freeze_Rotation(Operator):
	bl_idname = "object.freeze_rotation"
	bl_label = "Freeze Rotation"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
			self.report({'OPERATOR'},'bpy.ops.object.freeze_rotation()')
			return{"FINISHED"}

class Object_OT_Transform_To_Zero(Operator):
	bl_idname = "object.transform_to_zero"
	bl_label = "Transform To Zero"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			for obj in ctx.selected_objects:
				obj.location = [0,0,0]
				obj.rotation_euler = [0,0,0]
		elif ctx.mode == 'POSE':
			bpy.ops.pose.loc_clear()
			bpy.ops.pose.rot_clear()
			bpy.ops.pose.scale_clear()
		self.report({'OPERATOR'},'bpy.ops.object.transform_to_zero()')
		return{"FINISHED"}

class Object_OT_Rotation_To_Zero(Operator):
	bl_idname = "object.rotation_to_zero"
	bl_label = "Rotation To Zero"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.rotation_clear()
		elif ctx.mode == 'POSE':
			bpy.ops.pose.rot_clear()
		self.report({'OPERATOR'},'bpy.ops.object.rotation_to_zero()')
		return{"FINISHED"}

classes = [Object_OT_Freeze_Transform,
	Object_OT_Freeze_Rotation,
	Object_OT_Transform_To_Zero,
	Object_OT_Rotation_To_Zero]

def register_transform_control():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_transform_control():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_transform_control()