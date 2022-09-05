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

# import bpy#, mathutils
from mathutils import Vector, geometry
from math import pi
from bpy_extras.view3d_utils import (region_2d_to_location_3d,
									region_2d_to_vector_3d,
									region_2d_to_origin_3d)



def get_view_orientation(ctx):
	r = lambda x: round(x, 2)
	
	orientation_dict = {(0, 0, 0):'TOP', (r(pi), 0, 0):'BOTTOM',
				(r(-pi/2), 0, 0):'FRONT', (r(pi/2), 0, r(-pi)):'BACK',
				(r(-pi/2), r(pi/2), 0):'LEFT', (r(-pi/2), r(-pi/2), 0):'RIGHT'}
	
	r3d = ctx.area.spaces.active.region_3d
	view_rot = r3d.view_matrix.to_euler()
	
	view_orientation = orientation_dict.get(tuple(map(r, view_rot)), 'USER')
	view_type = r3d.view_perspective
	
	return view_orientation, view_type



def get_triface_from_orient(gride, click_point):
	orient = click_point.view_orient
	x, y, z, = gride.location if gride else Vector((0, 0, 0))
	
	if orient in {'FRONT','BACK'}:
		return ((0, y, 0), (1, y, 0), (0, y, 1))
	
	elif orient in {'LEFT','RIGHT'}:
		return ((x, 0, 0), (x, 1, 0), (x, 0, 1))
	
	else:
		return ((0, 0, z), (0, 1, z), (1, 0, z))



def switch_axis_by_orient(orient, point):
	x, y, z = point
	# Top bottom are same as Prespective then can be ignored
	if orient in ['FRONT', 'BACK']:
		return Vector((x, z, y))
	
	elif orient in ['LEFT', 'RIGHT']:
		return Vector((y, z, x))
	
	else:
		return Vector((x, y, z))



def visible_objects_and_duplis(ctx):
	""" Loop over (object, matrix) pairs (mesh only) """

	depsgraph = ctx.evaluated_depsgraph_get()
	for dup in depsgraph.object_instances:
		if dup.is_instance:  # Real dupli instance
			obj = dup.instance_object
			yield (obj, dup.matrix_world.copy())
		else:  # Usual object
			obj = dup.object
			yield (obj, obj.matrix_world.copy())



def obj_ray_cast(obj, matrix, ray_origin, ray_target):
	""" Wrapper for ray casting that moves the ray into object space """

	# get the ray relative to the object
	matrix_inv = matrix.inverted()
	ray_origin_obj = matrix_inv @ ray_origin
	ray_target_obj = matrix_inv @ ray_target
	ray_direction_obj = ray_target_obj - ray_origin_obj

	# cast the ray
	success, location, normal, face = obj.ray_cast(ray_origin_obj, ray_direction_obj)

	if success:
		return location, normal, face
	else:
		return None, None, None



def ray_cast(ctx, mouse_x, mouse_y):
	""" Shoots a ray from the cursor position into the scene and returns the closest intersection

	Args:
		mouse_x (float): x position of the cursor in pixels
		mouse_y (float): y position of the cursor in pixels

	Returns:
		(Vector, Vector, int, bpy.types.Object): A tuple containing the position, normal,
												 face id and object of the closest intersection
	"""
	region = ctx.region
	region_data = ctx.space_data.region_3d

	view_vector = region_2d_to_vector_3d(region, region_data, (mouse_x, mouse_y))
	ray_origin = region_2d_to_origin_3d(region, region_data, (mouse_x, mouse_y))

	ray_target = ray_origin + view_vector

	best_length_squared = -1.0
	closest_loc = None
	closest_normal = None
	closest_obj = None
	closest_face = None

	for obj, matrix in visible_objects_and_duplis(ctx):
		if obj.type == 'MESH':
			hit, normal, face = obj_ray_cast(obj, matrix, ray_origin, ray_target)
			if hit is not None:
				_, rot, _ = matrix.decompose()
				hit_world = matrix @ hit
				normal_world = rot.to_matrix() @ normal
				length_squared = (hit_world - ray_origin).length_squared
				if closest_loc is None or length_squared < best_length_squared:
					best_length_squared = length_squared
					closest_loc = hit_world
					closest_normal = normal_world
					closest_face = face
					closest_obj = obj

	return closest_loc, closest_normal, closest_face, closest_obj


def get_click_point_on_face(ctx, face, x, y):
	region = ctx.region
	region_data = ctx.space_data.region_3d
	_, view_type = get_view_orientation(ctx)
	
	if view_type in {'PERSP', 'CAMERA'}:
		region = ctx.region
		region_data = ctx.space_data.region_3d
		view_matrix = region_data.view_matrix.inverted()
		ray_start = view_matrix.to_translation()
		ray_depth = view_matrix @ Vector((0, 0, -1000000))
		ray_end = region_2d_to_location_3d(region, region_data, (x, y), ray_depth)
	
		click_point = geometry.intersect_ray_tri(face[0], face[1], face[2],
											ray_end, ray_start, False)
		if click_point:
			return click_point
		
		#TODO
		# z = ctx.area.spaces.active.region_3d.view_matrix.to_translation().z
		# print(ctx.area.spaces.active.region_3d.view_matrix.to_translation())
		# print(">Z>", z)
		# face[0].z, face[1].z, face[2].z = z, z, z

		# print(">>>",face[0], face[1], face[2])

		# click_point = geometry.intersect_ray_tri(face[0], face[1], face[2],
		# 									ray_end, ray_start, False)
		# print(">>CP>>",click_point)
		return Vector((0, 0, 0))

	return region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))