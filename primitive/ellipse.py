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



def get_ellipse_shape(length, width, outline, Thickness):
	Shapes = []
	el = [[length, width]]
	if outline:
		el.append([length + Thickness, width + Thickness])
	for r1, r2 in el:
		t1 = r1 * 0.551786
		t2 = r2 * 0.551786
		pc1, pl1, pr1 = ( 0,-r2, 0), (-t1, -r2, 0), (  t1, -r2, 0)
		pc2, pl2, pr2 = ( r1, 0, 0), ( r1, -t2, 0), (  r1,  t2, 0)
		pc3, pl3, pr3 = ( 0, r2, 0), ( t1,  r2, 0), ( -t1,  r2, 0)
		pc4, pl4, pr4 = (-r1, 0, 0), ( -r1, t2, 0), ( -r1, -t2, 0)
		pt1 = (pc1, pl1, 'FREE', pr1, 'FREE')
		pt2 = (pc2, pl2, 'FREE', pr2, 'FREE')
		pt3 = (pc3, pl3, 'FREE', pr3, 'FREE')
		pt4 = (pc4, pl4, 'FREE', pr4, 'FREE')
		Shapes.append([pt1, pt2, pt3, pt4])
	return Shapes



class Ellipse(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Ellipse"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True

	def reset(self):
		self.__init__()

	def create(self, ctx):
		shapes = get_ellipse_shape(0, 0, False, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		# length, width, outline, Thickness
		shapes = get_ellipse_shape(pd.width, pd.length, pd.outline, pd.thickness)
		self.update_curve(shapes)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Ellipse(Draw_Primitive):
	bl_idname = "create.ellipse"
	bl_label = "Ellipse"
	subclass = Ellipse()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			if self.ctrl:
				self.params.width = dimantion.width
				self.params.length = dimantion.length
			else:
				self.params.width = dimantion.width/2
				self.params.length = dimantion.length/2
				self.subclass.owner.location = dimantion.center

	def finish(self):
		pass



def register_ellipse():
	bpy.utils.register_class(Create_OT_Ellipse)

def unregister_ellipse():
	bpy.utils.unregister_class(Create_OT_Ellipse)

if __name__ == '__main__':
	register_ellipse()