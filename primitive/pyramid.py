import bpy
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass
from bsmax.actions import delete_objects

def GetPyramidMesh(width, depth, height, wsegs, dsegs, hsegs):
	verts, edges, faces = [], [], []
	w, d, h = width / 2.0, depth / 2.0, height
	ws, ds, hs = width / wsegs, depth / dsegs, height / hsegs
	wc, dc, hc = w / hsegs, d / hsegs, h / hsegs
	# get floor vertexes
	for i in range(wsegs + 1):
		for j in range(dsegs + 1):
			x = -w + i * ws
			y = -d + j * ds
			verts.append((x, y, 0))
	# get side vertexes x
	for i in range(1, hsegs):
		s = (((hsegs - i) * hc) / h)
		for j in range(dsegs):
			x = (-w + i * wc)
			y = (-d + j * ds) * s
			z = i * hs
			verts.append((x, y, z))
		for j in range(wsegs):
			x = (-w + j * ws) * s
			y = (-d + i * dc) * -1
			z = i * hs
			verts.append((x, y, z))
		for j in range(dsegs):
			x = (-w + i * wc) * -1
			y = (-d + (dsegs - j) * ds) * s
			z = i * hs
			verts.append((x, y, z))
		for j in range(wsegs):
			x = (-w + (wsegs - j) * ws) * s
			y = (-d + i * dc)
			z = i * hs
			verts.append((x, y, z))
	# add top vertex
	verts.append((0, 0, h))
	# get floor faces
	for i in range(wsegs):
		for j in range(dsegs):
			r = i * (dsegs + 1)
			a = r + j
			b = a + 1
			c = b + dsegs + 1
			d = c - 1
			faces.append((a, b, c, d))
	f = (wsegs + 1) * (dsegs + 1)
	l = (wsegs + dsegs) * 2
	for i in range(hsegs - 2):
		for j in range(l):
			a = f + i * l + j
			if j < l - 1:
				b = a + 1
				c = b + l
				d = c - 1
			else:
				b = f + i * l
				c = f + (i + 1) * l
				d = a + l
			faces.append((d, c, b, a))
	v = len(verts) - 1 # last vertex index
	f2 = f + l * (hsegs - 2) # last line first vertext
	if hsegs > 1:
		# top
		for i in range(l):
			a = f2 + i
			if i < l - 1:
				b = a + 1
			else:
				b = f2
			c = v
			faces.append((c, b, a))
		# silde lowr line 1
		for i in range(dsegs):
			a = i
			b = a + 1
			c = f + i + 1
			d = f + i
			faces.append((d, c, b, a))
		# silde lowr line 2
		fl, fu = dsegs, f + dsegs
		for i in range(wsegs):
			a = fl + i * (dsegs + 1)
			b = a + dsegs + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		fl = (wsegs + 1) * (dsegs + 1) - 1
		fu = f + wsegs + dsegs
		for i in range(dsegs):
			a = fl - i
			b = a - 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		fl = (dsegs + 1) * wsegs
		fu = (wsegs + 3) * (dsegs + 1) + (wsegs - 2)
		for i in range(wsegs):
			a = fl - i * (dsegs + 1)
			b = a - (dsegs + 1)
			if i < wsegs - 1:
				c = fu + i + 1
			else:
				c = f
			d = fu + i
			faces.append((d, c, b, a))
	else:
		for i in range(dsegs):
			a, b = i, i + 1
			faces.append((v, b, a))
		l = (dsegs + 1)
		for i in range(wsegs):
			a = (i + 1) * l - 1
			b = a + l
			faces.append((v, b, a))
		for i in range(dsegs):
			a = f - i - 1
			b = a - 1
			faces.append((v, b, a))
		f = l * wsegs
		for i in range(wsegs):
			a = f - l * i
			b = f - l * (i + 1)
			faces.append((v, b, a))
	return verts, edges, faces

class Pyramid(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Pyramid"
		self.finishon = 3
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = GetPyramidMesh(0, 0, 0, 1, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs, pd.lsegs, pd.hsegs = 1, 1, 1
	def update(self):
		pd = self.data.primitivedata
		mesh = GetPyramidMesh(pd.width, pd.length, pd.height,
					pd.wsegs, pd.lsegs, pd.hsegs)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreatePyramid(CreatePrimitive):
	bl_idname = "bsmax.createpyramid"
	bl_label = "Pyramid (Create)"
	subclass = Pyramid()

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
		elif clickcount == 2:
			self.params.height = dimantion.height
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def pyramid_cls(register):
	c = BsMax_OT_CreatePyramid
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	pyramid_cls(True)

__all__ = ["pyramid_cls", "Pyramid"]