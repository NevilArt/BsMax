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
from mathutils import Matrix


def lock_transform(obj, move, rotate, scale):
	""" Lock unlock given object transform

		args:
			obj: array of objects
			move: boolean
			rotate: boolean
			scale: boolean
		return:
			None
	"""
	for i in range(3):
		obj.lock_location[i] = move
		obj.lock_rotation[i] = rotate
		obj.lock_scale[i] = scale



def modifier_add(objs, modifier, name=''):
	""" Add modifier to multible object at same time

		args:
			objs: arry of objects
			modifier: string modifier type
			name: string name of modifier default same as type
		return:
			None
	"""
	for obj in objs:
		the_name = modifier if name else name
		obj.modifiers.new(name=the_name, type=modifier)



def link_to_scene(ctx, objs):
	""" Link given obj(s) to scene and active collection

		args:
			ctx: bpy.context
			objs: array or object
		return:
			none
	"""
	activelayername = ctx.view_layer.active_layer_collection.name
	
	if activelayername in {'Master Collection', 'Scene Collection'}:
		collection = ctx.scene.collection
	else:
		collection = bpy.data.collections[activelayername]

	if isinstance(objs, list):
		for obj in objs:
			if not collection in obj.users_collection:
				collection.objects.link(obj)
	else:
		if not collection in objs.users_collection:
			collection.objects.link(objs)	



def set_as_active_object(ctx, obj):
	""" Deselect all objects and set given object as active

		args:
			ctx: bpy.context
			obj: object
		return:
			None
	"""
	if obj:
		bpy.ops.object.select_all(action = 'DESELECT')
		obj.select_set(state = True)
		ctx.view_layer.objects.active = obj



def delete_objects(objs):
	bpy.ops.object.delete({'selected_objects': objs})



def set_create_target(obj, target, distance=(0.0, 0.0, -2.0), align=True):
	""" Add a lookat constraint with basic setting """
	""" Create an empty object as target if target is None """
	constraint = obj.constraints.new('TRACK_TO')

	if target == None:
		target = bpy.data.objects.new('empty', None)
		target.empty_display_type = 'CUBE'
		target.empty_display_size = 0.25
		collection = obj.users_collection[0]
		collection.objects.link(target)
		target.name = obj.name + '_target'

	if align:
		target.location = obj.location
		target.rotation_euler = obj.rotation_euler
		target.matrix_basis @= Matrix.Translation(distance)

	constraint.target = target
	constraint.track_axis = 'TRACK_NEGATIVE_Z'
	constraint.up_axis = 'UP_Y'

	return target



def link_to(obj, target):
	obj.parent = target
	obj.matrix_parent_inverse = target.matrix_world.inverted()



def get_object_target(obj):
	return None



def set_origen(ctx, obj, location):
	scene = ctx.scene
	saved_location = scene.cursor.location.copy()
	saved_rotation = scene.cursor.rotation_euler.copy()
	scene.cursor.location = location
	bpy.ops.object.select_all(action='DESELECT')
	ctx.view_layer.objects.active = obj
	obj.select_set(state=True)
	bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
	scene.cursor.location = saved_location
	scene.cursor.rotation_euler = saved_rotation



def match_transform(ctx, obj, target):
	""" Kepp obj offset set origen fit on target in world space """
	target_location = target.matrix_world.to_translation()
	target_rotation = target.matrix_world.to_euler()
	target_scale = target.matrix_world.to_scale()
	
	# store and set the mode
	use_transform_state = ctx.scene.tool_settings.use_transform_data_origin
	ctx.scene.tool_settings.use_transform_data_origin = True

	# arrange selection
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(state=True)
	ctx.view_layer.objects.active = obj
	
	#TODO Rotation part not perfect but work for most cases
	# match the rotation axis by axis
	obj_rotation = obj.matrix_world.to_euler()
	delta_rotation_x = obj_rotation.x - target_rotation.x
	
	bpy.ops.transform.rotate(
			value=delta_rotation_x,
			orient_axis='X',
			orient_type='LOCAL',
		)

	obj_rotation = obj.matrix_world.to_euler()
	delta_rotation_y = obj_rotation.y - target_rotation.y
	
	bpy.ops.transform.rotate(
			value=delta_rotation_y,
			orient_axis='Y',
			orient_type='LOCAL',
		)

	obj_rotation = obj.matrix_world.to_euler()
	delta_rotation_z = obj_rotation.z - target_rotation.z
	bpy.ops.transform.rotate(
			value=delta_rotation_z,
			orient_axis='Z',
			orient_type='LOCAL',
		)
	
	# Match Location
	obj_location = obj.matrix_world.to_translation()
	delta_location = target_location - obj_location
	dlx, dly, dlz = delta_location
	bpy.ops.transform.translate(value=(dlx, dly, dlz), 	orient_type='GLOBAL')

	
	# Match Scale
	obj_scale = obj.matrix_world.to_scale()
	dsx = target_scale.x / obj_scale.x
	dsy = target_scale.y / obj_scale.y
	dsz = target_scale.z / obj_scale.z
	bpy.ops.transform.resize(value=(dsx, dsy, dsz))

	# Restore Transform Mode
	ctx.scene.tool_settings.use_transform_data_origin = use_transform_state



