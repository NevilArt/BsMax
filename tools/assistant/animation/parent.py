import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from bsmax.state import has_constraint

class BsMax_OT_linkConstraint(Operator):
	bl_idname="animation.linkconstraint"
	bl_label="Link Constraint"
	bl_description="Link/Unlink constraint"
	bl_options={'REGISTER', 'UNDO'}
	linkto: EnumProperty(name='Link To',default='OBJECT',
		items =[('WORLD','World',''),('OBJECT','Active Object','')])

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.selected_objects) > 0:
				if ctx.active_object != None:
					return True
		return False

	def get_pre_link(self, obj):
		for c in obj.constraints:
			if c.type == 'CHILD_OF':
				if c.influence == 1:
					return c
		return None

	def set_free(self, obj, frame):
		const = self.get_pre_link(obj)
		if const != None:
			worldlocation = obj.matrix_world
			const.influence = 0 # in time 0
			const.keyframe_insert(data_path="influence", index=-1, frame=frame)
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

	def set_link(self, obj, parent, frame):
		const = obj.constraints.new('CHILD_OF')
		#const.show_expanded = False
		const.target = parent
		const.influence = 0 # in time 0
		const.keyframe_insert(data_path="influence", index=-1, frame=0)
		for fcurve in obj.animation_data.action.fcurves:
			fcurve.keyframe_points[-1].interpolation = 'CONSTANT'
		const.influence = 1 # in time current
		const.keyframe_insert(data_path="influence", index=-1, frame=frame)
		for fcurve in obj.animation_data.action.fcurves:
			fcurve.keyframe_points[-1].interpolation = 'CONSTANT'
		const.inverse_matrix = const.target.matrix_world.inverted()

	def execute(self, ctx):
		""" check the user info """
		objs = ctx.selected_objects
		frame = ctx.scene.frame_current

		if self.linkto == 'OBJECT':
			parent = ctx.active_object
			objs.remove(parent) # parent will use as target
			for obj in objs:
				self.set_free(obj, frame)
				self.set_link(obj, parent, frame)

		if self.linkto == 'WORLD':
			for obj in objs:
				self.set_free(obj, frame)
		return{"FINISHED"}

def parent_cls(register):
	classes = [BsMax_OT_linkConstraint]
	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	parent_cls(True)

__all__ = ["parent_cls"]