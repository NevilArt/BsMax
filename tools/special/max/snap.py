import bpy
from bpy.types import Operator

class BsMax_OT_SnapSetting(Operator):
	bl_idname = "bsmax.snapsetting"
	bl_label = "Snap Setting"
	Snap = ""

	def execute(self, ctx):
		tool_set = ctx.scene.tool_settings
		# Snap To (Poly)
		if self.Snap == "Grid Points":
			tool_set.snap_elements = {'INCREMENT'}
		elif self.Snap == "Vertex":
			tool_set.snap_elements = {'VERTEX'}
		elif self.Snap == "Edge/Segment":
			tool_set.snap_elements = {'EDGE'}
		elif self.Snap == "Face":
			tool_set.snap_elements = {'FACE'}
		elif self.Snap == "Volume":
			tool_set.snap_elements = {'VOLUME'}

		# Snap To (UV)
		elif self.Snap == "Vertex UV":
			tool_set.snap_uv_element = 'VERTEX'
		elif self.Snap == "Grid Points UV":
			tool_set.snap_uv_element = 'INCREMENT'

		# Snap The
		elif self.Snap == "Active":
			tool_set.snap_target = 'ACTIVE'
		elif self.Snap == "Mediom":
			tool_set.snap_target = 'MEDIAN'
		elif self.Snap == "Center":
			tool_set.snap_target = 'CENTER'
		elif self.Snap == "Closest":
			tool_set.snap_target = 'CLOSEST'

		# Snap Setting
		elif self.Snap == "Rotation":
			State = tool_set.use_snap_align_rotation
			tool_set.use_snap_align_rotation = not State
		elif self.Snap == "Peelobject":
			State = tool_set.use_snap_peel_object
			tool_set.use_snap_peel_object = not State
		#update toolbar command neded
		return{"FINISHED"}

class BsMax_OT_SnapToggle(Operator):
	bl_idname = "bsmax.snaptoggle"
	bl_label = "Snap Toggle"
	def execute(self, ctx):
		State = ctx.scene.tool_settings.use_snap
		ctx.scene.tool_settings.use_snap = not State
		return{"FINISHED"}

class BsMax_OT_AngelSnap(Operator):
	bl_idname = "bsmax.angelsnap"
	bl_label = "Angel Snap"
	def execute(self, ctx):
		tool_set = ctx.scene.tool_settings
		tool_set.use_snap = True
		tool_set.snap_elements = {'INCREMENT'}
		tool_set.use_snap_translate = False
		tool_set.use_snap_rotate = True
		tool_set.use_snap_scale = False
		return{"FINISHED"}

def snap_cls(register):
	classes = [BsMax_OT_SnapSetting,BsMax_OT_SnapToggle,BsMax_OT_AngelSnap]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	snap_cls(True)

__all__ = ["snap_cls"]