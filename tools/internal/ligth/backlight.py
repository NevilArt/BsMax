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
import math

from bpy.types import Operator
from bpy.props import EnumProperty
from bpy.utils import register_class, unregister_class


from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


def _get_object_world_center(obj):
	"""World-space bounding box center — more reliable than obj.location
	(handles offset origins, armatures, etc.)"""
	bbox_world = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
	center = sum(bbox_world, Vector()) / 8
	return center


def _is_in_camera_frustum(camera, world_point, scene=None):
	scene = scene or bpy.context.scene
	co_ndc = world_to_camera_view(scene, camera, world_point)
	# x,y in [0,1] = inside frame; z > 0 = in front of camera (not behind it)
	return 0.0 <= co_ndc.x <= 1.0 and 0.0 <= co_ndc.y <= 1.0 and co_ndc.z > 0


def _is_light_visible_from_character(light, character_location, scene=None, max_distance=1000.0):
	"""
	Raycasts from the character toward the light to check for occlusion
	(e.g. a closed door blocking moonlight, a wall blocking a point light).

	light               : bpy.types.Object (the light being tested)
	character_location  : Vector, world-space character position
	scene                : bpy.types.Scene (defaults to current scene)
	max_distance         : ray length for SUN lights (which have no real
							position, only direction)

	Returns: bool — True if the light can currently reach the character
				unobstructed, False if blocked.
	"""
	scene = scene or bpy.context.scene
	depsgraph = bpy.context.evaluated_depsgraph_get()

	if light.data.type == 'SUN':
		# sun light travels along its local -Z axis (Blender convention);
		# incoming light arrives from the opposite direction
		sun_direction = (light.matrix_world.to_quaternion() @ Vector((0, 0, -1))).normalized()
		ray_direction = -sun_direction
		ray_origin = character_location + ray_direction * 0.01  # nudge off surface
		result, loc, normal, index, obj, matrix = scene.ray_cast(
			depsgraph, ray_origin, ray_direction, distance=max_distance
		)
		return not result  # blocked if ray hits something before escaping

	else:
		light_loc = light.matrix_world.translation
		to_light = light_loc - character_location
		dist = to_light.length
		if dist == 0:
			return True
		ray_direction = to_light.normalized()
		ray_origin = character_location + ray_direction * 0.01

		result, loc, normal, index, obj, matrix = scene.ray_cast(
			depsgraph, ray_origin, ray_direction, distance=dist - 0.02
		)
		return not result  # blocked if something's between character and light


def get_backlight_candidates(
	camera,
	target_obj,
	lights,
	min_behind_margin=0.0,
	exclude_names=("Backlight-Main",),
	check_occlusion=True,
	scene=None,
):

	scene = scene or bpy.context.scene
	cam_loc = camera.matrix_world.translation
	obj_center = _get_object_world_center(target_obj)

	view_vec = obj_center - cam_loc
	obj_dist = view_vec.length
	if obj_dist == 0:
		return []
	view_axis = view_vec.normalized()

	candidates = []
	for light in lights:
		if light.name in exclude_names:
			continue

		light_loc = light.matrix_world.translation
		to_light = light_loc - cam_loc
		proj = to_light.dot(view_axis)

		if proj < 0:
			continue
		if proj < obj_dist + min_behind_margin:
			continue

		# TODO do not work
		# if check_occlusion and not _is_light_visible_from_character(light, obj_center, scene):
		# 	continue  # e.g. moonlight blocked by a closed door

		lateral_vec = to_light - view_axis * proj
		lateral_offset = lateral_vec.length

		candidates.append({
			"light": light,
			"depth_behind_object": proj - obj_dist,
			"lateral_offset": lateral_offset,
			"in_camera_frustum": _is_in_camera_frustum(camera, light_loc),
		})

	return candidates


