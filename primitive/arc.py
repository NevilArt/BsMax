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
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from math import hypot, atan2, sqrt, sin, cos, pi, degrees, radians
from bsmax.actions import delete_objects
from bsmax.bsmatrix import points_to_local_matrix, matrix_inverse


def circle_from_three_points(p1, p2, p3):
	""" Get 3 3D points return Center and radius of Circle """
	x1, y1 = p1.x, p1.y
	x2, y2 = p2.x, p2.y
	x3, y3 = p3.x, p3.y
	
	a = x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2
	a = a if a != 0 else 0.000001 # protect from devide by zero
	b = (x1*x1+y1*y1)*(y3-y2)+(x2*x2+y2*y2)*(y1-y3)+(x3*x3+y3*y3)*(y2-y1)
	c = (x1*x1+y1*y1)*(x2-x3)+(x2*x2+y2*y2)*(x3-x1)+(x3*x3+y3*y3)*(x1-x2)
	
	x = -b / (2 * a)
	y = -c / (2 * a)
	# z = ??

	return Vector((x, y, 0)), hypot(x-x1, y-y1) # center, radius



def angle_between(center, point):
	"""  """
	x = point.x - center.x
	y = point.y - center.y
	return degrees(atan2(y, x))



def arc_from_three_points(p1, p2, p3):
	"""  """
	center, radius = circle_from_three_points(p1, p2, p3)
	start = angle_between(center, p1)
	end = angle_between(center, p2)
	return center, radius, start, end



def get_arc_shape(radius, start, end, pie):
	""" Get Radius Start End as Degre and Pie on/off return curve data """
	start, end = radians(start), radians(end)
	Shape = []
	kappa = 4 * (sqrt(2) - 1) / 3
	step = (end - start) / 4.0
	unitVec = step * kappa / (pi/2)
	lx = radius
	ly = 0
	if pie:
		sx, sy = radius * sin(start), radius * cos(start)
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



class Arc(Primitive_Curve_Class):
	def init(self):
		self.classname = "Arc"
		self.finishon = 3
		self.close = False

		# Local space draw arc
		self.point1 = Vector((0,0,0))
		self.point2 = Vector((0,0,0))
		self.point3 = None
		# World space draw line
		self.start = Vector((0,0,0))
		self.end = Vector((0,0,0))
		# Control stuff
		self.drawing = False
		self.matrix = None
		# second methods
		self.radius = 0

	def create(self, ctx):
		shapes = get_arc_shape(0, 0, 270, False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def draw(self):
		if self.point3:
			pd = self.data.primitivedata
			self.close = pd.sliceon = True
			p1, p2, p3 = self.point1, self.point2, self.point3
			center, pd.radius1, pd.sfrom, pd.sto = arc_from_three_points(p1, p2, p3)
			
			shapes = get_arc_shape(pd.radius1, pd.sfrom, pd.sto, pd.sliceon)

			location = points_to_local_matrix(center, self.matrix)
			self.owner.location = location

		else:
			shapes = get_line_shape(self.start, self.end)

		self.update_curve(shapes)

	def update(self):
		if self.drawing:
			return

		pd = self.data.primitivedata
		self.close = pd.sliceon
		shapes = get_arc_shape(pd.radius1, pd.sfrom, pd.sto, pd.sliceon)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Arc(Draw_Primitive):
	bl_idname = "create.arc"
	bl_label = "Arc"
	subclass = Arc()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.matrix = matrix_inverse(self.gride.gride_matrix)
		self.subclass.drawing = True

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.subclass.drawing = False
				self.params.radius1 = dimension.radius
				self.params.sfrom = 0
				self.params.sto = 270
				self.params.sliceon = True
				self.subclass.owner.location = self.gride.location
				self.subclass.owner.rotation_euler = self.gride.rotation
			else:
				self.subclass.start = dimension.start
				self.subclass.end = dimension.end
				self.subclass.point2 = dimension.local
				self.subclass.drawing = True

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.subclass.point3 = dimension.local
			self.subclass.owner.rotation_euler = self.gride.rotation

		if clickcount > 0 and not self.use_single_draw:
			self.subclass.draw()

	def finish(self):
		self.subclass.drawing = False



def register_arc():
	bpy.utils.register_class(Create_OT_Arc)

def unregister_arc():
	bpy.utils.unregister_class(Create_OT_Arc)

if __name__ == "__main__":
	register_arc()