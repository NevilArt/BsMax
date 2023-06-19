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

from mathutils import Vector

# local bounding box
# world bounding box
# selected mesh bounding box
# selected curve bounding box
# empty local bounding box
# empty world bounding box



def get_bound_from_object_local(self):
	b = [self.obj.matrix_world @ Vector(v) for v in self.obj.bound_box]

	self.min.x = min(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
	self.max.x = max(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
	self.min.y = min(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
	self.max.y = max(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
	self.min.z = min(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
	self.max.z = max(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
	
	self.center.x = (self.min.x + self.max.x) / 2
	self.center.y = (self.min.y + self.max.y) / 2
	self.center.z = (self.min.z + self.max.z) / 2



def get_bound_from_verts(self, verts):
	if not verts:
		return
	
	min = verts[0].copy()
	max = verts[0].copy()

	for co in verts:
		if min.x > co.x:
			min.x = co.x

		if min.y > co.y:
			min.y = co.y

		if min.z > co.z:
			min.z = co.z

		if max.x < co.x:
			max.x = co.x

		if max.y < co.y:
			max.y = co.y

		if max.z < co.z:
			max.z = co.z
	
	self.center.x = (min.x + max.x) / 2
	self.center.y = (min.y + max.y) / 2
	self.center.z = (min.z + max.z) / 2



class BoundBox():
	def __init__(self, obj):
		self.obj = obj
		self.min = Vector((0,0,0))
		self.max = Vector((0,0,0))
		self.center = Vector((0,0,0))
	
	def get_local_bound(self):
		get_bound_from_object_local(self)
	
	def get_world_bound(self):
		matrix_world = self.obj.matrix_world
		
		if self.obj.type == "MESH":
			vertices = self.obj.data.vertices
			verts = [matrix_world @ vert.co for vert in vertices]
			get_bound_from_verts(self, verts)

		elif self.obj.type == "CURVE":
			verts = []
			for spn in self.obj.data.splines:
				verts += [matrix_world @ pts.co for pts in spn.bezier_points]
			get_bound_from_verts(self, verts)

		elif self.obj.type == "EMPTY":
			pass

		elif self.obj.type == "LIGHT":
			pass
	
	def get_from_selection(self):
		matrix_world = self.obj.matrix_world

		if self.obj.type == "MESH":
			vertices = self.obj.data.vertices
			verts = [matrix_world @ vert.co for vert in vertices if vert.select]
			get_bound_from_verts(self, verts)

		if self.obj.type == "CURVE":
			verts = []
			for spline in self.obj.data.splines:
				verts += [matrix_world @ pts.co for pts in spline.bezier_points
	      			if pts.select_control_point]
			get_bound_from_verts(self, verts)