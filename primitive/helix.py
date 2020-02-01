import bpy
from math import radians, pi, sin, cos
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_bias

def GetHelixshape(radius1, radius2, height, turns, segs, bias, ccw):
	shape = []
	r1,r2 = radius1,radius2
	totatdig = (pi*2)*turns
	if ccw:
		totatdig *= -1
	if turns == 0:
		turns = 0.0001
	piece = totatdig/(segs*turns)
	hpiece = height/(segs*turns)
	rpiece = (r1-r2)/(segs*turns)
	for i in range(int(segs*turns)):
		x = sin(piece*i)*(r1-(rpiece*i))
		y = cos(piece*i)*(r1-(rpiece*i))
		if height > 0:
			percent = (hpiece*i)/height
		else:
			percent = 0
		z = height*get_bias(bias,percent)
		p = (x,y,z)
		shape.append((p,p,'ALIGNED',p,'ALIGNED'))
	return [shape]

class Helix(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Helix"
		self.finishon = 4
		self.owner = None
		self.data = None
		self.close = False
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetHelixshape(0,0,0,3,20,0,False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.turns = 3
		pd.ssegs = 20
	def update(self, ctx):
		pd = self.data.primitivedata
		# radius1, radius2, height, turns, segs, bias, ccw
		shapes = GetHelixshape(pd.radius1, pd.radius2, pd.height,
					pd.turns, pd.ssegs, pd.bias_np, pd.ccw)
		self.update_curve(ctx, shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateHelix(CreatePrimitive):
	bl_idname = "bsmax.createhelix"
	bl_label = "Helix (Create)"
	subclass = Helix()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
			self.params.radius2 = dimantion.radius
		if clickcount == 2:
			self.params.height = dimantion.height
		if clickcount == 3:
			radius = self.params.radius1 + dimantion.height_np
			self.params.radius2 = 0 if radius < 0 else radius
		if clickcount > 0:
			self.subclass.update(ctx)
	def finish(self):
		pass

def helix_cls(register):
	c = BsMax_OT_CreateHelix
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	helix_cls(True)

__all__ = ["helix_cls", "Helix"]