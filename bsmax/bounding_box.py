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
# 2024/05/05

from mathutils import Vector
from math import pi, cos, sin


def get_bound_from_points(cls, points):
	if not points:
		cls.min = Vector((0, 0, 0))
		cls.max = Vector((0, 0, 0))
		cls.center = Vector((0, 0, 0))
		return
	
	cls.min = points[0].copy()
	cls.max = points[0].copy()

	for co in points:
		cls.min.x = min(cls.min.x, co.x)
		cls.max.x = max(cls.max.x, co.x)
		cls.min.y = min(cls.min.y, co.y)
		cls.max.y = max(cls.max.y, co.y)
		cls.min.z = min(cls.min.z, co.z)
		cls.max.z = max(cls.max.z, co.z)
	
	# Calculate Center
	cls.center.x = (cls.min.x + cls.max.x) / 2
	cls.center.y = (cls.min.y + cls.max.y) / 2
	cls.center.z = (cls.min.z + cls.max.z) / 2


def create_sphere_points(radius, segments):
	points = []

	for i in range(segments + 1):
		theta = i * pi / segments
		sin_theta = sin(theta)
		cos_theta = cos(theta)
		
		for j in range(segments + 1):
			phi = j * 2 * pi / segments
			sin_phi = sin(phi)
			cos_phi = cos(phi)

			x_vertex = radius * sin_theta * cos_phi
			y_vertex = radius * sin_theta * sin_phi
			z_vertex = radius * cos_theta

			points.append(Vector((x_vertex, y_vertex, z_vertex)))

	return points


def create_ellipse_points(radius_x, radius_y, segments):
	points = []
	for i in range(segments):
		angle = 2 * pi * i / segments
		x = radius_x * cos(angle)
		y = radius_y * sin(angle)
		points.append(Vector((x, y, 0)))

	return points


def create_sphere_slice_points(radius, theta, segments):
	points = []
	
	sin_theta = sin(theta)
	cos_theta = cos(theta)
	z_vertex = radius * cos_theta

	for j in range(segments + 1):
		phi = j * 2 * pi / segments

		x_vertex = radius * sin_theta * cos(phi)
		y_vertex = radius * sin_theta * sin(phi)

		points.append(Vector((x_vertex, y_vertex, z_vertex)))

	return points


def get_light_points(obj):
	matrix_world = obj.matrix_world

	if obj.data.type == 'POINT':
		size = obj.data.shadow_soft_size
		return [
			matrix_world @ point
			for point in create_ellipse_points(size, size, 10)
		]

	if obj.data.type == 'SUN':
		return [matrix_world @ Vector((0, 0, 0))]

	if obj.data.type == 'SPOT':
		size = obj.data.shadow_soft_size
		points = create_ellipse_points(size, size, 10)
		points += create_sphere_slice_points(size, obj.data.spot_size, 32)
		return [matrix_world @ point for point in points]

	if obj.data.type == 'AREA':
		if obj.data.shape == 'SQUARE':
			return [
				matrix_world @ Vector((-size, -size, 0)),
				matrix_world @ Vector((size, -size, 0)),
				matrix_world @ Vector((size, size, 0)),
				matrix_world @ Vector((-size, size, 0))
			]

		if obj.data.shape == 'RECTANGLE':
			size = obj.data.size
			size_y = obj.data.size_y
			return [
				matrix_world @ Vector((-size, -size_y, 0)),
				matrix_world @ Vector((size, -size_y, 0)),
				matrix_world @ Vector((size, size_y, 0)),
				matrix_world @ Vector((-size, size_y, 0))
			]

		if obj.data.shape == 'DISK':
			size = obj.data.size
			return [
				matrix_world @ point
				for point in create_ellipse_points(size, size, 32)
			]

		if obj.data.shape == 'ELLIPSE':
			size = obj.data.size
			size_y = obj.data.size_y
			return [
				matrix_world @ point
				for point in create_ellipse_points(size, size_y, 32)
			]

	return []


def get_armature_points(obj, selection):
	matrix_world = obj.matrix_world
	# poseBones = obj.pose.bones
	poseBones = obj.data.bones
	points = []

	if selection:
		for poseBone in poseBones:
			if poseBone.bone.select:
				points.append(matrix_world @ bone.head_local)
				if not bone.children:
					points.append(matrix_world @ bone.tail_local)

	else:
		for bone in poseBones:
			points.append(matrix_world @ bone.head_local)
			if not bone.children:
				points.append(matrix_world @ bone.tail_local)

	return points


def get_curve_points(obj, selection):
	matrix_world = obj.matrix_world
	splines = obj.data.splines
	points = []

	if selection:
		for spline in splines:
			points += [
				matrix_world @ point.co
				for point in spline.bezier_points
				if point.select_control_point
			]
		return points

	for spline in splines:
		points += [
			matrix_world @ point.co for point in spline.bezier_points
		]
	return points


def get_lattice_points(obj, selection):
	matrix_world = obj.matrix_world
	points = obj.data.points

	if not selection:
		return [matrix_world @ point.co for point in points]
	return [matrix_world @ point.co for point in points if point.select]


