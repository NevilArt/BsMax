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

import bpy, bmesh
from bpy.types import Operator

class Vertex:
	def __init__(self):
		self.index = 0
		self.edges = []
		self.faces = []

class Edge:
	def __init__(self):
		self.index = 0
		self.verts = []
		self.faces = []

class Face:
	def __init__(self):
		self.index = 0
		self.verts = []
		self.edges = []

class Mesh:
	def __init__(self, data):
		self.data = data
		self.vertices = []
		self.edges = []
		self.polygons = []
		self.read_data(data)
	
	def is_unique_ege(self,v1,v2):
		return True

	def read_data(self, data):
		""" read faces """
		for index, poly in enumerate(data.polygons):
			face = Face()
			face.index = index
			face.verts = [v.index for v in poly.vertices]
			for i,v in enumerate(face.verts):
				pass
			self.polygons.append(face)

class Fast_Mesh:
	def __init__(self, owner):
		self.owner = owner
		self.vertices = []
		self.edges = []
		self.polygons = []
		self.read_deata()
	
	def get_faces(self, index, source):
		if source == 'vertics':
			pass
		if source == 'edge':
			pass
		if source == 'face':
			polygons = self.owner.data.polygons
			if index < len(polygons):
				return [v for v in polygons[index].vertices]
		return []
	
	def read_deata(self):
		data = self.owner.data
		self.vertices = data.vertices
		self.polygons = data.polygons
	
	def get_center_loop(self, method):
		if method == 1:
			""" fast method no analyze """
			return [v for v in self.vertices if v.co.x == 0]
		else:
			return []
	
	def select_verts(self, indexes):
		data = self.owner.data
		bm = bmesh.from_edit_mesh(data)
		for v in bm.verts:
			v.select_set(False)
		for i in indexes:
			bm.verts[i].select_set(True)
		bm.select_mode = {'VERT'}
		bm.select_flush_mode()
		bmesh.update_edit_mesh(data)

class Mesh_OT_Topo_Symmetry(Operator):
	bl_idname = "mesh.topo_symmetry"
	bl_label = "Topo Symmetry"

	mesh = None

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	# def draw(self,ctx):
	# 	self.layout

	def execute(self, ctx):
		fm = Fast_Mesh(ctx.active_object)
		indexes = fm.get_center_loop(1)
		print(indexes)
		fm.select_verts(indexes)
		return{"FINISHED"}
	
	# def cancel(self,ctx):
	# 	return None

	# def invoke(self,ctx,event):
	# 	return ctx.window_manager.invoke_props_dialog(self)


def register_topo():
	bpy.utils.register_class(Mesh_OT_Topo_Symmetry)

def unregister_topo():
	bpy.utils.unregister_class(Mesh_OT_Topo_Symmetry)

if __name__ == "__main__":
	register_topo()