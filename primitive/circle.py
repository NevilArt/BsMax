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
from primitive.primitive import PrimitiveCurveClass, Draw_Primitive
from bsmax.actions import delete_objects

def get_circle_shape(radius):
	Shapes = []
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
	Shapes.append([pt1,pt2,pt3,pt4])
	return Shapes

class Circle(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Circle"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True

	def reset(self):
		self.__init__()

	def create(self, ctx):
		shapes = get_circle_shape(0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		shapes = get_circle_shape(pd.radius1)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



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
	
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
	
	def finish(self):
		pass

def register_circle():
	bpy.utils.register_class(Create_OT_Circle)

def unregister_circle():
	bpy.utils.unregister_class(Create_OT_Circle)