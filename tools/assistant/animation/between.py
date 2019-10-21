import bpy
from bpy.types import Operator

class BsMax_TO_Between(Operator):
	bl_idname = "animation.between"
	bl_label = "Between"
	def execute(self, contecxt):
		print(between)
		return{"FINISHED"}

def between_cls(register):
	classes = [BsMax_TO_Between]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	between_cls(True)

__all__ = ["between_cls"]