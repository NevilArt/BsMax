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
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

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

class Plane(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Plane"
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
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
		delete_objects([self.owner])

class Create_OT_Plane(CreatePrimitive):
	bl_idname = "create.plane"
	bl_label = "Plane"
	subclass = Plane()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.width = dimantion.width
			self.params.length = dimantion.length
			self.subclass.owner.location = dimantion.center
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_plane():
	bpy.utils.register_class(Create_OT_Plane)

def unregister_plane():
	bpy.utils.unregister_class(Create_OT_Plane)