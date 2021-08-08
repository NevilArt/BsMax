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

class View3D_OT_Copy_Data(Operator):
	bl_idname = "view3d.copy_data"
	bl_label = "Copy Object/Data"
	bl_options = {'REGISTER'}

	object: BoolProperty(name='Object', default=True)
	material: BoolProperty(name='Material', default=False)
	modifier: BoolProperty(name='Modifier', default=False)
	animation: BoolProperty(name='Animation', default=False)

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def draw(self,ctx):
		layout = self.layout
		box = layout.box()
		box.prop(self, 'object')
		if len(ctx.selected_objects) == 1:
			box.prop(self, 'material')
			box.prop(self, 'modifier')
			box.prop(self, 'animation')
	
	def create_buffer_object(self, ctx, name):
		source = ctx.active_object
		''' Create buffer object '''
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.mesh.primitive_cube_add()
		ctx.active_object.name = name
		target = ctx.active_object
		''' Active Source Object '''
		source.select_set(state=True)
		ctx.view_layer.objects.active = source
		return target
	
	def send_to_buffer(self, ctx, target):
		bpy.ops.object.select_all(action='DESELECT')
		target.select_set(state=True)
		ctx.view_layer.objects.active = target
		bpy.ops.view3d.copybuffer()
		bpy.ops.object.delete_plus()

	def execute(self, ctx):
		if self.object:
			bpy.ops.view3d.copybuffer()
		
		if self.material:
			target = self.create_buffer_object(ctx,
				'BsMax_Copy_Past_Material_Temprary_Object')
			bpy.ops.object.make_links_data(type='MATERIAL')
			# self.send_to_buffer(target)
		
		if self.modifier:
			target = self.create_buffer_object(ctx, 
				'BsMax_Copy_Past_Modifier_Temprary_Object')
			bpy.ops.object.make_links_data(type='MODIFIERS')
			self.send_to_buffer(target)
		
		if self.animation:
			target = self.create_buffer_object(ctx,
				'BsMax_Copy_Past_Animation_Temprary_Object')
			bpy.ops.object.make_links_data(type='ANIMATION')
			self.send_to_buffer(target)
		
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self, width=100)

classes = [View3D_OT_Copy_Data]

def register_copy_past():
	[bpy.utils.register_class(c) for c in classes]

def unregister_copy_past():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_copy_past()