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

def transform_cls(register):
	classes = [BsMax_OT_FreezeTransform,
		BsMax_OT_FreezeRotation,
		BsMax_OT_TransformToZero,
		BsMax_OT_RotationToZero]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	transform_cls(True)

__all__ = ["transform_cls"]