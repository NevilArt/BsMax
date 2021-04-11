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

import bpy, mathutils
from bpy.types import Operator
from mathutils import Vector
from bsmax.state import has_constraint
from bsmax.operator import PickOperator

def get_pre_link(obj):
	for c in obj.constraints:
		if c.type == 'CHILD_OF':
			if c.influence == 1:
				return c
	return None

def set_free(self, obj, frame):
	const = get_pre_link(obj)
	if const != None:
		worldlocation = obj.matrix_world
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		for fcurve in obj.animation_data.action.fcurves:
			fcurve.keyframe_points[-1].interpolation = 'CONSTANT'
		# set new position
		obj.keyframe_insert(data_path='location', frame=frame-1)
		obj.keyframe_insert(data_path='scale', frame=frame-1)
		obj.keyframe_insert(data_path='rotation_euler', frame=frame-1)
		obj.matrix_world = worldlocation
		obj.keyframe_insert(data_path='location', frame=frame)
		obj.keyframe_insert(data_path='scale', frame=frame)
		obj.keyframe_insert(data_path='rotation_euler', frame=frame)

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
		const = obj.constraints.new('CHILD_OF')
		# const.show_expanded = False
		const.target = parent
		if subtarget != None:
			const.subtarget = subtarget.name
			const.set_inverse_pending = True

		const.influence = 0 # in time 0
		const.keyframe_insert(data_path='influence', index=-1, frame=0)
		for fcurve in obj.animation_data.action.fcurves:
			fcurve.keyframe_points[-1].interpolation = 'CONSTANT'
		const.influence = 1 # in time current
		const.keyframe_insert(data_path='influence', index=-1, frame=frame)
		for fcurve in obj.animation_data.action.fcurves:
			fcurve.keyframe_points[-1].interpolation = 'CONSTANT'
		const.inverse_matrix = const.target.matrix_world.inverted()

		""" Fix loacation for Armatore Bone """
		if subtarget != None:
			bpy.ops.constraint.childof_set_inverse(constraint=const.name, owner='OBJECT')
	
	def picked(self, ctx, source, subsource, target, subtarget):
		frame = ctx.scene.frame_current
		for obj in source:
			set_free(self, obj, frame)
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
		objs = ctx.selected_objects
		frame = ctx.scene.frame_current
		for obj in objs:
			set_free(self, obj, frame)
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
		const.offset = -100
		obj.keyframe_insert(data_path=data_path, frame=end)

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
	[bpy.utils.register_class(c) for c in classes]

def unregister_parent():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_parent()