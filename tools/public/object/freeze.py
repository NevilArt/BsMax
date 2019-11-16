import bpy
from bpy.types import Operator

class BsMax_OT_FreezeSelected(Operator):
	bl_idname = "bsmax.freezeselectedobjects"
	bl_label = "Freeze Objects"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.hide_select = True
		return{"FINISHED"}

class BsMax_OT_UnFreezeAll(Operator):
	bl_idname = "bsmax.unfreezeallobjects"
	bl_label = "Freeze Objects"
	def execute(self, ctx):
		for obj in bpy.data.objects:
			obj.hide_select = False
		return{"FINISHED"}

def freeze_cls(register):
	classes = [BsMax_OT_FreezeSelected, BsMax_OT_UnFreezeAll]

	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	freeze_cls(True)

__all__ = ["freeze_cls"]