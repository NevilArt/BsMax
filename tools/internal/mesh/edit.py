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
from bsmax.state import is_mode

class Mesh_OT_Chamfer(Operator):
	bl_idname = "mesh.chamfer"
	bl_label = "Chamfer"
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == "MESH_EDIT"
	
	def execute(self, ctx):
		vert,edge,face = ctx.tool_settings.mesh_select_mode
		v = vert and not edge and not face
		bpy.ops.mesh.bevel(vertex_only=v)
		self.report({'OPERATOR'},'bpy.ops.mesh.chamfer()')
		return{"FINISHED"}

class Mesh_OT_Drag(Operator):
	bl_idname = "mesh.drag"
	bl_label = "Mesh Drag"
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == "MESH_EDIT"
	
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


classes = [Mesh_OT_Chamfer, Mesh_OT_Drag]

def register_edit():
	[bpy.utils.register_class(c) for c in classes]

def unregister_edit():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_edit()