import bpy, mathutils
from bpy.types import Operator
from mathutils import Matrix
from bsmax.actions import set_create_target, set_as_active_object, delete_objects
from bsmax.state import has_constraint

class BsMax_OT_MakeTargetCamera(Operator):
	bl_idname = "bsmax.maketargetcamera"
	bl_label = "Make Target Camera"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'CAMERA' and not has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.active_object
		set_create_target(cam, None)
		set_as_active_object(ctx, cam)
		return {'FINISHED'}

class BsMax_OT_MakeFreeCamera(Operator):
	bl_idname = "bsmax.makefreecamera"
	bl_label = "Make Free Camera"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'CAMERA' and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.active_object
		transfoem = cam.matrix_world.copy()
		targ = cam.constraints["Track To"].target
		delete_objects([targ])
		TrackToConts = [ c for c in cam.constraints if c.type == 'TRACK_TO' ]
		for c in TrackToConts:
			cam.constraints.remove(c)
		cam.matrix_world = transfoem
		return {'FINISHED'}

class BsMax_OT_SelectTarget(Operator):
	bl_idname = "bsmax.selecttarget"
	bl_label = "Select Target"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type in ['CAMERA', 'LIGHT'] and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		obj = ctx.active_object
		targ = obj.constraints["Track To"].target
		set_as_active_object(ctx, targ)
		return {'FINISHED'}

def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("bsmax.maketargetcamera")
	layout.operator("bsmax.makefreecamera")
	layout.operator("bsmax.selecttarget")

def targetcamera_cls(register):
	classes = [BsMax_OT_MakeTargetCamera,
		BsMax_OT_MakeFreeCamera,
		BsMax_OT_SelectTarget]

	if register:
		[bpy.utils.register_class(c) for c in classes]
		bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)
	else:
		bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)
		[bpy.utils.unregister_class(c) for c in classes]
		

if __name__ == '__main__':
	targetcamera_cls(True)

__all__ = ["targetcamera_cls"]