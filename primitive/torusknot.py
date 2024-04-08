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
import numpy as np

from math import pi, sin, cos, floor

from primitive.primitive import Primitive_Curve_Class, Draw_Primitive


def get_torusknot_shape(radius1, radius2, height, lsegs, p, q):
	""" create torusknot splien
		args:
			radius1: Torus Radius
			radius2: Torus Thiknes
			height: height scale
			lsegs: length segment count
			p: Rotation
			q: Twist
		return:
			[spline]
	"""
	spline = []
	theta = np.linspace(0, 2 * pi, lsegs).tolist()

	# Remove last element if spline is close
	if p == floor(p) and q == floor(q):
		theta.pop()

	for t in theta:
		co = (
			(radius1 + (radius2 * cos(q * t))) * cos(p * t), #x_coord
			(radius1 + (radius2 * cos(q * t))) * sin(p * t), #y_cord
			radius2 * sin(q * t) * height #z_coord
		)
		# conver to bezier point and add to spline
		spline.append((co, co, 'FREE', co, 'FREE'))

	return [spline] #return a shape with a single spline


class TorusKnot(Primitive_Curve_Class):
	def __init__(self):
		self.classname = "TorusKnot"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True

	def create(self, ctx):
		shapes = get_torusknot_shape(0, 0, 0, 32, 2, 3)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.height, pd.lsegs, pd.turns, pd.twist = 2.2, 64, 2, 3
		self.data.resolution_u = 1

	def update(self):
		pd = self.data.primitivedata
		shapes = get_torusknot_shape(
			pd.radius1, pd.radius2,
			pd.height, pd.lsegs,
			pd.turns, pd.twist
		)
		
		self.close = pd.turns == floor(pd.turns) and pd.twist == floor(pd.twist)
		self.update_curve(shapes)


class Create_OT_TorusKnot(Draw_Primitive):
	bl_idname = "create.torusknot"
	bl_label = "TorusKnot"
	subclass = TorusKnot()
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
			self.params.radius2 = dimension.radius / 2.32
			# self.subclass.data.bevel_depth = self.params.radius1 / 3

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.params.thickness = dimension.radius


def register_torusknot():
	bpy.utils.register_class(Create_OT_TorusKnot)


def unregister_torusknot():
	bpy.utils.unregister_class(Create_OT_TorusKnot)


if __name__ == "__main__":
	register_torusknot()