def get_empty_points(obj):
	matrix_world = obj.matrix_world
	display_type = obj.empty_display_type
	size = obj.empty_display_size

	if display_type == 'PLAIN_AXES':
		return [
			matrix_world @ Vector((size, 0, 0)),
			matrix_world @ Vector((-size, 0, 0)),
			matrix_world @ Vector((0, size, 0)),
			matrix_world @ Vector((0, -size, 0)),
			matrix_world @ Vector((0, 0, size)),
			matrix_world @ Vector((0, 0, -size))
		]
	
	if display_type == 'ARROWS':
		return [
			matrix_world @ Vector((0, 0, 0)),
			matrix_world @ Vector((size, 0, 0)),
			matrix_world @ Vector((0, size, 0)),
			matrix_world @ Vector((0, 0, size)),
		]
	
	if display_type == 'SINGLE_ARROW':
		width = size * 0.035
		height = size * 0.75
		return [
			matrix_world @ Vector((0, 0, 0)),
			matrix_world @ Vector((0, 0, size)),
			matrix_world @ Vector((-width, -width, height)),
			matrix_world @ Vector((width, -width, height)),
			matrix_world @ Vector((width, width, height)),
			matrix_world @ Vector((-width, width, height))
		]
	
	if display_type == 'CIRCLE':
		points = []
		for i in range(100):
			angle = 2 * pi * i / 100
			x = size * cos(angle)
			z = size * sin(angle)
			points.append(matrix_world @ Vector((x, 0, z)))
		return points
	
	if display_type == 'CUBE':
		return [
			matrix_world @ Vector((-size, -size, size)),
			matrix_world @ Vector((size, -size, size)),
			matrix_world @ Vector((size, size, size)),
			matrix_world @ Vector((-size, size, size)),
			matrix_world @ Vector((-size, -size, -size)),
			matrix_world @ Vector((size, -size, -size)),
			matrix_world @ Vector((size, size, -size)),
			matrix_world @ Vector((-size, size, -size))
		]

	if display_type == 'SPHERE':
		points = []
		for i in range(100):
			angle = 2 * pi * i / 100
			a = size * cos(angle)
			b = size * sin(angle)
			points.append(matrix_world @ Vector((a, b, 0)))
			points.append(matrix_world @ Vector((a, 0, b)))
			points.append(matrix_world @ Vector((0, a, b)))
		return points

	if display_type == 'CONE':
		points = [matrix_world @ Vector((0, -size*2, 0))]
		for i in range(8):
			angle = 2 * pi * i / 8
			x = size * cos(angle)
			z = size * sin(angle)
			points.append(matrix_world @ Vector((x, 0, z)))
		return points

	elif display_type == 'IMAGE':
		#TODO
		return [
			matrix_world @ Vector((-size/2, -size/2, 0)),
			matrix_world @ Vector((size/2, -size/2, 0)),
			matrix_world @ Vector((size/2, size/2, 0)),
			matrix_world @ Vector((-size/2, size/2, 0))
		]


def get_font_points(obj):
	splines = obj.data.splines
	matrix_world = obj.matrix_world
	points = []
	for spline in splines:
		points += [
			matrix_world @ point.co for point in spline.bezier_points
		]
	return points


def get_mesh_points(obj, selection):
	matrix_world = obj.matrix_world
	vertices = obj.data.vertices

	if selection:
		return [matrix_world @ vert.co for vert in vertices if vert.select]

	return [matrix_world @ vert.co for vert in vertices]


def get_surface_points(obj):
	for spn in obj.data.splines:
		cld += [obj.matrix_world @ pts.co for pts in spn.points]


def get_points(obj, selection):
	if obj.type == 'ARMATURE':
		return get_armature_points(obj, selection)
	
	if obj.type == 'EMPTY':
		return get_empty_points(obj)
	
	if obj.type == 'FONT':
		return []
	
	if obj.type == 'CURVE':
		return get_curve_points(obj, selection)
	
	if obj.type == 'LATTICE':
		return get_lattice_points(obj, selection)
	
	if obj.type == 'LIGHT':
		return get_light_points(obj)

	if obj.type == 'MESH':
		return get_mesh_points(obj, selection)
	
	if obj.type == 'SURFACE':
		return []
	
	return []


class BoundBox():
	def __init__(self, obj):
		self.obj = obj
		self.subtargte = None
		self.min = Vector((0, 0, 0))
		self.max = Vector((0, 0, 0))
		self.center = Vector((0, 0, 0))

		if self.obj:
			self.calculate()

	def get_center(self):
		self.center.x = (self.min.x + self.max.x) / 2
		self.center.y = (self.min.y + self.max.y) / 2
		self.center.z = (self.min.z + self.max.z) / 2
	
	def calculate(self, selection=False):
		points = get_points(self.obj, selection)
		get_bound_from_points(self, points)


if __name__ == '__main__':
	pass
	# import bpy
	# from primitive.primitive import Primitive_Geometry_Class
	
	# class Mesh(Primitive_Geometry_Class):
	# 	def init(self):
	# 		self.classname = "NewMesh"

	# 	def create(self, ctx):
	# 		# verts = create_sphere_points(1, 32)
	# 		# verts = create_ellipse_points(1, 2, 32)	
	# 		verts = create_sphere_slice_points(1, pi/4, 32)
	# 		mesh = verts, [], []
	# 		self.create_mesh(ctx, mesh, self.classname)
	# 		self.update_mesh(mesh)

	# 	def update(self):
	# 		pass

	# newMesh = Mesh()
	# newMesh.create(bpy.context)