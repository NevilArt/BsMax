import bpy
from bpy.types import Operator
from bpy.props import StringProperty

# Coordinate
class BsMax_OT_CoordSystem(Operator):
	bl_idname = "bsmax.coordinatesystem"
	bl_label = "Coordinate System"
	coordsys: bpy.props.StringProperty(default = 'GLOBAL')
	def execute(self, ctx):
		# NORMAL, GIMBAL, LOCAL, VIEW, GLOBAL, CURSOR
		ctx.window.scene.transform_orientation_slots[0].type = self.coordsys
		return{"FINISHED"}

class BsMax_OT_SetLocalCoordinPoseMode(Operator):
	bl_idname = "bsmax.setlocalcoordinposemode"
	bl_label = "Local (Pose)"
	def execute(self, ctx):
		ctx.window.scene.transform_orientation_slots[0].type = 'LOCAL'
		ctx.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
		return{"FINISHED"} 

def coordinate_cls(register):
	classes = [BsMax_OT_CoordSystem, BsMax_OT_SetLocalCoordinPoseMode]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	coordinate_cls(True)

__all__ = ["coordinate_cls"]