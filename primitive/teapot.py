import bpy
from mathutils import Vector
from math import sin, cos, pi, radians
from bsmax.curve import Spline, Bezier_point
from bsmax.math import point_on_vector
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass

def get_path(part):
	body_path = Spline(None)
	points = []
	if part == 'body':
		points = (((0,0,0),(0,0,0),(0.358946,0,0.00480962)),
			((0.774773,0,-0.000830472),(0.75,0,0.075),(0.791808,0,0.150003)),
			((0.978876,0,0.20208),(1,0,0.45),(1.02112,0,0.69792)),
			((0.805268,0,1.06392),(0.750701,0,1.2012),(0.695276,0,1.29381)),
			((0.676157,0,1.2304),(0.7,0,1.2),(0.7,0,1.2)))
	elif part == 'lid':
		points = (((0,0,1.575),(0,0,1.575),(0.400656,0,1.56443)),
			((0.00236605,0,1.43537),(0.1,0,1.35),(0.211611,0,1.27556)),
			((0.657876,0,1.26831),(0.65,0,1.2),(0.65,0,1.2)))
	elif part == 'spout':
		points = (((0.850668,1.23725,0.507198),(0.850668,1.23725,0.507198),(1.38542,1.23725,0.549446)),
			((1.19781,1.23725,1.09924),(1.54661,1.23725,1.23185),(1.54661,1.23725,1.23185)))
	elif part == 'handle_path':
		points = (((-0.775849,0,1.07083),(-0.775849,0,1.07083),(-1.09616,0,1.06615)),
			((-1.40217,0,1.09104),(-1.4273,0,0.922712),(-1.45329,0,0.649498)),
			((-1.18858,0,0.50098),(-0.917913,0,0.328547),(-0.917913,0,0.328547)))
	elif part == 'handle_shape':
		points = (((-0.803255,0.108984,1.03168),(-0.803255,0.108984,1.06697),(-0.803255,0.108984,1.10225)),
			((-0.803255,0.0601358,1.12498),(-0.803255,0,1.12498),(-0.803255,-0.0601359,1.12498)),
			((-0.803255,-0.108984,1.10225),(-0.803255,-0.108984,1.06697),(-0.803255,-0.108984,1.03168)),
			((-0.803255,-0.0601359,1.01323),(-0.803255,0,1.01323),(-0.803255,0.0601358,1.01323)))
	for p in points:
		newbp = Bezier_point(None)
		newbp.handle_left = Vector((p[0]))
		newbp.co = Vector((p[1]))
		newbp.handle_right = Vector((p[2]))
		body_path.bezier_points.append(newbp)
	return body_path

def get_verts(spline, ssegs, scale):
	verts = []
	for index in range(len(spline.bezier_points)-1):
		a,b,c,d = spline.get_segment(index)
		for j in range(ssegs):
			t = 1/ssegs * j
			newvert = point_on_vector(a,b,c,d,t)
			verts.append(newvert * scale)
		if index == len(spline.bezier_points)-2:
			verts.append(d * scale)
	return verts

def get_teapot_mesh(radius,csegs,body,handle,spout,lid):
	verts,edges,faces = [],[],[]
	cs = csegs*4
	step = (pi*2)/cs
	#print("-------------------------------------")
	if body:
		""" Create body vertexes """
		body_path = get_path('body')
		sides = get_verts(body_path, csegs, radius)
		l = len(sides)-1
		verts.append(sides[0])
		for i in range(1,l):
			x = sides[i].x
			for j in range(cs):
				d = j*step
				X = sin(d)*x 
				Y = cos(d)*x
				Z = sides[i].z
				verts.append([X,Y,Z])
		""" first body triangle faces """
		for i in range(cs):
			faces.append((0,i,i+1))
		faces.append((0,cs,1))
		""" body quad faces """
		f = 1 # First vertex of element
		for i in range(l-2):
			for j in range(cs):
				a = f+j+(i*cs)
				if j < cs-1:
					b = a+1
					c = a+cs+1
					d = c-1
				else: 
					b = f+i*cs
					c = a+1
					d = a+cs
				faces.append((d,c,b,a))

	if lid:
		f = len(verts) # First vertex of element
		""" create lid vertexes """
		lid_path = get_path('lid')
		sides = get_verts(lid_path, csegs, radius)
		l = len(sides)-1
		verts.append(sides[0])
		for i in range(1,len(sides)):
			x = sides[i].x
			for j in range(cs):
				d = j*step
				X = sin(d)*x 
				Y = cos(d)*x
				Z = sides[i].z
				verts.append([X,Y,Z])
		""" first lid triangle faces """
		for i in range(cs):
			faces.append((f+i+1,f+i,f))
		faces.append((f+1,f+cs,f))
		""" lid quad faces """
		f += 1
		for i in range(l-1):
			print(i)
			for j in range(cs):
				a = f+j+(i*cs)
				if j < cs-1:
					b = a+1
					c = a+cs+1
					d = c-1
				else: 
					b = f+i*cs
					c = a+1
					d = c+cs-1
				faces.append((a,b,c,d))
	
	""" create handel vertexes """
	if handle:
		f = len(verts)

	""" create spout vertexes """
	if spout:
		f = len(verts)

	return verts,edges,faces

class Teapot(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Teapot"
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = get_teapot_mesh(0,4,True,True,True,True)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.csegs = 4
		pd.bool1,pd.bool2,pd.bool3,pd.bool4 = True,True,True,True
	def update(self):
		pd = self.data.primitivedata
		mesh = get_teapot_mesh(pd.radius1,pd.csegs,pd.bool1,pd.bool2,pd.bool3,pd.bool4)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateTeapot(CreatePrimitive):
	bl_idname = "bsmax.createteapot"
	bl_label = "Teapot (Create)"
	subclass = Teapot()

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

def teapot_cls(register):
	c = BsMax_OT_CreateTeapot
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	teapot_cls(True)

__all__ = ["teapot_cls", "Teapot"]