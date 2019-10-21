import bpy
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import delete_objects

def GetEllipseShape(length, width, outline, Thickness):
	Shapes = []
	el = [[length, width]]
	if outline:
		el.append([length + Thickness, width + Thickness])
	for r1, r2 in el:
		t1 = r1 * 0.551786
		t2 = r2 * 0.551786
		pc1, pl1, pr1 = ( 0,-r2, 0), (-t1, -r2, 0), (  t1, -r2, 0)
		pc2, pl2, pr2 = ( r1, 0, 0), ( r1, -t2, 0), (  r1,  t2, 0)
		pc3, pl3, pr3 = ( 0, r2, 0), ( t1,  r2, 0), ( -t1,  r2, 0)
		pc4, pl4, pr4 = (-r1, 0, 0), ( -r1, t2, 0), ( -r1, -t2, 0)
		pt1 = (pc1, pl1, 'FREE', pr1, 'FREE')
		pt2 = (pc2, pl2, 'FREE', pr2, 'FREE')
		pt3 = (pc3, pl3, 'FREE', pr3, 'FREE')
		pt4 = (pc4, pl4, 'FREE', pr4, 'FREE')
		Shapes.append([pt1, pt2, pt3, pt4])
	return Shapes

class Ellipse(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Ellipse"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetEllipseShape(0, 0, False, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		# length, width, outline, Thickness
		shapes = GetEllipseShape(pd.width, pd.length, pd.outline, pd.thickness)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateEllipse(CreatePrimitive):
	bl_idname = "bsmax.createellipse"
	bl_label = "Ellipse (Create)"
	subclass = Ellipse()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.width = dimantion.width
			self.params.length = dimantion.length
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def ellipse_cls(register):
	c = BsMax_OT_CreateEllipse
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	ellipse_cls(True)

__all__ = ["ellipse_cls", "Ellipse"]