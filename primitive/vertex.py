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
# 2024/05/29

import bpy
from bpy.props import EnumProperty
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive


def get_vertex_mesh(verts, mode):
	edges, faces = [], []
	if mode == "EDGE" and len(verts) > 1 or len(verts) == 2:
		for i in range(len(verts) - 1):
			edges.append([i, i+1])
	elif mode == "FACE":
		if len(verts) > 2:
			face = []
			for i in range(len(verts)):
				face.append(i)
			faces.append(face)
		elif len(verts) == 2:
			edges.append([0, 1])
	return verts, edges, faces


class Vertex(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Vertex"
		self.finishon = 0 # infinit
		self.mode = 'NONE' # 'VERT' 'EDGE' 'FACE'
		self.verts = []

	def reset(self):
		mode = self.mode
		self.__init__()
		self.mode = mode

	def create(self, ctx):
		mesh = get_vertex_mesh([], self.mode)
		self.create_mesh(ctx, mesh, self.classname)

	def update(self):
		mesh = get_vertex_mesh(self.verts, self.mode)
		self.update_mesh(mesh)

	def abort(self):
		if self.owner:
			bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')



class Create_OT_Vertex(Draw_Primitive):
	bl_idname="create.vertex"
	bl_label="Vertex"
	subclass = Vertex()
	lastclick = 1
	fill_type: EnumProperty(
		name='Fill Mode',default='NONE',
		items =[
			('NONE', "None", ""),
			('VERT', "Vertex Only", ""),
			('EDGE', "Connect Edges", ""),
			('FACE', "Create Face", "")
		]
	) # type: ignore

	def create(self, ctx):
		if self.fill_type == 'NONE':
			self.subclass.finishon = 2
		self.subclass.mode = self.fill_type
		self.subclass.verts.append(self.point_current.location)
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata

	def update(self, ctx, clickcount, dimension):
		if self.drag:
			self.subclass.verts[-1] = dimension.end
		else:
			if clickcount != self.lastclick:
				self.subclass.verts.append(dimension.end)
				self.lastclick = clickcount
		self.subclass.update()

	def finish(self):
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
		self.subclass.reset()



def register_vertex():
	bpy.utils.register_class(Create_OT_Vertex)
	
def unregister_vertex():
	bpy.utils.unregister_class(Create_OT_Vertex)

if __name__ == '__main__':
	register_vertex()