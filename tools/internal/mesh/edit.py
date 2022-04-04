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



classes = [Mesh_OT_Chamfer, Mesh_OT_Drag]

def register_edit():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_edit():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_edit()