def freeze_transform(objs, location=True, rotation=True, scale=True):
	""" Add current transform to deleta transform and
		reset to 0 in given objects

		args:
			objs: array of objects
			location: boolean defoult True
			rotation: boolean defoult True
			scale: boolean defoult True
		retuen:
			None
	"""
	
	for obj in objs:
		if location:
			obj.delta_location += obj.location
			obj.location = [0, 0, 0]
		
		if rotation:
			if obj.rotation_mode == 'XYZ':
				obj.delta_rotation_euler.x += obj.rotation_euler.x
				obj.delta_rotation_euler.y += obj.rotation_euler.y
				obj.delta_rotation_euler.z += obj.rotation_euler.z
				obj.rotation_euler = [0, 0, 0]

			elif obj.rotation_mode == 'QUATERNION':
				obj.delta_rotation_quaternion.w += obj.rotation_quaternion.w
				obj.delta_rotation_quaternion.x += obj.rotation_quaternion.x
				obj.delta_rotation_quaternion.y += obj.rotation_quaternion.y
				obj.delta_rotation_quaternion.z += obj.rotation_quaternion.z

			elif obj.rotation_mode == 'AXIS_ANGLE':
				#TODO
				pass

		if scale:
			obj.delta_scale *= obj.scale
			obj.scale = [1, 1, 1]



def insert_key_to_current_state(chanel, frame, location, rotation, scale):
	# Set key for Location and Scale always is same
	if location:
		chanel.keyframe_insert(data_path='location', frame=frame)

	if scale:
		chanel.keyframe_insert(data_path='scale', frame=frame)

	# Sey key by rotation mode
	if rotation:
		if chanel.rotation_mode == 'QUATERNION':
			chanel.keyframe_insert(data_path='rotation_quaternion', frame=frame)

		elif chanel.rotation_mode == 'AXIS_ANGLE':
			chanel.keyframe_insert(data_path='rotation_axis_angle', frame=frame)

		else:
			chanel.keyframe_insert(data_path='rotation_euler', frame=frame)



def copy_array_to_clipboard(key, array):
	""" Convert given array to string lines and copy to clipboard

		args:
			key: string value detector for check on paste
			array: only 1D array with basic variables allowed
		retuen:
			No return
	"""
	string = key + "\n"

	for var in array:
		variable_type = str(type(var))
		variable_type = variable_type.split("'")[1]

		string += variable_type + "(" + str(var) + ")\n"

	bpy.context.window_manager.clipboard = string



def paste_array_from_clipboard(key):
	""" Read array from clipboard

		args:
			key: string value detector for check, given on copy
		return:
			array of casted variables
	"""
	# read clipboard
	string = bpy.context.window_manager.clipboard
	# split by lines
	lines = string.splitlines()
	# check key and ignore wrongs
	if lines:
		if lines[0] != key:
			return None
	else:
		return None
	# cast all line to variable and return the array
	return [eval(line) for line in lines[1:]]



def catche_collection(ctx, name):
	""" Find and return collection by name, create new one if not exist.

		args:
			ctx: bpy.context
			name: string collection name
		rettun:
			collection
	"""
	if name in bpy.data.collections:
		return bpy.data.collections[name]

	collection = bpy.data.collections.new(name)
	ctx.scene.collection.children.link(collection)
	return collection



def move_to_collection(obj, collection):
	""" Clear all collection and link to given one

		args:
			obj: Object or list
			collection: collection
		return:
			None
	"""
	if isinstance(obj, list):
		for o in obj:
			for c in o.users_collection:
				c.objects.unlink(o)
			collection.objects.link(o)
	else:
		for c in obj.users_collection:
			c.objects.unlink(obj)
		collection.objects.link(obj)



def clear_relations(obj):
	""" Clear objecrts all relations and make it free

			args:
				obj = Object
			return:
				None
	"""
	# store transform
	matrix_world = obj.matrix_world.copy()

	# delete animation
	obj.animation_data_clear()

	# delete constraints
	for constraint in obj.constraints:
		obj.constraints.remove(constraint)

	# unparent
	obj.parent = None

	# restor transform
	obj.matrix_world = matrix_world



def convert_to_solid_mesh(obj):
	"""Convert mesh object to a soled freezed collapsed object

		args:
			obj: mesh object
		return: None
	"""
	# make unique
	obj.data = obj.data.copy()

	# collaps shapekeys
	if hasattr(obj.data, "shape_keys"):
		obj.shape_key_add(name='CombinedKeys', from_mix=True)
		if obj.data.shape_keys:
			for shapeKey in obj.data.shape_keys.key_blocks:
				obj.shape_key_remove(shapeKey)

	# apply modifiers and shapekeys
	obj.to_mesh()