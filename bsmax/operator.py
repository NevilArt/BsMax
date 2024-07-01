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
# 2024/04/08

import bpy

from bpy.types import Operator
from mathutils import Vector

from bsmax.graphic import Rubber_Band, get_screen_pos


def curve_tool_invoke(self, ctx):
	self.get_data(ctx)
	if self.typein:
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)
	else:
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def pick_operator_modal(self, ctx, event):
	ctx.area.tag_redraw()
	if not event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'MOUSEMOVE', 'ESC'}:
		return {'PASS_THROUGH'}
	
	elif event.type == 'MOUSEMOVE':
		""" update the line coordinate """
		""" self.center is a 3D coordinate """
		######################################################
		self.start = get_screen_pos(ctx,self.center) 
		self.end = event.mouse_region_x, event.mouse_region_y

		if self.start != None:
			sx = int(self.start.x)
			sy = int(self.start.y)
		else:
			sx, sy = 0, 0

		if self.end != None:
			ex = self.end[0]
			ey = self.end[1]
		else:
			ex, ey = 0, 0

		self.rb.create(sx, sy, ex, ey)
		######################################################

	elif event.type == 'LEFTMOUSE':
		if event.value == 'PRESS':
			""" clear all selection """
			if ctx.mode != 'OBJECT':
				bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

			bpy.ops.object.select_all(action='DESELECT')
			ctx.view_layer.objects.active = None
			
			""" Pick new object as target """
			coord = event.mouse_region_x, event.mouse_region_y
			bpy.ops.view3d.select(extend=False, location=coord)

			""" Ignore source obects as target """
			if ctx.active_object in self.source:
				if self.subsource == []:
					ctx.view_layer.objects.active = None

		if event.value =='RELEASE':
			""" if target selected check and return """
			picked_object = ctx.view_layer.objects.active

			if picked_object:
				allowed = False
				""" Filter the selection types """
				if 'ANY' in self.filters:
					allowed = True
				
				if picked_object.type in self.filters:
					allowed = True
				
				if 'AUTO' in self.filters and len(self.source) > 0:
					#TODO need to smarter method
					if self.source[0].type == picked_object.type and \
						self.source[0] != picked_object:

						allowed = True
			
				if allowed:
					self.rb.unregister()
					self.finish(ctx, event, picked_object)
					return {'CANCELLED'}
				else:
					ctx.view_layer.objects.active = None
					bpy.ops.object.select_all(action='DESELECT')
			
			self.restore_mode(ctx)

		return {'RUNNING_MODAL'}

	elif event.type in {'RIGHTMOUSE','ESC'}:
		self.rb.unregister()
		return {'CANCELLED'}

	return {'RUNNING_MODAL'}


def get_objects_center(objs):
	""" Return selected objects midil """
	location = Vector((0,0,0))
	for obj in objs:
		location += obj.matrix_world.translation

	if objs:
		return location / len(objs)

	return location


def pick_operator_get_bone(self, ctx, event, armature):
	coord = event.mouse_region_x, event.mouse_region_y
	ctx.view_layer.objects.active = armature

	if self.mode == 'EDIT_ARMATURE':
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bpy.ops.armature.select_all(action='DESELECT')
		bpy.ops.view3d.select(extend=False, location=coord)
		selection = ctx.selected_bones
	else:
		bpy.ops.object.mode_set(mode='POSE', toggle=False)
		bpy.ops.pose.select_all(action='DESELECT')
		bpy.ops.view3d.select(extend=False, location=coord)
		selection = ctx.selected_pose_bones

	bone = selection[0] if len(selection) > 0 else None
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

	return bone


def pick_operator_get_sub_itme(ctx, objs):
	if ctx.mode == 'POSE':
		return ctx.selected_pose_bones
	elif ctx.mode == 'EDIT_ARMATURE':
		return ctx.selected_bones
	return []


def pick_operator_setup(self, ctx, event):
	self.mode = ctx.mode
	self.active = ctx.active_object
	self.source = ctx.selected_objects.copy()
	self.subsource = self.get_sub_itme(ctx, self.source)
	self.center = self.get_center(self.source)
	######################################################
	self.start = self.end = event.mouse_region_x, event.mouse_region_y
	######################################################


def pick_operator_set_mode(ctx, mode):
	if mode in {'OBJECT', 'POSE'}:
		if ctx.mode != mode:
			bpy.ops.object.mode_set(mode=mode, toggle=False)
	else:
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)


def pick_operator_restore_mode(self, ctx):
	if ctx.mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	bpy.ops.object.select_all(action='DESELECT')
	ctx.view_layer.objects.active = self.active

	for obj in self.source:
		obj.select_set(state = True)
	self.set_mode(ctx, self.mode)

	for sub in self.subsource:
		if ctx.mode == 'POSE':
			sub.bone.select = True
		elif ctx.mode == 'EDIT_ARMATURE':
			sub.select = True


def pick_operator_finish(self, ctx, event, target):
	subtarget = self.get_bone(ctx, event, target) \
				if target.type == 'ARMATURE' else None

	self.restore_mode(ctx)
	self.picked(ctx, self.source, self.subsource, target, subtarget)


def pick_operator_invoke(self, ctx, event):
	self.pre_setup(ctx, event)
	self.setup(ctx, event)
	self.rb.register()
	ctx.window_manager.modal_handler_add(self)
	return {'RUNNING_MODAL'}

#TODO preview the object name under the cursure befor pick
#TODO convert to raycast picker rathr than select base operator
class PickOperator(Operator):
	""" Call a function with early selected and new selected Objects """
	source = []
	subsource, active = None, None
	start, center, end = None, Vector((0, 0, 0)), None
	mode, filters = 'OBJECT' , ['ANY']
	rb = Rubber_Band()

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False

	def modal(self, ctx, event):
		return pick_operator_modal(self, ctx, event)
	
	def get_center(self, objs):
		return get_objects_center(objs)
	
	def get_bone(self, ctx, event, armature):
		return pick_operator_get_bone(self, ctx, event, armature)
	
	def get_sub_itme(self, ctx, objs):
		return pick_operator_get_sub_itme(ctx, objs)
	
	def pre_setup(self, ctx, event):
		pass
	
	def setup(self, ctx, event):
		pick_operator_setup(self, ctx, event)
	
	def set_mode(self, ctx, mode):
		pick_operator_set_mode(ctx, mode)
	
	def restore_mode(self, ctx):
		pick_operator_restore_mode(self, ctx)
			
	def cancel(self, ctx):
		self.set_mode(ctx, self.modal)

	def finish(self, ctx, event, target):
		pick_operator_finish(self, ctx, event, target)
	
	def picked(self, ctx, source, subsource, target, subtarget):
		pass

	def invoke(self, ctx, event):
		return pick_operator_invoke(self, ctx, event)

# class picker_OT_test(PickOperator):
# 	bl_idname = "object.picker"
# 	bl_label = "picker test"
# 	filters = ['ANY']
# 	def picked(self, ctx, source, subsource, target, subtarget):
# 		print("---------------------------------------")
# 		print("source: ", source)
# 		print("subsource: ", subsource)
# 		print("target: ", target)
# 		print("subtarget: ", subtarget)

# bpy.utils.register_class(picker_OT_test)