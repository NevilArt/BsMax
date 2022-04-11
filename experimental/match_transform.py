import bpy
from bpy.types import Operator

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


class Object_TO_Match_Transform(Operator):
	bl_idname = 'object.match_transform'
	bl_label = 'Match Transform'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		target = ctx.object
		objs = [obj for obj in ctx.selected_objects if obj != target]
		for obj in objs:
			match_transform(ctx, obj, target)
		return{'FINISHED'}

bpy.utils.register_class(Object_TO_Match_Transform)



