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
from math import radians, pi, sin, cos
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_bias

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

class Create_OT_Helix(CreatePrimitive):
	bl_idname = "create.helix"
	bl_label = "Helix"
	subclass = Helix()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
			self.params.radius2 = dimantion.radius
		if clickcount == 2:
			self.params.height = dimantion.height
		if clickcount == 3:
			radius = self.params.radius1 + dimantion.height_np
			self.params.radius2 = 0 if radius < 0 else radius
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_helix():
	bpy.utils.register_class(Create_OT_Helix)
	
def unregister_helix():
	bpy.utils.unregister_class(Create_OT_Helix)