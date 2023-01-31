############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy

from mathutils import Vector
from bpy.types import Operator
from bpy.props import IntProperty

from primitive.primitive import Primitive_Curve_Class, Draw_Primitive



def Flet(point, radius, mirror_x, mirror_y, rivers):
	p,points = point,[]
	if radius == 0:
		points.append([p,p,'FREE',p,'FREE'])
	else:
		rx,ry = radius * mirror_x, radius * mirror_y
		tx,ty = rx - (rx * 0.551786), ry - (ry * 0.551786)
		p1 = [Vector((p[0]+rx,p[1],0)),Vector((p[0]+rx,p[1],0)),Vector((p[0]+tx,p[1],0))]
		p2 = [Vector((p[0],p[1]+ry,0)),Vector((p[0],p[1]+ty,0)),Vector((p[0],p[1]+ry,0))]
		if rivers:
			points.append([p2[0],p2[2],'FREE',p2[1],'FREE'])
			points.append([p1[0],p1[2],'FREE',p1[1],'FREE'])
		else:
			points.append([p1[0],p1[1],'FREE',p1[2],'FREE'])
			points.append([p2[0],p2[1],'FREE',p2[2],'FREE'])
	return points



def Rectangle(length, width, cornerradius, rivers):
	shape = []
	w,l,r = width / 2, length / 2, cornerradius
	# Create the Sharp shape
	p1 = Vector((-w,-l,0))
	p2 = Vector((-w,l,0))
	p3 = Vector((w,l,0))
	p4 = Vector((w,-l,0))
	# Create shape
	if rivers:
		for p in Flet(p4, r, -1, 1, False):
			shape.append(p)
		for p in Flet(p3, r, -1, -1, True):
			shape.append(p)
		for p in Flet(p2, r, 1, -1, False):
			shape.append(p)
		for p in Flet(p1, r, 1, 1, True):
			shape.append(p)
	else:
		for p in Flet(p1, r, 1, 1, False):
			shape.append(p)
		for p in Flet(p2, r, 1, -1, True):
			shape.append(p)
		for p in Flet(p3, r, -1, -1, False):
			shape.append(p)
		for p in Flet(p4, r, -1, 1, True):
			shape.append(p)
	return shape



def Circle(length, width, revers):
	l, w = length, width
	tl, tw = l * 0.551786, w * 0.551786
	points = []
	#				Knut				Left			 Right
	points.append([Vector((-w,0,0)),Vector((-w,-tl,0)),Vector((-w,tl,0))])
	points.append([Vector((0,l,0)),Vector((-tw,l,0)),Vector((tw,l,0))])
	points.append([Vector((w,0,0)),Vector((w,tl,0)),Vector((w,-tl,0))])
	points.append([Vector((0,-l,0)),Vector((tw,-l,0)),Vector((-tw,-l,0))])
	shape = []
	if revers:
		# revers order and swap left & Right Tangents
		for i in range(len(points), 0, -1):
			p = points[i - 1]
			shape.append([p[0], p[2], 'FREE', p[1], 'FREE'])
	else:
		for i in range(len(points)):
			p = points[i]
			shape.append([p[0], p[1], 'FREE', p[2], 'FREE'])
	return shape



def Angle(length, width, thickness, synccorner, cornerradius1, cornerradius2, edgeradius):
	shape = []
	# L shape
	w,l,t = width / 2, length / 2, thickness
	r1,r2,re = cornerradius1, cornerradius2, edgeradius
	# Create the Sharp shape
	p0 = Vector((-w,l,0))
	p1 = Vector((-w+t,l,0))
	p2 = Vector((-w+t,-l+t,0))
	p3 = Vector((w,-l+t,0))
	p4 = Vector((w,-l,0))
	p5 = Vector((-w,-l,0))
	# synnc corrners
	if synccorner:
		w1,w2,r1 = width, width - thickness, cornerradius1
		if w2 > w1 - r1 * 2:
			r2 = (w2 - (w1 - r1 * 2)) / 2
		else:
			r2 = 0
	# Create shape
	shape.append([p0, p0, 'FREE', p0, 'FREE'])
	for p in Flet(p1, re, -1, -1, False):
		shape.append(p)
	for p in Flet(p2, r2, 1, 1, True):
		shape.append(p)
	for p in Flet(p3, re, -1, -1, False):
		shape.append(p)
	shape.append([p4, p4, 'FREE', p4, 'FREE'])
	for p in Flet(p5, r1, 1, 1, False):
		shape.append(p)
	return [shape]



