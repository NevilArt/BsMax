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
# 2026/08/02 Hair Style On/Off added

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty


def get_hair_objects_with_multiple_geonodes():
	result = []

	for obj in bpy.data.objects:
		if obj.type != 'CURVES':
			continue

		geonode_count = sum(1 for mod in obj.modifiers if mod.type == 'NODES')

		if geonode_count > 1:
			result.append(obj)

	return result


def set_hair_modifiers_viewport_state(obj, state):
	for mod in obj.modifiers:
		if mod.type != 'NODES':
			continue

		if mod.show_render:
			mod.show_viewport = state
		else:
			mod.show_viewport = not state


class OBJECT_OT_hair_style_on_off(Operator):
	bl_idname = "object.hair_style_set"
	bl_label = "Set Hair Style State"
	bl_description = "Sets the hair style effect on or off"
	bl_options = {'REGISTER', 'UNDO'}

	state: BoolProperty(
		name="Hair Style On",
		description="True = On, False = Off",
		default=False
	) # type: ignore

	def execute(self, context):
		objs = get_hair_objects_with_multiple_geonodes() 

		for obj in objs:
			set_hair_modifiers_viewport_state(obj, self.state)

		return {'FINISHED'}

def draw_hair_style_toggle(self, context):
	layout = self.layout
	obj = context.object

	layout.label(text="Hair Style")
	row = layout.row(align=True)
	row.operator("object.hair_style_set", text="On").state = True
	row.operator("object.hair_style_set", text="Off").state = False


classes = {
	OBJECT_OT_hair_style_on_off
}

def register_simplify():
	for cls in classes:
		register_class(cls)

	bpy.types.CYCLES_RENDER_PT_curves.append(draw_hair_style_toggle)
	bpy.types.RENDER_PT_eevee_hair.append(draw_hair_style_toggle)


def unregister_simplify():
	bpy.types.CYCLES_RENDER_PT_curves.remove(draw_hair_style_toggle)
	bpy.types.RENDER_PT_eevee_hair.remove(draw_hair_style_toggle)

	for cls in classes:
		unregister_class(cls)


if __name__ == "__main__":
	register_simplify()