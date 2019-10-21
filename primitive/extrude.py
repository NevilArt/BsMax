import bpy
from bpy.types import Operator
from primitive.primitive import PrimitiveCurveClass
from bsmax.actions import delete_objects

def GetExtrudeShape(height, segs, start_height, end_height):
	Shape,heights = [],[0]
	if start_height > 0:
		heights.append(start_height)
	length = height - start_height - end_height
	step = length/segs
	for i in range(1,segs):
		h = start_height+i*step
		heights.append(h)
	if end_height > 0:
		heights.append(height - end_height)
	heights.append(height)
	for h in heights:
		p = (0,0,h)
		v = (p,p,'VECTOR',p,'VECTOR')
		Shape.append(v)
	Shape.reverse()
	return [Shape]

class Extrude(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Extrude"
		self.finishon = 0
		self.owner = None
		self.data = None
		self.close = False
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetExtrudeShape(1,1,0,0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		shapes = GetExtrudeShape(pd.height, pd.hsegs, pd.chamfer2, pd.chamfer1)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateExtrude(Operator):
	bl_idname = "bsmax.createextrudeshape"
	bl_label = "Extrude (Create)"
	bl_options = {"UNDO"}
	subclass = Extrude()

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.active_object != None:
				return ctx.active_object.type == 'CURVE'
		return False

	def execute(self, ctx):
		if len(ctx.selected_objects) == 1:
			target = ctx.selected_objects[0]
			self.subclass.create(ctx)
			self.subclass.data.bevel_object = target
			self.subclass.owner.location = target.location
			self.subclass.owner.rotation_euler = target.rotation_euler
		return{"FINISHED"}

def extrude_cls(register):
	c = BsMax_OT_CreateExtrude
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	extrude_cls(True)

__all__ = ["extrude_cls", "Extrude"]