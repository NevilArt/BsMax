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
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive



def get_plane_mesh(width, length, WSegs, LSegs):
	verts, edges, faces = [], [], []
	# Create vertexes
	w = width / WSegs
	whalf = width / 2.0
	l = length / LSegs
	lhalf = length / 2.0
	for i in range(WSegs + 1):
		for j in range(LSegs + 1):
			verts.append(((w * i) - whalf, (l * j) - lhalf, 0.0))
	# create faces
	for i in range(WSegs):
		for j in range(LSegs):
			r = i * (LSegs + 1)
			a = r + j
			b = a + 1
			c = b + LSegs + 1
			d = c - 1
			faces.append((d, c, b, a)) 
	return verts, edges, faces



class Plane(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Plane"
		self.finishon = 2

	def create(self, ctx):
		mesh = get_plane_mesh(0, 0, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		mesh = get_plane_mesh(pd.width, pd.length, pd.wsegs, pd.lsegs)
		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Plane(Draw_Primitive):
	bl_idname = "create.plane"
	bl_label = "Plane"
	subclass = Plane()
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
		if clickcount > 0:
			self.subclass.update()



def register_plane():
	bpy.utils.register_class(Create_OT_Plane)

def unregister_plane():
	bpy.utils.unregister_class(Create_OT_Plane)

if __name__ == '__main__':
	register_plane()