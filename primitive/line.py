import bpy
from mathutils import Vector
from bsmax.math import get_axis_constraint
from primitive.primitive import CreatePrimitive, PrimitiveCurveClass
from bsmax.actions import delete_objects

class knot:
	def __init__(self, pos, invec, outvec, mode):
		self.pos = pos
		self.invec = invec
		self.outvec = outvec
		self.mode = mode

def GetLineShape(knots):
	shape = []
	for k in knots:
		shape.append((k.pos, k.invec, k.mode, k.outvec, k.mode))
	return [shape]

class Line(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Line"
		self.finishon = 0 # infinit
		self.owner = None
		self.data = None
		self.close = False
		self.knots = []
		self.lastknot = []
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetLineShape([])
		self.create_curve(ctx, shapes, "")
	def update(self):
		shapes = GetLineShape(self.knots + self.lastknot)
		self.update_curve(shapes)
	def abort(self):
		if len(self.knots) < 2:
			delete_objects([self.owner])
		else:
			self.lastknot = []
			self.knots.pop()
			self.update()
			bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

class BsMax_OT_CreateLine(CreatePrimitive):
	bl_idname = "bsmax.createline"
	bl_label = "Line (Create)"
	subclass = Line()
	lastclick = 1

	def create(self, ctx, clickpoint):
		self.usedkeys += ['LEFT_SHIFT', 'RIGHT_SHIFT', 'BACK_SPACE']
		self.requestkey = ['BACK_SPACE']
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		newknot = knot(clickpoint.view, clickpoint.view, clickpoint.view, "VECTOR")
		self.subclass.knots.append(newknot)

	def update(self, clickcount, dimantion):
		dim = dimantion
		if self.shift:
			index = -1 if len(self.subclass.knots) < 2 else -2
			lastpoint = self.subclass.knots[index].pos
			dim.view = get_axis_constraint(lastpoint, dim.view)

		if self.drag:
			pos = self.subclass.knots[-1].pos
			outvec = dim.view
			invec = Vector((0,0,0))
			invec.x = pos.x - (outvec.x - pos.x)
			invec.y = pos.y - (outvec.y - pos.y)
			invec.z = pos.z - (outvec.z - pos.z)
			newknot = knot(pos, invec, outvec, 'ALIGNED')
		else:
			newknot = knot(dim.view, dim.view, dim.view, "VECTOR")

		if clickcount != self.lastclick:
			self.subclass.knots.append(newknot)
			self.lastclick = clickcount

		self.subclass.knots[-1] = newknot
		self.subclass.lastknot = [knot(dim.view, dim.view, dim.view, "VECTOR")]

		if self.subclass.lastknot[0].pos == self.subclass.knots[0].pos:
			#TODO close on click near the start point
			#self.subclass.close = True
			print("close")
		
		self.subclass.update()

	def event(self, event, value):
		if event == 'BACK_SPACE':
			if value == 'RELEASE':
				if len(self.subclass.knots) > 2:
					self.subclass.knots.pop()
	def finish(self):
		pass

def line_cls(register):
	c = BsMax_OT_CreateLine
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	line_cls(True)

__all__ = ["line_cls"]