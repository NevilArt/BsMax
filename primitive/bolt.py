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
# 2024/05/19

import bpy

from primitive.primitive import(
	Primitive_Geometry_Class, Draw_Primitive
)

from primitive.bolt_mesh import(
    Bolt_Mesh, Nut_Mesh, RemoveDoubles, Scale_Mesh_Verts
)


def get_bolt_mesh(props):

	if props.bf_Model_Type == 'bf_Model_Bolt':
		verts, faces = Bolt_Mesh(props)

	elif props.bf_Model_Type == 'bf_Model_Nut':
		verts, faces = Nut_Mesh(props)

	verts, faces = RemoveDoubles(verts, faces)

	scale = props.height
	verts = Scale_Mesh_Verts(verts, scale)
	return verts, [], faces


class Bolt(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Bolt"
		self.finishon = 2
		self.shading = 'AUTO'

	def create(self, ctx):
		mesh = [], [], []
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.height = 1
		self.update()

	def update(self):
		mesh = get_bolt_mesh(self.data.primitivedata)
		# mesh.validate()
		self.update_mesh(mesh)


class Create_OT_Bolt(Draw_Primitive):
	bl_idname = 'create.bolt'
	bl_label = "Bolt"
	subclass = Bolt()
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


def register_bolt():
	bpy.utils.register_class(Create_OT_Bolt)


def unregister_bolt():
	bpy.utils.unregister_class(Create_OT_Bolt)


if __name__ == '__main__':
	register_bolt()
	obj = Bolt()
	obj.create(bpy.context)
	obj.update()