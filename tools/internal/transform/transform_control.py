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

from mathutils import Vector

from bpy.types import Operator, Menu
from bpy.props import BoolProperty

from bsmax.bsmatrix import (
				    matrix_from_elements,
					matrix_to_array,
					array_to_matrix
					)
from bsmax.actions import (
					freeze_transform,
					copy_array_to_clipboard,
					paste_array_from_clipboard
					)



class Object_OT_Freeze_Transform(Operator):
	""" Copy selected objects transform to Delta transform and
		reset transform values
	"""
	bl_idname = "object.freeze_transform"
	bl_label = "Freeze Transform"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	location: BoolProperty(name="Location", default=True)
	rotation: BoolProperty(name="Rotation", default=True)
	scale: BoolProperty(name="Scale", default=True)
	
	def execute(self, ctx):
		freeze_transform(ctx.selected_objects,
			location=self.location,
			rotation=self.rotation,
			scale=self.scale)
		return{"FINISHED"}



class Object_OT_Transform_To_Zero(Operator):
	""" Clare transform """
	bl_idname = "object.transform_to_zero"
	bl_label = "Transform To Zero"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	location: BoolProperty(name="Location", default=True)
	rotation: BoolProperty(name="Rotation", default=True)
	scale: BoolProperty(name="Scale", default=True)
	
	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			if self.location:
				bpy.ops.object.location_clear(clear_delta=False)
			if self.rotation:
				bpy.ops.object.rotation_clear(clear_delta=False)
			if self.scale:
				bpy.ops.object.scale_clear(clear_delta=False)

		elif ctx.mode == 'POSE':
			if self.location:
				bpy.ops.pose.loc_clear()
			if self.rotation:
				bpy.ops.pose.rot_clear()
			if self.scale:
				bpy.ops.pose.scale_clear()

		return{"FINISHED"}



class Object_OT_Transform_Copy(Operator):
	""" Copy Transform to buffer """
	bl_idname = "object.transform_copy"
	bl_label = "Copy Transform"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT' and ctx.active_object

	def execute(self, ctx):
		copy_array_to_clipboard('BSMAXTRANSFORMCLIPBOARD',
								matrix_to_array(ctx.object.matrix_world))
		return{"FINISHED"}



def get_clipboard_key():
	string = bpy.context.window_manager.clipboard
	lines = string.splitlines()
	if lines:
		return lines[0]
	return None



class Object_OT_Transform_Paste(Operator):
	""" Paste transform from buffer """
	bl_idname = "object.transform_paste"
	bl_label = "Paste Transform"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT' and ctx.active_object
		
	def execute(self, ctx):
		key = get_clipboard_key()

		if key == 'BSMAXTRANSFORMCLIPBOARD':

			array = paste_array_from_clipboard('BSMAXTRANSFORMCLIPBOARD')
			if array:
				matrix_world = array_to_matrix(array)

				if matrix_world:
					ctx.object.matrix_world = matrix_world
		
		elif key == "BSMAXTRANSFORMCLIPBOARDV2":
			lines = (bpy.context.window_manager.clipboard).splitlines()
			cbData = [float(f) for f in lines[1].split(",")]

			location = Vector((cbData[0], cbData[1], cbData[2]))
			rotation = Vector((cbData[3], cbData[4], cbData[5]))
			scale = Vector((cbData[6], cbData[7], cbData[8]))
			
			matrix = matrix_from_elements(
							location=location,
							euler_rotation=rotation,
							scale=scale
			)
			ctx.object.matrix_world = matrix
			# print(matrix)
		
		return{"FINISHED"}



#TODO for now is ok but need to move to better place if add more items
class Object_MT_Object_Copy(Menu):
	bl_idname = "OBJECT_MT_object_copy"
	bl_label = "Copy"

	def draw(self, ctx):
		layout=self.layout
		layout.operator("view3d.copybuffer", text="Object")
		layout.operator("object.transform_copy", text="Transform")



class Object_MT_Object_Paste(Menu):
	bl_idname = "OBJECT_MT_object_paste"
	bl_label = "Paste"

	def draw(self, ctx):
		layout=self.layout
		layout.operator("view3d.pastebuffer", text="Object")
		layout.operator("object.transform_paste", text="Transform")



classes = (
	Object_OT_Freeze_Transform,
	Object_OT_Transform_To_Zero, 
	Object_OT_Transform_Copy,
	Object_OT_Transform_Paste,
	Object_MT_Object_Copy,
	Object_MT_Object_Paste
)



def register_transform_control():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_transform_control():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_transform_control()