def Bar(length, width, cornerradius1):
	shapes = []
	shapes.append(Rectangle(length, width, cornerradius1, False))
	return shapes



def Channel(length, width, thickness, synccorner, cornerradius1, cornerradius2):
	shape = []
	# C shape
	w,l,t = width / 2, length / 2, thickness
	r1,r2 = cornerradius1, cornerradius2
	# Create the Sharp shape
	p0 = Vector((-w,l,0))
	p1 = Vector((w,l,0))
	p2 = Vector((w,l-t,0))
	p3 = Vector((-w+t,l-t,0))
	p4 = Vector((-w+t,-l+t,0))
	p5 = Vector((w,-l+t,0))
	p6 = Vector((w,-l,0))
	p7 = Vector((-w,-l,0))
	# synnc corrners
	if synccorner:
		w1,w2,r1 = width, width - thickness, cornerradius1
		r2 = (w2-(w1-r1*2))/2 if w2>w1-r1*2 else 0
	# Create shape
	for p in Flet(p0, r1, 1, -1, True):
		shape.append(p)
	shape.append([p1, p1, 'FREE', p1, 'FREE'])
	shape.append([p2, p2, 'FREE', p2, 'FREE'])
	for p in Flet(p3, r2, 1, -1, False):
		shape.append(p)
	for p in Flet(p4, r2, 1, 1, True):
		shape.append(p)
	shape.append([p5, p5, 'FREE', p5, 'FREE'])
	shape.append([p6, p6, 'FREE', p6, 'FREE'])
	for p in Flet(p7, r1, 1, 1, False):
		shape.append(p)
	return [shape]



def Cylinder(radius, slicefrom, sliceto):
	shapes = []
	# TODO Slice from to did not added yet
	# take it from arc shape
	r = radius
	t = r * 0.551786
	pc1,pl1,pr1 = Vector((0,-r,0)), Vector((-t,-r,0)), Vector((t,-r,0))
	pc2,pl2,pr2 = Vector((r,0,0)), Vector((r,-t,0)), Vector((r,t,0))
	pc3,pl3,pr3 = Vector((0,r,0)), Vector((t,r,0)), Vector((-t,r,0))
	pc4,pl4,pr4 = Vector((-r,0,0)), Vector((-r,t,0)), Vector((-r,-t,0))
	pt1 = [pc1, pl1, 'FREE', pr1, 'FREE']
	pt2 = [pc2, pl2, 'FREE', pr2, 'FREE']
	pt3 = [pc3, pl3, 'FREE', pr3, 'FREE']
	pt4 = [pc4, pl4, 'FREE', pr4, 'FREE']
	shapes.append([pt1, pt2, pt3, pt4])
	return shapes



def Pipe(radius, thickness):
	shapes = []
	shapes.append(Circle(radius, radius, False))
	shapes.append(Circle(radius - thickness, radius - thickness, True))
	return shapes



def Tee(length, width, thickness, cornerradius1):
	shape = []
	# T shape
	w,l,t,r = width / 2, length / 2, thickness, cornerradius1
	# Create the Sharp shape
	p0 = Vector((-w,l,0))
	p1 = Vector((w,l,0))
	p2 = Vector((w,l-t,0))
	p3 = Vector((t/2,l-t,0))
	p4 = Vector((t/2,-l,0))
	p5 = Vector((-t/2,-l,0))
	p6 = Vector((-t/2,l-t,0))
	p7 = Vector((-w,l-t,0))
	# Create shape
	shape.append([p0, p0, 'FREE', p0, 'FREE'])
	shape.append([p1, p1, 'FREE', p1, 'FREE'])
	shape.append([p2, p2, 'FREE', p2, 'FREE'])
	for p in Flet(p3, r, 1, -1, False):
		shape.append(p)
	shape.append([p4, p4, 'FREE', p4, 'FREE'])
	shape.append([p5, p5, 'FREE', p5, 'FREE'])
	for p in Flet(p6, r, -1, -1, True):
		shape.append(p)
	shape.append([p7, p7, 'FREE', p7, 'FREE'])
	return [shape]



