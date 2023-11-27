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


def calculate_center(self):
	self.center.x = (self.min.x + self.max.x) / 2
	self.center.y = (self.min.y + self.max.y) / 2
	self.center.z = (self.min.z + self.max.z) / 2



def get_bound_from_object_local(self):
	b = [self.obj.matrix_world @ Vector(v) for v in self.obj.bound_box]

	self.min.x = min(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
	self.max.x = max(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
	self.min.y = min(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
	self.max.y = max(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
	self.min.z = min(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
	self.max.z = max(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
	
	calculate_center(self)



def get_bound_from_verts(self, verts):
	if not verts:
		return
	
	self.min = verts[0].copy()
	self.max = verts[0].copy()

	for co in verts:
		if self.min.x > co.x:
			self.min.x = co.x

		if self.min.y > co.y:
			self.min.y = co.y

		if self.min.z > co.z:
			self.min.z = co.z

		if self.max.x < co.x:
			self.max.x = co.x

		if self.max.y < co.y:
			self.max.y = co.y

		if self.max.z < co.z:
			self.max.z = co.z
	
	calculate_center(self)



def get_empty_bound(self):
	displayType = self.obj.empty_display_type
	size = self.obj.empty_display_size
	location = self.obj.matrix_world.translation

	if displayType in ('PLAIN_AXES', 'SPHERE', 'CUBE'):
		#TODO need to apply transfomr for cube and plane_axes
		self.min.x = location.x - size
		self.max.x = location.x + size
		self.min.y = location.y - size
		self.max.y = location.y + size
		self.min.z = location.z - size
		self.max.z = location.z + size
		self.center = location

	elif displayType == 'ARROWS':
		#TODO need to apply transfomr
		self.min.x = location.x
		self.max.x = location.x + size
		self.min.y = location.y
		self.max.y = location.y + size
		self.min.z = location.z
		self.max.z = location.z + size
		calculate_center(self)

	elif displayType == 'SINGLE_ARROW':
		#TODO need to aply transform
		width = size * 0.07
		self.min.x = location.x - width
		self.max.x = location.x + width
		self.min.y = location.y - width
		self.max.y = location.y + width
		self.min.z = location.z
		self.max.z = location.z + size
		calculate_center(self)

	elif displayType == 'CIRCLE':
		#TODO need to apply transfomr
		self.min.x = location.x - size
		self.max.x = location.x + size
		self.min.y = location.y
		self.max.y = location.y
		self.min.z = location.z - size
		self.max.z = location.z + size
		self.center = location

	elif displayType == 'CONE':
		#TODO need to apply transfomr
		self.min.x = location.x - size
		self.max.x = location.x + size
		self.min.y = location.y
		self.max.y = location.y + size*2
		self.min.z = location.z - size
		self.max.z = location.z + size
		calculate_center(self)

	elif displayType == 'IMAGE':
		#TODO need to calculate aspect ratio from image
		# and apply to transform
		self.min.x = location.x - size
		self.max.x = location.x + size
		self.min.y = location.y - size
		self.max.y = location.y + size
		self.min.z = location.z
		self.max.z = location.z
		calculate_center(self)



def get_light_bound(self):
	pass



def bound_box_get_world_bound(self):
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
		get_empty_bound(self)

	elif self.obj.type == "LIGHT":
		get_light_bound(self)



def bound_box_get_from_selection(self):
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



class BoundBox():
	def __init__(self, obj):
		self.obj = obj
		self.min = Vector((0,0,0))
		self.max = Vector((0,0,0))
		self.center = Vector((0,0,0))
	
	def get_local_bound(self):
		get_bound_from_object_local(self)
	
	def get_world_bound(self):
		bound_box_get_world_bound(self)
	
	def get_from_selection(self):
		bound_box_get_from_selection(self)