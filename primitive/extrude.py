import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from mathutils import Vector
from primitive.primitive import PrimitiveCurveClass,PrimitiveGeometryClass
from bsmax.actions import delete_objects
from bsmax.curve import Curve,Segment

def get_extrude_curve(height, segs, start_height, end_height):
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

def get_extrude_mesh(curve, height, hsegs, csegs, segmode, capu, capl, start_height, end_height):
	verts,edges,faces = [],[],[]

	def get_csegs_count(spline,index,csegs,mode):
		return spline.resolution_u if mode == 'Curve' else csegs

	def get_segment_vertexes(spline,index,mode,count,offset):
		points = []
		seg = Segment(spline, index)
		for i in range(count):
			t = i/count
			newpoint = seg.get_point_on(t)
			newpoint += offset
			points.append(newpoint)
		return points

	if curve == None:
		""" create a default mesh if target not exist"""
		verts = [[0,0,0],[0,1,0],[1,0,0],[0,0,1]]
		faces = [[0,1,2],[1,2,3],[2,0,3],[0,1,3]]
	else:
		localcurve = Curve(curve)
		first = 0
		for spline in localcurve.splines:
			sverts, length = [],0
			""" create verts """
			for i in range(hsegs+1):	
				h = (height/hsegs)*i
				for j in range(len(spline.bezier_points)):
					count = get_csegs_count(spline,j,csegs,segmode)
					offset = Vector((0,0,h))
					v = get_segment_vertexes(spline,j,segmode,count,offset)
					sverts += v
				if length == 0:
					length = len(sverts)
			verts += sverts
			""" create body faces """
			for i in range(hsegs):
				f = i*length+first
				for j in range(length):
					a = f+j
					if j < length-1:
						b = a+1
						c = b+length
						d = c-1
					else:
						b = f
						c = b+length
						d = a+length
					faces.append([a,b,c,d])
			""" create upepr cap """
			if capl:
				newface = [first+i for i in range(length-1,-1,-1)]
				faces.append(newface)
			""" create lower cap """
			if capu:
				f = first+length*hsegs
				newface = [f+i for i in range(length)]
				faces.append(newface)
			first += len(sverts)
	return verts,edges,faces

class Extrude_Curve(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Extrude_Curve"
		self.finishon = 0
		self.owner = None
		self.data = None
		self.close = False
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = get_extrude_curve(1,1,0,0)
		self.create_curve(ctx, shapes, self.classname)
		self.data.use_fill_caps = True
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.height = 1
	def update(self):
		pd = self.data.primitivedata
		shapes = get_extrude_curve(pd.height,pd.hsegs,pd.chamfer2,pd.chamfer1)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class Extrude_Mesh(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Extrude_Mesh"
		self.finishon = 0
		self.owner = None
		self.data = None
		self.target = ""
	def reset(self):
		self.__init__()
	def create(self, ctx):
		target = ctx.active_object
		mesh = get_extrude_mesh(target,1,5,3,"Manual",True,True,0,0)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.height,pd.hsegs,pd.csegs = 1,5,3
		pd.bool1,pd.bool2 = True,True
		pd.target = target.name
	def update(self):
		pd = self.data.primitivedata
		target = None if pd.target == "" else bpy.context.scene.objects[pd.target]
		mesh = get_extrude_mesh(target,pd.height,pd.hsegs,pd.csegs,
								pd.extrude_segmode,pd.bool1,pd.bool2,
								pd.chamfer2,pd.chamfer1)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateExtrude(Operator):
	bl_idname = "bsmax.createextrude"
	bl_label = "Extrude (Create)"
	bl_options = {"UNDO"}
	subclass = None
	mode: EnumProperty(name='Type',default='Mesh',
		items =[('Curve','Curve',''),('Mesh','Mesh','')])

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.active_object != None:
				return ctx.active_object.type == 'CURVE'
		return False

	def execute(self, ctx):
		self.subclass = Extrude_Curve() if self.mode == "Curve" else Extrude_Mesh()

		if len(ctx.selected_objects) == 1:
			target = ctx.selected_objects[0]
			self.subclass.create(ctx)
			if self.mode == "Curve":
				self.subclass.data.bevel_object = target
			else:
				self.subclass.target = target.name
			self.subclass.owner.location = target.location
			self.subclass.owner.rotation_euler = target.rotation_euler
		return{"FINISHED"}

def extrude_cls(register):
	c = BsMax_OT_CreateExtrude
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	extrude_cls(True)

__all__ = ["extrude_cls", "Extrude_Curve", "Extrude_Mesh"]