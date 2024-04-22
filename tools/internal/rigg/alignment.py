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


def get_bone_tail_location(bone):
	if len(bone.children) == 0:
		return bone.tail
	
	location = Vector((0, 0, 0))
	for child in bone.children:
		location += child.head
	location /= len(bone.children)
	
	return location


def align_bone_to_parent(bone):
	if bone.parent == None:
		return

	parent = bone.parent
	normalVector = (parent.tail - parent.head).normalized()
	bone.tail = bone.head + (bone.length * normalVector)


class Armature_TO_auto_bone_alignment(Operator):
	bl_idname = 'armature.auto_bone_align'
	bl_label = 'Auto Bone Alignment'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_ARMATURE'

	def execute(self,ctx):
		for bone in ctx.object.data.edit_bones:
			bone.tail = get_bone_tail_location(bone)

			if len(bone.children) == 0:
				align_bone_to_parent(bone)

		return{"FINISHED"}


def register_alignment():
	bpy.utils.register_class(Armature_TO_auto_bone_alignment)


def unregister_alignment():
	bpy.utils.unregister_class(Armature_TO_auto_bone_alignment)


if __name__ == "__main__":
	register_alignment()