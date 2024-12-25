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
# 2024/04/15

import bpy

from bpy.types import Operator
from bpy.props import IntProperty, EnumProperty, BoolProperty
from bpy.utils import register_class, unregister_class

from bsmax.state import is_active_object


class Armature_OT_Bone_Type(Operator):
	bl_idname = 'armature.bone_type'
	bl_label = "Bone Type"
	bl_description = "Set Armatur Bone Type"
	bl_options = {'REGISTER', 'UNDO'}
	
	mode: EnumProperty(
		name="Bone Draw type",
		items=[
			('OCTAHEDRAL', "Octahedral", ""),
			('STICK', "Stick", ""),
			('BBONE', "BBone", ""),
			('ENVELOPE', "Envelope", ""),
			('WIRE', "Wire", "")
		],
		default='BBONE',
		description="Armature Bone Draw Type"
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		return is_active_object(ctx, 'ARMATURE')
	
	def execute(self, ctx):
		ctx.object.data.display_type = self.mode
		return{'FINISHED'}


#TODO rename the operator
class Armature_OT_Bone_Devide(Operator):
	bl_idname = 'armature.bone_devide'
	bl_label = "Bone Devide"
	bl_description = "Devide Bone by number dialog"
	bl_options = {'REGISTER', 'UNDO'}

	devides: IntProperty(name="Devides", default=1) # type: ignore
	typein: BoolProperty(name="Type In:", default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_ARMATURE'
	
	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'devides', text="Devides")
	
	def execute(self, ctx):
		bpy.ops.armature.subdivide(number_cuts=self.devides)
		return {'FINISHED'}

	def modal(self, ctx, event):
		bpy.ops.armature.subdivide(number_cuts=self.devides)
		return {'CANCELLED'}

	def invoke(self, ctx, event):		
		if self.typein:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self, width=150)

		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class Armature_OT_Freeze(Operator):
	""" Freeze / Unfreeze Bones """
	bl_idname = 'bone.freeze'
	bl_label = "Freeze / Unfreeze"
	bl_description = "Freeze / Unfreeze Bones"
	bl_options = {'REGISTER', 'UNDO'}

	mode: EnumProperty(
		items=[
			('selection', "Freeze Selection", ""),
			('unselected', "Freeze Unselected", ""),
			('clear', "Unfreezee All", "")
		],
		default='selection'
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode in {'POSE', 'EDIT_ARMATURE'}

	def execute(self, ctx):
		original_mode = ctx.mode
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		if self.mode == 'selection':
			for bone in ctx.object.data.bones:
				if bone.select:
					bone.hide_select = True

		elif self.mode == 'unselected':
			for bone in ctx.object.data.bones:
				if not bone.select:
					bone.hide_select = True

		elif self.mode == 'clear':
			for bone in ctx.object.data.bones:
				bone.hide_select = False
		
		if original_mode == 'POSE':
			bpy.ops.object.mode_set(mode='POSE', toggle=False)
		else:
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)

		return{'FINISHED'}


class Armature_OT_Select_Keyed_Bone(Operator):
	bl_idname = 'armature.select_keyed_bones'
	bl_label = "Select Keyed Bones"
	bl_options = {'REGISTER', 'UNDO'}

	invert: BoolProperty() # type: ignore
	deselect: BoolProperty() # type: ignore
	current_frame: BoolProperty() # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'POSE'
	
	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'invert', text="Invert")
		layout.prop(self, 'deselect', text="Deselect")
	
	def select(self, armature):
		action = armature.animation_data.action
		keyed_bones = []

		for fcurve in action.fcurves:
			pose_bone_path = fcurve.data_path.rpartition('.')[0]
			pose_bone = armature.path_resolve(pose_bone_path)
			if not pose_bone in keyed_bones:
				keyed_bones.append(pose_bone)

		state = not self.deselect

		for bone in armature.pose.bones:
			if self.invert:
				if not bone in keyed_bones:
					bone.bone.select = state
			else:
				if bone in keyed_bones:
					bone.bone.select = state
	
	def execute(self, ctx):

		for armature in ctx.objects_in_mode:
			if armature.animation_data:
				self.select(armature)		
		#TODO Current frame
		return {'FINISHED'}


def select_keyed_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('armature.select_keyed_bones')


classes = {
	Armature_OT_Bone_Type,
	Armature_OT_Bone_Devide,
	Armature_OT_Freeze,
	Armature_OT_Select_Keyed_Bone
}


def register_bone():
	for cls in classes:
		register_class(cls)
	
	bpy.types.VIEW3D_MT_select_pose.append(select_keyed_menu)


def unregister_bone():
	bpy.types.VIEW3D_MT_select_pose.remove(select_keyed_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_bone()