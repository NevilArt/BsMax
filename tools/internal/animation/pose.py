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
# 2024/05/30

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class


def get_selected_bones(ctx, armature):
	if ctx.mode == 'POSE':
		return [bone for bone in armature.data.bones if bone.select]

	elif ctx.mode == 'EDIT_ARMATURE':
		return [bone for bone in armature.data.edit_bones if bone.select]

	return []


def collect_children(bones):
	children = []
	for bone in bones:
		for child in bone.children:
			if not child.select:
				children.append(child)
				child.select = True
	return children


def select_children(selected, full, extend):
	newSelectionCount = len(selected) # New Selected Count

	if full == True:
		children = selected
		while newSelectionCount != 0:
			children = collect_children(children)
			newSelectionCount = len(children)

	else:
		for bone in selected:
			for child in bone.children:
				child.select = True

			if not extend:
				bone.select = False


def select_parent(selected, extend):
	child_less = []
	for bone in selected:
		if len(bone.children) == 0:
			child_less.append(bone)

		if bone.parent:
			bone.parent.select = True

		if not extend:
			bone.select = False

	if not extend:
		for bone in child_less:
			bone.select = False


#TODO pose tool but works on edit_armature too
# has to rename to armature tool
#TODO in edit armature mode do not select some bone heads has to fix
class Pose_OT_Select_Hierarchy_Plus(Operator):
	bl_idname = "pose.select_hierarchy_plus"
	bl_label = "Select Hierarchy (Plus)"
	bl_description = "Select Parent/Children of selected Bones"
	bl_options = {'REGISTER', 'UNDO'}
	
	full: BoolProperty(default=False) # type: ignore
	extend: BoolProperty(default=False) # type: ignore
	direction: EnumProperty(
		name='Direction',
		items=[
			(
				'PARENT', 'Parent',
    			'Select parent of each selected Bone'
			),
			(
				'CHILDREN', 'Children',
				'Select children of each selected Bone'
			)
		],
		default='CHILDREN'
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode in ('POSE', 'EDIT_ARMATURE')
	
	def execute(self, ctx):
		for armature in ctx.selected_objects:
			if armature.type != 'ARMATURE':
				continue

			selected = get_selected_bones(ctx, armature)

			if self.direction == 'CHILDREN':
				select_children(selected, self.full, self.extend)

			elif self.direction == 'PARENT':
				select_parent(selected, self.extend)

		return{'FINISHED'}


def full_selected_armatures(ctx):
	armatures = [obj for obj in ctx.selected_objects if obj.type == 'ARMATURE']
	fullSelected = []

	for armature in armatures:
		selectedBoneCount = 0

		for bone in armature.data.bones:
			if bone.select:
				selectedBoneCount += 1

		if selectedBoneCount == len(armature.data.bones):
			fullSelected.append(armature)

	return fullSelected


class Pose_OT_Paste_Pose_Plus(Operator):
	bl_idname = 'pose.paste_plus'
	bl_label = "Paste Pose (Plus)"
	bl_description = "Paste Pose on multiply selected Armatures"
	bl_options = {'REGISTER', 'UNDO'}

	flipped: BoolProperty(default=False) # type: ignore
	selected_mask: BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'POSE'

	def execute(self, ctx):
		currentActiveObject = ctx.active_object

		fullSelectedArmatures = full_selected_armatures(ctx)

		if len(fullSelectedArmatures) > 1:
			for armature in fullSelectedArmatures:
				ctx.view_layer.objects.active = armature
				bpy.ops.pose.paste(
					flipped = self.flipped,
					selected_mask = self.selected_mask
				)

			ctx.view_layer.objects.active = currentActiveObject
			return{'FINISHED'}

		bpy.ops.pose.paste(flipped=self.flipped, selected_mask=self.selected_mask)
		return{'FINISHED'}


classes = {
	Pose_OT_Select_Hierarchy_Plus,
	Pose_OT_Paste_Pose_Plus
}


def register_pose():
	for cls in classes:
		register_class(cls)


def unregister_pose():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_pose()