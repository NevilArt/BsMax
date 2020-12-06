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
from bpy.props import StringProperty,BoolProperty,FloatProperty
from bpy.types import Operator

class View3D_OT_Transform_Gizmo_Size(Operator):
	bl_idname = "view3d.transform_gizmosize"
	bl_label = "Transform Gizmo Size"
	
	step: FloatProperty()

	def execute(self, ctx):
		if bpy.app.version[1] < 81:
			ctx.user_preferences.view.gizmo_size += self.step
		else:
			ctx.preferences.view.gizmo_size += self.step
		self.report({'OPERATOR'},'bpy.ops.view3d.transform_gizmosize()')
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

class Object_OT_Move(Operator):
	bl_idname = "object.move"
	bl_label = "Move"
	
	smax: BoolProperty()

	def execute(self, ctx):
		tool = get_tool(ctx)
		if tool == "builtin.select":
			set_gizmo(ctx,True,False,False)
		else:
			if tool == "builtin.move":
				coordinate_toggle(ctx)
			else:	
				bpy.ops.wm.tool_set_by_id(name="builtin.move")
		bpy.ops.object.snap_toggle(auto=self.smax)
		# self.report({'OPERATOR'},'bpy.ops.object.move()')
		return{"FINISHED"}

class Object_OT_Rotate(Operator):
	bl_idname = "object.rotate"
	bl_label = "Rotate"
	
	smax: BoolProperty()
	
	def execute(self, ctx):
		tool = get_tool(ctx)
		if tool == "builtin.select":
			set_gizmo(ctx,False,True,False)
		else:
			if tool == "builtin.rotate":
				coordinate_toggle(ctx)
			else:
				bpy.ops.wm.tool_set_by_id(name="builtin.rotate")
		bpy.ops.object.angel_snap(auto=self.smax)
		# self.report({'OPERATOR'},'bpy.ops.object.rotate()')
		return{"FINISHED"}

class Object_OT_Scale(Operator):
	bl_idname = "object.scale"
	bl_label = "Scale"
	
	cage: BoolProperty(default=False)
	
	def execute(self, ctx):
		tool = get_tool(ctx)
		if tool == "builtin.select":
			set_gizmo(ctx,False,False,True)
		else:
			if self.cage:
				if tool == "builtin.scale":
					coordinate_toggle(ctx)
				else:
					bpy.ops.wm.tool_set_by_id(name="builtin.scale",cycle=True)
			else:
				bpy.ops.wm.tool_set_by_id(name="builtin.scale",cycle=True)
		# self.report({'OPERATOR'},'bpy.ops.object.scale()')
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
			bpy.ops.transform.transform('INVOKE_DEFAULT',mode=self.tmode)#,release_confirm=self.release)
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

classes = [View3D_OT_Transform_Gizmo_Size,View3D_OT_Tweak_Better,
			Object_OT_Move,Object_OT_Rotate,Object_OT_Scale]

def register_transforms():
	[bpy.utils.register_class(c) for c in classes]

def unregister_transforms():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_transforms()