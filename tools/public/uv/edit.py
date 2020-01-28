import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

class BsMax_OT_TurnUV(Operator):
	bl_idname = "uv.turn"
	bl_label = "Turn (UV)"
	ccw: BoolProperty(name= "CCW")
	@classmethod
	def poll(self, ctx):
		return True
	def execute(self, ctx):
		value = 1.5708 if self.ccw else -1.5708
		bpy.ops.transform.rotate(value=value,orient_axis='Z',orient_type='VIEW',
						orient_matrix=((-1,-0,-0),(-0,-1,-0),(-0,-0,-1)),
						orient_matrix_type='VIEW',mirror=True,
						use_proportional_edit=False,proportional_edit_falloff='SMOOTH',
						proportional_size=1,use_proportional_connected=False,
						use_proportional_projected=False)
		return{"FINISHED"}

class BsMax_OT_test(Operator):
	bl_idname = "test.ok"
	bl_label = "Test"
	def execute(self, ctx):
		print("OK Pressed")
		return {'FINISHED'}

class BsMax_OT_test(Operator):
	bl_idname = "test.test"
	bl_label = "Test"
	def execute(self, ctx):
		if(bpy.ops.invoke_props_dialog(BsMax_OT_test)== {'FINISHED'}):
			if main(bpy.ctx):
				return {'FINISHED'}
		return {'CANCELLED'}


# class BsMax_OT_test(Operator):
# 	bl_idname = "test.test"
# 	bl_label = "Test"
# 	def execute(self, ctx):
# 		if(bpy.ops.invoke_props_dialog(<some_arguments_here>)== {'FINISHED'}):
# 			if main(bpy.ctx):
# 				return {'FINISHED'}
# 		return {'CANCELLED'}
# 	def invoke(self, context, event):
#         wm = context.window_manager
#         return wm.window_manager.invoke_props_dialog(operator, width=300, height=20)


def edit_cls(register):
	classes = [BsMax_OT_TurnUV, BsMax_OT_test]
	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	edit_cls(True)

__all__ = ["edit_cls"]

