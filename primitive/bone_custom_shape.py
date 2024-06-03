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
# 2024/05/27

import bpy

from mathutils import Vector
from math import pi, sin, cos, radians
from bpy.utils import register_class, unregister_class

from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_custom_mesh(type, radius):
	verts, edges, faces = [], [], []
	return verts, edges, faces


class BoneCustomShape(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Bone Shape"
		self.finishon = 1
		self.owner = None
		self.data = None

	def create(self, ctx):
		mesh = get_custom_mesh('CIRCLE', 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		mesh = get_custom_mesh('CIRCLE', 1)
		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete(confirm=False)


class Create_OT_CustomShape(Draw_Primitive):
	bl_idname = "create.custom_bone_shape"
	bl_label = "Custom Bone Shape"
	subclass = BoneCustomShape()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, _, clickcount, dimension):
		if clickcount == 1:
			self.params.height = dimension.radius

		if clickcount > 0:
			self.subclass.update()


def register_bone_custom_shape():
	register_class(Create_OT_CustomShape)


def unregister_bone_custom_shape():
	unregister_class(Create_OT_CustomShape)


if __name__ == '__main__':
	register_bone_custom_shape()