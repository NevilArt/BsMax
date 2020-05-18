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

import bpy, bmesh, itertools
from bpy.types import Operator
from .bsmesh  import *

# Original code from https://blenderartists.org/u/maxiv94
# https://blenderartists.org/t/interactive-tools-for-blender-2-8/1164932

class BsMax_OT_SmartCreate(Operator):
	bl_idname = "mesh.smart_create"
	bl_label = "Smart Create"
	bl_description = "Context sensitive creation"
	bl_options = {'REGISTER', 'UNDO'}

	def connect_verts_to_last(self, selection):
		bm = get_bmesh()
		ordered_selection = []
		for vert in selection:
			if vert not in bm.select_history:
				ordered_selection.append(vert)
		for item in bm.select_history:
			ordered_selection.append(item)
		for vert in ordered_selection:
			select_from_item([vert,ordered_selection[-1]], verts = True, replace= True)
			bpy.ops.mesh.vert_connect()
		select_from_item(selection, verts = True, replace= True)

	def select_rings_inner_loop(self):
		new_selection = get_selected(edges = True, get_item = True)
		vert_list = [vert for edge in new_selection for vert in edge.verts]
		vert_list = list(filter(lambda x: len(list_intersection(x.link_edges,new_selection)) == 2, vert_list))
		new_selection = [edge for vert in vert_list for edge in vert.link_edges if edge not in new_selection]
		select_from_item(new_selection, edges = True, replace = True)

	def super_smart_create(self,ctx):
		# bm = get_bmesh()
		selectionMode = (tuple(ctx.scene.tool_settings.mesh_select_mode))
		#if Vertex is selected
		if selectionMode[0]:
			selection = get_selected(verts = True, get_item = True)
			if len(selection) == 1 or (verts_share_edge(selection) and are_border_verts(selection)):
				# mesh_f2.bpy.ops.mesh.f2('INVOKE_DEFAULT')
				bpy.ops.mesh.f2('INVOKE_DEFAULT')
			elif verts_share_face(selection):
				self.connect_verts_to_last(selection)
			else:    
				bpy.ops.mesh.vert_connect()
		#if Edge is selected
		elif selectionMode[1]:
			selection = get_selected(edges = True, get_item = True)
			if len(selection) == 1:
				split_edge_select_vert(change_selection = True) 					
			elif is_border(selection):
				bpy.ops.mesh.edge_face_add()
				ctx.scene.tool_settings.mesh_select_mode = [False,True,False]
			elif is_ring(selection):
				bpy.ops.mesh.subdivide_edgering(number_cuts = 1,
												interpolation = 'LINEAR',
												profile_shape = 'LINEAR',
												smoothness = 0)
				self.select_rings_inner_loop()
			elif is_adjacent(selection):
				bpy.ops.mesh.edge_face_add()
				ctx.scene.tool_settings.mesh_select_mode = [False,True,False]
			else:
				bpy.ops.mesh.bridge_edge_loops()
				ctx.scene.tool_settings.mesh_select_mode = [False,True, False]
		#if Face is selected		   
		elif selectionMode[2]:
			selection = get_selected(faces = True, get_item = True)
			if len(selection) == 1:
				quad_fill()
			if len(selection) > 1:
				bpy.ops.mesh.bridge_edge_loops()

	def execute(self,ctx):
		self.super_smart_create(ctx)
		return{'FINISHED'}

def register_smartcreate():
	bpy.utils.register_class(BsMax_OT_SmartCreate)

def unregister_smartcreate():
	bpy.utils.unregister_class(BsMax_OT_SmartCreate)