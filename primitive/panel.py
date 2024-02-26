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
# 2024/02/07

import bpy

from bpy.types import Panel, Operator
from bpy.utils import register_class, unregister_class

from bsmax.primitive_ui import get_primitive_edit_panel


class Primitive_PT_Panel(Panel):
	bl_label = "Parameters"
	bl_idname = "DATA_PT_Primitives"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	@classmethod
	def poll(cls, ctx):
		if ctx.object.type in ('MESH', 'CURVE'):
			if ctx.object.data.primitivedata.classname != "":
				return True
		return False

	def draw(this, ctx):
		layout = this.layout
		self = ctx.object.data.primitivedata
		get_primitive_edit_panel(self, layout)
		col = layout.column(align=True)
		col.operator("primitive.cleardata", text="Convert to Ragular Object")


class Primitive_OT_Edit(Operator):
	bl_idname = "primitive.edit"
	bl_label = "Edit Primitive"
	bl_options = {"UNDO"}

	@classmethod
	def poll(self,ctx):
		if ctx.active_object != None:
			if ctx.active_object.type in ('MESH', 'CURVE'):
				if ctx.active_object.data.primitivedata != "":
					return True
		return False

	def draw(this,ctx):
		self = ctx.active_object.data.primitivedata
		get_primitive_edit_panel(self,this.layout)

	def execute(self,ctx):
		return {'FINISHED'}

	def invoke(self,ctx,event):
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self,width=200)


class BsMax_OT_Set_Object_Mode(Operator):
	bl_idname="bsmax.mode_set"
	bl_label="Set Object Mode"

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None

	def execute(self, ctx):
		classname = ""
		if ctx.active_object.type in ('MESH', 'CURVE'):
			classname = ctx.active_object.data.primitivedata.classname

		if classname != "":
			bpy.ops.primitive.edit('INVOKE_DEFAULT')
		else:
			if ctx.active_object.type == 'GPENCIL':
				bpy.ops.gpencil.editmode_toggle()

			elif ctx.active_object.type in {'MESH','CURVE','SURFACE',
											'META','FONT','ARMATURE',
											'LATTICE'}:
				# igone the edit mode for proxy and libraryoverirde #
				# TODO need to a method to check linked or not rather than use try #
				try:
					bpy.ops.object.editmode_toggle()
				except:
					pass
			# ignor this types {'EMPTY','LIGHT','LIGHT_PROBE','CAMERA','SPEAKER',}
		return {"FINISHED"}


classes = (
	Primitive_PT_Panel,
	Primitive_OT_Edit,
	BsMax_OT_Set_Object_Mode
)

def register_panel():
	for c in classes: 
		register_class(c)

def unregister_panel():
	for c in classes:
		unregister_class(c)