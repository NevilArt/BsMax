import bpy, mathutils
from bpy.types import Operator
from mathutils import Matrix
from bsmax.actions import set_create_target, set_as_active_object, delete_objects
from bsmax.state import has_constraint

class BsMax_OT_MakeTargetLight(Operator):
	bl_idname = "bsmax.maketargetlight"
	bl_label = "Make Target Light"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and not has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		light = ctx.active_object
		set_create_target(light, None)
		set_as_active_object(ctx, light)
		return {'FINISHED'}

class BsMax_OT_MakeFreeLight(Operator):
	bl_idname = "bsmax.makefreelight"
	bl_label = "Make Free Light"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		obj = ctx.active_object
		transfoem = obj.matrix_world.copy()
		targ = obj.constraints["Track To"].target
		delete_objects([targ])
		TrackToConts = [ c for c in obj.constraints if c.type == 'TRACK_TO' ]
		for c in TrackToConts:
			obj.constraints.remove(c)
		obj.matrix_world = transfoem
		return {'FINISHED'}

def targetlight_cls(register):
	classes = [BsMax_OT_MakeTargetLight, BsMax_OT_MakeFreeLight]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	targetlight_cls(True)

__all__ = ["targetlight_cls"]