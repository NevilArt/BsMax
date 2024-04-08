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

from math import pi, cos, sin, tan
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive


def get_circle_shape(radius, ssegs):
	spline = []
	angle = 2 * pi / ssegs
	distance = (4/3) * tan(pi/(2*ssegs)) * radius

	for i in range(ssegs):
		theta = i * angle
		co = (radius * cos(theta), radius * sin(theta), 0)
		in_tangent = (
					co[0] + distance * sin(theta),
					co[1] - distance * cos(theta),
					0
		)

		out_tangent = (
					co[0] - distance * sin(theta),
					co[1] + distance * cos(theta),
					0
		)

		spline.append((co, in_tangent, 'FREE', out_tangent, 'FREE'))

	return [spline]


class Circle(Primitive_Curve_Class):
	def __init__(self):
		self.classname = "Circle"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True

	def create(self, ctx):
		shapes = get_circle_shape(0, 4)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 4

	def update(self):
		pd = self.data.primitivedata
		shapes = get_circle_shape(pd.radius1, pd.ssegs)
		self.update_curve(shapes)


class Create_OT_Circle(Draw_Primitive):
	bl_idname = "create.circle"
	bl_label = "Circle"
	subclass = Circle()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		owner = self.subclass.owner
		self.params = owner.data.primitivedata
		owner.location = self.gride.location
		owner.rotation_euler = self.gride.rotation
	
	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius


def register_circle():
	bpy.utils.register_class(Create_OT_Circle)

def unregister_circle():
	bpy.utils.unregister_class(Create_OT_Circle)

if __name__ == "__main__":
	new_circle = Circle()
	new_circle.create(bpy.context)
	new_circle.data.primitivedata.radius1 = 1
	new_circle.update()
	bpy.ops.primitive.cleardata()