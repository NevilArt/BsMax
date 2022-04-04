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
from bpy.types import Operator
from mathutils import Vector
from bsmax.operator import PickOperator



def insert_key_for_current_state(chanel, frame):
	""" Set key for Location and Scale always is same """
	chanel.keyframe_insert(data_path='location', frame=frame)
	chanel.keyframe_insert(data_path='scale', frame=frame)

	""" Sey key by rotation mode """
	if chanel.rotation_mode == 'QUATERNION':
		chanel.keyframe_insert(data_path='rotation_quaternion', frame=frame)
	elif chanel.rotation_mode == 'AXIS_ANGLE':
		chanel.keyframe_insert(data_path='rotation_axis_angle', frame=frame)
	else:
		chanel.keyframe_insert(data_path='rotation_euler', frame=frame)



def set_last_key_type(chanel, key_type):
	""" Find the newest added key and change the key type """
	for fcurve in chanel.animation_data.action.fcurves:
		fcurve.keyframe_points[-1].interpolation = key_type



def get_object_pre_link(obj):
	""" Return the Child of constraint with influence == 1 (Active one) """
	for constraint in obj.constraints:
		if constraint.type == 'CHILD_OF':
			if constraint.influence == 1:
				return constraint
	return None



def get_bone_pre_link(armatur, bone):
	""" Return the Child of constraint with influence == 1 (Active one) """
	for constraint in armatur.pose.bones[bone.name].constraints:
		if constraint.type == 'CHILD_OF':
			if constraint.influence == 1:
				return constraint
	return None



def set_object_free(self, obj, frame):
	""" Get active child of constraint """
	const = get_object_pre_link(obj)
	
	if const != None:
		""" Store the world position """
		worldlocation = obj.matrix_world
		
		""" Insert key frame on frame Zero with value Zero """
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		set_last_key_type(obj, 'CONSTANT')
		
		""" set key in previous frame for current position """
		insert_key_for_current_state(obj, frame-1)
		
		""" Return to worl position and insert a new key """
		obj.matrix_world = worldlocation
		insert_key_for_current_state(obj, frame)



def set_bone_free(self, armature, bone, frame):
	""" Get active child of constraint """
	const = get_bone_pre_link(armature, bone)
	bone = armature.pose.bones[bone.name] # get pose bone
	
	if const != None:
		""" Store the world position """
		matrix_world = armature.matrix_world @ bone.matrix
	
		""" Insert key frame on frame Zero with value Zero """
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		
		set_last_key_type(armature, 'CONSTANT')
		
		""" set key in previous frame for current position """
		insert_key_for_current_state(bone, frame-1)
		
		""" Return to worl position and insert a new key """
		bone.matrix = matrix_world
		insert_key_for_current_state(bone, frame)



class Anim_OT_Link_Constraint(PickOperator):
	bl_idname = 'anim.link_constraint'
	bl_label = 'Link Constraint'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def set_link(self, obj, parent, subtarget, frame):
		""" Create a new constraint modifier """
		const = obj.constraints.new('CHILD_OF')
		# const.show_expanded = False
		
		""" set constrant values """
		const.target = parent
		if subtarget != None:
			const.subtarget = subtarget.name
			const.set_inverse_pending = True

		""" Set 0 value key in frame 0 """
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=0)
		set_last_key_type(obj, 'CONSTANT')
		
		""" set value 1 in current frame """
		const.influence = 1 # in time current
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		
		set_last_key_type(obj, 'CONSTANT')
		
		const.inverse_matrix = const.target.matrix_world.inverted()

		""" Fix loacation for Armatore Bone """
		if subtarget != None:
			bpy.ops.constraint.childof_set_inverse(constraint=const.name, owner='OBJECT')
	
	def set_bonelink(self, armature, bone, parent, subtarget, frame):
		""" Create a new constraint modifier """
		const = armature.pose.bones[bone.name].constraints.new('CHILD_OF')
		# const.show_expanded = False
		
		""" set constrant values """
		const.target = parent
		if subtarget != None:
			const.subtarget = subtarget.name
			const.set_inverse_pending = True

		""" Set 0 value key in frame 0 """
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=0)
		set_last_key_type(armature, 'CONSTANT')
		
		""" set value 1 in current frame """
		const.influence = 1 # in time current
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		set_last_key_type(armature, 'CONSTANT')
	
		const.inverse_matrix = const.target.matrix_world.inverted()

		""" Fix loacation for Armatore Bone """
		if subtarget != None:
			bpy.ops.constraint.childof_set_inverse(constraint=const.name, owner='OBJECT')
	
	def picked(self, ctx, source, subsource, target, subtarget):
		frame = ctx.scene.frame_current
		for obj in source:
			if obj.type == 'ARMATURE' and subsource:
				for bone in subsource:
					set_bone_free(self, obj, bone, frame)
					self.set_bonelink(obj, bone, target, subtarget, frame)
			else:
				set_object_free(self, obj, frame)
				self.set_link(obj, target, subtarget, frame)
		self.report({'OPERATOR'},'bpy.ops.anim.link_constraint()')


