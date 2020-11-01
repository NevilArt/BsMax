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

class Render_TO_Light_Lister(Operator):
	bl_idname = "render.light_lister"
	bl_label = "Light lister"
	lights = []

	def get_field(self,row,light):
		icon = 'LIGHT_' + light.data.type
		row.operator("object.select_by_name",icon=icon,text=light.name).name = light.name
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
		self.report({'INFO'},'bpy.ops.render.light_lister()')
		return{"FINISHED"}
	
	def cancel(self,ctx):
		return None
	
	def get_lights(self):
		lights = []
		for light in bpy.data.objects:
			if light.type == 'LIGHT':
				isnew = True
				for l in lights:
					if light.data == l.data:
						isnew = False
						break
				if isnew:
					lights.append(light)
		return lights

	def invoke(self,ctx,event):
		self.lights = self.get_lights() 
		return ctx.window_manager.invoke_props_dialog(self,width=700)

def render_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("render.light_lister",text="Light Lister",icon='LIGHT_SUN')

classes = [Render_TO_Light_Lister]

def register_lightlister():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.TOPBAR_MT_render.append(render_menu)

def unregister_lightlister():
	bpy.types.TOPBAR_MT_render.remove(render_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_lightlister()