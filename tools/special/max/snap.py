import bpy
from bpy.types import Operator

class BsMax_OT_SnapSetting(Operator):
	bl_idname = "bsmax.snapsetting"
	bl_label = "Snap Setting"
	snap = ""

	def execute(self, ctx):
		t = ctx.scene.tool_settings
		# snap To (Poly)
		if self.snap == "Grid Points":
			t.snap_elements = {'INCREMENT'}
		elif self.snap == "Vertex":
			t.snap_elements = {'VERTEX'}
		elif self.snap == "Edge/Segment":
			t.snap_elements = {'EDGE'}
		elif self.snap == "Face":
			t.snap_elements = {'FACE'}
		elif self.snap == "Volume":
			t.snap_elements = {'VOLUME'}

		# snap To (UV)
		elif self.snap == "Vertex UV":
			t.snap_uv_element = 'VERTEX'
		elif self.snap == "Grid Points UV":
			t.snap_uv_element = 'INCREMENT'

		# snap The
		elif self.snap == "Active":
			t.snap_target = 'ACTIVE'
		elif self.snap == "Mediom":
			t.snap_target = 'MEDIAN'
		elif self.snap == "Center":
			t.snap_target = 'CENTER'
		elif self.snap == "Closest":
			t.snap_target = 'CLOSEST'

		# snap Setting
		elif self.snap == "Rotation":
			t.use_snap_align_rotation = not t.use_snap_align_rotation
		elif self.snap == "Peelobject":
			t.use_snap_peel_object = not t.use_snap_peel_object
		#update toolbar command neded
		return{"FINISHED"}

class Snap:
	def __init__(self,snap_elements,use_snap_translate,
					use_snap_rotate,use_snap_scale):
		self.snap_elements = snap_elements
		self.use_snap_translate = use_snap_translate
		self.use_snap_rotate = use_snap_rotate
		self.use_snap_scale = use_snap_scale
	def store(self,ctx):
		self.snap_elements = ctx.scene.tool_settings.snap_elements
	def restore(self,ctx):
		t = ctx.scene.tool_settings
		t.snap_elements = self.snap_elements
		t.use_snap_translate = self.use_snap_translate
		t.use_snap_rotate = self.use_snap_rotate
		t.use_snap_scale = self.use_snap_scale

class snap_setting:
	move = Snap({'INCREMENT'},True,False,False)
	rotate = Snap({'INCREMENT'},False,True,False)
	#scale = Snap(t.snap_elements,False,False,True)

class BsMax_OT_SnapToggle(Operator):
	bl_idname = "bsmax.snaptoggle"
	bl_label = "Snap Toggle"
	def execute(self, ctx):
		t = ctx.scene.tool_settings
		if t.use_snap_translate and t.use_snap:
			snap_setting.move.store(ctx)
			t.use_snap = False
			t.use_snap_translate = False
		else:
			t.use_snap = True
			snap_setting.move.restore(ctx)
			t.use_snap_translate = t.use_snap
		return{"FINISHED"}

class BsMax_OT_AngelSnap(Operator):
	bl_idname = "bsmax.angelsnap"
	bl_label = "Angel Snap"
	def execute(self, ctx):
		t = ctx.scene.tool_settings
		if t.use_snap_translate and t.use_snap:
			snap_setting.move.store(ctx)
			t.use_snap_translate = False

		if t.use_snap_rotate and t.use_snap:
			t.use_snap = False
			t.use_snap_rotate = False
		else:
			t.use_snap = True
			snap_setting.rotate.restore(ctx)
			t.use_snap_rotate = True
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