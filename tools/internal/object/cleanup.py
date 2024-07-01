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
# 2024/06/20

import bpy

from bpy.utils import register_class, unregister_class
from bpy.types import Operator
from bpy.props import EnumProperty


def clear_sculp_mask_data(ctx, objects):
	active_object = ctx.active_object
	customdata_mask_clear = bpy.ops.mesh.customdata_mask_clear
	
	bpy.ops.object.select_all(action='DESELECT')
	
	for object in objects:
		object.select_set(state=True)
		ctx.view_layer.objects.active = object
	
		if customdata_mask_clear.poll():
			customdata_mask_clear()
	
		object.select_set(state=False)

	for object in objects:
		object.select_set(state=True)
	ctx.view_layer.objects.active = active_object


def clear_skin_data(ctx, objects):
	active_object = ctx.active_object
	customdata_skin_clear = bpy.ops.mesh.customdata_skin_clear

	bpy.ops.object.select_all(action='DESELECT')

	for object in objects:
		object.select_set(state=True)
		ctx.view_layer.objects.active = object

		if customdata_skin_clear.poll():
			customdata_skin_clear()

		object.select_set(state=False)

	for object in objects:
		object.select_set(state=True)
	ctx.view_layer.objects.active = active_object


def clear_custom_split_normals_data(ctx, objects):
	active_object = ctx.active_object
	bpy.ops.object.select_all(action='DESELECT')

	for object in objects:
		if not hasattr(object.data, 'has_custom_normals'):
			continue

		if object.data.has_custom_normals:
			object.select_set(state=True)
			ctx.view_layer.objects.active = object
			bpy.ops.mesh.customdata_custom_splitnormals_clear()

		object.select_set(state=False)

	for object in objects:
		object.select_set(state=True)

	ctx.view_layer.objects.active = active_object


def validate_mesh_data(objects):
	for object in objects:
		if hasattr(object.data, 'validate'):
			object.data.validate()


class Mesh_OT_Clear(Operator):
	bl_idname = 'mesh.clear'
	bl_label = "Clear"
	bl_description = "Clear Mesh Data"
	bl_options = {'REGISTER', 'UNDO'}

	action: EnumProperty(
		name="Clear",
		items=[
			('MASK', "Scalpt Mask Data", ""),
			('SKIN', "Skin Data", ""),
			('NORMAL', "Custom Split Normals Data", ""),
			('VALIDATE', "Validate Mesh Data", "")
		]
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'OBJECT'
		return False
	
	def execute(self, ctx):
		if self.action == 'MASK':
			clear_sculp_mask_data(ctx, ctx.selected_objects)

		elif self.action == 'SKIN':
			clear_skin_data(ctx, ctx.selected_objects)

		elif self.action == 'NORMAL':
			clear_custom_split_normals_data(ctx, ctx.selected_objects)
		
		elif self.action == 'VALIDATE':
			validate_mesh_data(ctx.selected_objects)

		return{'FINISHED'}


def cleanup_additional_menu(self, _):
	layout = self.layout
	layout.separator()
	layout.operator(
		'mesh.clear', text="Clear Sculpt Mask Data"
	).action='MASK'

	layout.operator(
		'mesh.clear', text="Clear Skin Data"
	).action='SKIN'

	layout.operator(
		'mesh.clear', text="Clear Custom Split Normals Data"
	).action='NORMAL'

	layout.operator(
		'mesh.clear', text="Validate Mesh Data"
	).action='VALIDATE'


classes = {
	Mesh_OT_Clear
}


def register_cleanup():
	for cls in classes:
		register_class(cls)

	bpy.types.VIEW3D_MT_object_cleanup.append(cleanup_additional_menu)


def unregister_cleanup():
	bpy.types.VIEW3D_MT_object_cleanup.remove(cleanup_additional_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_cleanup()