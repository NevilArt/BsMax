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



def get_rectangle_shapes(width, length, corner):
	Shapes = []
	w, l = width / 2, length / 2
	r, c = corner, corner - (corner * 0.551786)
	if corner == 0:
		p1, p2, p3, p4 = (-w, -l, 0), (-w,  l, 0), ( w,  l, 0), ( w, -l, 0)
		pt1 = (p1, p1, 'VECTOR', p1, 'VECTOR')
		pt2 = (p2, p2, 'VECTOR', p2, 'VECTOR')
		pt3 = (p3, p3, 'VECTOR', p3, 'VECTOR')
		pt4 = (p4, p4, 'VECTOR', p4, 'VECTOR')
		Shapes.append([pt1, pt2, pt3, pt4])
	else:
		pc1, pl1, pr1 = (-w + r, -l, 0), (-w + c, -l, 0), (-w + r, -l, 0)
		pc2, pl2, pr2 = ( w - r, -l, 0), ( w - r, -l, 0), ( w - c, -l, 0)
		pc3, pl3, pr3 = ( w, -l + r, 0), ( w, -l + c, 0), ( w, -l + r, 0)
		pc4, pl4, pr4 = ( w, l - r, 0), ( w, l - r, 0), ( w, l - c, 0)
		pc5, pl5, pr5 = (  w - r, l, 0), (  w - c, l, 0), (  w - r, l, 0) 
		pc6, pl6, pr6 = ( -w + r, l, 0), ( -w + r, l, 0), ( -w + c, l, 0)
		pc7, pl7, pr7 = ( -w, l - r, 0), ( -w, l - c, 0), ( -w, l - r, 0)
		pc8, pl8, pr8 = ( -w, -l + r, 0), ( -w, -l + r, 0), ( -w, -l + c, 0)
		pt1 = (pc1, pl1, 'FREE', pr1, 'VECTOR')
		pt2 = (pc2, pl2, 'VECTOR', pr2, 'FREE')
		pt3 = (pc3, pl3, 'FREE', pr3, 'VECTOR')
		pt4 = (pc4, pl4, 'VECTOR', pr4, 'FREE')
		pt5 = (pc5, pl5, 'FREE', pr5, 'VECTOR')
		pt6 = (pc6, pl6, 'VECTOR', pr6, 'FREE')
		pt7 = (pc7, pl7, 'FREE', pr7, 'VECTOR')
		pt8 = (pc8, pl8, 'VECTOR', pr8, 'FREE')
		Shapes.append([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8])
	return Shapes



class Rectangle(Primitive_Curve_Class):
	def init(self):
		self.classname = "Rectangle"
		self.finishon = 2
		self.close = True

	def create(self, ctx):
		shapes = get_rectangle_shapes(0, 0, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		shapes = get_rectangle_shapes(pd.width, pd.length, pd.chamfer1)
		self.update_curve(shapes)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Rectangle(Draw_Primitive):
	bl_idname = "create.rectangle"
	bl_label = "Rectangle"
	subclass = Rectangle()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.width = dimension.radius
				self.params.length = dimension.radius
			else:
				self.params.width = abs(dimension.width)
				self.params.length = abs(dimension.length)
				self.subclass.owner.location = dimension.center



def register_rectangle():
	bpy.utils.register_class(Create_OT_Rectangle)

def unregister_rectangle():
	bpy.utils.unregister_class(Create_OT_Rectangle)

if __name__ == '__main__':
	register_rectangle()