def get_or_create_main_backlight():
	"""
	Returns the scene's single dedicated backlight object, named
	'Backlight-Main'. If it already exists (as a light object), reuse it.
	Otherwise create a new AREA light with that name and sensible defaults,
	link it to the scene's active collection, and return it.

	scene      : bpy.types.Scene (defaults to current scene)
	light_name : name to search for / assign
	energy     : Watts, only applied when creating a new light
	size       : area light size (meters), only applied when creating
	color      : RGB tuple, only applied when creating

	Returns: bpy.types.Object (the light object)
	"""

	scene = bpy.context.scene
	light_name="Backlight-Main"

	# 1. Look for an existing object with this name that is actually a light
	existing = bpy.data.objects.get(light_name)
	
	if existing is not None and existing.type == 'LIGHT':
		# make sure it's linked into the current scene's collection tree
		if existing.name not in scene.collection.all_objects:
			scene.collection.objects.link(existing)
		return existing

	# if the name exists but isn't a light (name collision), don't clobber it
	if existing is not None and existing.type != 'LIGHT':
		raise ValueError(
			f"Object '{light_name}' already exists but is not a LIGHT "
			f"(it's a {existing.type}). Rename or remove it first."
		)

	# 2. Create new light datablock + object
	light_data = bpy.data.lights.new(name=light_name, type='AREA')
	light_data.energy = 1000.0
	light_data.size = 1.0
	light_data.color = (1.0, 1.0, 1.0)

	light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
	scene.collection.objects.link(light_obj)

	return light_obj


def _compute_candidate_weights(candidate_lights, character_location, epsilon=0.01):
	raw_weights = []
	for c in candidate_lights:
		light = c["light"]
		if light.data.type == 'SUN':
			weight = light.data.energy
		else:
			light_loc = light.matrix_world.translation
			dist = max((light_loc - character_location).length, epsilon)
			weight = light.data.energy / (dist ** 2)
		raw_weights.append(weight)

	total = sum(raw_weights)
	if total <= 0:
		return [0.0] * len(candidate_lights)

	return [w / total for w in raw_weights]


def get_virtual_backlight_source(candidate_lights, character_location, epsilon=0.01, default_distance=5.0):
	"""
	Consolidates all candidate backlight sources into a single virtual
	light description: one position, direction, color, and power that
	represents their combined lighting effect on the character.

	candidate_lights   : list of candidate dicts from get_backlight_candidates()
	character_location : Vector, world-space character position
	epsilon             : min distance clamp (avoid div-by-zero)
	default_distance    : fallback distance if no candidates have a real
							position-based distance (e.g. sun-only scene)

	Returns: dict {
		"position": Vector,       # world-space placement for the virtual light
		"direction": Vector,      # unit vector, character -> source
		"distance": float,
		"color": (r, g, b),       # normalized, max channel = 1.0
		"power": float,           # equivalent energy at 'distance'
		"weights": list[float],   # per-candidate influence, same order as input
	} or None if candidate_lights is empty / all zero-weight.
	"""
	if not candidate_lights:
		return None

	weights = _compute_candidate_weights(candidate_lights, character_location, epsilon)
	if sum(weights) <= 0:
		return None

	direction_sum = Vector((0.0, 0.0, 0.0))
	color_sum = Vector((0.0, 0.0, 0.0))
	total_irradiance = 0.0
	weighted_distance_sum = 0.0
	distance_weight_total = 0.0

	for c, w in zip(candidate_lights, weights):
		if w <= 0:
			continue

		light = c["light"]

		if light.data.type == 'SUN':
			light_forward = (light.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))).normalized()
			incoming_dir = -light_forward
			dist = None
			irradiance = light.data.energy
		else:
			light_loc = light.matrix_world.translation
			to_light = light_loc - character_location
			dist = max(to_light.length, epsilon)
			incoming_dir = to_light.normalized()
			irradiance = light.data.energy / (dist ** 2)

		direction_sum += incoming_dir * w
		color_sum += Vector(light.data.color[:3]) * w
		total_irradiance += irradiance

		if dist is not None:
			weighted_distance_sum += dist * w
			distance_weight_total += w

	if direction_sum.length == 0:
		return None
	direction = direction_sum.normalized()

	distance = (weighted_distance_sum / distance_weight_total) if distance_weight_total > 0 else default_distance

	max_channel = max(color_sum)
	normalized_color = tuple(color_sum / max_channel) if max_channel > 0 else (1.0, 1.0, 1.0)

	power = total_irradiance * (distance ** 2)  # equivalent energy to preserve irradiance at 'distance'

	position = character_location + direction * distance

	return {
		"position": position,
		"direction": direction,
		"distance": distance,
		"color": normalized_color,
		"power": power,
		"weights": weights,
	}


import math


