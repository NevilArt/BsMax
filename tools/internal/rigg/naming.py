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

from bpy.types import Operator



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



def is_unnamed(name):
	return False



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
		
		elif is_unnamed(self.name):
			#TODO
			# get bone direction
			# create a name depend of location
			pass

	def get_blender_name(self):
		if self.direction:
			return self.base + "." + self.direction
		return self.name



class Armature_TO_auto_side_rename(Operator):
	bl_idname = 'armature.auto_direction_rename'
	bl_label = 'Armature Auto Rename'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode in ('EDIT_ARMATURE', 'POSE')

	def execute(self, ctx):
		for bone in ctx.object.data.bones:
			boneName = BoneName(name=bone.name)
			bone.name = boneName.get_blender_name()
		return{"FINISHED"}



def register_naming():
	bpy.utils.register_class(Armature_TO_auto_side_rename)



def unregister_naming():
	bpy.utils.unregister_class(Armature_TO_auto_side_rename)



if __name__ == "__main__":
	register_naming()