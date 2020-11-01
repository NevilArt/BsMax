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
from bpy.props import StringProperty

class CharacterSet:
	def __init__(self):
		self.enabled = False
		self.characters = []
	
	def get_scene_characters(self):
		self.characters = [char for char in bpy.data.objects if char.type == 'ARMATURE']
	
	def get_character_by_name(self, name):
		for char in self.characters:
			if char.name == name:
				return char
		return None

cs = CharacterSet()



class Armature_TO_Character_Hide(Operator):
	""" Hide/Unhide Character (for now only Armature) """
	bl_idname = "anim.character_hide"
	bl_label = "Character Hide"
	name: StringProperty(default="")

	@classmethod
	def poll(self, ctx):
		return cs.enabled
	
	def execute(self,ctx):
		character = cs.get_character_by_name(self.name)
		if character:
			state = not character.hide_viewport
			character.hide_viewport = state
			character.hide_render = False
			character.hide_select = False
		return{"FINISHED"}



class Armature_TO_Character_Isolate(Operator):
	""" Isolate only this Character (for now only Armature) """
	bl_idname = "anim.character_isolate"
	bl_label = "Character Isolate"
	name: StringProperty(default="")

	@classmethod
	def poll(self, ctx):
		return cs.enabled
	
	def execute(self,ctx):
		character = cs.get_character_by_name(self.name)
		if character:
			for char in cs.characters:
				if char != character:
					char.hide_viewport = True
					char.hide_render = True
					char.hide_select = True
				else:
					char.hide_viewport = False
					char.hide_render = False
					char.hide_select = False
		return{"FINISHED"}



class Armature_TO_Character_Rest(Operator):
	""" Rest/Pose Switch """
	bl_idname = "anim.character_rest"
	bl_label = "Character Rest/Pose"
	name: StringProperty(default="")

	@classmethod
	def poll(self, ctx):
		return cs.enabled
	
	def execute(self,ctx):
		character = cs.get_character_by_name(self.name)
		if character:
			state = character.data.pose_position
			state = 'POSE' if state == 'REST' else 'REST'
			character.data.pose_position = state
		return{"FINISHED"}



class Anim_TO_Character_Lister(Operator):
	""" List of Character for quick managment """
	bl_idname = "anim.character_lister"
	bl_label = "Character lister"

	def get_field(self,row,character):
		name = character.name
		row.operator("object.select_by_name", icon='ARMATURE_DATA', text=character.name).name = name
		
		hide_icon = 'HIDE_ON' if character.hide_viewport else 'HIDE_OFF'
		row.operator("anim.character_hide", icon=hide_icon, text='').name = name
		
		isolate_icon = 'RADIOBUT_OFF' if character.hide_viewport else 'RADIOBUT_ON'
		row.operator("anim.character_isolate", icon=isolate_icon, text='').name = name
		
		rest_icon = 'ARMATURE_DATA' if character.data.pose_position == 'REST' else 'EVENT_T'
		row.operator("anim.character_rest", icon=rest_icon, text='').name = name

	def draw(self,ctx):
		box = self.layout.box()
		col = box.column()
		row = col.row()
		row.label(text='')
		for character in cs.characters:
			self.get_field(col.row(align=True), character)
	
	def execute(self,ctx):
		self.report({'INFO'},'bpy.ops.anim.character_lister()')
		cs.enabled = False
		return{"FINISHED"}
	
	def cancel(self,ctx):
		cs.enabled = False
	
	def invoke(self,ctx,event):
		""" collect armature objects in scene """
		cs.get_scene_characters()
		cs.enabled = True
		return ctx.window_manager.invoke_props_dialog(self,width=200)



classes = [Armature_TO_Character_Hide,
	Armature_TO_Character_Isolate,
	Armature_TO_Character_Rest,
	Anim_TO_Character_Lister]

def register_character_lister():
	[bpy.utils.register_class(c) for c in classes]

def unregister_character_lister():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_character_lister()