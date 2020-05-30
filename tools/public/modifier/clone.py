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
from bpy.props import BoolProperty,StringProperty

class Modifier_OT_CopyToSelection(Operator):
	bl_idname = "modifier.copy_to_selection"
	bl_label = "Copy to Selection"

	expanded_only: BoolProperty()

	def execute(self, ctx):
		modifiers = []
		for modifier in ctx.active_object.modifiers:
			if modifier.show_expanded or self.expanded_only:
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

class Modifier_OT_MatchSelection(Operator):
	bl_idname = "modifier.match_selection"
	bl_label = "Match Selection"

	name: StringProperty()

	def execute(self, ctx):
		if self.name in ctx.active_object.modifiers:
			modifier = ctx.active_object.modifiers[self.name]
			properties = []
			for prop in modifier.bl_rna.properties:
				if not prop.is_readonly:
					properties.append(prop.identifier)
		else:
			return{"FINISHED"}

		for obj in ctx.selected_objects:
			if obj != ctx.active_object:
				for m in obj.modifiers:
					if m.type == modifier.type:
						for prop in properties:
							setattr(m, prop, getattr(modifier, prop))
		
		return{"FINISHED"}


# TODO add to modifire panel
# More tools copy props, delet modifiers

classes = [Modifier_OT_CopyToSelection, Modifier_OT_MatchSelection]

def register_clone():
	[bpy.utils.register_class(c) for c in classes]

def unregister_clone():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	register_clone()