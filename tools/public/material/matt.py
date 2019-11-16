import bpy
from bpy.types import Operator

class BsMax_OT_AssignToSelection(Operator):
	bl_idname = "material.assigntoselection"
	bl_label = "Assign to selected objects"
	bl_description = "Assign Material to selected objects"

	# @classmethod
	# def poll(self, ctx):
	# 	return len(ctx.selected_objects) > 1

	def execute(self, ctx):
		for o in ctx.selected_objects:
			pass
		print(ctx.area.type)
		print(ctx.space_data.type)
		return{"FINISHED"}

def matt_cls(register):
	classes = [BsMax_OT_AssignToSelection]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	matt_cls(True)

__all__ = ["matt_cls"]