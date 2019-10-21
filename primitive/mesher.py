import bpy, bmesh
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def get_mesher_mesh(radius):
	r, h = radius / 2, radius
	verts = [(-r,-r,0),(r,-r,0),(r,r,0),(-r,r,0),(0,0,h)]
	faces = [(3,2,1,0),(1,4,0),(2,4,1),(3,4,2),(0,4,3)]
	return verts, [], faces

def update_mesher(self, ctx):
	# check is target avalible
	#print(self.target)
	if self.target in bpy.data.objects:
		target = bpy.data.objects[self.target]
		if target.type in {'MESH', 'CURVE'}:
			self.owner.select_set(False)
			ctx.view_layer.objects.active = target
			target.select_set(True)
			bpy.ops.object.duplicate()
			newobject = ctx.view_layer.objects.active
			newobject.select_set(True)
			bpy.ops.object.convert(target = 'MESH', keep_original = False)
			tmpmesh = newobject.data
			bm = bmesh.new()
			bm.from_mesh(tmpmesh)
			bm.to_mesh(self.data)
			bm.free()
			bpy.data.meshes.remove(tmpmesh)
			bpy.ops.object.delete()
			self.owner.select_set(True)
			ctx.view_layer.objects.active = self.owner

class Mesher(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Mesher"
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = get_mesher_mesh(0)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		if pd.target == "":
			mesh = get_mesher_mesh(pd.radius1)
			self.update_mesh(mesh)
		else:
			self.target = pd.target
			ctx = bpy.context
			update_mesher(self, ctx)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateMesher(CreatePrimitive):
	bl_idname = "bsmax.createmesher"
	bl_label = "Mesher (Create)"
	subclass = Mesher()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius / 2
			self.subclass.owner.location = dimantion.center
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def mesher_cls(register):
	c = BsMax_OT_CreateMesher
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	mesher_cls(True)

__all__ = ["mesher_cls"]