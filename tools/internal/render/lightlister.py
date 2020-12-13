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
		self.report({'OPERATOR'},'bpy.ops.render.light_lister()')
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



class Render_TO_Camera_Lister(Operator):
	bl_idname = "render.camera_lister"
	bl_label = "Camera lister"
	lights = []

	def get_field(self,row,camera):
		row.operator("object.select_by_name",icon='CAMERA_DATA',text=camera.name).name = camera.name
		
		srow = row.row(align=True)
		srow.prop(camera.data,'type',text="")
		srow.prop(camera.data,'lens',text="")

		srow = row.row(align=True)
		srow.prop(camera.data,'clip_start',text="")
		srow.prop(camera.data,'clip_end',text="")
		
		srow = row.row(align=True)
		srow.prop(camera.data.dof,'use_dof',text="")
		srow.prop(camera.data.dof,'focus_distance',text="")

		srow = row.row(align=True)
		srow.prop(camera.data,'display_size',text="")

	def draw(self,ctx):
		box = self.layout.box()
		col = box.column(align=True)

		row = col.row()
		row.label(text='Name')
		row.label(text='Type')
		row.label(text='Lens')
		row.label(text='Clip Start')
		row.label(text='Clip End')
		row.label(text='FOV')
		row.label(text='Size')

		for cam in self.cameras:
			self.get_field(col.row(align=False),cam)
	
	def execute(self,ctx):
		self.report({'OPERATOR'},'bpy.ops.render.camera_lister()')
		return{"FINISHED"}
	
	def cancel(self,ctx):
		return None
	
	def get_cameras(self):
		cameras = []
		for light in bpy.data.objects:
			if light.type == 'CAMERA':
				isnew = True
				for l in cameras:
					if light.data == l.data:
						isnew = False
						break
				if isnew:
					cameras.append(light)
		return cameras

	def invoke(self,ctx,event):
		self.cameras = self.get_cameras() 
		return ctx.window_manager.invoke_props_dialog(self,width=700)



def render_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("render.light_lister",text="Light Lister",icon='LIGHT_SUN')
	layout.operator("render.camera_lister",text="Camera Lister",icon='CAMERA_DATA')

classes = [Render_TO_Light_Lister, Render_TO_Camera_Lister]

def register_lightlister():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.TOPBAR_MT_render.append(render_menu)

def unregister_lightlister():
	bpy.types.TOPBAR_MT_render.remove(render_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_lightlister()