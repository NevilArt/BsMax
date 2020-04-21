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
from bpy.props import StringProperty

class BsMax_TO_SelectLightByName(Operator):
	bl_idname = "light.selectbyname"
	bl_label = "select light by name"
	name: StringProperty(default="")
	
	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self,ctx):
		bpy.ops.object.select_all(action='DESELECT')
		if self.name != "":
			bpy.data.objects[self.name].select_set(True)
		return{"FINISHED"}

class BsMax_TO_LightLister(Operator):
	bl_idname = "render.lightlister"
	bl_label = "Light lister"
	lights = []

	def get_field(self,row,light):
		icon = 'LIGHT_' + light.data.type
		row.operator("light.selectbyname",icon=icon,text=light.name).name = light.name
		row.prop(light.data,'color',text="")
		row.prop(light.data,'energy',text="")
		row.prop(light.data,'specular_factor',text="")
		row.prop(light.data,'shadow_soft_size',text="")
		row.prop(light.data,'use_custom_distance',text="")
		row.prop(light.data,'cutoff_distance',text="")
		row.prop(light.data,'use_shadow',text="")
		row.prop(light.data,'shadow_buffer_clip_start',text="")
		row.prop(light.data,'shadow_buffer_bias',text="")

	def draw(self,ctx):
		box = self.layout.box()
		col = box.column()

		row = col.row()
		row.label(text='')
		row.label(text='  Color')
		row.label(text='  Energy')
		row.label(text='       Specular')
		row.label(text='')
		row.label(text='Size')
		row.label(text='Distance')
		row.label(text='Shadow')
		row.label(text='Start')
		row.label(text='Bias')

		for light in self.lights:
			self.get_field(col.row(align=True),light)
	
	def execute(self,ctx):
		return{"FINISHED"}
	
	def cancel(self,ctx):
		return None

	def invoke(self,ctx,event):
		self.lights = [o for o in bpy.data.objects if o.type == 'LIGHT']
		return ctx.window_manager.invoke_props_dialog(self,width=600)

classes = [BsMax_TO_LightLister,BsMax_TO_SelectLightByName]

def register_lightlister():
	[bpy.utils.register_class(c) for c in classes]

def unregister_lightlister():
	[bpy.utils.unregister_class(c) for c in classes]