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
# 2024/04/19

import bpy

from mathutils import Vector
from bpy.types import Operator


# Add display object for control bones to scene
def add_custom_control_empty(ctx, armature):
	control_obj_name = 'BENDY_CTRL'

	# no need to add another custom control if it's already here
	if control_obj_name in bpy.data.objects:
		return False

	# switch to OBJECT mode to add empty
	bpy.ops.object.mode_set(mode='OBJECT')

	# add, name and hide empty object
	bpy.ops.object.empty_add(type='SPHERE')
	ctx.object.name = control_obj_name
	ctx.object.hide_viewport = True

	# select armature again
	ctx.view_layer.objects.active = armature

	# switch mode back to EDIT
	bpy.ops.object.mode_set(mode='EDIT')


# Connect control bones to active bone by parenting and constraints
def setup_ctrl_bone_relationships(
		ctx, armature, bendy_bone, start_bone, end_bone
	):

	# parent active bone to start bone
	bendy_bone.parent = start_bone
	bendy_bone.use_connect = True

	# set main bone start and end handle attributes to ABSOLUTE
	bendy_bone.bbone_handle_type_start = 'ABSOLUTE'
	bendy_bone.bbone_handle_type_end = 'ABSOLUTE'

	# set custom control handles for current active bone
	bendy_bone.bbone_custom_handle_start = start_bone
	bendy_bone.bbone_custom_handle_end = end_bone

	bendy_bone_name = bendy_bone.name
	start_name = start_bone.name
	end_name = end_bone.name
	
	set_control_display_obj(
		ctx, armature, bendy_bone_name, start_name, end_name
	)


# Change display of control bones to empty object
def set_control_display_obj(
		ctx, armature, bendy_bone_name, start_name, end_name
	):

	bpy.ops.object.mode_set(mode='POSE')
	bendy_bone = ctx.object.pose.bones[bendy_bone_name]

	# add stretchTo constraint to active bone using end bone as target
	const = bendy_bone.constraints.new(type='STRETCH_TO')
	const.target = armature
	const.subtarget = end_name

	# set custom handles for start and end handles
	bones = ctx.object.pose.bones
	shape = bpy.data.objects['BENDY_CTRL']
	bones[start_name].custom_shape = shape
	bones[end_name].custom_shape = shape



# create and place control bones
def create_control_bones(ctx, armature, bendy_bone_name):
	bpy.ops.object.mode_set(mode='EDIT')

	bendy_bone = armature.data.edit_bones[bendy_bone_name]
	
	start_scale_factor = 1
	end_scale_factor = 1

	startControllerSize = 0.1
	endControllerSize = 0.1

	# get roll of active bone
	roll = bendy_bone.roll

	# get scale
	scale_x = bendy_bone.bbone_x
	scale_z = bendy_bone.bbone_z

	# get active bone head and tail (returns Vector position data)
	head = bendy_bone.head
	tail = bendy_bone.tail

	v1 = Vector((head[0] - tail[0], head[1] - tail[1], head[2] - tail[2],))
	v1.normalize()

	#TODO need to a name genarator with left right detect	
	start_name = "CTRL_" + bendy_bone.name + "_Start"
	end_name = "CTRL_" + bendy_bone.name + "_End"

	# create start bone
	start_bone = armature.data.edit_bones.new(name=start_name)

	# turn off use_deform for start bone
	start_bone.use_deform = False

	# place start bone
	start_bone.tail = head
	start_bone.head = (
		head[0] + (v1[0] * startControllerSize),
		head[1] + (v1[1] * startControllerSize),
		head[2] + (v1[2] * startControllerSize)
	)

	start_bone.bbone_x = scale_x * start_scale_factor
	start_bone.bbone_z = scale_z * end_scale_factor
	start_bone.roll = roll

	# create end bone
	end_bone = armature.data.edit_bones.new(name=end_name)

	# turn off use_deform for end bone
	end_bone.use_deform = False

	# place end bone
	end_bone.head = tail
	end_bone.tail = (
		tail[0] + (v1[0] * -endControllerSize),
		tail[1] + (v1[1] * -endControllerSize),
		tail[2] + (v1[2] * -endControllerSize)
	)

	end_bone.bbone_x = scale_x * start_scale_factor
	end_bone.bbone_z = scale_z * end_scale_factor
	end_bone.roll = roll

	# link new bones to bendy bone
	setup_ctrl_bone_relationships(
		ctx, armature, bendy_bone, start_bone, end_bone
	)


# performs action of adding controllers
class BBone_Add_Controller(Operator):
	bl_idname = 'bone.add_bbone_controller'
	bl_label = "Add BBone Control"
	bl_description = "Create Bendy Bones Control"
	bl_options = { 'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode in {'POSE', 'EDIT_ARMATURE'}
		return False

	def execute(self, ctx):

		armature = ctx.object
		armature.data.display_type = 'BBONE'
		
		if ctx.mode == 'POSE':
			bone_names = [bone.name for bone in ctx.selected_pose_bones]
		elif ctx.mode == 'EDIT_ARMATURE':
			bone_names = [bone.name for bone in ctx.selected_editable_bones]
		else:
			bone_names = []

		if bone_names:
			add_custom_control_empty(ctx, armature)

		for bone_name in bone_names:
			create_control_bones(ctx, armature, bone_name)

		return {'FINISHED'}


def register_bendy_bone():
	bpy.utils.register_class(BBone_Add_Controller)


def unregister_bendy_bone():
	bpy.utils.unregister_class(BBone_Add_Controller)


if __name__ == '__main__':
	register_bendy_bone()