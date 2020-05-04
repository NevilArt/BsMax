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
from bpy.types import Operator,Panel

class BsMax_OT_CopyModifiers(Operator):
	bl_idname = "modifier.copy_to_selection"
	bl_label = "Copy to Selection"
	def execute(self, ctx):
		modifiers = []
		for modifier in ctx.active_object.modifiers:
			if modifier.show_expanded:
				properties = []
				for prop in modifier.bl_rna.properties:
					if not prop.is_readonly:
						properties.append(prop.identifier)
				modifiers.append([modifier,properties])

		for obj in ctx.selected_objects:
			if obj != ctx.active_object:
				for modifier in modifiers:
					obj.modifiers.new(modifier[0].name, modifier[0].type)
					for prop in modifier[1]:
						setattr(obj.modifiers[modifier[0].name], prop, getattr(modifier[0], prop))

		return{"FINISHED"}

# TODO add to modifire panel
# More tools copy props, delet modifiers

def register_modifier():
	bpy.utils.register_class(BsMax_OT_CopyModifiers)

def unregister_modifier():
	bpy.utils.unregister_class(BsMax_OT_CopyModifiers)
