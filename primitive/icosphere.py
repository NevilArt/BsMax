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

import bpy, bmesh
from mathutils import Matrix
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive
from bsmax.actions import delete_objects
from bsmax.state import version



class Icosphere(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Icosphere"
		self.finishon = 2
		self.version = version()

	def create(self, ctx):
		# Create an empty mesh and the object.
		new_mesh = bpy.data.meshes.new(self.classname)
		self.owner = bpy.data.objects.new(self.classname, new_mesh)
		# Add the object into the scene.
		ctx.collection.objects.link(self.owner)
		ctx.view_layer.objects.active = self.owner
		self.owner.select_set(state=True)
		# Construct the bmesh icosphere and assign it to the blender mesh
		bm = bmesh.new()
		bmesh.ops.create_icosphere(bm, matrix=Matrix.Scale(0, 4), calc_uvs=False)
		bm.to_mesh(new_mesh)
		bm.free()
		self.data = self.owner.data
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs = 1

	def update(self):
		pd = self.data.primitivedata
		orgmesh = bpy.data.meshes[self.data.name]
		bm = bmesh.new()
		if self.version >= 300:
			bmesh.ops.create_icosphere(bm, subdivisions=pd.wsegs,
							radius=pd.radius1,
							matrix=Matrix(), calc_uvs=True)
		else:
			bmesh.ops.create_icosphere(bm, subdivisions=pd.wsegs,
							diameter=pd.radius1,
							matrix=Matrix(), calc_uvs=True)
		bm.to_mesh(orgmesh.id_data)
		bm.free()

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Icosphere(Draw_Primitive):
	bl_idname = "create.uicosphere"
	bl_label = "Icosphere"
	subclass = Icosphere()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		if clickcount > 0:
			self.subclass.update()
	
	def finish(self):
		# claculate uv at the end
		pass



def register_icosphere():
	bpy.utils.register_class(Create_OT_Icosphere)

def unregister_icosphere():
	bpy.utils.unregister_class(Create_OT_Icosphere)

if __name__ == "__main__":
	register_icosphere()