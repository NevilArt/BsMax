import bpy
from bpy.types import Operator
from math import pi, sin, cos, radians
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def GetCapsuleMesh(radius, height, ssegs, csegs, hsegs, sliceon, sfrom, sto):
	verts, edges, faces = [], [], []
	sides, heights = [], []
	arcrange, slicestep, r = pi*2, 0, radius
	# height
	if sliceon:
		arcrange, slicestep = radians(sto - sfrom), 1

	# collect segments x y onece
	for i in range(ssegs + slicestep):
		d = (arcrange / ssegs) * i + radians(sfrom)
		sides.append([sin(d), cos(d)])

	# collect cap arc height and scale
	for i in range(csegs):
		d = ((pi/2) / csegs) * i
		s = cos(d)
		h = sin(d)
		heights.append([h, s])
	heights.reverse()

	# add one more step if sclise is on
	ssegs += slicestep
	# Create vertexes data
	step = (pi*2) / ssegs

	# first vertex
	verts.append([0,0,0])
	# lower part
	for h, s in heights:
		for x, y in sides:
			X = r * x * s
			Y = r * y * s
			Z = radius - r * h
			verts.append([X, Y, Z])
		if sliceon:
			verts.append([0, 0, Z])

	# Cylinder part
	h = height / hsegs
	for i in range(1, hsegs):
		for x, y in sides:
			X = r * x
			Y = r * y
			Z = radius + h * i
			verts.append([X, Y, Z])
		if sliceon:
				verts.append([0, 0, Z])

	# uppaer part
	heights.reverse()
	for h, s in heights:
		for x, y in sides:
			X = r * x * s
			Y = r * y * s
			Z = radius + r * h + height
			verts.append([X, Y, Z])
		if sliceon:
			verts.append([0, 0, Z])
	# add last vertex
	verts.append([0,0,radius * 2 + height])

	# uper triangles faces
	if sliceon:
		ssegs += 1
	for i in range(ssegs):
		a = i + 1
		b = i + 2
		c = 0
		if i < ssegs - 1:
			faces.append((a, b, c))
		else:
			faces.append((a, 1, c))

	# body faces
	for i in range(csegs * 2 + hsegs - 2):
		for j in range(ssegs):
			a = i * ssegs + j + 1
			if j < ssegs - 1:
				b = a + 1
				c = a + ssegs + 1
				d = c - 1
			else:
				b = a - (ssegs - 1)
				c = a + 1
				d = a + ssegs
			faces.append((d, c, b, a))

	# lover triangels
	f = ssegs * (((csegs - 1) * 2) + hsegs) + 1
	c = len(verts) - 1
	for i in range(ssegs):
		a = i + f
		b = a + 1 
		if i < ssegs - 1:
			faces.append((c, b, a))
		else:
			faces.append((c, f, a))
	return verts, edges, faces

class Capsule(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Capsule"
		self.finishon = 3
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = GetCapsuleMesh(0, 0, 18, 8, 6, False, 0, 360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.csegs, pd.hsegs = 18, 8, 3
		pd.center = True
	def update(self, ctx):
		pd = self.data.primitivedata
		csegs = pd.csegs if not pd.seglock else pd.ssegs - 2
		if pd.center:
			height = pd.height
		else:
			diameter = pd.radius1 * 2
			if pd.height < diameter:
				pd.height = diameter
			height = pd.height - pd.radius1 * 2
		mesh = GetCapsuleMesh(pd.radius1, height,
			pd.ssegs, csegs, pd.hsegs,
			pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(ctx, mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateCapsule(CreatePrimitive):
	bl_idname = "bsmax.createcapsule"
	bl_label = "Capsule (Create)"
	subclass = Capsule()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		elif clickcount == 2:
			self.params.height = dimantion.height
		if clickcount > 0:
			self.subclass.update(ctx)
	def finish(self):
		pass

def capsule_cls(register):
	c = BsMax_OT_CreateCapsule
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	capsule_cls(True)

__all__ = ["capsule_cls", "Capsule"]