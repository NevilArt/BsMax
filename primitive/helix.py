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
from primitive.primitive import PrimitiveCurveClass, Draw_Primitive
from bsmax.actions import delete_objects
from bsmax.math import get_bias, get_distance



def get_helix_shape(radius1, radius2, height, turns, segs, bias, ccw):
	shape = []
	r1,r2 = radius1,radius2
	totatdig = (pi*2)*turns
	if ccw:
		totatdig *= -1
	if turns == 0:
		turns = 0.0001
	piece = totatdig/(segs*turns)
	hpiece = height/(segs*turns)
	rpiece = (r1-r2)/(segs*turns)
	segments = int(segs*turns)
	for i in range(segments):
		x = sin(piece*i)*(r1-(rpiece*i))
		y = cos(piece*i)*(r1-(rpiece*i))
		if height > 0:
			percent = (hpiece*i)/height
		else:
			percent = 0
		z = height*get_bias(bias,percent)
		p = (x,y,z)
		vector_type = 'FREE' if 0 < i > segments else 'AUTO'#'ALIGNED'
		shape.append((p,p,vector_type,p,vector_type))
	return [shape]



class Helix(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Helix"
		self.finishon = 4
		self.owner = None
		self.data = None
		self.close = False
	def reset(self):
		self.__init__()
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