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

from bpy.types import Operator
from mathutils import Vector

from bpy.props import IntProperty, FloatProperty

from primitive.primitive import Draw_Primitive, Primitive_Public_Class
from bsmax.actions import delete_objects
from bsmax.bsmatrix import transform_point_to_matrix



class Lattice(Primitive_Public_Class):
	def init(self):
		self.finishon = 3
		self.owner = None

	def create(self, ctx, gride):
		bpy.ops.object.add(type='LATTICE', location=gride.location)
		self.owner = ctx.active_object
		self.owner.rotation_euler = gride.rotation

	def abort(self):
		delete_objects([self.owner])



class Create_OT_Lattice(Draw_Primitive):
	bl_idname = "create.lattice"
	bl_label = "Lattice"
	subclass = Lattice()

	resolution: IntProperty(name="Resolation", min= 2, max= 64)
	width, length, height = 0, 0, 0
	location = Vector((0,0,0))
	owner_matrix = None

	def create(self, ctx):
		self.subclass.create(ctx, self.gride)
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.data.points_u = self.resolution
		self.subclass.owner.data.points_v = self.resolution
		self.subclass.owner.data.points_w = self.resolution

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.width = dimension.width
			self.length = dimension.length
			self.location = self.subclass.owner.location = dimension.center
			self.owner_matrix = self.subclass.owner.matrix_world.copy()

		if clickcount == 2:
			self.height = dimension.height

			# height correction
			offset = Vector((self.width/2, self.length/2, self.height/2))
			location = transform_point_to_matrix(offset, self.gride.gride_matrix)
			self.subclass.owner.location = location

		self.subclass.owner.scale = (abs(self.width), abs(self.length), self.height)
	
	def finish(self):
		self.width, self.length, self.height = 0, 0, 0
		self.location = Vector((0,0,0))
		self.owner_matrix = None	
	



class Lattice_OT_Edit(Operator):
	bl_idname = "lattice.edit"
	bl_label = "Edit Lattice"
	bl_options = {"UNDO"}

	width: FloatProperty(name="Width", min= 0)
	length: FloatProperty(name="Length", min= 0)
	height: FloatProperty(name="Height", min= 0)
	u_res: IntProperty(name="Resolation U", min= 2, max= 1000)
	v_res: IntProperty(name="Resolation V", min= 2, max= 1000)
	w_res: IntProperty(name="Resolation W", min= 2, max= 1000)
	obj = None

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			if ctx.active_object.type == 'LATTICE':
				return True
		return False

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		Box = row.box()
		Col = Box.column(align = True)
		
		Col.label(text = "Parameters")
		Col.prop(self, "width")
		Col.prop(self, "length")
		Col.prop(self, "height")
		
		Col = Box.column(align = True)
		Col.prop(self, "u_res")
		Col.prop(self, "v_res")
		Col.prop(self, "w_res")

	def check(self, ctx):
		self.obj.dimensions = (self.width, self.length, self.height)
		self.obj.data.points_u = self.u_res
		self.obj.data.points_v = self.v_res
		self.obj.data.points_w = self.w_res
		return True

	def execute(self, ctx):
		return {'FINISHED'}

	def cancel(self, ctx):
		return None

	def invoke(self, ctx, event):
		self.obj = ctx.active_object
		if self.obj.type == "LATTICE":
			self.width = self.obj.dimensions.x
			self.length = self.obj.dimensions.y
			self.height = self.obj.dimensions.z
			self.u_res = self.obj.data.points_u
			self.v_res = self.obj.data.points_v
			self.w_res = self.obj.data.points_w
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self, width = 140)



classes = [Create_OT_Lattice,Lattice_OT_Edit]

def register_lattice():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_lattice():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_lattice()