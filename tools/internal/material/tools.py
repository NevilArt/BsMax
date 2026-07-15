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
# 2024/02/25
# 2026/07/15 auto texture renamer operator added

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


def get_main_shader(material):
	for node in material.node_tree.nodes:
		if node.type == 'OUTPUT_MATERIAL':
			pass #TODO


def rename_texture(material, obj_name):
	for node in material.node_tree.nodes:
		pass


class Object_TO_Material_Slot_Remove_Plus(Operator):
	bl_idname = 'object.material_slot_remove_plus'
	bl_label = 'Remove Material Slot'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	bl_description = "Remove The Selected Material Slot"
	
	@classmethod
	def poll(self, context):
		return context.mode == 'EDIT_MESH'
	
	def execute(self,context):
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		bpy.ops.object.material_slot_remove()
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		return{'FINISHED'}
	

class Object_TO_Auto_Texture_Rename(Operator):
	bl_idname = 'object.auto_texture_rename'
	bl_label = 'Auto Texture Rename'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	bl_description = "Auto Rename Textures Based on Object Name"

	@classmethod
	def poll(self, context):
		return context.mode == 'OBJECT'
	
	def rename_texture(self, obj):
		if obj.type != 'MESH':
			return
		
		if len(obj.data.materials) != 1:
			return
		
		matterial = obj.data.materials[0]
		rename_texture(matterial, obj.name)

	def execute(self, context):
		for obj in context.selected_objects:
			self.rename_texture(obj)

		return {'FINISHED'}


classes = {
	Object_TO_Material_Slot_Remove_Plus,
	Object_TO_Auto_Texture_Rename
}


def register_tools():
	for cls in classes:
		register_class(cls)


def unregister_tools():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_tools()