############################################################################
#	BsMax, 3D apps inteface simulator and tools pack for Blender
#	Copyright (C) 2021  Naser Merati (Nevil)
#
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

ctx = bpy.context

def transform_to_matrix(transform):
	matrix = None
	return matrix



def set_last_key_type(chanel, key_type):
	''' Find the newest added key and change the key type '''
	for fcurve in chanel.animation_data.action.fcurves:
		fcurve.keyframe_points[-1].interpolation = key_type



def set_positon_key(obj, time, pos_x, pos_y, pos_z):
	obj.location = (pos_x, pos_y, pos_z)
	obj.keyframe_insert(data_path='location', index=-1, frame=time)



def set_rotation_eular_key(obj, time, rot_x, rot_y, rot_z):
	obj.rotation_euler = (rot_x, rot_y, rot_z)
	obj.keyframe_insert(data_path='rotation_euler', index=-1, frame=time)



def create_camera(name, location, rotation):
	bpy.ops.object.camera_add()
	cam = ctx.active_object
	cam.name = name
	cam.location = location #(0, 0, 0)
	cam.rotation_euler = rotation #(0, 0, 0)
	return cam



def set_attribute():
	pass



def create_target(obj):
	constraint = obj.constraints.new('TRACK_TO')
	target = bpy.data.objects.new('empty', None)
	target.empty_display_type = 'CUBE'
	target.empty_display_size = 0.25
	active_layer_name = bpy.context.view_layer.active_layer_collection.name
	col = bpy.data.collections[active_layer_name]
	col.objects.link(target)
	target.name = obj.name + '_target'
	constraint.target = target
	constraint.track_axis = 'TRACK_NEGATIVE_Z'
	constraint.up_axis = 'UP_Y'
	return target



def create_mesh(data):
	return



def create_curve(data):
	return



def create_object(type, name, transform):
	if type == 'CAMERA':
		bpy.ops.object.camera_add()
		obj = ctx.active_object
	
	obj.name = name

	# obj.location = location #(0, 0, 0)
	# obj.rotation_euler = rotation #(0, 0, 0)
	# obj.scale = scale
	return obj
