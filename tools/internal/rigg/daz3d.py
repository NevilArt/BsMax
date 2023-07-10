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

from mathutils import Vector

from bpy.types import Operator
from bpy.props import EnumProperty



def is_blender_name(name):
	if len(name) < 2:
		return False
	return name[-2] == '.' and name[-1].lower() in ('r', 'l')



def is_daz3d_name(name):
	if len(name) < 2:
		return False
	
	if name[0] in ('r', 'l') and name[-2] != '.':
		return True
	
	parts = name.split(' ')
	if parts[0].lower() in ('left', 'right'):
		return True



def get_blender_bone_name_direction(name):
	return name[-1]



def get_blender_bone_name_base(name):
	return name[:-2]



def get_daz3d_bone_name_direction(name):
	if name[0] in ('r', 'l') and name[-2] != '.':
		return name[0]
	
	parts = name.split(' ')
	if parts[0].lower() in ('left', 'right'):
		return parts[0].lower()
	
	if parts[-1].lower in ('left', 'right'):
		return parts[-1]
	
	return ""



def get_das3d_bone_name_base(name):
	if name[0] in ('r', 'l') and name[-2] != '.':
		return name[1:]
	
	parts = name.split(' ')
	if parts[0].lower() in ('left', 'right'):
		retName = ""
		for part in parts[1:-1]:
			retName += part + " "
		retName += parts[-1]
		return retName
	
	return ""



class BoneName:
	def __init__(self, name):
		self.name = name
		self.direction = None
		self.base = None
		self.scan()
	
	def scan(self):
		if is_blender_name(self.name):
			self.direction = get_blender_bone_name_direction(self.name)
			self.base = get_blender_bone_name_base(self.name)
		
		elif is_daz3d_name(self.name):
			self.direction = get_daz3d_bone_name_direction(self.name)
			self.base = get_das3d_bone_name_base(self.name)

	def get_blender_name(self):
		if self.direction:
			return self.base + "." + self.direction
		return self.name
	
	def get_daz3d_Name(self):
		if self.direction:
			if len(self.direction) > 1:
				return self.direction + " " + self.base
			return self.direction + self.base
		return self.name
	


def rename_bones_to_daz3d_standard(armature):
	for bone in armature.data.bones:
		boneName = BoneName(name=bone.name)
		bone.name = boneName.get_daz3d_Name()



def rename_bones_to_blender_standard(armature):
	for bone in armature.data.bones:
		boneName = BoneName(name=bone.name)
		bone.name = boneName.get_blender_name()



class Armature_TO_daz3d_auto_rename(Operator):
	bl_idname = 'armature.daz3d_auto_rename'
	bl_label = 'Daz3D Armature Autor Rename'
	bl_options = {'REGISTER', 'UNDO'}

	direction: EnumProperty(
		items=[
			("BLENDER", "To Blender", "Rename Bones to Blender Standard"),
			("DAZ", "To Daz3D", "Rename Armature Bones to Daz3D standard")
		]
	)
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode in ('EDIT_ARMATURE', 'POSE')

	def draw(self, ctx):
		self.layout.prop(self, 'direction', text='')
	
	def execute(self,ctx):

		if self.direction == "DAZ":
			rename_bones_to_daz3d_standard(ctx.object)
		else:
			rename_bones_to_blender_standard(ctx.object)

		return{"FINISHED"}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self, width=400)



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



class Armature_TO_daz3d_auto_bone_align(Operator):
	bl_idname = 'armature.daz3d_auto_bone_align'
	bl_label = 'Daz3D Armature Autor Bone Align'
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



classes = (
	Armature_TO_daz3d_auto_rename,
	Armature_TO_daz3d_auto_bone_align
)
	


def register_daz3d():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_daz3d():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_daz3d()