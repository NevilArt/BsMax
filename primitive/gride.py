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

from mathutils import Vector, Matrix, Euler
from math import pi, sqrt
from bpy_extras.view3d_utils import region_2d_to_location_3d

from bsmax.state import get_view_orientation
from bsmax.mouse import ray_cast, get_click_point_on_face
from bsmax.bsmatrix import (matrix_from_elements,
							transform_point_to_matrix,
							points_to_local_matrix)



class Dimension:
	def __init__(self, gride, start, end):
		self.gride = gride
		self.start = start
		self.end = end

		self.width = 0
		self.length = 0
		self.height = 0
		""" Distance of start and current """
		self.radius = 0
		""" Distance of gride and current """
		self.distance = 0
		self.center = Vector((0, 0, 0))
		self.local = Vector((0,0,0))
		self.calculate()
	
	def calculate(self):
		# radiue distance of start and end point
		x = self.end.x - self.start.x
		y = self.end.y - self.start.y
		z = self.end.z - self.start.z
		self.radius = sqrt(x**2 + y**2 + z**2)
		
		# distance of gride and end point
		x = self.end.x - self.gride.location.x
		y = self.end.y - self.gride.location.y
		z = self.end.z - self.gride.location.z
		self.distance = sqrt(x**2 + y**2 + z**2)
		
		# convert to local matrix
		sx, sy, _ = points_to_local_matrix(self.start, self.gride.gride_matrix)
		ex, ey, ez = points_to_local_matrix(self.end, self.gride.gride_matrix)

		# get dimension from matrix
		# self.width = abs(ex-sx)
		# self.length = abs(ey-sy)
		self.width = ex-sx
		self.length = ey-sy
		self.height = self.radius

		self.local = Vector((ex, ey, ez))
	
		# Get Center in world matrix
		self.center.x = (self.start.x + self.end.x) / 2
		self.center.y = (self.start.y + self.end.y) / 2
		self.center.z = (self.start.z + self.end.z) / 2



class Click_Point:
	def __init__(self):
		self.location = Vector((0, 0, 0))
		self.normal = None

	def reset(self):
		self.location = Vector((0, 0, 0))
		self.normal = None


#TODO correct gride directin with piced face longest edge
class Gride:
	def __init__(self):
		# First click location on view 3D
		self.location = Vector((0, 0, 0))
		# Gride rotation
		self.rotation = Vector((0, 0, 0)) # Gride rotaion
		# Floor oriantation
		self.floor_rotation = Vector((0, 0, 0))
		# Size of gride for graphic drawing
		self.size = 1
		# Click detector virtual mesh (Face) on surface
		self.gride_face = self.get_defualt_face()
		# Click detector virtual mesh (Face) on floore
		self.floor_face = self.get_defualt_face()
		# World Transform matrix
		self.gride_matrix = None
		self.floor_matrix = None
	
	def get_defualt_face(self):
		return (
				Vector((-self.size, -self.size, 0)),
				Vector((self.size, -self.size, 0)),
				Vector((self.size, self.size, 0)),
				Vector((-self.size, self.size, 0))
		)

	def reset(self):
		self.location = Vector((0, 0, 0))
		self.rotation = Vector((0, 0, 0))
		self.floor_rotation = Vector((0, 0, 0))
		self.gride_face = self.get_defualt_face()
		self.floor_face = self.get_defualt_face()
	
	def update(self):
		# calculate matrix and meshes
		self.gride_matrix = matrix_from_elements(self.location, self.rotation, Vector((1,1,1)))
		self.floor_matrix = matrix_from_elements(Vector((0,0,0)), self.floor_rotation, Vector((1,1,1)))
		self.gride_face = transform_point_to_matrix(self.get_defualt_face(), self.gride_matrix)
		self.floor_face = transform_point_to_matrix(self.get_defualt_face(), self.floor_matrix)

	def get_normal_direction(self, normal):
		if normal:
			direction = normal.normalized()
			matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
			self.rotation = matrix.to_euler()
			self.rotation.y += pi/2
		else:
			self.rotation = Euler((0, 0, 0), 'XYZ')

	def get_vector_direction(self, start, end, normal):
		if start and end and normal:
			direction = (end - start).normalized()
			matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
			return matrix.to_euler()
		return Euler((0, 0, 0), 'XYZ') #TODO

	def get_click_point_gride(self, ctx, x, y):
		return get_click_point_on_face(ctx, self.gride_face, x, y)
	
	def get_click_point_surface(self, ctx, x, y):
		point, _, _, _ = ray_cast(ctx, x, y)
		if point:
			return point
		# Hit floor if surface missed
		return get_click_point_on_face(ctx, self.gride_face, x, y)
	
	def get_coordinate_view(self, ctx, x, y):
		region = ctx.region
		region_3d = ctx.space_data.region_3d
		location = ctx.scene.cursor.location

		click_location = region_2d_to_location_3d(region, region_3d, (x, y ), location)
		view_rotation =	region_3d.view_matrix.inverted().to_euler()

		return click_location, view_rotation

	def get_coordinate_surface(self, ctx, x, y):
		start, normal, _, _ = ray_cast(ctx, x, y)
		end, _, _, _ = ray_cast(ctx, x+1, y)
		if normal:
			rotation = self.get_vector_direction(start, end, normal)
			location = start if start else Vector((0, 0, 0))
			return location, rotation
		return None, None
	
	def get_coordinate(self, ctx, x, y):
		""" call once at first click to ganarate virtual gride """
		draw_mode = ctx.scene.primitive_setting.draw_mode
		view_orient, _ = get_view_orientation(ctx)

		if draw_mode == 'VIEW':
			location, rotation = self.get_coordinate_view(ctx, x, y)
			self.location = location
			self.rotation = rotation
			self.floor_rotation = rotation.copy()
		
		elif draw_mode == 'SURFACE':
			if view_orient == 'USER':
				self.location = get_click_point_on_face(ctx, self.floor_face, x, y)
				self.rotation = Vector((0, 0, 0))
				self.floor_rotation = Vector((0, 0, 0))
			else:
				location, rotation = self.get_coordinate_view(ctx, x, y)
				self.location = location
				self.rotation = rotation
				self.floor_rotation = rotation.copy()

			surf_location, surf_rotation = self.get_coordinate_surface(ctx, x, y)

			if surf_location and surf_rotation:
				self.location = surf_location
				self.rotation = surf_rotation
			else:
				if view_orient == 'USER':
					self.location = get_click_point_on_face(ctx, self.floor_face, x, y)
					self.rotation = Vector((0, 0, 0))
					self.floor_rotation = Vector((0, 0, 0))
				else:
					location, rotation = self.get_coordinate_view(ctx, x, y)
					self.location = location
					self.rotation = rotation
					self.floor_rotation = rotation.copy()
			
		else: # draw_mode == 'FLOOR':
			if view_orient == 'USER':
				self.location = get_click_point_on_face(ctx, self.floor_face, x, y)
				self.rotation = Vector((0, 0, 0))
				self.floor_rotation = Vector((0, 0, 0))
			else:
				location, rotation = self.get_coordinate_view(ctx, x, y)
				self.location = location
				self.rotation = rotation
				self.floor_rotation = rotation.copy()
	
		self.update()		