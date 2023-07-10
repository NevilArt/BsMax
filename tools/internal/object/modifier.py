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
from bpy.props import EnumProperty



class Modifier_OT_Copy_Selected(Operator):
	bl_idname = "modifier.copy_selected"
	bl_label = "Copy Selected Modifiers"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, ctx):
		return True

	def get_modifiers(self, ctx):
		return [(mod.name, mod.name, '') for mod in ctx.object.modifiers]

	modifiers: EnumProperty(
		name='Modifiers',
		description='List of modifiers to copy', 
		items=get_modifiers,
		options={"ENUM_FLAG"}
	)

	def draw(self,ctx):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'modifiers')

	def copy_modifier(self, ctx, name):
		surce = ctx.object
		targets = [obj for obj in ctx.selected_objects
					if obj != surce and obj.type == surce.type]

		for obj in targets:
			source = surce.modifiers[name]

			destanation = obj.modifiers.get(source.name, None)
			if not destanation:
				destanation = obj.modifiers.new(source.name, source.type)

			# collect names of writable properties
			properties = [p.identifier for p in source.bl_rna.properties
						  if not p.is_readonly]

			# copy those properties
			for prop in properties:
				setattr(destanation, prop, getattr(source, prop))

	def execute(self, ctx):
		for name in self.modifiers:
			self.copy_modifier(ctx, name)
		return{"FINISHED"}

	def invoke(self,ctx,event):
		return ctx.window_manager.invoke_props_dialog(self)



def register_modifier():
	bpy.utils.register_class(Modifier_OT_Copy_Selected)



def unregister_modifier():
	bpy.utils.unregister_class(Modifier_OT_Copy_Selected)



if __name__ == "__main__":
	register_modifier()