class Anim_OT_Link_To_World(Operator):
	bl_idname = 'anim.link_to_world'
	bl_label = 'Link To World'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def execute(self, ctx):
		""" get current state info """
		objs = ctx.selected_objects
		frame = ctx.scene.frame_current
		
		for obj in objs:
			if obj.type == 'ARMATURE' and ctx.mode == 'POSE':
				for bone in obj.data.bones:
					set_bone_free(self, obj, bone, frame)
			else:
				set_object_free(self, obj, frame)
		
		self.report({'OPERATOR'},'bpy.ops.anim.link_to_world()')
		return{'FINISHED'}



class Anim_OT_Path_Constraint(PickOperator):
	bl_idname = 'anim.path_constraint'
	bl_label = 'Path Constraint'
	bl_description = ''
	bl_options = {'REGISTER', 'UNDO'}

	filters = ['CURVE']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def get_first_pint_position(self, curve):
		if len(curve.data.splines) > 0:
			if len(curve.data.splines[0].bezier_points) > 0:
				point = curve.data.splines[0].bezier_points[0].co.copy()
				return curve.location + point * curve.scale
		return curve.location

	def set_path_constraint(self, ctx, obj, path):
		const = obj.constraints.new('FOLLOW_PATH')
		const.target = path
		const.use_curve_follow = True
		const.forward_axis = 'FORWARD_X'
		path.data.use_path_follow = True
		obj.location = Vector((0,0,0))

		data_path = 'constraints["' + const.name + '"].offset'
		start, end = ctx.scene.frame_start, ctx.scene.frame_end
		const.offset = 0
		obj.keyframe_insert(data_path=data_path, frame=start)
		set_last_key_type(obj, 'LINEAR')
		const.offset = -100
		obj.keyframe_insert(data_path=data_path, frame=end)
		set_last_key_type(obj, 'LINEAR')

	def picked(self, ctx, source, subsource, target, subtarget):
		for obj in source:
			if obj != target:
				self.set_path_constraint(ctx, obj, target)
		self.report({'OPERATOR'},'bpy.ops.anim.path_constraint()')



class Anim_OT_Lookat_Constraint(PickOperator):
	bl_idname = 'anim.lookat_constraint'
	bl_label = 'Lookat Constraint'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False

	def set_lookat(self, obj, target, subtarget):
		const = obj.constraints.new('TRACK_TO')
		const.target = target
		if subtarget != None:
			const.subtarget = subtarget.name
			const.target_space = 'POSE'
		const.track_axis = 'TRACK_X'
		const.up_axis = 'UP_Z'

	def picked(self, ctx, source, subsource, target, subtarget):
		for obj in source:
			self.set_lookat(obj, target, subtarget)
		self.report({'OPERATOR'},'bpy.ops.anim.lookat_constraint()')



class Anim_OT_Location_Constraint(PickOperator):
	bl_idname = 'anim.location_constraint'
	bl_label = 'Location Constraint'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False

	def set_location(self, obj, target, subtarget):
		const = obj.constraints.new('COPY_LOCATION')
		const.target = target
		if subtarget != None:
			const.subtarget = subtarget.name

	def picked(self, ctx, source, subsource, target, subtarget):
		for obj in source:
			self.set_location(obj, target, subtarget)
		self.report({'OPERATOR'},'bpy.ops.anim.location_constraint()')



class Anim_OT_Orientation_Constraint(PickOperator):
	bl_idname = 'anim.orientation_constraint'
	bl_label = 'Orientation Constraint'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False

	def set_orient(self, obj, target, subtarget):
		const = obj.constraints.new('COPY_ROTATION')
		const.target = target
		if subtarget != None:
			const.subtarget = subtarget.name

	def picked(self, ctx, source, subsource, target, subtarget):
		for obj in source:
			self.set_orient(obj, target, subtarget)
		self.report({'OPERATOR'},'bpy.ops.anim.orientation_constraint()')



classes = [	Anim_OT_Link_Constraint,
			Anim_OT_Link_To_World,
			Anim_OT_Path_Constraint,
			Anim_OT_Lookat_Constraint,
			Anim_OT_Location_Constraint,
			Anim_OT_Orientation_Constraint]

def register_parent():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_parent():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_parent()