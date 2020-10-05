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

class Object_OT_Collaps_Modifiers(Operator):
	bl_idname = "object.collaps_modifiers"
	bl_label = "Apply All Modifiers"
	# bl_description = ""

	target: bpy.props.EnumProperty(default='MESH',items=[('MESH','Mesh',''),('CURVE','Curve','')])

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == "EDIT_MESH"
	# len(ctx.active_object.modifiers) > 0

	def draw(self,ctx):
		self.layout.label(text="(Click out for No)")
	
	def execute(self, ctx):
		selected_objects = ctx.selected_objects.copy()
		bpy.ops.object.select_all(action='DESELECT')
		for obj in selected_objects:
			obj.select_set(True)
			for modifier in ctx.active_object.modifiers:
				bpy.ops.object.modifier_apply(modifier=modifier.name)
			obj.select_set(False)
		for obj in selected_objects:
			obj.select_set(True)
		bpy.ops.primitive.cleardata('INVOKE_DEFAULT')
		bpy.ops.object.convert(target=self.target)
		return{"FINISHED"}
	
	def cancel(self,ctx):
		return None

	def invoke(self,ctx,event):
		return ctx.window_manager.invoke_props_dialog(self)

class Object_OT_Convert(Operator):
	bl_idname = "object.smart_convert"
	bl_label = "Smart Convert"
	# bl_description = ""

	target: bpy.props.EnumProperty(default='MESH',items=[('MESH','Mesh',''),('CURVE','Curve','')])

	def execute(self, ctx):
		if len(ctx.active_object.modifiers) > 0:
			bpy.ops.object.collaps_modifiers(target=self.target)
		else:
			bpy.ops.primitive.cleardata('INVOKE_DEFAULT')
			bpy.ops.object.convert(target=self.target)
		return{"FINISHED"}
classes = [Object_OT_Collaps_Modifiers, Object_OT_Convert]

def register_convert():
	[bpy.utils.register_class(c) for c in classes]

def unregister_convert():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_convert()