def _set_backlight_position(backlight, camera, virtual_source, character_location, max_angle_deg=45.0):
	"""
	Positions Backlight-Main based on the virtual consolidated light source,
	clamped to the +/-45 deg cone around the camera->character back-axis.

	- If virtual source direction is within 45 deg of the back-axis (B zone):
		use that direction as-is.
	- If beyond 45 deg (L/R zone): clamp direction to exactly 45 deg,
		on the same side, never rotating further out.
	- Distance is always half the virtual source's distance from character.

	backlight          : bpy.types.Object (Backlight-Main)
	camera              : bpy.types.Object (active camera)
	virtual_source      : dict from get_virtual_backlight_source()
	character_location  : Vector, world-space character position
	max_angle_deg        : clamp angle (default 45)

	Returns: Vector, the position that was applied to backlight.location
	"""
	cam_loc = camera.matrix_world.translation

	# back-axis: direction from camera through character, extended beyond
	back_axis = (character_location - cam_loc)
	if back_axis.length == 0:
		return backlight.location  # degenerate, camera at character - bail
	back_axis.normalize()

	source_dir = virtual_source["direction"]
	source_dist = virtual_source["distance"]
	target_dist = source_dist / 2.0

	# angle between source direction and back-axis
	dot = max(-1.0, min(1.0, back_axis.dot(source_dir)))
	angle = math.degrees(math.acos(dot))

	max_angle_rad = math.radians(max_angle_deg)

	if angle <= max_angle_deg:
		# B zone - use direction as-is
		final_dir = source_dir
	else:
		# L/R zone - clamp to exactly max_angle_deg, same side/plane
		# perpendicular component of source_dir relative to back_axis
		perp = source_dir - back_axis * dot
		if perp.length == 0:
			# source_dir is exactly opposite/degenerate - pick any perpendicular
			perp = back_axis.cross(Vector((0, 0, 1)))
			if perp.length == 0:
				perp = back_axis.cross(Vector((0, 1, 0)))
		perp.normalize()

		final_dir = (back_axis * math.cos(max_angle_rad)) + (perp * math.sin(max_angle_rad))
		final_dir.normalize()

	position = character_location + final_dir * target_dist
	backlight.location = position

	return position

def set_backlight(backlight, camera, candidate_lights, character_location):
	"""
	Configures the managed 'Backlight-Main' light using scene data:
	position, angle (rotation), color, and power — derived from the
	candidate backlight sources and the character's location.

	backlight        : bpy.types.Object (the light returned by
						get_or_create_main_backlight)
	candidate_lights  : list of candidate dicts, as returned by
						get_backlight_candidates()
	character_location: Vector, world-space position of the character
						(e.g. from _get_object_world_center(target_obj))

	Returns: the same backlight object, updated in place.
	"""

	if not candidate_lights:
		return

	virtual_source = get_virtual_backlight_source(
		backlight_candidates, character_location, epsilon=0.01, default_distance=5.0)

	# --- Step 1: Position ---------------------------------------------
	# TODO: calculate world-space position for backlight
	_set_backlight_position(backlight, camera, [virtual_source], character_location)

	# --- Step 2: Angle / Rotation ---------------------------------------
	# TODO: calculate rotation so the light aims correctly at the character
	# _set_backlight_angle(backlight, camera, candidate_lights, character_location)

	# --- Step 3: Color ---------------------------------------------------
	# TODO: derive color from candidate lights (average / dominant / etc.)
	# _set_backlight_color(backlight, camera, candidate_lights, character_location)

	# --- Step 4: Power / Energy ------------------------------------------
	# TODO: derive intensity from candidate lights and/or distance falloff
	# _set_backlight_power(backlight, camera, candidate_lights, character_location)

	return backlight


classes = {}


def register_backlight():
	for cls in classes:
		register_class(cls)


def unregister_backlight():
	for cls in classes:
		unregister_class(cls)

if __name__ == "__main__":
	register_backlight()
	camera = bpy.context.scene.camera
	target_obj = bpy.context.active_object
	character_location = _get_object_world_center(target_obj)
	lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']
	backlight_candidates = get_backlight_candidates(camera, target_obj, lights, min_behind_margin=0.0)
	backlight = get_or_create_main_backlight()
	for candidate in backlight_candidates:
		light = candidate["light"]
		depth_behind_object = candidate["depth_behind_object"]
		lateral_offset = candidate["lateral_offset"]
		in_camera_frustum = candidate["in_camera_frustum"]
		print(f"Candidate: {light.name}, Depth: {depth_behind_object:.2f}, Lateral Offset: {lateral_offset:.2f}, In Frustum: {in_camera_frustum}")
	
	set_backlight(backlight, camera, backlight_candidates, target_obj.location)

	