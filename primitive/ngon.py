import bpy
from math import pi, sqrt, sin, cos
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import delete_objects

def GetNGonShape(radius, sides, cornerradius, circular):
	Shape = []
	kappa = 4 * (sqrt(2) - 1) / 3
	step = (pi*2) / sides
	unitVec = step * kappa / (pi/2)
	# corrective for 3 side shape
	# elif sides == 3:
	# 	unitVec = step * kappa / 3.00196 #86.0 in dggre
	for i in range(sides):
		theta = step * i
		lx = radius * cos(theta)
		ly = radius * sin(theta)
		xTan = -ly * unitVec
		yTan =  lx * unitVec
		pcn = (lx, ly, 0)
		pln = ((lx - xTan), (ly - yTan), 0)
		prn = ((lx + xTan), (ly + yTan), 0)

		if circular:
			Shape.append([pcn, pln, 'ALIGNED', prn, 'ALIGNED'])
		else:
			Shape.append([pcn, pln, 'VECTOR', prn, 'VECTOR'])
	return [Shape]

class NGon(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "NGon"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetNGonShape(0, 5, 0, False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 5
	def update(self):
		pd = self.data.primitivedata
		# radius, sides, cornerradius, circular
		shapes = GetNGonShape(pd.radius1, pd.ssegs, pd.chamfer1, pd.smooth)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateNGon(CreatePrimitive):
	bl_idname = "bsmax.createngon"
	bl_label = "NGon (Create)"
	subclass = NGon()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def ngon_cls(register):
	c = BsMax_OT_CreateNGon
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	ngon_cls(True)

__all__ = ["ngon_cls", "NGon"]