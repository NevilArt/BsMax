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
class BsMax_OT_CreateShapeFromEdges(Operator):
	bl_idname = "bsmax.createshapefromedge"
	bl_label = "Create Shape from Edges"
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		v,e,f = ctx.tool_settings.mesh_select_mode
		if ctx.mode == 'EDIT_MESH' and e:
			bpy.ops.mesh.duplicate(mode=1)
			bpy.ops.mesh.separate(type='SELECTED')
		return{"FINISHED"}

# simulate 3d max Loop select
class BsMax_OT_LoopSelect(Operator):
	bl_idname = "bsmax.loopselect"
	bl_label = "Loop Select"
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
		return{"FINISHED"}

# simulate 3d max Ring select
class BsMax_OT_RingSelect(Operator):
	bl_idname = "bsmax.ringselect"
	bl_label = "Ring Select"
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
		return{"FINISHED"}

# DotLoop select
class BsMax_OT_DotLoop(Operator):
	bl_idname = "bsmax.dotloop"
	bl_label = "Dot loop"
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.bmax.loopselect()
			bpy.ops.mesh.select_nth()
		return{"FINISHED"}

# Dotring select
class BsMax_OT_DotRing(Operator):
	bl_idname = "bsmax.dotring"
	bl_label = "Dot Ring"
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.bmax.ringselect()
			bpy.ops.mesh.select_nth()
		return{"FINISHED"}

# Edit poly connect
class BsMax_OT_ConnectPoly(Operator):
	bl_idname = "bsmax.connectpoly"
	bl_label = "Connect (Poly)"
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
		return{"FINISHED"}

# remove ver, edge, face
class BsMax_OT_RemoveMesh(Operator):
	bl_idname = "bsmax.removemesh"
	bl_label = "Remove (Mesh)"
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
		return{"FINISHED"}

class BsMax_OT_DeleteMesh(Operator):
	bl_idname = "bsmax.deletemesh"
	bl_label = "Delete (Mesh)"
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
		return{"FINISHED"}

# remove isolated geometry operator
class BsMAx_OT_RemoveIsolatedGeometry(Operator):
	bl_idname = "bsmax.removeisolatedgeometry"
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
		return {'FINISHED'}

classes = [BsMax_OT_CreateShapeFromEdges,
		BsMax_OT_LoopSelect,
		BsMax_OT_RingSelect,
		BsMax_OT_DotLoop,
		BsMax_OT_DotRing,
		BsMax_OT_ConnectPoly,
		BsMax_OT_RemoveMesh,
		BsMax_OT_DeleteMesh,
		BsMAx_OT_RemoveIsolatedGeometry]

def register_meshs():
	[bpy.utils.register_class(c) for c in classes]

def unregister_meshs():
	[bpy.utils.unregister_class(c) for c in classes]