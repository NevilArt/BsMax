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
# 2024/04/21

from mathutils import Vector, Matrix, Euler
from math import pi, sqrt

from bpy_extras.view3d_utils import region_2d_to_location_3d

from bsmax.state import get_view_orientation
from bsmax.mouse import ray_cast, get_click_point_on_face

from bsmax.bsmatrix import (
	matrix_from_elements, transform_point_to_matrix, points_to_local_matrix
)


def dimension_calculate(cls):
	# radiue distance of start and end point
	x = cls.end.x - cls.start.x
	y = cls.end.y - cls.start.y
	z = cls.end.z - cls.start.z
	cls.radius = sqrt(x**2 + y**2 + z**2)
	
	# distance of gride and end point
	x = cls.end.x - cls.gride.location.x
	y = cls.end.y - cls.gride.location.y
	z = cls.end.z - cls.gride.location.z
	cls.distance = sqrt(x**2 + y**2 + z**2)
	
	# convert to local matrix
	sx, sy, _ = points_to_local_matrix(cls.start, cls.gride.gride_matrix)
	ex, ey, ez = points_to_local_matrix(cls.end, cls.gride.gride_matrix)

	# get dimension from matrix
	# self.width = abs(ex-sx)
	# self.length = abs(ey-sy)
	cls.width = ex-sx
	cls.length = ey-sy
	cls.height = cls.radius

	cls.local = Vector((ex, ey, ez))

	# Get Center in world matrix
	cls.center.x = (cls.start.x + cls.end.x) / 2
	cls.center.y = (cls.start.y + cls.end.y) / 2
	cls.center.z = (cls.start.z + cls.end.z) / 2


def gride_get_defualt_face(cls):
	return (
		Vector((-cls.size, -cls.size, 0)),
		Vector((cls.size, -cls.size, 0)),
		Vector((cls.size, cls.size, 0)),
		Vector((-cls.size, cls.size, 0))
	)


def gride_update(cls):
	# calculate matrix and meshes
	cls.gride_matrix = matrix_from_elements(
		cls.location, cls.rotation, Vector((1,1,1))
	)
	
	cls.floor_matrix = matrix_from_elements(
		Vector((0,0,0)), cls.floor_rotation, Vector((1,1,1))
	)
	
	cls.gride_face = transform_point_to_matrix(
		gride_get_defualt_face(cls), cls.gride_matrix
	)
	
	cls.floor_face = transform_point_to_matrix(
		gride_get_defualt_face(cls), cls.floor_matrix
	)


def gride_get_normal_direction(cls, normal):
	if normal:
		direction = normal.normalized()

		matrix = Matrix(
			[direction, -direction.cross(normal), normal]
		).transposed()

		cls.rotation = matrix.to_euler()
		cls.rotation.y += pi/2
	
	else:
		cls.rotation = Euler((0, 0, 0), 'XYZ')


def gride_get_vector_direction(start, end, normal):
	if start and end and normal:
		direction = (end - start).normalized()

		matrix = Matrix(
			[direction, -direction.cross(normal), normal]
		).transposed()

		return matrix.to_euler()

	return Euler((0, 0, 0), 'XYZ') #TODO


def get_coordinate_view(ctx, x, y):
	region = ctx.region
	region_3d = ctx.space_data.region_3d
	location = ctx.scene.cursor.location

	click_location = region_2d_to_location_3d(
		region, region_3d, (x, y ), location
	)

	view_rotation =	region_3d.view_matrix.inverted().to_euler()

	return click_location, view_rotation


def gride_get_coordinate_surface(ctx, x, y):
	start, normal, _, _ = ray_cast(ctx, x, y)
	end, _, _, _ = ray_cast(ctx, x+1, y)
	if normal:
		rotation = gride_get_vector_direction(start, end, normal)
		location = start if start else Vector((0, 0, 0))
		return location, rotation

	return None, None

def gride_get_coordinate(cls, ctx, x, y):
	""" call once at first click to ganarate virtual gride """
	draw_mode = ctx.scene.primitive_setting.draw_mode
	view_orient, _ = get_view_orientation(ctx)

	if draw_mode == 'VIEW':
		location, rotation = get_coordinate_view(ctx, x, y)
		cls.location = location
		cls.rotation = rotation
		cls.floor_rotation = rotation.copy()
	
	elif draw_mode == 'SURFACE':
		if view_orient == 'USER':
			cls.location = get_click_point_on_face(
				ctx, cls.floor_face, x, y
			)

			cls.rotation = Vector((0, 0, 0))
			cls.floor_rotation = Vector((0, 0, 0))

		else:
			location, rotation = get_coordinate_view(ctx, x, y)
			cls.location = location
			cls.rotation = rotation
			cls.floor_rotation = rotation.copy()

		surfaceCordinate = gride_get_coordinate_surface(ctx, x, y)
		surf_location, surf_rotation = surfaceCordinate

		if surf_location and surf_rotation:
			cls.location = surf_location
			cls.rotation = surf_rotation
		else:
			if view_orient == 'USER':
				cls.location = get_click_point_on_face(
					ctx, cls.floor_face, x, y
				)

				cls.rotation = Vector((0, 0, 0))
				cls.floor_rotation = Vector((0, 0, 0))
			else:
				location, rotation = get_coordinate_view(ctx, x, y)
				cls.location = location
				cls.rotation = rotation
				cls.floor_rotation = rotation.copy()
		
	else: # draw_mode == 'FLOOR':
		if view_orient == 'USER':
			cls.location = get_click_point_on_face(
				ctx, cls.floor_face, x, y
			)

			cls.rotation = Vector((0, 0, 0))
			cls.floor_rotation = Vector((0, 0, 0))

		else:
			location, rotation = get_coordinate_view(ctx, x, y)
			cls.location = location
			cls.rotation = rotation
			cls.floor_rotation = rotation.copy()

	gride_update(cls)	


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
		dimension_calculate(self)
	
	# def calculate(self):
	# 	dimension_calculate(self)


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
		self.location = Vector((0, 0, 0)) # First click location on view 3D
		self.rotation = Vector((0, 0, 0)) # Gride rotaion
		self.floor_rotation = Vector((0, 0, 0)) # Floor oriantation
		self.size = 1 # Size of gride for graphic drawing
		# Click detector virtual mesh (Face) on surface
		self.gride_face = gride_get_defualt_face(self)
		# Click detector virtual mesh (Face) on floore
		self.floor_face = gride_get_defualt_face(self)
		# World Transform matrix
		self.gride_matrix = None
		self.floor_matrix = None

	def reset(self):
		self.location = Vector((0, 0, 0))
		self.rotation = Vector((0, 0, 0))
		self.floor_rotation = Vector((0, 0, 0))
		self.gride_face = gride_get_defualt_face(self)
		self.floor_face = gride_get_defualt_face(self)
	
	def update(self):
		gride_update(self)

	def get_click_point_gride(self, ctx, x, y):
		return get_click_point_on_face(ctx, self.gride_face, x, y)

	def get_click_point_surface(self, ctx, x, y):
		point, _, _, _ = ray_cast(ctx, x, y)

		if point:
			return point

		# Hit floor if surface missed
		return get_click_point_on_face(ctx, self.gride_face, x, y)

	def get_coordinate(self, ctx, x, y):
		gride_get_coordinate(self, ctx, x, y)