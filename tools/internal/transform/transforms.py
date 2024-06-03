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
# 2024/05/29

import bpy

from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy.types import Operator


def get_tool(ctx):
	if not ctx.area.spaces.active:
		return ''

	space_type = ctx.area.spaces.active.type
	if space_type == 'VIEW_3D':
		tools = ctx.workspace.tools 
		return tools.from_space_view3d_mode(ctx.mode, create=False).idname

	elif space_type == 'IMAGE_EDITOR':
		tools = ctx.workspace.tools
		return tools.from_space_image_mode("UV", create=False).idname

	else:
		return ''


def set_gizmo(ctx, translate, rotate, scale):
	ctx.space_data.show_gizmo_object_translate = translate
	ctx.space_data.show_gizmo_object_rotate = rotate
	ctx.space_data.show_gizmo_object_scale = scale


def coordinate_toggle(ctx):
	coord = ctx.window.scene.transform_orientation_slots[0]
	if coord.type == 'LOCAL':
		coord.type = 'GLOBAL'
	elif coord.type == 'GLOBAL':
		coord.type = 'LOCAL'


def is_transform_avalible(ctx):
	return not ctx.mode in {
		'PAINT_TEXTURE', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PARTICLE'
	}


class Transform_Mode:
	def __init__(self):
		self.auto_switch = False

transform_mode = Transform_Mode()


class View3D_OT_Transform_Gizmo_Size(Operator):
	bl_idname = 'view3d.transform_gizmosize'
	bl_label = "Transform Gizmo Size"
	bl_options= {'REGISTER', 'INTERNAL'}
	
	step: IntProperty() # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		ctx.preferences.view.gizmo_size += self.step
		return{'FINISHED'}


class Object_OT_Auto_Coordinate_Toggle(Operator):
	bl_idname = 'object.auto_coordinate_toggle'
	bl_label = "Auto Coordinate Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, _):
		global transform_mode
		transform_mode.auto_switch = not transform_mode.auto_switch
		return{'FINISHED'}


class Object_OT_Move(Operator):
	bl_idname = 'object.move'
	bl_label = "Move"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	smax: BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'EDIT_TEXT':
			return False
		return ctx.area.type in {'VIEW_3D', 'IMAGE_EDITOR'}

	def execute(self, ctx):
		if is_transform_avalible(ctx):
			
			tool = get_tool(ctx)
			
			if tool == 'builtin.select':
				set_gizmo(ctx, True, False, False)
			
			else:
				""" Cordinate tooggle work only if actived """
				global transform_mode
				if transform_mode.auto_switch:
					if tool == 'builtin.move':
						coordinate_toggle(ctx)
						return{'FINISHED'}
				
				bpy.ops.wm.tool_set_by_id(name='builtin.move')
		
		return{'FINISHED'}


class Object_OT_Rotate(Operator):
	bl_idname = 'object.rotate'
	bl_label = "Rotate"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	smax: BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'EDIT_TEXT':
			return False
		return ctx.area.type in {'VIEW_3D', 'IMAGE_EDITOR'}
	
	def execute(self, ctx):
		if is_transform_avalible(ctx):
			
			tool = get_tool(ctx)
			if tool == 'builtin.select':
				set_gizmo(ctx, False, True, False)
			
			else:
				""" Cordinate tooggle work only if actived """
				global transform_mode
				if transform_mode.auto_switch:
					if tool == 'builtin.rotate':
						coordinate_toggle(ctx)
						return{'FINISHED'}
			
				bpy.ops.wm.tool_set_by_id(name='builtin.rotate')
		
		return{'FINISHED'}


class Object_OT_Scale(Operator):
	bl_idname = 'object.scale'
	bl_label = "Scale"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	cage: BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'EDIT_TEXT':
			return False
		return ctx.area.type in {'VIEW_3D', 'IMAGE_EDITOR'}
	
	def execute(self, ctx):
		if is_transform_avalible(ctx):
			
			tool = get_tool(ctx)
			if tool == 'builtin.select':
				set_gizmo(ctx,False,False,True)
			
			else:
				""" Cordinate tooggle work only if actived """
				global transform_mode
				if transform_mode.auto_switch:
					if self.cage:
						if tool == 'builtin.scale':
							coordinate_toggle(ctx)
							return{'FINISHED'}
	
				bpy.ops.wm.tool_set_by_id(name='builtin.scale', cycle=True)
		
		return{'FINISHED'}


# "TweakBetter" created by Dan Pool (dpdp)
# original addon "qwer_addon"
# https://blenderartists.org/t/qwer-addon-or-how-i-stopped-using-the-transform-active-tools/1157507
class View3D_OT_Tweak_Better(Operator):
	"""Fix the select active tool"""
	bl_idname = 'view3d.tweak_better'
	bl_label = "Tweak Better"
	
	tmode: StringProperty(name="Transform Mode") # type: ignore
	release: BoolProperty(name="Confirm on Release") # type: ignore

	def modal(self, _, event):
		if event.type == 'MOUSEMOVE':
			#TODO check the operator
			bpy.ops.transform.transform('INVOKE_DEFAULT', mode=self.tmode)
			return {'FINISHED'}
		return {'RUNNING_MODAL'}

	def execute(self, _):
		return{'FINISHED'}

	def invoke(self, ctx, _):
		if ctx.object:
			if ctx.space_data.show_gizmo_object_translate == True:
				self.tmode = 'TRANSLATION'

			elif ctx.space_data.show_gizmo_object_rotate == True:
				self.tmode = 'ROTATION'

			elif ctx.space_data.show_gizmo_object_scale == True:
				self.tmode = 'RESIZE'

			else: self.tmode = 'TRANSLATION'

			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}

		else:
			self.report({'WARNING'}, "No active object, could not finish")
			return {'CANCELLED'}


classes = {
	View3D_OT_Transform_Gizmo_Size,
	Object_OT_Auto_Coordinate_Toggle,
	Object_OT_Move,
	Object_OT_Rotate,
	Object_OT_Scale,
	View3D_OT_Tweak_Better
}


def register_transforms():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister_transforms():
	for cls in classes:
		bpy.utils.unregister_class(cls)


if __name__ == '__main__':
	[bpy.utils.register_class(cls) for cls in classes]