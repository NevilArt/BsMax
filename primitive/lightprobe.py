import bpy
from mathutils import Vector
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_offset_by_orient

class LightProbe:
	def __init__(self):
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateLightProbeGrid(CreatePrimitive):
	bl_idname="bsmax.createlightprobegrid"
	bl_label="Irradiance Volume (Create)"
	subclass = LightProbe()
	width,length,height,distance = 0,0,0,0
	location = Vector((0,0,0))

	def create(self, ctx, clickpoint):
		self.subclass.finishon = 4
		bpy.ops.object.lightprobe_add(type='GRID', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.width = dimantion.width / 2
			self.length = dimantion.length / 2
			self.location = self.subclass.owner.location = dimantion.center
		if clickcount == 2:
			self.height = dimantion.height / 2
			offset = get_offset_by_orient(Vector((0,0,dimantion.height / 2)), dimantion.view_name)
			self.subclass.owner.location = self.location + offset
		if clickcount == 3:
			scale = 1 / max(self.width, self.length, self.height)
			self.distance = dimantion.height * scale
		if clickcount > 0:
			self.subclass.owner.scale = (self.width, self.length, self.height)
			self.subclass.owner.data.influence_distance = self.distance
	def finish(self):
		self.width,self.length,self.height,self.distance = 0,0,0,0

class BsMax_OT_CreateLightProbePlaner(CreatePrimitive):
	bl_idname="bsmax.createlightprobeplaner"
	bl_label="Reflection Plane (Create)"
	subclass = LightProbe()
	width,length,distance = 0,0,0

	def create(self, ctx, clickpoint):
		self.subclass.finishon = 3
		bpy.ops.object.lightprobe_add(type='PLANAR', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.width = dimantion.width
			self.length = dimantion.length
		if clickcount == 2:
			self.distance = dimantion.height
		if clickcount > 0:
			self.subclass.owner.scale = (self.width, self.length, 1)
			self.subclass.owner.data.influence_distance = self.distance
	def finish(self):
		pass

class BsMax_OT_CreateLightProbeCubemap(CreatePrimitive):
	bl_idname = "bsmax.createlightprobecubemap"
	bl_label = "Reflection Cubemap (Create)"
	subclass = LightProbe()

	def create(self, ctx, clickpoint):
		bpy.ops.object.lightprobe_add(type='CUBEMAP', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.data.influence_distance = dimantion.radius
			self.subclass.owner.scale = (1,1,1)
	def finish(self):
		pass

def lightprobe_cls(register):
	classes = [BsMax_OT_CreateLightProbeGrid,
			BsMax_OT_CreateLightProbePlaner,
			BsMax_OT_CreateLightProbeCubemap]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	lightprobe_cls(True)

__all__ = ["lightprobe_cls"]