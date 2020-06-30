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

import bpy, math
from mathutils import Vector
from primitive.primitive import CreatePrimitive, PrimitiveCurveClass
from bsmax.mouse import switch_axis_by_orient
from math import hypot, atan2, sqrt, sin, cos, pi, radians
from bsmax.actions import delete_objects

def circle_from_three_points(p1, p2, p3):
	x1, y1 = p1.x, p1.y
	x2, y2 = p2.x, p2.y
	x3, y3 = p3.x, p3.y
	a = x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2
	a = a if a != 0 else 0.000001
	b = (x1*x1+y1*y1)*(y3-y2)+(x2*x2+y2*y2)*(y1-y3)+(x3*x3+y3*y3)*(y2-y1)
	c = (x1*x1+y1*y1)*(x2-x3)+(x2*x2+y2*y2)*(x3-x1)+(x3*x3+y3*y3)*(x1-x2)
	x = -b / (2 * a)
	y = -c / (2 * a)
	return Vector((x, y, 0)), hypot(x-x1, y-y1) # center, radius

def angle_between(center, point):
	x = point.x - center.x
	y = point.y - center.y
	angel = atan2(y, x)
	return angel

def arc_from_three_points(p1, p2, p3):
	center, radius = circle_from_three_points(p1, p2, p3)
	start = angle_between(center, p1)
	end = angle_between(center, p2)
	return center, radius, start, end

def get_arc_shape(radius, start, end, pie):
	Shape = []
	kappa = 4 * (sqrt(2) - 1) / 3
	step = (end - start) / 4.0
	unitVec = step * kappa / (pi/2)
	lx = radius
	ly = 0
	if pie:
		s = radians(start)
		sx, sy = radius * sin(s), radius * cos(s)
		pc1, pl1, pr1 = (0,0,0), (0,0,0), (sx,sy,0)
		Shape.append([pc1,pl1,'VECTOR',pr1,'VECTOR'])
	for i in range(5):
		theta = start + (step*i)
		lx = radius * cos(theta)
		ly = radius * sin(theta)
		xTan = -ly * unitVec
		yTan =  lx * unitVec
		pcn = (lx,ly,0)
		pln = ((lx-xTan),(ly-yTan),0)
		prn = ((lx+xTan),(ly+yTan),0)
		lknottype = rknottype = 'ALIGNED'
		if pie:
			if i == 0:
				lknottype, rknottype = 'VECTOR', 'FREE'
			elif i == 4:
				lknottype, rknottype = 'FREE', 'VECTOR'
		Shape.append([pcn,pln,lknottype,prn,rknottype])
	return [Shape]

def get_line_shape(p1, p2):
	Shape = []
	Shape.append([p1,p1,'FREE',p1,'FREE'])
	Shape.append([p2,p2,'FREE',p2,'FREE'])
	return [Shape]

class Arc(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Arc"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = False
		self.p1 = Vector((0,0,0))
		self.p2 = None
		self.p3 = None
		self.orient = None

	def reset(self):
		self.__init__()

	def create(self, ctx):
		shapes = get_arc_shape(0, 0, 360, False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def draw(self, ctx):
		pd = self.data.primitivedata
		if self.p3 == None:
			shapes = get_line_shape(self.p1, self.p2)
		else:
			p1, p2, p3 = self.p1, self.p2, self.p3
			p1 = switch_axis_by_orient(self.orient, p1)
			p2 = switch_axis_by_orient(self.orient, p2)
			p3 = switch_axis_by_orient(self.orient, p3)
			center, pd.radius1, pd.sfrom, pd.sto = arc_from_three_points(p1, p2, p3)
			center = switch_axis_by_orient(self.orient, center)
			self.owner.location = center
			self.close = pd.sliceon = True
			shapes = get_arc_shape(pd.radius1, pd.sfrom, pd.sto, pd.sliceon)
		self.update_curve(shapes)

	def update(self):
		pd = self.data.primitivedata
		self.close = pd.sliceon
		shapes = get_arc_shape(pd.radius1, pd.sfrom, pd.sto, pd.sliceon)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])

class Create_OT_Arc(CreatePrimitive):
	bl_idname = "create.arc"
	bl_label = "Arc"
	subclass = Arc()
	view = None
	orient = None
	gotp1 = False

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.view = clickpoint.view
		self.orient = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if not self.gotp1:
				self.subclass.p1 = dimantion.local
				self.orient = dimantion.orient
				self.gotp1 = True
			self.subclass.p2 = dimantion.local
		elif clickcount == 2:
			self.subclass.p3 = dimantion.local
			self.subclass.owner.location = dimantion.view
			self.subclass.owner.rotation_euler = dimantion.orient
		if clickcount > 0:
			self.subclass.orient = dimantion.view_name
			self.subclass.draw(ctx)
	def finish(self):
		self.gotp1 = False

def register_arc():
	bpy.utils.register_class(Create_OT_Arc)

def unregister_arc():
	bpy.utils.unregister_class(Create_OT_Arc)