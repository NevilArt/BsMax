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
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from bsmax.actions import delete_objects



def get_donut_shape(radius1, radius2):
	shapes = []
	for radius in [radius1, radius2]:
		r = radius
		t = r * 0.551786
		pc1,pl1,pr1 = (0,-r,0),(-t,-r,0),(t,-r,0)
		pc2,pl2,pr2 = (r,0,0),(r,-t,0),(r,t,0)
		pc3,pl3,pr3 = (0,r,0),(t,r,0),(-t,r,0)
		pc4,pl4,pr4 = (-r,0,0),(-r,t,0),(-r,-t,0)
		pt1 = (pc1,pl1,'FREE',pr1,'FREE')
		pt2 = (pc2,pl2,'FREE',pr2,'FREE')
		pt3 = (pc3,pl3,'FREE',pr3,'FREE')
		pt4 = (pc4,pl4,'FREE',pr4,'FREE')
		shapes.append([pt1,pt2,pt3,pt4])
	return shapes



class Donut(Primitive_Curve_Class):
	def __init__(self):
		self.classname = "Donut"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = True

	def create(self, ctx):
		shapes = get_donut_shape(0, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		shapes = get_donut_shape(pd.radius1, pd.radius2)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Donut(Draw_Primitive):
	bl_idname = "create.donut"
	bl_label = "Donut"
	subclass = Donut()
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
				self.params.radius2 = dimantion.radius/2
			else:
				self.params.radius1 = dimantion.radius
		
		if clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return
			self.params.radius2 = dimantion.distance



def register_donut():
	bpy.utils.register_class(Create_OT_Donut)

def unregister_donut():
	bpy.utils.unregister_class(Create_OT_Donut)

if __name__ == "__main__":
	register_donut()