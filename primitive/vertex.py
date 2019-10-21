import bpy
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass

def GetVertexMesh(verts, mode):
	edges,faces = [],[]
	if mode == "EDGE" and len(verts) > 1 or len(verts) == 2:
		for i in range(len(verts) - 1):
			edges.append([i, i+1])
	elif mode == "FACE":
		if len(verts) > 2:
			face = []
			for i in range(len(verts)):
				face.append(i)
			faces.append(face)
		elif len(verts) == 2:
			edges.append([0,1])
	return verts, edges, faces

class Vertex(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Vertex"
		self.finishon = 0 # infinit
		self.owner = None
		self.data = None
		self.mode = "NONE"#'VERT' 'EDGE' 'FACE'
		self.verts = []
	def reset(self):
		mode = self.mode
		self.__init__()
		self.mode = mode
	def create(self, ctx):
		mesh = GetVertexMesh([], self.mode)
		self.create_mesh(ctx, mesh, self.classname)
	def update(self):
		mesh = GetVertexMesh(self.verts, self.mode)
		self.update_mesh(mesh)
	def abort(self):
		if self.owner != None:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

class BsMax_OT_CreateVertex(CreatePrimitive):
	bl_idname="bsmax.createvertex"
	bl_label="Vertex (Create)"
	subclass = Vertex()
	lastclick = 1
	fill_type: EnumProperty(name='Fill Mode',default='NONE',
		items =[('NONE','None',''),('VERT','Vertex Only',''),
				('EDGE','Connect Edges',''),('FACE','Create Face','')])

	def create(self, ctx, clickpoint):
		if self.fill_type == "NONE":
			self.subclass.finishon = 2
		self.subclass.mode = self.fill_type
		self.subclass.verts.append(clickpoint.view)
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
	def update(self, clickcount, dimantion):
		if self.drag:
			self.subclass.verts[-1] = dimantion.view
		else:
			if clickcount != self.lastclick:
				self.subclass.verts.append(dimantion.view)
				self.lastclick = clickcount
		self.subclass.update()
	def finish(self):
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',center='MEDIAN')
		self.subclass.reset()

def vertex_cls(register):
	c = BsMax_OT_CreateVertex
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	vertex_cls(True)

__all__ = ["vertex_cls"]