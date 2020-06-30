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
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_offset_by_orient

class Lattice:
	def __init__(self):
		self.finishon = 3
		self.owner = None
	def reset(self):
		self.__init__()
	def create(self, ctx, clickpoint):
		bpy.ops.object.add(type='LATTICE', location=clickpoint.view)
		self.owner = ctx.active_object
		self.owner.rotation_euler = clickpoint.orient
	def update(self, ctx):
		pass
	def abort(self):
		delete_objects([self.owner])

class Create_OT_Lattice(CreatePrimitive):
	bl_idname = "create.lattice"
	bl_label = "Lattice"
	subclass = Lattice()

	resolution: IntProperty(name="Resolation", min= 2, max= 64)
	width, length, height = 0, 0, 0
	location = Vector((0,0,0))

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx, clickpoint)
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.data.points_u = self.resolution
		self.subclass.owner.data.points_v = self.resolution
		self.subclass.owner.data.points_w = self.resolution

	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.width = dimantion.width
			self.length = dimantion.length
			self.location = self.subclass.owner.location = dimantion.center
		if clickcount == 2:
			self.height = dimantion.height
			offset = get_offset_by_orient(Vector((0,0,dimantion.height / 2)), dimantion.view_name)
			self.subclass.owner.location = self.location + offset
		self.subclass.owner.scale = (self.width, self.length, self.height)
	def finish(self):
		pass

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
	[bpy.utils.register_class(c) for c in classes]

def unregister_lattice():
	[bpy.utils.unregister_class(c) for c in classes]