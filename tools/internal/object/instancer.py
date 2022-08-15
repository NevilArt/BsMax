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
from bpy.props import BoolProperty



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



class Object_TO_Instancer_Select(Operator):
	""" collect and select object may suld be instance """
	bl_idname = 'object.instancer_select'
	bl_label = 'Instancer Select'
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		# collect ans select object has data with siliar name
		return{"FINISHED"}



class Object_TO_Make_Unique(Operator):
	bl_idname = 'object.make_unique'
	bl_label = 'Make Unique'
	bl_options = {'REGISTER', 'UNDO'}

	make_unique: BoolProperty(name="Make Unique")
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'make_unique')
		if self.make_unique:
			text='Make each object has unique data'
		else:
			text = "Keep selected object linked with each other"
		layout.label(text=text)
	
	def is_linked(self, objs):
		for obj in objs:
			if objs[0].data != obj.data:
				return False
		return True
	
	def execute(self,ctx):
		objs = ctx.selected_objects
		if self.is_linked(objs):
			if self.make_unique:
				for obj in objs:
					obj.data = obj.data.copy()
				return{"FINISHED"}

			if len(objs) > 1:
				data = objs[0].data.copy()
				for obj in objs:
					obj.data = data

		return{"FINISHED"}
	


def make_unique_menu(self, ctx):
	self.layout.operator('object.make_unique')

classes = (OBJECT_TO_Data_Auto_Rename, Object_TO_Make_Unique)

def register_instancer():
	for c in classes:
		bpy.utils.register_class(c)
	
	bpy.types.VIEW3D_MT_object_relations.append(make_unique_menu)


def unregister_instancer():
	bpy.types.VIEW3D_MT_object_relations.remove(make_unique_menu)

	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_instancer()