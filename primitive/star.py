import bpy
from math import pi, sin, cos
from random import random, seed
from primitive.primitive import CreatePrimitive, PrimitiveCurveClass
from bsmax.actions import delete_objects

def get_star_shape(radius1, radius2, points, distortion, 
						filletradius1, filletradius2, randseed, randval):
	shape = []
	step = (pi*2) / float(points)
	seed(randseed)
	drnd = randval*2
	for i in range(points):
		s = i*((pi*2)/points)
		r = [random()*drnd - randval for i in range(4)] if randval != 0 else [0,0,0,0]
		x0 = sin(s+distortion)*radius1+r[0]
		y0 = cos(s+distortion)*radius1+r[1]
		x1 = sin(s+(step/2))*radius2+r[2]
		y1 = cos(s+(step/2))*radius2+r[3]
		pc0,pl0,pr0 = (x0,y0,0),(x0,y0,0),(x0,y0,0)
		pc1,pl1,pr1 = (x1,y1,0),(x1,y1,0),(x1,y1,0)       
		shape.append((pc0,pl0,'VECTOR',pr0,'VECTOR'))
		shape.append((pc1,pl1,'VECTOR',pr1,'VECTOR'))
	return [shape]

class Star(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Star"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = get_star_shape(0,0,5,0,0,0,0,0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 5
	def update(self, ctx):
		pd = self.data.primitivedata
		#radius1, radius2, points, distortion, filletradius1, filletradius2, seed, randval
		shapes = get_star_shape(pd.radius1, pd.radius2, pd.ssegs, pd.twist, 
						pd.chamfer1, pd.chamfer2, pd.seed, pd.random)
		self.update_curve(ctx, shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateStar(CreatePrimitive):
	bl_idname = "bsmax.createstar"
	bl_label = "Star (Create)"
	subclass = Star()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
			self.params.radius2 = self.params.radius1 / 2
		elif clickcount == 2:
			self.params.radius2 = dimantion.radius_from_start_point
		if clickcount > 0:
			self.subclass.update(ctx)
	def finish(self):
		pass

def star_cls(register):
	c = BsMax_OT_CreateStar
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	star_cls(True)

__all__ = ["star_cls", "Star"]