import bpy
ctx = bpy.context

def set_last_key_type(chanel, key_type):
	''' Find the newest added key and change the key type '''
	for fcurve in chanel.animation_data.action.fcurves:
		fcurve.keyframe_points[-1].interpolation = key_type

def set_transform_keytime(obj, time, pos_x, pos_y, pos_z, rot_x, rot_y, rot_z):
	obj.location = (pos_x, pos_y, pos_z)
	obj.rotation_euler = (rot_x, rot_y, rot_z)
	obj.keyframe_insert(data_path='location', index=-1, frame=time)
	obj.keyframe_insert(data_path='rotation_euler', index=-1, frame=time)
	# set_last_key_type(obj, 'CONSTANT')

def set_key(obj, chanel, value, time, type):
	obj.chanel
	obj.keyframe_insert(data_path='location', index=-1, frame=time)

def create_camera(name, location, rotation):
	bpy.ops.object.camera_add()
	cam = ctx.active_objec
	cam.name = name
	cam.location = location #(0, 0, 0)
	cam.rotation_euler = rotation #(0, 0, 0)
	return cam