############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Scene, Panel, Operator

class BsMax_OT_AttachMesh(Operator):
	bl_idname = "bsmax.attachmesh"
	bl_label = "Attach (Mesh)"
	#custom_property: PointerProperty(type = bpy.types.Object)
	def execute(self, ctx):
		# print("Attach by eyedrop working on progress")
		return{"FINISHED"}

class BsMax_OT_AttachListMesh(Operator):
	bl_idname = "bsmax.attachlistmesh"
	bl_label = "Attach List (Mesh)"
	def execute(self, ctx):
		# print("Attach by list working on progress")
		return{"FINISHED"}

class BsMax_OT_DetachMesh(Operator):
	bl_idname = "bsmax.detachmesh"
	bl_label = "Detach (Mesh)"

	name:StringProperty(name="Name")
	element:BoolProperty(default=False)
	clone:BoolProperty(default=False)

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.column()
		row.prop(self,"name",text="Detach as:")
		row.prop(self,"element",text ="Detach To Element")
		row.prop(self,"clone",text="Detach as clone")

	def execute(self, ctx):
		if self.clone:
			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1},
				TRANSFORM_OT_translate={"value":(0, 0, 0),
				"orient_type":'GLOBAL',
				"orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)),
				"orient_matrix_type":'GLOBAL',
				"constraint_axis":(False, False, False),
				"mirror":False,
				"use_proportional_edit":False,
				"proportional_edit_falloff":'SMOOTH',
				"proportional_size":1,
				"use_proportional_connected":False,
				"use_proportional_projected":False,
				"snap":False,
				"snap_target":'CLOSEST',
				"snap_point":(0, 0, 0),
				"snap_align":False,
				"snap_normal":(0, 0, 0),
				"gpencil_strokes":False,
				"cursor_transform":False,
				"texture_space":False,
				"remove_on_cancel":False,
				# "release_confirm":False,
				"use_accurate":False})
		if self.element:
			bpy.ops.mesh.split('INVOKE_DEFAULT')
		else:
			bpy.ops.mesh.separate(type = 'SELECTED')
		return{"FINISHED"}
	def invoke(self, ctx, event):
		if ctx.active_object != None:
			self.name = ctx.active_object.name
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)

classes = [BsMax_OT_AttachMesh, BsMax_OT_AttachListMesh, BsMax_OT_DetachMesh]

def register_attach():
	[bpy.utils.register_class(c) for c in classes]

def unregister_attach():
	[bpy.utils.unregister_class(c) for c in classes]