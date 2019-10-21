import bpy
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def GetPlaneMesh(width, length, WSegs, LSegs):
	verts, edges, faces = [], [], []
	# Create vertexes
	w = width / WSegs
	whalf = width / 2.0
	l = length / LSegs
	lhalf = length / 2.0
	for i in range(WSegs + 1):
		for j in range(LSegs + 1):
			verts.append(((w * i) - whalf, (l * j) - lhalf, 0.0))
	# create faces
	for i in range(WSegs):
		for j in range(LSegs):
			r = i * (LSegs + 1)
			a = r + j
			b = a + 1
			c = b + LSegs + 1
			d = c - 1
			faces.append((d, c, b, a)) 
	return verts, edges, faces

class Plane(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Plane"
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = GetPlaneMesh(0, 0, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		mesh = GetPlaneMesh(pd.width, pd.length, pd.wsegs, pd.lsegs)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreatePlane(CreatePrimitive):
	bl_idname = "bsmax.createplane"
	bl_label = "Plane (Create)"
	subclass = Plane()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.width = dimantion.width
			self.params.length = dimantion.length
			self.subclass.owner.location = dimantion.center
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def plane_cls(register):
	c = BsMax_OT_CreatePlane
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	plane_cls(True)

__all__ = ["plane_cls", "Plane"]