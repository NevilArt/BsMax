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
# 2024/08/30

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty


def create_buffer_object(ctx, name):
	source = ctx.object
	''' Create buffer object '''
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_cube_add()
	ctx.object.name = name
	target = ctx.active_object
	''' Active Source Object '''
	source.select_set(state=True)
	ctx.view_layer.objects.active = source
	return target


def send_to_buffer(ctx, target):
	bpy.ops.object.select_all(action='DESELECT')
	target.select_set(state=True)
	ctx.view_layer.objects.active = target
	bpy.ops.view3d.copybuffer()
	bpy.ops.object.delete_plus()


class View3D_OT_Copy_Data(Operator):
	bl_idname = 'view3d.copy_data'
	bl_label = "Copy Object / Data"
	bl_options = {'REGISTER'}

	object: BoolProperty(name='Object', default=True) # type: ignore
	material: BoolProperty(name='Material', default=False) # type: ignore
	modifier: BoolProperty(name='Modifier', default=False) # type: ignore
	animation: BoolProperty(name='Animation', default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.selected_objects
		return False
	
	def draw(self,ctx):
		layout = self.layout
		box = layout.box()
		box.prop(self, 'object')
		if len(ctx.selected_objects) == 1:
			box.prop(self, 'material')
			box.prop(self, 'modifier')
			box.prop(self, 'animation')

	def execute(self, ctx):
		if self.object:
			bpy.ops.view3d.copybuffer()
		
		if self.material:
			name = "BsMax_Copy_Past_Material_Temprary_Object"
			target = create_buffer_object(ctx, name)
			bpy.ops.object.make_links_data(type='MATERIAL')
			# send_to_buffer(target)
		
		if self.modifier:
			name = "BsMax_Copy_Past_Modifier_Temprary_Object"
			target = create_buffer_object(ctx, name)
			bpy.ops.object.make_links_data(type='MODIFIERS')
			send_to_buffer(target)
		
		if self.animation:
			name = "BsMax_Copy_Past_Animation_Temprary_Object"
			target = create_buffer_object(ctx, name)
			
			bpy.ops.object.make_links_data(type='ANIMATION')
			send_to_buffer(target)
		
		return{'FINISHED'}
	
	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self, width=100)


def register_copy_past():
	bpy.utils.register_class(View3D_OT_Copy_Data)


def unregister_copy_past():
	bpy.utils.unregister_class(View3D_OT_Copy_Data)


if __name__ == '__main__':
	register_copy_past()