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

class Object_OT_Convert_TO(Operator):
	bl_idname = "object.convert_to"
	bl_label = "Convert to (BsMax)"
	bl_description = "Simulate 3DsMax Convert To operator"
	bl_options = {'REGISTER', 'UNDO'}

	target: bpy.props.EnumProperty(default='MESH',
		items=[('MESH','Mesh',''),('CURVE','Curve',''),
		('GPENCIL','Grease Pencil',''),('POINTCLOUD','Point Cloude','')])

	def execute(self, ctx):
		selected_objects = ctx.selected_objects.copy()
		bpy.ops.object.select_all(action='DESELECT')
		
		for obj in selected_objects:
			obj.select_set(True)
			ctx.view_layer.objects.active = obj
			
			""" clear primitive data """
			if obj.type in {'MESH','CURVE'}:
				obj.data.primitivedata.classname = ""

			""" make unique """
			obj.data = obj.data.copy()
			
			""" collaps modifiers """
			for modifier in obj.modifiers:
				bpy.ops.object.modifier_apply(modifier=modifier.name)
			
			""" set the target mode """
			bpy.ops.object.convert(target=self.target)

			obj.select_set(False)
		
		for obj in selected_objects:
			obj.select_set(True)
		return{"FINISHED"}

class Object_OT_Join_Plus(Operator):
	bl_idname = "object.join_plus"
	bl_label = "Join (Plus)"
	# bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None

	def execute(self, ctx):
		targte = ctx.active_object
		selected_objects = ctx.selected_objects.copy()
		bpy.ops.object.select_all(action='DESELECT')
		
		for obj in selected_objects:
			obj.select_set(True)
			ctx.view_layer.objects.active = obj
			
			""" clear primitive data """
			if obj.type in {'MESH','CURVE'}:
				obj.data.primitivedata.classname = ""

			""" make unique """
			obj.data = obj.data.copy()
			
			""" collaps modifiers """
			for modifier in obj.modifiers:
				bpy.ops.object.modifier_apply(modifier=modifier.name)
			
			obj.select_set(False)

		for obj in selected_objects:
			obj.select_set(True)
		
		targte.select_set(True)
		ctx.view_layer.objects.active = targte

		bpy.ops.object.join()	
		return{"FINISHED"}

classes = [Object_OT_Convert_TO, Object_OT_Join_Plus]

def register_convert():
	[bpy.utils.register_class(c) for c in classes]

def unregister_convert():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_convert()