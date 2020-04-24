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

class BsMax_OT_FreezeTransform(Operator):
	bl_idname = "bsmax.freezetransform"
	bl_label = "Freeze Transform"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_location = obj.location
			obj.location = [0,0,0]
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
		return{"FINISHED"}

class BsMax_OT_FreezeRotation(Operator):
	bl_idname = "bsmax.freezerotation"
	bl_label = "Freeze Rotation"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.delta_rotation_euler = obj.rotation_euler
			obj.rotation_euler = [0,0,0]
			return{"FINISHED"}

class BsMax_OT_TransformToZero(Operator):
	bl_idname = "bsmax.transformtozero"
	bl_label = "Transform To Zero"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.location = [0,0,0]
			obj.rotation_euler = [0,0,0]
		return{"FINISHED"}

class BsMax_OT_RotationToZero(Operator):
	bl_idname = "bsmax.rotationtozero"
	bl_label = "Rotation To Zero"
	def execute(self, ctx):
		bpy.ops.object.rotation_clear()
		return{"FINISHED"}

classes = [BsMax_OT_FreezeTransform,
	BsMax_OT_FreezeRotation,
	BsMax_OT_TransformToZero,
	BsMax_OT_RotationToZero]

def register_transform():
	[bpy.utils.register_class(c) for c in classes]

def unregister_transform():
	[bpy.utils.unregister_class(c) for c in classes]