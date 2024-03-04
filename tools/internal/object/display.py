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
# 2024/03/03

import bpy

from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty, StringProperty
from bpy.utils import register_class, unregister_class

from bsmax.actions import set_as_active_object


class Object_TO_Select_By_Name(Operator):
	bl_idname = "object.select_by_name"
	bl_label = "Select Object By Name"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	name: StringProperty(default="")
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		bpy.ops.object.select_all(action='DESELECT')

		if self.name:
			set_as_active_object(ctx, bpy.data.objects[self.name])

		return{"FINISHED"}


class Object_OT_Freeze(Operator):
	bl_idname = "object.freeze"
	bl_label = "Freeze / Unfreeze"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	mode: EnumProperty(
		items=[
			('SELECTION', 'Freeze Selection', ''),
			('UNSELECTED', 'Freeze Unselected', ''),
			('CLEAR', 'Unfreezee All', '')
		],
		default='SELECTION'
	)
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def execute(self, ctx):
		if self.mode == 'SELECTION':
			for obj in ctx.selected_objects:
				obj.hide_select = True
				obj.display_type = 'SOLID'

		elif self.mode == 'UNSELECTED':
			for obj in bpy.data.objects:
				if not obj.select_get():
					obj.hide_select = True
					obj.display_type = 'SOLID'

		elif self.mode == 'CLEAR':
			for obj in bpy.data.objects:
				obj.hide_select = False
				obj.display_type = 'TEXTURED'

			# TODO open a dialog and ask for unreaze layers
			for collection in bpy.data.collections:
				collection.hide_select = False

		return{"FINISHED"}


class Object_OT_Hide(Operator):
	bl_idname = "object.hide"
	bl_label = "Hide/Unhide"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	mode: EnumProperty(
		items=[
			('SELECTION', 'Hide Selection', 'Hide Selected Objects'),
			('UNSELECTED', 'Hide Unselected', 'Hide Unselected Objects'),
			('CLEAR', 'Unhide All', 'Unhide all hidden Objects')
		],
		default='SELECTION'
	)

	collection: BoolProperty(default=False)

	def execute(self, ctx):
		if self.mode == 'SELECTION':
			for obj in ctx.selected_objects:
				obj.hide_viewport = True

		elif self.mode == 'UNSELECTED':
			for obj in bpy.data.objects:
				if not obj.select_get():
					obj.hide_viewport = True

		elif self.mode == 'CLEAR':
			if self.collection:
				for collection in bpy.data.collections:
					collection.hide_viewport = False

			for obj in bpy.data.objects:
				obj.hide_viewport = False

			bpy.ops.object.hide_view_clear('INVOKE_DEFAULT')

		return{"FINISHED"}


classes = (
	Object_OT_Freeze,
	Object_OT_Hide,
	Object_TO_Select_By_Name
)


def register_display():
	for c in classes:
		register_class(c)


def unregister_dispaly():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_display()