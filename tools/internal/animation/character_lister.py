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
# 2024/05/26

import bpy

from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class
from bsmax.actions import set_as_active_object


class CharacterSet:
	def __init__(self):
		self.characters = []
	
	def get_scene_characters(self):
		self.characters = [
			char for char in bpy.data.objects
			if char.type == 'ARMATURE'
		]
	
	def get_character_by_name(self, name):
		for char in self.characters:
			if char.name == name:
				return char
		return None

character_set = CharacterSet()


class Armature_TO_Character_Hide(Operator):
	""" Hide/Unhide Character (for now only Armature) """
	bl_idname = 'anim.character_hide'
	bl_label = "Character Hide"
	bl_description = ""
	bl_options={'REGISTER', 'INTERNAL'}

	name: StringProperty(default="") # type: ignore

	def execute(self, _):
		character = character_set.get_character_by_name(self.name)
		if character:
			state = not character.hide_viewport
			character.hide_viewport = state
			character.hide_render = False
			character.hide_select = False

		return{'FINISHED'}


class Armature_TO_Character_Isolate(Operator):
	""" Isolate only this Character (for now only Armature) """
	bl_idname = 'anim.character_isolate'
	bl_label = "Character Isolate"
	bl_description = ""
	bl_options={'REGISTER', 'INTERNAL'}

	name: StringProperty(default="") # type: ignore

	def execute(self, _):
		character = character_set.get_character_by_name(self.name)
		if character:
			for char in character_set.characters:
				if char != character:
					char.hide_viewport = True
					char.hide_render = True
					char.hide_select = True
				else:
					char.hide_viewport = False
					char.hide_render = False
					char.hide_select = False

		return{'FINISHED'}


class Armature_TO_Character_Rest(Operator):
	""" Rest/Pose Switch """
	bl_idname = 'anim.character_rest'
	bl_label = "Character Rest/Pose"
	bl_description = ""
	bl_options={'REGISTER', 'INTERNAL'}

	name: StringProperty(default="") # type: ignore

	def execute(self, _):
		character = character_set.get_character_by_name(self.name)
		if character:
			state = character.data.pose_position
			state = 'POSE' if state == 'REST' else 'REST'
			character.data.pose_position = state

		return{'FINISHED'}


class Anim_TO_Character_Lister(Operator):
	""" List of Character for quick managment """
	bl_idname = 'anim.character_lister'
	bl_label = "Character lister"
	bl_description = ""
	bl_options={'REGISTER'}

	def get_field(self, row, character):
		name = character.name
		row.operator(
			'object.select_by_name', icon='ARMATURE_DATA', text=character.name
		).name = name

		hide_icon = 'HIDE_ON' if character.hide_viewport else 'HIDE_OFF'
		row.operator(
			'anim.character_hide', icon=hide_icon, text=""
		).name = name

		hide_viewport = character.hide_viewport
		isolate_icon = 'RADIOBUT_OFF' if hide_viewport else 'RADIOBUT_ON'
		row.operator(
			'anim.character_isolate', icon=isolate_icon, text=""
		).name = name

		pose_position = character.data.pose_position
		rest_icon = 'ARMATURE_DATA' if pose_position == 'REST' else 'EVENT_T'
		row.operator(
			'anim.character_rest', icon=rest_icon, text=""
		).name = name

	def draw(self, _):
		box = self.layout.box()
		col = box.column()
		row = col.row()
		row.label(text="")
		for character in character_set.characters:
			self.get_field(col.row(align=True), character)
	
	def execute(self, _):
		return{'FINISHED'}

	def invoke(self, ctx, _):
		""" collect armature objects in scene """
		character_set.get_scene_characters()
		return ctx.window_manager.invoke_props_dialog(self,width=200)


class Object_TO_Make_Override_Library_plus(Operator):
	""" Convert Multiple selection to library overide """
	bl_idname = 'object.make_override_library_multi'
	bl_label = "Make Library Override (Multi)"
	bl_description = ""
	bl_options={'REGISTER'}

	@classmethod
	def poll(self, _):
		return bpy.ops.object.make_override_library.poll()
	
	def execute(self, ctx):
		objs = []
		for obj in ctx.selected_objects:
			if obj.type == 'EMPTY':
				if obj.instance_type == 'COLLECTION':
					objs.append(obj)

		bpy.ops.object.select_all(action='DESELECT')

		for obj in objs:
			set_as_active_object(ctx, obj)
			if bpy.ops.object.make_override_library.poll():
				bpy.ops.object.make_override_library()

		return{'FINISHED'}


def library_override_menu(self, _):
	self.layout.operator('object.make_override_library_multi')


classes = {
	Armature_TO_Character_Hide,
	Armature_TO_Character_Isolate,
	Armature_TO_Character_Rest,
	Anim_TO_Character_Lister,
	Object_TO_Make_Override_Library_plus
}


def register_character_lister():
	for cls in classes:
		register_class(cls)

	bpy.types.VIEW3D_MT_object_relations.prepend(library_override_menu)
	

def unregister_character_lister():
	bpy.types.VIEW3D_MT_object_relations.remove(library_override_menu)

	for cls in classes:
		unregister_class(cls)

if __name__ == "__main__":
	register_character_lister()