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
from bpy.props import EnumProperty, StringProperty

from bsmax.operator import PickOperator



class Armature_OT_Attach(PickOperator):
	bl_idname = 'armature.attach'
	bl_label = 'Attach'
	
	filters = ['AUTO'] #text, curve, mesh

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.object and ctx.mode == 'OBJECT' #edit armature
		return False
	
	def convert(self, ctx, obj):
		obj.select_set(True)
		ctx.view_layer.objects.active = obj
		
		""" collaps modifiers """
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)

		# """ set the target mode """
		# bpy.ops.object.convert(target="MESH")


	def picked(self, ctx, source, subsource, target, subtarget):
		self.report({'OPERATOR'},'bpy.ops.armature.attach()')



class Object_TO_Connect_Script_to_Object(Operator):
	bl_idname = 'object.connect_script_to_object'
	bl_label = 'Connect Script To Active Object'
	# bl_property = 'scripts'
	bl_options = {'REGISTER', 'UNDO'}

	def get_scripts(self, ctx):
		return [((text.name_full, text.name_full, '')) for text in bpy.data.texts]

	scripts: EnumProperty(items=get_scripts)
	name: StringProperty(default='my_script')
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.active_object
		return False

	def draw(self, ctx):
		layout = self.layout
		row = layout.row(align=True)
		row.label(text=('"' + ctx.active_object.name + '"'))
		row.prop(self, 'name', text='')
		row.prop(self, 'scripts', text='')
	
	def execute(self,ctx):
		if self.scripts != '':
			ctx.active_object[self.name] = bpy.data.texts[self.scripts]
		return{"FINISHED"}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self, width=400)



def register_attach():
	bpy.utils.register_class(Object_TO_Connect_Script_to_Object)



def unregister_attach():
	bpy.utils.unregister_class(Object_TO_Connect_Script_to_Object)



if __name__ == "__main__":
	register_attach()