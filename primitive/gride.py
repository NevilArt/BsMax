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

import numpy
from mathutils import Vector, geometry, Matrix, Euler
from math import pi, sin, cos, sqrt
from bpy_extras.view3d_utils import region_2d_to_location_3d

from bsmax.math import matrix_from_elements, to_local_matrix, transform_points_to_matrix
from bsmax.mouse import ray_cast, get_click_point_on_face



def get_view_orientation(ctx):
	""" return = (str, str) (view_orientation, view_type) """
	r = lambda x: round(x, 2)

	orientation_dict = {
		(0, 0, 0):'TOP',
		(r(pi), 0, 0):'BOTTOM',
		(r(-pi/2), 0, 0):'FRONT',
		(r(pi/2), 0, r(-pi)):'BACK',
		(r(-pi/2), r(pi/2), 0):'LEFT',
		(r(-pi/2), r(-pi/2), 0):'RIGHT'}
	
	r3d = ctx.area.spaces.active.region_3d
	view_rot = r3d.view_matrix.to_euler()
	
	view_orientation = orientation_dict.get(tuple(map(r, view_rot)), 'USER')
	view_type = r3d.view_perspective
	
	return view_orientation, view_type



def get_rotation_of_view_orient(view_orient):
		if view_orient == 'TOP':
			return Vector((0, 0, 0))
		if view_orient == 'BOTTOM':
			return Vector((pi, 0, 0))
		if view_orient == 'FRONT':
			return Vector((pi/2, 0, 0))
		if view_orient == 'BACK':
			return Vector((-pi/2, pi, 0))
		if view_orient == 'LEFT':
			return Vector((pi/2, 0, -pi/2))
		if view_orient == 'RIGHT':
			return Vector((pi/2, 0, pi/2))
		return Vector((0, 0, 0))



def transfer_points_to(points ,location, direction):
	xa, ya, za = direction
	rx = numpy.matrix([[1, 0, 0], [0, cos(xa),-sin(xa)], [0, sin(xa), cos(xa)]])
	ry = numpy.matrix([[cos(ya), 0, sin(ya)], [0, 1, 0], [-sin(ya), 0, cos(ya)]])
	rz = numpy.matrix([[cos(za), -sin(za), 0], [sin(za), cos(za) ,0], [0, 0, 1]])
	tr = rx * ry * rz

	for i in range(len(points)):
		px, py, pz = points[i]
		points[i].x = px*tr.item(0) + py*tr.item(1) + pz*tr.item(2) + location.x
		points[i].y = px*tr.item(3) + py*tr.item(4) + pz*tr.item(5) + location.y
		points[i].z = px*tr.item(6) + py*tr.item(7) + pz*tr.item(2) + location.z

	return points
	


def get_click_point_on_face(ctx, face, x, y):
	region = ctx.region
	region_data = ctx.space_data.region_3d
	_, view_type = get_view_orientation(ctx)
	if view_type in {'PERSP', 'CAMERA'}:
		region = ctx.region
		region_data = ctx.space_data.region_3d
		view_matrix = region_data.view_matrix.inverted()
		ray_start = view_matrix.to_translation()
		ray_depth = view_matrix @ Vector((0, 0, -1000000)) #TODO from view
		ray_end = region_2d_to_location_3d(region, region_data, (x, y), ray_depth)
		return geometry.intersect_ray_tri(face[0], face[1], face[2], ray_end, ray_start, False)
	return region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))



class Dimantion:
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
		sx, sy, sz = to_local_matrix(self.start, self.gride.gride_matrix)
		ex, ey, ez = to_local_matrix(self.end, self.gride.gride_matrix)

		# get dimantion from matrix
		self.width = abs(ex-sx)
		self.length = abs(ey-sy)
		self.height = self.radius

		self.local = Vector((ex, ey, ez))
	
		# Get Center in world matrix
		# cx = (self.start.x + self.end.x) / 2
		# cy = (self.start.y + self.end.y) / 2
		# cz = 0#(self.start.z + self.end.z) / 2
		self.center.x = (self.start.x + self.end.x) / 2
		self.center.y = (self.start.y + self.end.y) / 2
		self.center.z = (self.start.z + self.end.z) / 2
		# self.center = to_local_matrix(Vector((cx, cy, cz)), self.gride.gride_matrix)



class Click_Point:
	def __init__(self):
		self.location = Vector((0, 0, 0))
		self.normal = None

	def reset(self):
		self.location = Vector((0, 0, 0))
		self.normal = None


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
		return (Vector((-self.size, -self.size, 0)), Vector((self.size, -self.size, 0)),
			Vector((self.size, self.size, 0)), Vector((-self.size, self.size, 0)))
	
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
		self.gride_face = transform_points_to_matrix(self.get_defualt_face(), self.gride_matrix)
		self.floor_face = transform_points_to_matrix(self.get_defualt_face(), self.floor_matrix)

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
				self.rotation = Vector((0,0,0))
				self.floor_rotation = Vector((0,0,0))
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
					self.rotation = Vector((0,0,0))
					self.floor_rotation = Vector((0,0,0))
				else:
					location, rotation = self.get_coordinate_view(ctx, x, y)
					self.location = location
					self.rotation = rotation
					self.floor_rotation = rotation.copy()
			
		else: # draw_mode == 'FLOOR':
			if view_orient == 'USER':
				self.location = get_click_point_on_face(ctx, self.floor_face, x, y)
				self.rotation = Vector((0,0,0))
				self.floor_rotation = Vector((0,0,0))
			else:
				location, rotation = self.get_coordinate_view(ctx, x, y)
				self.location = location
				self.rotation = rotation
				self.floor_rotation = rotation.copy()
	
		self.update()		