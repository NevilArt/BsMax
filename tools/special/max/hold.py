import bpy
from bpy.types import Operator

class BsMax_OT_Hold(Operator):
		bl_idname = "bsmax.hold"
		bl_label = "Hold"
		def execute(self, ctx):
			print("Hold coming soon")
			return{"FINISHED"}

class BsMax_OT_Fetch(Operator):
		bl_idname = "bsmax.fetch"
		bl_label = "Fetch"
		def execute(self, ctx):
				print("Fetch coming soon")
				return{"FINISHED"}

def hold_cls(register):
	classes = [BsMax_OT_Hold, BsMax_OT_Fetch]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	hold_cls(True)

__all__ = ["hold_cls"]