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

def solve_missing_activeobject(ctx, objs):
	""" Make first selected object as active_object if missing """
	if ctx.active_object == None:
		if len(objs) > 0:
			ctx.view_layer.objects.active = objs[0]

def lock_transform(obj, move, rotate, scale):
	for i in range(3):
		obj.lock_location[i] = move
		obj.lock_rotation[i] = rotate
		obj.lock_scale[i] = scale

def set_transform(obj, coordinate, location, rotation, dimantion):
	if coordinate == 'locaL':
		pass
	elif coordinate in {'world', 'global'}:
		pass
	elif coordinate == 'parent':
		pass
	obj.location = location
	obj.rotation_euler = rotation
	obj.dimensions = dimantion

def duplicate_linked(ctx, obj):
	# not a god method has to fix
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(state = True)
	bpy.ops.object.duplicate(linked=True, mode='TRANSLATION')
	return ctx.view_layer.objects.active

def duplicate_copy(ctx, obj):
	# not a god method has to fix
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(state = True)
	bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
	return ctx.view_layer.objects.active

def modifier_add(ctx, objs, modifier, name=''):
	for obj in objs:
		the_name = modifier if name == '' else name
		obj.modifiers.new(name=the_name, type=modifier)

def link_to_scene(ctx, obj):
	activelayername = ctx.view_layer.active_layer_collection.name
	if activelayername == 'Master Collection':
		collection = ctx.scene.collection
	else:
		collection = bpy.data.collections[activelayername]
	# apply if collection was not same
	# for now 
	try:
		collection.objects.link(obj)
	except:
		pass

def set_as_active_object(ctx, obj):
	if obj != None:
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
		active_layer_name = bpy.context.view_layer.active_layer_collection.name
		col = bpy.data.collections[active_layer_name]
		col.objects.link(target)
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
	saved_location = scene.cursor.location
	saved_rotation = scene.cursor.rotation_euler
	scene.cursor.location = location
	bpy.ops.object.select_all(action='DESELECT')
	ctx.view_layer.objects.active = obj
	obj.select_set(state = True)
	bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
	scene.cursor.location = saved_location
	scene.cursor.rotation_euler = saved_rotation

def freeze_transform(objs):
	""" simulate freeze transform action """
	""" put actual transform to delta then reset the transform """
	#TODO if selta has vale had to combine with new value or get from world or parent coordinate
	for obj in objs:
		obj.delta_location = obj.location
		obj.location = [0,0,0]
		obj.delta_rotation_euler = obj.rotation_euler
		obj.rotation_euler = [0,0,0]