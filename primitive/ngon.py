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
# 2024/04/04

import bpy
from math import pi, sqrt, sin, cos
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive


def get_ngon_shape(radius, sides, cornerradius, circular):
	Shape = []
	kappa = 4 * (sqrt(2) - 1) / 3
	step = (pi*2) / sides
	unitVec = step * kappa / (pi/2)
	# corrective for 3 side shape
	# elif sides == 3:
	# 	unitVec = step * kappa / 3.00196 #86.0 in dggre
	for i in range(sides):
		theta = step * i
		lx = radius * cos(theta)
		ly = radius * sin(theta)
		xTan = -ly * unitVec
		yTan =  lx * unitVec
		pcn = (lx, ly, 0)
		pln = ((lx - xTan), (ly - yTan), 0)
		prn = ((lx + xTan), (ly + yTan), 0)

		if circular:
			Shape.append([pcn, pln, 'ALIGNED', prn, 'ALIGNED'])
		else:
			Shape.append([pcn, pln, 'VECTOR', prn, 'VECTOR'])

	return [Shape]


class NGon(Primitive_Curve_Class):
	def init(self):
		self.classname = "NGon"
		self.finishon = 2
		self.close = True

	def create(self, ctx):
		shapes = get_ngon_shape(0,5,0,False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 5

	def update(self):
		pd = self.data.primitivedata
		# radius, sides, cornerradius, circular
		shapes = get_ngon_shape(pd.radius1, pd.ssegs, pd.chamfer1, pd.smooth)
		self.update_curve(shapes)


class Create_OT_NGon(Draw_Primitive):
	bl_idname = "create.ngon"
	bl_label = "NGon"
	subclass = NGon()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius


def register_ngon():
	bpy.utils.register_class(Create_OT_NGon)


def unregister_ngon():
	bpy.utils.unregister_class(Create_OT_NGon)


if __name__ == "__main__":
	register_ngon()