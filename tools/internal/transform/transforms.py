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
from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy.types import Operator
from bsmax.state import version



class View3D_OT_Transform_Gizmo_Size(Operator):
	bl_idname = "view3d.transform_gizmosize"
	bl_label = "Transform Gizmo Size"
	bl_options= {'REGISTER', 'INTERNAL'}
	
	step: IntProperty()

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		if version() == 280:
			ctx.user_preferences.view.gizmo_size += self.step
		else:
			ctx.preferences.view.gizmo_size += self.step
		return{"FINISHED"}



def get_tool(ctx):
	space_type = ctx.area.spaces.active.type
	if space_type == "VIEW_3D":
		return ctx.workspace.tools.from_space_view3d_mode(ctx.mode,create=False).idname
	elif space_type == "IMAGE_EDITOR":
		return ctx.workspace.tools.from_space_image_mode("UV",create=False).idname
	else:
		return ""



def set_gizmo(ctx,translate,rotate,scale):
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
	return not ctx.mode in {'PAINT_TEXTURE', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PARTICLE'}



class Transform_Mode:
	def __init__(self):
		self.auto_switch = False
transform_mode = Transform_Mode()



class Object_OT_Auto_Coordinate_Toggle(Operator):
	bl_idname = "object.auto_coordinate_toggle"
	bl_label = "Auto Coordinate Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		transform_mode.auto_switch = not transform_mode.auto_switch
		return{"FINISHED"}



class Object_OT_Move(Operator):
	bl_idname = "object.move"
	bl_label = "Move"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	smax: BoolProperty(default=False)

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'EDIT_TEXT':
			return False
		return ctx.area.type in {'VIEW_3D', 'IMAGE_EDITOR'}

	def execute(self, ctx):
		if is_transform_avalible(ctx):
			
			tool = get_tool(ctx)
			
			if tool == 'builtin.select':
				set_gizmo(ctx,True,False,False)
			
			else:
				""" Cordinate tooggle work only if actived """
				if transform_mode.auto_switch:
					if tool == 'builtin.move':
						coordinate_toggle(ctx)
						return{"FINISHED"}
				
				bpy.ops.wm.tool_set_by_id(name='builtin.move')
		
		return{"FINISHED"}



class Object_OT_Rotate(Operator):
	bl_idname = "object.rotate"
	bl_label = "Rotate"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	smax: BoolProperty(default=False)

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'EDIT_TEXT':
			return False
		return ctx.area.type in {'VIEW_3D', 'IMAGE_EDITOR'}
	
	def execute(self, ctx):
		if is_transform_avalible(ctx):
			
			tool = get_tool(ctx)
			if tool == 'builtin.select':
				set_gizmo(ctx,False,True,False)
			
			else:
				""" Cordinate tooggle work only if actived """
				if transform_mode.auto_switch:
					if tool == 'builtin.rotate':
						coordinate_toggle(ctx)
						return{"FINISHED"}
			
				bpy.ops.wm.tool_set_by_id(name='builtin.rotate')
		
		return{"FINISHED"}



class Object_OT_Scale(Operator):
	bl_idname = "object.scale"
	bl_label = "Scale"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	cage: BoolProperty(default=False)

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
				if transform_mode.auto_switch:
					if self.cage:
						if tool == 'builtin.scale':
							coordinate_toggle(ctx)
							return{"FINISHED"}
	
				bpy.ops.wm.tool_set_by_id(name='builtin.scale', cycle=True)
		
		return{"FINISHED"}



# "TweakBetter" created by Dan Pool (dpdp)
# original addon "qwer_addon"
# https://blenderartists.org/t/qwer-addon-or-how-i-stopped-using-the-transform-active-tools/1157507
class View3D_OT_Tweak_Better(Operator):
	"""Fix the select active tool"""
	bl_idname = "view3d.tweak_better"
	bl_label = "Tweak Better"
	
	tmode: StringProperty(name="Transform Mode")
	release: BoolProperty(name="Confirm on Release")

	def modal(self, ctx, event):
		if event.type == 'MOUSEMOVE':
			#TODO check the operator
			bpy.ops.transform.transform('INVOKE_DEFAULT',mode=self.tmode)
			return {'FINISHED'}
		return {'RUNNING_MODAL'}

	def execute(self,ctx):
		self.report({'OPERATOR'},'bpy.ops.view3d.tweak_better()')
		return{"FINISHED"}

	def invoke(self, ctx, event):
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



classes = [	View3D_OT_Transform_Gizmo_Size,
			Object_OT_Auto_Coordinate_Toggle,
			Object_OT_Move,
			Object_OT_Rotate,
			Object_OT_Scale,
			View3D_OT_Tweak_Better]



def register_transforms(preferences):
	for c in classes:
		bpy.utils.register_class(c)

def unregister_transforms():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	[bpy.utils.register_class(c) for c in classes]