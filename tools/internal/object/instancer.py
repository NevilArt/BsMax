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
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


class OBJECT_TO_Data_Auto_Rename(Operator):
	""" Object.Data.Name = Object.Name in selection """
	bl_idname = 'object.data_auto_rename'
	bl_label = 'Data Auto Rename'
	bl_description = 'Copy Object Name to Data Name much as possible'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		for obj in ctx.selected_objects:
			obj.data.name = obj.name
		
		return{"FINISHED"}


class Object_TO_Make_Unique(Operator):
	""" Unlink selected objects data, keep in group relation """
	bl_idname = 'object.make_unique'
	bl_label = 'Make Unique'
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Make Unique Selected Instance Object"

	group: BoolProperty(
		name="Keep In group with each other", default=True,
		description="Keep selected groupe with each others"
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			return ctx.object.data.users > 1
		return False
	
	def draw(self, _):
		layout = self.layout
		layout.prop(self, 'group')
		if self.group:
			layout.label(
				text="Keep Instance with each other"
			)
		else:
			layout.label(
				text="Convert to all unique objects"
			)
	
	def execute(self, ctx):
		newData = ctx.object.data.copy()
		instances = [
			obj for obj in ctx.selected_objects
			if obj.data == ctx.object.data
		]

		for obj in instances:
			obj.data = newData if self.group else obj.data.copy()
		
		return{"FINISHED"}
	
	def invoke(self, ctx, _):
		if len(ctx.selected_objects) > 1:
			return ctx.window_manager.invoke_props_dialog(self)

		self.execute(ctx)
		return{"FINISHED"}
	

def make_unique_menu(self, _):
	self.layout.operator('object.make_unique')


classes = {
	OBJECT_TO_Data_Auto_Rename,
	Object_TO_Make_Unique
}


def register_instancer():
	for c in classes: 
		register_class(c)
	
	bpy.types.VIEW3D_MT_object_relations.append(make_unique_menu)


def unregister_instancer():
	for c in classes:
		unregister_class(c)
	
	bpy.types.VIEW3D_MT_object_relations.remove(make_unique_menu)


if __name__ == '__main__':
	register_instancer()