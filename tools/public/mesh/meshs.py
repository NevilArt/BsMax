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
from bpy.props import BoolProperty

# create shape from selected edges poly
class Mesh_OT_Create_Curve_From_Edges(Operator):
	bl_idname = "mesh.create_curve_from_edge"
	bl_label = "Create Shape from Edges"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		# v,e,f = ctx.tool_settings.mesh_select_mode
		e = ctx.tool_settings.mesh_select_mode[1]
		if ctx.mode == 'EDIT_MESH' and e:
			bpy.ops.mesh.duplicate(mode=1)
			bpy.ops.mesh.separate(type='SELECTED')
		self.report({'INFO'},'bpy.ops.mesh.create_curve_from_edge()')
		return{"FINISHED"}

class Mesh_OT_Auto_Loop_Select(Operator):
	bl_idname = "mesh.auto_loop_select"
	bl_label = "Auto Loop Select"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v or e:
				bpy.ops.mesh.loop_multi_select(ring=False)
			elif f:
				#TODO "Face loop"
				pass
		self.report({'INFO'},'bpy.ops.mesh.auto_loop_select()')
		return{"FINISHED"}

class Mesh_OT_Auto_Ring_Select(Operator):
	bl_idname = "mesh.auto_ring_select"
	bl_label = "Auto Ring Select"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v or e:
				bpy.ops.mesh.loop_multi_select(ring=True)
			elif f:
				# TODO face ring
				pass
		self.report({'INFO'},'bpy.ops.mesh.auto_ring_select()')
		return{"FINISHED"}

class Mesh_OT_Dot_Loop_Select(Operator):
	bl_idname = "mesh.dot_loop_select"
	bl_label = "Dot Loop Select"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.bmax.loopselect()
			bpy.ops.mesh.select_nth()
		self.report({'INFO'},'bpy.ops.mesh.dot_loop_select()')
		return{"FINISHED"}

class Mesh_OT_Dot_Ring_Select(Operator):
	bl_idname = "mesh.dot_ring_select"
	bl_label = "Dot Ring"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.bmax.ringselect()
			bpy.ops.mesh.select_nth()
		self.report({'INFO'},'bpy.ops.mesh.dot_ring_select()')
		return{"FINISHED"}

class Mesh_OT_Connect(Operator):
	bl_idname = "mesh.connect"
	bl_label = "Connect"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v: 
				bpy.ops.mesh.vert_connect()
			elif e:
				bpy.ops.mesh.subdivide()
				bpy.ops.mesh.select_all(action='DESELECT')
				#TODO select new created edges
		self.report({'INFO'},'bpy.ops.mesh.connect()')
		return{"FINISHED"}

class Mesh_OT_Remove(Operator):
	bl_idname = "mesh.remove"
	bl_label = "Remove"
	vert: bpy.props.BoolProperty(name="Use Verts",default=False)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v:
				bpy.ops.mesh.dissolve_verts()
			if e:
				bpy.ops.mesh.dissolve_edges(use_verts=self.vert)
			if f:
				bpy.ops.mesh.dissolve_faces(use_verts=self.vert)
		self.report({'INFO'},'bpy.ops.mesh.remove(vert='+ str(self.vert) +')')
		return{"FINISHED"}

class Mesh_OT_Delete_Auto(Operator):
	bl_idname = "mesh.delete_auto"
	bl_label = "Delete (Auto)"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v:
				bpy.ops.mesh.delete(type='VERT')
			if e:
				bpy.ops.mesh.delete(type='EDGE')
			if f:
				bpy.ops.mesh.delete(type='FACE')
		self.report({'INFO'},'bpy.ops.mesh.delete_auto()')
		return{"FINISHED"}

class Mesh_OT_Remove_Isolated_Geometry(Operator):
	bl_idname = "mesh.remove_isolated_geometry"
	bl_label = "Remove Isolated Geometry"
	bl_description = "Remove isolated vertices and edges"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		v,e,f = ctx.tool_settings.mesh_select_mode
		bpy.ops.mesh.select_loose()
		if v:
			bpy.ops.mesh.delete(type='VERT')
		if e:
			bpy.ops.mesh.delete(type='EDGE')
		if f:
			bpy.ops.mesh.delete(type='FACE')
		self.report({'INFO'},'bpy.ops.mesh.remove_isolated_geometry()')
		return {'FINISHED'}

classes = [Mesh_OT_Create_Curve_From_Edges,
		Mesh_OT_Auto_Loop_Select,
		Mesh_OT_Auto_Ring_Select,
		Mesh_OT_Dot_Loop_Select,
		Mesh_OT_Dot_Ring_Select,
		Mesh_OT_Connect,
		Mesh_OT_Remove,
		Mesh_OT_Delete_Auto,
		Mesh_OT_Remove_Isolated_Geometry]

def register_meshs():
	[bpy.utils.register_class(c) for c in classes]

def unregister_meshs():
	[bpy.utils.unregister_class(c) for c in classes]