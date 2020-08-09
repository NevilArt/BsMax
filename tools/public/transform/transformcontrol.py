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
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_location = obj.location
			obj.location = [0,0,0]
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
		self.report({'INFO'},'bpy.ops.object.freeze_transform()')
		return{"FINISHED"}

class Object_OT_Freeze_Rotation(Operator):
	bl_idname = "object.freeze_rotation"
	bl_label = "Freeze Rotation"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
			self.report({'INFO'},'bpy.ops.object.freeze_rotation()')
			return{"FINISHED"}

class Object_OT_Transform_To_Zero(Operator):
	bl_idname = "object.transform_to_zero"
	bl_label = "Transform To Zero"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.location = [0,0,0]
			obj.rotation_euler = [0,0,0]
		self.report({'INFO'},'bpy.ops.object.transform_to_zero()')
		return{"FINISHED"}

class Object_OT_Rotation_To_Zero(Operator):
	bl_idname = "object.rotation_to_zero"
	bl_label = "Rotation To Zero"
	def execute(self, ctx):
		bpy.ops.object.rotation_clear()
		self.report({'INFO'},'bpy.ops.object.rotation_to_zero()')
		return{"FINISHED"}

classes = [Object_OT_Freeze_Transform,
	Object_OT_Freeze_Rotation,
	Object_OT_Transform_To_Zero,
	Object_OT_Rotation_To_Zero]

def register_transformcontrol():
	[bpy.utils.register_class(c) for c in classes]

def unregister_transformcontrol():
	[bpy.utils.unregister_class(c) for c in classes]