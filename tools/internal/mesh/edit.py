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

from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty

from bsmax.mesh import get_selected_verts
from bsmax.actions import copy_array_to_clipboard, paste_array_from_clipboard

#TODO Quick mesh boolean setup operator and float menu



class Mesh_OT_Chamfer(Operator):
	bl_idname = "mesh.chamfer"
	bl_label = "Chamfer"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"
	
	def execute(self, ctx):
		vert, edge, face = ctx.tool_settings.mesh_select_mode
		vertex_only = (vert and not edge and not face)
		affect = 'VERTICES' if vertex_only else 'EDGES'
		bpy.ops.mesh.bevel('INVOKE_DEFAULT', affect=affect)
		return{"FINISHED"}



class Mesh_OT_Drag(Operator):
	bl_idname = "mesh.drag"
	bl_label = "Mesh Drag"
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == "EDIT_MESH"
	
	# def modal(self, ctx, event):
	# 	print("--> Draging")
	# 	if event.type in {'RIGHTMOUSE', 'ESC'}:
	# 		return {'CANCELLED'}
	# 	return {'RUNNING_MODAL'}
	
	def execute(self, ctx):
		print("Draged")
		# bpy.ops.mesh.extrude_edges_move())
		return{"FINISHED"}
	
	# def invoke(self, ctx, event):
	# 	ctx.window_manager.modal_handler_add(self)
	# 	return {'RUNNING_MODAL'}



class Mesh_OT_Smart_Select(Operator):
	bl_idname = "mesh.smart_select"
	bl_label = "Smart Select"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	mode: EnumProperty(name='Mode', default='SET',
		items =[('SET', 'Set', ''), ('ADD', 'Add', ''), ('SUB', 'Sub', '')])
	
	def execute(self, ctx):
		_, edge, _ = ctx.tool_settings.mesh_select_mode
		if edge:
			bpy.ops.mesh.smart_select_loop()
		
		else:
			if self.mode == 'SUB':
				bpy.ops.mesh.select_linked_pick(deselect=True)
			else:
				bpy.ops.mesh.select_linked_pick(deselect=False)

		return{"FINISHED"}



class Mesh_OT_Copy(Operator):
	bl_idname = "mesh.copy"
	bl_label = "Copy Vertex Location"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def execute(self, ctx):
		mesh = ctx.object.data
		vert, _, _ = ctx.tool_settings.mesh_select_mode

		bpy.ops.object.mode_set(mode="OBJECT")

		if vert:
			verts = get_selected_verts(mesh)
			if len(verts) == 1:
				co = verts[0].co
				copy_array_to_clipboard("BSMAXVERTEXLOCATIONCLIPBOARD", co)

		bpy.ops.object.mode_set(mode="EDIT")
		return{"FINISHED"}



class Mesh_OT_paste(Operator):
	bl_idname = "mesh.paste"
	bl_label = "Paste Vertex Location"
	bl_options = {'REGISTER', 'UNDO'}

	mirror_x: BoolProperty(name="Mirror X")
	mirror_y: BoolProperty(name="Mirror Y")
	mirror_z: BoolProperty(name="Mirror Z")

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def execute(self, ctx):
		co = paste_array_from_clipboard("BSMAXVERTEXLOCATIONCLIPBOARD")

		if self.mirror_x:
			co[0] *= -1
		if self.mirror_y:
			co[1] *= -1
		if self.mirror_z:
			co[2] *= -1

		mesh = ctx.object.data
		vert, _, _ = ctx.tool_settings.mesh_select_mode

		bpy.ops.object.mode_set(mode="OBJECT")

		if vert and co:
			verts = get_selected_verts(mesh)
			if len(verts) == 1:			
				index = verts[0].index
				ctx.object.data.vertices[index].co = co

		bpy.ops.object.mode_set(mode="EDIT")
		return{"FINISHED"}



classes = [
			Mesh_OT_Chamfer,
			Mesh_OT_Smart_Select,
			Mesh_OT_Drag,
			Mesh_OT_Copy,
			Mesh_OT_paste
		]

def register_edit():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_edit():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_edit()