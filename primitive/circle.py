import bpy
from primitive.primitive import CreatePrimitive, PrimitiveCurveClass
from bsmax.actions import delete_objects

def GetCircleShape(radius):
	Shapes = []
	r = radius
	t = r * 0.551786
	#t = r * 0.5522847498307933984022516322796
	pc1,pl1,pr1 = (0,-r,0),(-t,-r,0),(t,-r,0)
	pc2,pl2,pr2 = (r,0,0),(r,-t,0),(r,t,0)
	pc3,pl3,pr3 = (0,r,0),(t,r,0),(-t,r,0)
	pc4,pl4,pr4 = (-r,0,0),(-r,t,0),(-r,-t,0)
	pt1 = (pc1,pl1,'FREE',pr1,'FREE')
	pt2 = (pc2,pl2,'FREE',pr2,'FREE')
	pt3 = (pc3,pl3,'FREE',pr3,'FREE')
	pt4 = (pc4,pl4,'FREE',pr4,'FREE')
	Shapes.append([pt1,pt2,pt3,pt4])
	return Shapes

class Circle(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Circle"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetCircleShape(0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		shapes = GetCircleShape(pd.radius1)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateCircle(CreatePrimitive):
	bl_idname = "bsmax.createcircle"
	bl_label = "Circle (Create)"
	subclass = Circle()

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

def circle_cls(register):
	c = BsMax_OT_CreateCircle
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	circle_cls(True)

__all__ = ["circle_cls", "Circle"]