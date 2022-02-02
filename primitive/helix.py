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
from mathutils import Vector
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from bsmax.actions import delete_objects
from bsmax.math import get_bias



def get_helix_shape(radius1, radius2, height, turns, segs, bias, ccw):

	total_degree = (pi*2)*turns

	if ccw:
		total_degree *= -1

	if turns == 0:
		turns = 0.0001

	segments = int(segs*turns)+1
	piece = total_degree / (segs*turns)
	height_pieces = height / (segments-1)
	round_pieces = (radius1-radius2) / (segs*turns)

	shape = []
	for i in range(segments):
		teta, length = piece*i, radius1-(round_pieces*i)
		x, y = sin(teta)*length, cos(teta)*length

		if height > 0:
			percent = (height_pieces*i)/height
		else:
			percent = 0

		z = height*get_bias(bias, percent)
		point = (x, y, z)

		vector_type = 'FREE' if 0 < i > segments else 'AUTO'
		shape.append((point, point, vector_type, point, vector_type))

	return [shape]



class Helix(Primitive_Curve_Class):
	def init(self):
		self.classname = "Helix"
		self.finishon = 4
		self.close = False

	def create(self, ctx):
		shapes = get_helix_shape(0,0,0,3,20,0,False)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.turns = 3
		pd.ssegs = 20

	def update(self):
		pd = self.data.primitivedata
		# radius1, radius2, height, turns, segs, bias, ccw
		shapes = get_helix_shape(pd.radius1, pd.radius2, pd.height,
					pd.turns, pd.ssegs, pd.bias_np, pd.ccw)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Helix(Draw_Primitive):
	bl_idname = "create.helix"
	bl_label = "Helix"
	subclass = Helix()
	use_gride = True
	gride_updated = False

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimantion.radius
				self.params.radius2 = dimantion.radius
				self.params.height = dimantion.radius*2
			else:
				self.params.radius1 = dimantion.radius
				self.params.radius2 = dimantion.radius

		if clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.params.height = dimantion.height

		if clickcount == 3:
			if not self.gride_updated:
				center = self.gride.gride_matrix @ Vector((0,0,self.params.height))
				self.gride.location = center
				self.gride.update()
				self.gride_updated = True

			self.params.radius2 = dimantion.distance

	def finish(self):
		self.gride_updated = False



def register_helix():
	bpy.utils.register_class(Create_OT_Helix)
	
def unregister_helix():
	bpy.utils.unregister_class(Create_OT_Helix)

if __name__ == "__main__":
	register_helix()