def Tube(length, width, thickness, synccorner, cornerradius1, cornerradius2):
	shapes = []
	# Outer rectangle
	R1 = [length, width, cornerradius1]
	# inner corner
	cr2 = cornerradius2
	if synccorner:
		w1,w2,r1 = width, width - thickness, cornerradius1
		cr2 = (w2-(w1-r1*2))/2 if w2>w1-r1*2 else 0
	# inner rectangle
	R2 = [length - thickness, width - thickness, cr2]
	shapes.append(Rectangle(R1[0], R1[1], R1[2], False))
	shapes.append(Rectangle(R2[0], R2[1], R2[2], True))
	return shapes



def Width_flange(length, width, thickness, cornerradius1):
	shape = []
	# H shape
	w,l,t,r = width / 2, length / 2, thickness, cornerradius1
	# Create the Sharp shape
	p0 = Vector((-w,l,0))
	p1 = Vector((w,l,0))
	p2 = Vector((w,l-t,0))
	p3 = Vector((t/2,l-t,0))
	p4 = Vector((t/2,-l+t,0))
	p5 = Vector((w,-l+t,0))
	p6 = Vector((w,-l,0))
	p7 = Vector((-w,-l,0))
	p8 = Vector((-w,-l+t,0))
	p9 = Vector((-t/2,-l+t,0))
	p10 = Vector((-t/2,l-t,0))
	p11 = Vector((-w,l-t,0))
	# Create shape
	shape.append([p0, p0, 'FREE', p0, 'FREE'])
	shape.append([p1, p1, 'FREE', p1, 'FREE'])
	shape.append([p2, p2, 'FREE', p2, 'FREE'])
	for p in Flet(p3, r, 1, -1, False):
		shape.append(p)
	for p in Flet(p4, r, 1, 1, True):
		shape.append(p)
	shape.append([p5, p5, 'FREE', p5, 'FREE'])
	shape.append([p6, p6, 'FREE', p6, 'FREE'])
	shape.append([p7, p7, 'FREE', p7, 'FREE'])
	shape.append([p8, p8, 'FREE', p8, 'FREE'])
	for p in Flet(p9, r, -1, 1, False):
		shape.append(p)
	for p in Flet(p10, r, -1, -1, True):
		shape.append(p)
	shape.append([p11, p11, 'FREE', p11, 'FREE'])
	return [shape]



def Elipse(length, width, outline, thickness):
	shapes = []
	shapes.append(Circle(length, width, False))
	if outline:
		shapes.append(Circle(length - thickness, width - thickness, True))
	return shapes



def get_volum_dimension(pcos):
	findmin = lambda l: min(l)
	# findCenter = lambda l: ( max(l) + min(l) ) / 2
	findmax = lambda l: max(l)
	x,y,z = [[v[i] for v in pcos] for i in range(3)]
	pmin = Vector([findmin(axis) for axis in [x,y,z]])
	pmax = Vector([findmax(axis) for axis in [x,y,z]])
	return pmin, pmax



