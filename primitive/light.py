import bpy
from bpy.props import BoolProperty
from math import pi, sin, cos
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import set_create_target, delete_objects

def GetCompassShape(radius):
	r = radius
	verts = [(0,r,0),(0.1*r,0.2*r,0),(0.3*r,0.3*r,0),(0.2*r,0.1*r,0),
			(r,0,0),(0.2*r,-0.1*r,0),(0.3*r,-0.3*r,0),(0.1*r,-0.2*r,0),
			(0,-1*r,0),(-0.1*r,-0.2*r,0),(-0.3*r,-0.3*r,0),(-0.2*r,-0.1*r,0),
			(-1.0*r,0,0),(-0.2*r,0.1*r,0),(-0.3*r,0.3*r,0),(-0.1*r,0.2*r,0)]
	shape = [(v,v,'FREE',v,'FREE') for v in verts]
	return [shape]

class Light:
	def __init__(self):
		self.finishon = 2
		self.owner = None
		self.target = None
	def reset(self):
		self.__init__()
	def create(self, ctx, datatype):
		name = datatype.capitalize()
		newdata = bpy.data.lights.new(name=name, type=datatype)
		newlight = bpy.data.objects.new(name=name, object_data=newdata)
		ctx.collection.objects.link(newlight)
		ctx.view_layer.objects.active = newlight
		newlight.select_set(True)
		self.owner = newlight
	def abort(self):
		delete_objects([self.owner, self.target])

class Compass(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Compass"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetCompassShape(0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self, ctx):
		pd = self.data.primitivedata
		shapes = GetCompassShape(pd.radius1)
		self.update_curve(ctx, shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreatePointLight(CreatePrimitive):
	bl_idname="bsmax.createpointlight"
	bl_label="Point Light (Create)"
	subclass = Light()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx, 'POINT')
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if self.drag:
			self.subclass.owner.location = dimantion.view
	def finish(self):
		pass

class BsMax_OT_CreateSpotLight(CreatePrimitive):
	bl_idname="bsmax.createspotlight"
	bl_label="Spot Light (Create)"
	subclass = Light()
	subclass.finishon = 2

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx, 'SPOT')
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.drag and self.subclass.target == None:
				self.subclass.target = set_create_target(self.subclass.owner, None)
			if self.subclass.target != None:
				self.subclass.target.location = dimantion.view
	def finish(self):
		pass

class BsMax_OT_CreateSunLight(CreatePrimitive):
	bl_idname="bsmax.creatsunlight"
	bl_label="Sun Light (Create)"
	subclass = Light()
	compass = Compass()
	distance = 0
	context = None

	def create(self, ctx, clickpoint):
		self.subclass.finishon = 3
		self.compass.create(ctx)
		self.compass.owner.location = clickpoint.view
		self.params = self.compass.owner.data.primitivedata
		self.context = ctx
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
			self.compass.update(ctx)
		if clickcount == 2:
			if self.subclass.owner == None:
				self.subclass.create(self.context, "SUN")
				self.subclass.target = self.compass.owner
				self.subclass.owner.location = self.compass.owner.location
				set_create_target(self.subclass.owner, self.subclass.target)
			self.distance = dimantion.height
			self.subclass.owner.location.z = self.distance
		if clickcount == 3:
			if self.distance > 0:
				# TODO create a better way to caculate angle
				# store angle in prim data
				dx = dimantion.width
				dy = dimantion.length
				delta = dx if abs(dx) > abs(dy) else dy
				delta = delta if delta < self.distance else self.distance
				delta = delta if delta > -self.distance else -self.distance
				teta = (-pi/2)*(delta/self.distance)
				x = sin(teta) * self.distance
				z = cos(teta) * self.distance
				self.subclass.owner.location.x = self.subclass.target.location.x + x
				self.subclass.owner.location.z = self.subclass.target.location.z + z
	def finish(self):
		self.subclass.owner.parent = self.subclass.target
		self.subclass.owner.matrix_parent_inverse = self.subclass.target.matrix_world.inverted()

class BsMax_OT_CreateAreaLight(CreatePrimitive):
	bl_idname="bsmax.createarealight"
	bl_label="Area Light (Create)"
	subclass = Light()
	free: BoolProperty(name="Free", default=False)

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx, 'AREA')
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
		self.subclass.finishon = 2 if self.free else 3
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			width = dimantion.width
			length = dimantion.length
			self.subclass.owner.data.size = max(width, length)
			if max(width, length) > 0:
				aspect = min(width, length) / max(width, length)
				if width > length:
					self.subclass.owner.scale = (1, aspect, 1)
				else:
					self.subclass.owner.scale = (aspect, 1, 1)
			self.subclass.owner.location = dimantion.center
		if clickcount == 2 and not self.free:
			if self.subclass.target == None:
				self.subclass.target = set_create_target(self.subclass.owner, None)
			self.subclass.target.location = dimantion.view
	def finish(self):
		pass


def light_cls(register):
	classes = [BsMax_OT_CreatePointLight, BsMax_OT_CreateSunLight,
			BsMax_OT_CreateSpotLight, BsMax_OT_CreateAreaLight]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	light_cls(True)

__all__ = ["light_cls", "Compass"]