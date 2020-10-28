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
from bsmax.actions import set_as_active_object

class Light_TO_Character_Set(Operator):
	bl_idname = "anim.character_set"
	bl_label = "character"
	
	name: StringProperty(default="")
	mode: StringProperty(default="")
	
	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self,ctx):
		self.report({'INFO'},'bpy.ops.anim.character_set()')
		return{"FINISHED"}

class Render_TO_Character_Lister(Operator):
	bl_idname = "anim.character_lister"
	bl_label = "Character lister"
	characters = []

	def get_field(self,row,character):
		row.label(text=character.name)

	def draw(self,ctx):
		box = self.layout.box()
		col = box.column()
		row = col.row()
		row.label(text='')
		for character in self.characters:
			self.get_field(col.row(align=True), character)
	
	def execute(self,ctx):
		self.report({'INFO'},'bpy.ops.anim.character_lister()')
		return{"FINISHED"}
	
	def cancel(self,ctx):
		return None
	
	def get_characters(self):
		characters = []
		for character in bpy.data.objects:
			if character.type == 'ARMATURE':
				isnew = True
				for c in characters:
					if character.data == c.data:
						isnew = False
						break
				if isnew:
					characters.append(character)
		return characters

	def invoke(self,ctx,event):
		self.characters = self.get_characters() 
		return ctx.window_manager.invoke_props_dialog(self,width=700)

classes = [Render_TO_Character_Lister, Light_TO_Character_Set]

def register_character_lister():
	[bpy.utils.register_class(c) for c in classes]

def unregister_character_lister():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_character_lister()