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
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive
from bsmax.actions import delete_objects



def get_mesher_mesh(radius):
	r, h = radius / 2, radius
	verts = [(-r,-r,0),(r,-r,0),(r,r,0),(-r,r,0),(0,0,h)]
	faces = [(3,2,1,0),(1,4,0),(2,4,1),(3,4,2),(0,4,3)]
	return verts, [], faces



def update_mesher(self, ctx):
	""" check is target avalible """
	if self.target in bpy.data.objects:
		target = bpy.data.objects[self.target]
		if target.type in {'MESH', 'CURVE'}:
			self.owner.select_set(False)
			ctx.view_layer.objects.active = target
			target.select_set(True)
			bpy.ops.object.duplicate()
			newobject = ctx.view_layer.objects.active
			newobject.select_set(True)
			bpy.ops.object.convert(target = 'MESH', keep_original = False)
			tmpmesh = newobject.data
			bm = bmesh.new()
			bm.from_mesh(tmpmesh)
			bm.to_mesh(self.data)
			bm.free()
			bpy.data.meshes.remove(tmpmesh)
			bpy.ops.object.delete()
			self.owner.select_set(True)
			ctx.view_layer.objects.active = self.owner



class Mesher(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Mesher"
		self.finishon = 2
		self.owner = None
		self.data = None

	def create(self, ctx):
		mesh = get_mesher_mesh(0)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		if pd.target == "":
			mesh = get_mesher_mesh(pd.radius1)
			self.update_mesh(mesh)
		else:
			self.target = pd.target
			update_mesher(self, bpy.context)

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Mesher(Draw_Primitive):
	bl_idname = "create.mesher"
	bl_label = "Mesher"
	subclass = Mesher()

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius / 2
			self.subclass.owner.location = dimension.center
		if clickcount > 0:
			self.subclass.update(ctx)




def register_mesher():
	bpy.utils.register_class(Create_OT_Mesher)

def unregister_mesher():
	bpy.utils.unregister_class(Create_OT_Mesher)