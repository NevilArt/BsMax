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
from primitive.primitive import PrimitiveCurveClass, CreatePrimitive
from bsmax.actions import delete_objects

def GetDonutShape(radius1, radius2):
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

class Donut(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Donut"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetDonutShape(0, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self):
		pd = self.data.primitivedata
		shapes = GetDonutShape(pd.radius1, pd.radius2)
		self.update_curve(shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateDonut(CreatePrimitive):
	bl_idname = "bsmax.createdonut"
	bl_label = "Donut (Create)"
	subclass = Donut()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		if clickcount == 2:
			self.params.radius2 = dimantion.radius_from_start_point
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_donut():
	bpy.utils.register_class(BsMax_OT_CreateDonut)

def unregister_donut():
	bpy.utils.unregister_class(BsMax_OT_CreateDonut)