def get_profilo_shape(Mode, length, width, thickness,
					cornerradius1, cornerradius2, edgeradius,
					radius, slicefrom, sliceto,	outline, synccorner,
					offset_x, offset_y, mirror_x, mirror_y,
					angel, pivotaligne): # pivotaligne int 1-9

	shapes = []
	if Mode == "Angle":
		shapes = Angle(length, width, thickness, synccorner, cornerradius1, cornerradius2, edgeradius)
	elif Mode == "Bar":
		shapes = Bar(length, width, cornerradius1)
	elif Mode == "Channel":
		shapes = Channel(length, width, thickness, synccorner, cornerradius1, cornerradius2)
	elif Mode == "Cylinder":
		shapes = Cylinder(radius, slicefrom, sliceto)
	elif Mode == "Pipe":
		shapes = Pipe(radius, thickness)
	elif Mode == "Tee":
		shapes = Tee(length, width, thickness, cornerradius1)
	elif Mode == "Tube":
		shapes = Tube(length, width, thickness, synccorner, cornerradius1, cornerradius2)
	elif Mode == "Width_flange":
		shapes = Width_flange(length, width, thickness, cornerradius1)
	elif Mode == "Elipse":
		shapes = Elipse(length, width, outline, thickness)

	# pivotangel
	pcos = []
	for shape in shapes:
		for knot in shape:
			for i in (0,1,3):
				pcos.append(knot[i])
	pmin, pmax = get_volum_dimension(pcos)
	ox, oy = offset_x, offset_y
	if pivotaligne in (1, 4, 7):
		ox += pmax.x
	if pivotaligne in (3, 6, 9):
		ox += pmin.x
	if pivotaligne in (1, 2, 3):
		oy += pmin.y
	if pivotaligne in (7, 8, 9):
		oy += pmax.y
	
	# mirrot and offset
	for shape in shapes:
		for p in shape:
			if mirror_x:
				p[0].x,p[1].x,p[3].x = (p[0].x* -1),(p[1].x* -1),(p[3].x* -1)
			if mirror_y:
				p[0].y,p[1].y,p[3].y = (p[0].y* -1),(p[1].y* -1),(p[3].y* -1)
			# offset
			p[0].x,p[1].x,p[3].x = (p[0].x+ox),(p[1].x+ox),(p[3].x+ox)
			p[0].y,p[1].y,p[3].y = (p[0].y+oy),(p[1].y+oy),(p[3].y+oy)
	
	
	# angel = radians(angel)
	# matrix = matrix_from_elements(Vector((0,0,0)), Vector((0,0,angel)), Vector((1,1,1)))
	# #[p_0, p_1, 'FREE', p_3, 'FREE']
	# for s, spline in enumerate(shapes):
	# 	for p, point in enumerate(spline):
	# 		print(point)
	# 		# shapes[s][p][0] = transform_points_to_matrix(Vector(point[0]), matrix)
	# 		# shapes[s][p][1] = transform_points_to_matrix(Vector(point[1]), matrix)
	# 		# shapes[s][p][3] = transform_points_to_matrix(Vector(point[3]), matrix)

	return shapes



class Profilo(Primitive_Curve_Class):
	def init(self):
		self.classname = "Profilo"
		self.finishon = 2
		self.close = True

	def create(self, ctx, mode):
		shapes = get_profilo_shape(mode,0, 0, 0, 0, 0, 0, 0, 0, 0,
					False, False, 0, 0,	False, False, 0, 5)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.profilo_mode = mode

	def update(self):
		pd = self.data.primitivedata
		shapes = get_profilo_shape(pd.profilo_mode, pd.length, pd.width, pd.thickness,
					pd.chamfer1, pd.chamfer2, pd.chamfer3,
					pd.radius1, pd.sfrom, pd.sto, pd.outline, pd.corner,
					pd.offset_x, pd.offset_y, pd.mirror_x, pd.mirror_y,
					pd.rotation, pd.pivotaligne)
		self.update_curve(shapes)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Profilo(Draw_Primitive):
	bl_idname = "create.profilo"
	bl_label = "Profilo"
	subclass = Profilo()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx, "Angle")
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			width = self.params.width = abs(dimension.width)
			length = self.params.length = abs(dimension.length)
			self.params.thickness = min(width, length) / 5
			self.subclass.owner.location = dimension.center



class Create_OT_Set_Profilo_Pivot_Aligne(Operator):
	bl_idname = "create.set_profilo_pivotaligne"
	bl_label = "Profilo"
	pivotaligne: IntProperty(min= 1, max= 9, default= 5)

	@classmethod
	def poll(self, ctx):
		if len(ctx.selected_objects) > 0:
			if ctx.active_object != None:
				if ctx.active_object.type == "CURVE":
					if ctx.active_object.data.primitivedata.classname == "Profilo":
						return True
		return False

	def execute(self, ctx):
		pd = ctx.active_object.data.primitivedata
		pd.pivotaligne = self.pivotaligne
		return {'FINISHED'}



classes = [Create_OT_Profilo, Create_OT_Set_Profilo_Pivot_Aligne]

def register_profilo():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_profilo():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_profilo()