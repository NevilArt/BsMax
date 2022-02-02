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
from math import pi, sin, cos
from random import random, seed
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from bsmax.actions import delete_objects



def get_star_shape(radius1, radius2, points, distortion, 
						filletradius1, filletradius2, randseed, randval):
	shape = []
	step = (pi*2) / float(points)
	seed(randseed)
	drnd = randval*2
	for i in range(points):
		s = i*((pi*2)/points)
		r = [random()*drnd - randval for i in range(4)] if randval != 0 else [0,0,0,0]
		x0 = sin(s+distortion)*radius1+r[0]
		y0 = cos(s+distortion)*radius1+r[1]
		x1 = sin(s+(step/2))*radius2+r[2]
		y1 = cos(s+(step/2))*radius2+r[3]
		pc0,pl0,pr0 = (x0,y0,0),(x0,y0,0),(x0,y0,0)
		pc1,pl1,pr1 = (x1,y1,0),(x1,y1,0),(x1,y1,0)       
		shape.append((pc0,pl0,'VECTOR',pr0,'VECTOR'))
		shape.append((pc1,pl1,'VECTOR',pr1,'VECTOR'))
	return [shape]



class Star(Primitive_Curve_Class):
	def init(self):
		self.classname = "Star"
		self.finishon = 3
		self.close = True

	def create(self, ctx):
		shapes = get_star_shape(0,0,5,0,0,0,0,0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs = 5

	def update(self):
		pd = self.data.primitivedata
		#radius1, radius2, points, distortion, filletradius1, filletradius2, seed, randval
		shapes = get_star_shape(pd.radius1, pd.radius2, pd.ssegs, pd.twist, 
						pd.chamfer1, pd.chamfer2, pd.seed, pd.random)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Star(Draw_Primitive):
	bl_idname = "create.star"
	bl_label = "Star"
	subclass = Star()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimantion.radius
				self.params.radius2 = self.params.radius1 / 2
			else:
				self.params.radius1 = dimantion.radius
				self.params.radius2 = self.params.radius1 / 2

		elif clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			self.params.radius2 = dimantion.distance



def register_star():
	bpy.utils.register_class(Create_OT_Star)

def unregister_star():
	bpy.utils.unregister_class(Create_OT_Star)

if __name__ == "__main__":
	register_star()