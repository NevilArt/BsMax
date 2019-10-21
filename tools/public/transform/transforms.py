import bpy
from bpy.props import StringProperty,BoolProperty,FloatProperty
from bpy.types import Operator

class BsMax_OT_TransformGizmoSize(Operator):
	bl_idname = "bsmax.transformgizmosize"
	bl_label = "Transform Gizmo Size"
	step: FloatProperty()
	def execute(self, ctx):
		ctx.user_preferences.view.gizmo_size += self.step
		return{"FINISHED"}

class BsMax_OT_Move(Operator):
	bl_idname = "bsmax.move"
	bl_label = "Move"
	def execute(self, ctx):
		mode = ctx.mode
		tool = ctx.workspace.tools.from_space_view3d_mode(mode,create=False).idname
		if tool == "builtin.select":
			ctx.space_data.show_gizmo_object_translate = True
			ctx.space_data.show_gizmo_object_rotate = False
			ctx.space_data.show_gizmo_object_scale = False
		else:
			bpy.ops.wm.tool_set_by_id(name="builtin.move")
		return{"FINISHED"}

class BsMax_OT_Rotate(Operator):
	bl_idname = "bsmax.rotate"
	bl_label = "Rotate"
	def execute(self, ctx):
		mode = ctx.mode
		tool = ctx.workspace.tools.from_space_view3d_mode(mode,create=False).idname
		if tool == "builtin.select":
			ctx.space_data.show_gizmo_object_translate = False
			ctx.space_data.show_gizmo_object_rotate = True
			ctx.space_data.show_gizmo_object_scale = False
		else:
			bpy.ops.wm.tool_set_by_id(name="builtin.rotate")
		return{"FINISHED"}

class BsMax_OT_Scale(Operator):
	bl_idname = "bsmax.scale"
	bl_label = "Scale"
	def execute(self, ctx):
		mode = ctx.mode
		tool = ctx.workspace.tools.from_space_view3d_mode(mode,create=False).idname
		if tool == "builtin.select":
			ctx.space_data.show_gizmo_object_translate = False
			ctx.space_data.show_gizmo_object_rotate = False
			ctx.space_data.show_gizmo_object_scale = True
		else:
			bpy.ops.wm.tool_set_by_id(name="builtin.scale",cycle=True)
		return{"FINISHED"}

# "TweakBetter" created by Dan Pool (dpdp)
# original addon "qwer_addon"
# https://blenderartists.org/t/qwer-addon-or-how-i-stopped-using-the-transform-active-tools/1157507
class BsMax_OT_TweakBetter(Operator):
	"""Fix the select active tool"""
	bl_idname = "bsmax.tweakbetter"
	bl_label = "Tweak Better"
	tmode: StringProperty(name="Transform Mode")
	release: BoolProperty(name="Confirm on Release")

	def modal(self, ctx, event):
		if event.type == 'MOUSEMOVE':
			bpy.ops.transform.transform('INVOKE_DEFAULT',mode=self.tmode,
										release_confirm=self.release)
			return {'FINISHED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		if ctx.object:
			if ctx.space_data.show_gizmo_object_translate == True:
				self.tmode = 'TRANSLATION'
			elif ctx.space_data.show_gizmo_object_rotate == True:
				self.tmode = 'ROTATION'
			elif ctx.space_data.show_gizmo_object_scale == True:
				self.tmode = 'RESIZE'
			else: self.tmode = 'TRANSLATION'
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "No active object, could not finish")
			return {'CANCELLED'}

def transforms_cls(register):
	classes = [BsMax_OT_TransformGizmoSize,BsMax_OT_TweakBetter,
			BsMax_OT_Move,BsMax_OT_Rotate,BsMax_OT_Scale]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	transforms_cls(True)

__all__ = ["transforms_cls"]