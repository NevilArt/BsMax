import bpy
from bpy.types import Operator

# Act like Convert to in 3ds Max
class BsMax_OT_ClearPrimitiveData(Operator):
	# TODO replace this with a smart conver tool
	bl_idname="bsmax.clearprimitivedta"
	bl_label="Clear Primitive Data"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.data.primitivedata.classname = ""
		return {"FINISHED"}

def BsMax_MT_PrimitiveDataCleanerMenu(self, context):
	self.layout.separator()
	self.layout.operator("bsmax.clearprimitivedta")

def ui_cls(register):
	c = BsMax_OT_ClearPrimitiveData
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	ui_cls(True)

__all__ = ["ui_cls", "BsMax_MT_PrimitiveDataCleanerMenu"]