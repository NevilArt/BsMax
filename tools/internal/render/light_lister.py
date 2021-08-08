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
from bsmax.actions import set_as_active_object

class Render_OT_Light_Lister(Operator):
	bl_idname = 'render.light_lister'
	bl_label = 'Light lister'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	lights, materials = [], []

	def get_light_field(self, col, light):
		data = light.data
		row = col.row()
		""" Create Icone name from type name """
		icon = 'LIGHT_' + data.type
		row.operator('object.select_by_name',
			icon=icon, text='').name = light.name
		
		row.prop(light, 'name', text='')
		row.prop(data, 'type', text='')
		row.prop(data, 'color', text='', icon='BLANK1')
		row.prop(data, 'energy', text='')

		if data.type == 'POINT':
			row.prop(data, 'shadow_soft_size', text='')
		elif data.type == 'SUN':
			row.prop(data, 'angle', text='')
		elif data.type == 'SPOT':
			row.prop(data, 'shadow_soft_size', text='')
		elif data.type == 'AREA':
			# row.prop(data, 'shape', text='')
			row.prop(data, 'size', text='')
		
		row.prop(data, 'use_shadow', text='', icon='COMMUNITY')
		
	def get_active_light_field(self, col, light):
		data = light.data
		row = col.row(align=True)
		
		icon = 'LIGHT_' + data.type
		row.label(text=light.name, icon=icon)

		if data.type == 'POINT':
			row = col.row()
			row.prop(data, 'use_custom_distance', text='Custom Distance')
			if data.use_custom_distance:
				row.prop(data, 'cutoff_distance', text='')
				row.label(text='')
				row.label(text='')
			
			row = col.row()
			row.prop(data, 'use_shadow', text='Shadow')
			if data.use_shadow:
				row.prop(data, 'shadow_buffer_clip_start', text='Clip Start')
				row.prop(data, 'shadow_buffer_bias', text='Bias')
				row.label(text='')
			
				row = col.row()
				row.prop(data, 'use_contact_shadow', text='Contact Shadow')
				if data.use_contact_shadow:
					row.prop(data, 'contact_shadow_distance', text='Distance')
					row.prop(data, 'contact_shadow_bias', text='Bias')
					row.prop(data, 'contact_shadow_thickness', text='Thickness')

		if data.type == 'SUN':
			row = col.row()
			row.prop(data, 'use_shadow', text='Shadow')
			if data.use_shadow:
				row.prop(data, 'shadow_buffer_bias', text='Bias')
				row.label(text='')
				row.label(text='')
			
			row = col.row()
			row.prop(data, 'shadow_cascade_count', text='Count')
			row.prop(data, 'shadow_cascade_fade', text='Fade')
			row.prop(data, 'shadow_cascade_max_distance', text='Max Distance')
			row.prop(data, 'shadow_cascade_exponent', text='Distribution')
			
			row = col.row()
			if data.use_shadow:
				row.prop(data, 'use_contact_shadow', text='Contact Shadow')
				if data.use_contact_shadow:
					row.prop(data, 'contact_shadow_distance', text='Distance')
					row.prop(data, 'contact_shadow_bias', text='Bias')
					row.prop(data, 'contact_shadow_thickness', text='Thikness')

		if data.type == 'SPOT':
			row = col.row()
			row.prop(data, 'use_custom_distance', text='Custom Distance')
			if data.use_custom_distance:
				row.prop(data, 'cutoff_distance', text='Distance')
				row.label(text='')
				row.label(text='')
			
			row = col.row()
			row.prop(data, 'show_cone', text='Show Cone')
			row.prop(data, 'spot_size', text='Size')
			row.prop(data, 'spot_blend', text='Blend')
			row.label(text='')

			row = col.row()
			row.prop(data, 'use_shadow', text='Shadow')
			if data.use_shadow:
				row.prop(data, 'shadow_buffer_clip_start', text='Clip Start')
				row.prop(data, 'shadow_buffer_bias', text='Bias')
				row.label(text='')
			
				row = col.row()
				row.prop(data, 'use_contact_shadow', text='Contact Shadow')
				if data.use_contact_shadow:
					row.prop(data, 'contact_shadow_distance', text='Distance')
					row.prop(data, 'contact_shadow_bias', text='Bias')
					row.prop(data, 'contact_shadow_thickness', text='Thikness')

		if data.type == 'AREA':
			row = col.row()
			row.prop(data, 'shape', text='')
			if data.shape in {'SQUARE', 'DISK'}:
				row.prop(data, 'size', text='Size')
				row.label(text='')
			if data.shape in {'RECTANGLE', 'ELLIPSE'}:
				row.prop(data, 'size', text='Size X')
				row.prop(data, 'size_y', text='Size')
			row.label(text='')

			row = col.row()
			row.prop(data, 'use_custom_distance', text='Custom Distance')
			if data.use_custom_distance:
				row.prop(data, 'cutoff_distance', text='Distance')
				row.label(text='')
				row.label(text='')

			row = col.row()
			row.prop(data, 'use_shadow', text='Shadow')
			if data.use_shadow:
				row.prop(data, 'shadow_buffer_clip_start', text='Clip Start')
				row.prop(data, 'shadow_buffer_bias', text='Bias')
				row.label(text='')

			row = col.row()
			row.prop(data, 'use_contact_shadow', text='Contact Shadow')
			if data.use_contact_shadow:
				row.prop(data, 'contact_shadow_distance', text='Distance')
				row.prop(data, 'contact_shadow_bias', text='Bias')
				row.prop(data, 'contact_shadow_thickness', text='Thikness')
	
	def is_free_node_input(self, input):
		return len(input.links) == 0
	
	def get_material_field(self, col, material, node):
		row = col.row()
		row.label(text= material.name)
		if node.type == 'EMISSION':
			
			color_slot = node.inputs['Color']
			if self.is_free_node_input(color_slot):
				row.prop(color_slot, 'default_value', text='', icon='BLANK1')
			else:
				row.label(text='', icon='LOCKED')
			
			strength_slot = node.inputs['Strength']
			if self.is_free_node_input(strength_slot):
				row.prop(strength_slot, 'default_value', text='Strength')
			else:
				row.label(text=' ', icon='LOCKED')
		
		if node.type == 'BSDF_PRINCIPLED':
			
			emission_slot = node.inputs['Emission']
			if self.is_free_node_input(emission_slot):
				row.prop(emission_slot, 'default_value', text='', icon='BLANK1')
			else:
				row.label(text='', icon='LOCKED')
			
			strength_slot = node.inputs['Emission Strength']
			if self.is_free_node_input(strength_slot):
				row.prop(strength_slot, 'default_value', text='Strength')
			else:
				row.label(text=' ', icon='LOCKED')
		
		row.label(text='')
		row.label(text='')

	def draw(self, ctx):
		layout = self.layout
		
		""" Get Light Field """
		box = layout.box()
		col = box.column()
		for light in self.lights:
			self.get_light_field(col, light)
		
		""" Get Active light field """
		box = layout.box()
		col = box.column()
		for light in self.lights:
			if light == ctx.active_object:
				self.get_active_light_field(col, light)
				break
		
		""" Get Material Field """
		box = layout.box()
		col = box.column()
		for material, node in self.materials:
			self.get_material_field(col, material, node)
	
	def execute(self, ctx):
		self.report({'OPERATOR'}, 'bpy.ops.render.light_lister()')
		return{'FINISHED'}
	
	def cancel(self, ctx):
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
	
	def get_emission_matts(self, ctx):
		emission, bsdf_principled = [], []

		for material in bpy.data.materials:
			if material.use_nodes:
				for node in material.node_tree.nodes:
					if node.type == 'OUTPUT_MATERIAL':
						if node.mute:
							continue
						
						for link in node.inputs['Surface'].links:
							if link.from_node.type == 'EMISSION':
								emission.append((material, link.from_node))

							if link.from_node.type == 'BSDF_PRINCIPLED':
								""" Ignore if emission color is Black """
								default_value = link.from_node.inputs['Emission'].default_value
								if default_value[0] == 0.0 and default_value[1] == 0.0 and \
									default_value[2] == 0.0 and default_value[3] == 1.0:
									break

								bsdf_principled.append((material, link.from_node))
							break

		return emission + bsdf_principled


	def invoke(self, ctx, event):
		self.lights = self.get_lights()
		self.materials = self.get_emission_matts(ctx)
		return ctx.window_manager.invoke_props_dialog(self, width=500)



class Camera_OT_Actve_By_Name(Operator):
	""" Set as active camera  """
	bl_idname = 'camera.active_by_name'
	bl_label = 'Active Camera by name'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	name: bpy.props.StringProperty(default='')
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		bpy.ops.object.select_all(action='DESELECT')
		if self.name != '':
			set_as_active_object(ctx,bpy.data.objects[self.name])
			bpy.ops.camera.set_active('INVOKE_DEFAULT')
		return{'FINISHED'}



class Render_OT_Camera_Lister(Operator):
	bl_idname = 'render.camera_lister'
	bl_label = 'Camera lister'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	lights = []

	def get_field(self, row, camera, active):
		srow = row.row(align=True)
		icon = 'OUTLINER_OB_CAMERA' if active else 'CAMERA_DATA'
		srow.operator('camera.active_by_name', icon=icon,
			text='').name = camera.name
		srow.operator('object.select_by_name',
			text=camera.name).name = camera.name
		
		srow = row.row(align=True)
		srow.label(text='', icon='DRIVER_ROTATIONAL_DIFFERENCE')
		srow.prop(camera.data, 'type', text='')
		srow.prop(camera.data, 'lens', text='')

		srow = row.row(align=True)
		srow.label(text='', icon='CURVE_PATH')
		srow.prop(camera.data, 'clip_start', text='')
		srow.prop(camera.data, 'clip_end', text='')
		
		srow = row.row(align=True)
		srow.label(text='', icon='ZOOM_SELECTED')
		srow.prop(camera.data.dof, 'use_dof', text='')
		srow.prop(camera.data.dof, 'focus_distance', text='')

		srow = row.row(align=True)
		srow.prop(camera.data, 'display_size', text='')

	def draw(self,ctx):
		box = self.layout.box()
		col = box.column(align=True)

		for cam in self.cameras:
			is_active = (cam == ctx.scene.camera)
			self.get_field(col.row(align=False), cam, is_active)
	
	def execute(self,ctx):
		return{'FINISHED'}
	
	def cancel(self,ctx):
		return None
	
	def get_cameras(self):
		cameras = []
		for camera in bpy.data.objects:
			if camera.type == 'CAMERA':
				isnew = True
				for l in cameras:
					if camera.data == l.data:
						isnew = False
						break
				if isnew:
					cameras.append(camera)
		return cameras

	def invoke(self,ctx,event):
		self.cameras = self.get_cameras() 
		return ctx.window_manager.invoke_props_dialog(self, width=700)



def render_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('render.light_lister',
		text='Light Lister', icon='LIGHT_SUN')
	layout.operator('render.camera_lister',
		text='Camera Lister', icon='CAMERA_DATA')



classes = [Render_OT_Light_Lister, 
		Camera_OT_Actve_By_Name,
		Render_OT_Camera_Lister]

def register_light_lister():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.TOPBAR_MT_render.append(render_menu)

def unregister_light_lister():
	bpy.types.TOPBAR_MT_render.remove(render_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	[bpy.utils.register_class(c) for c in classes]
	# register_light_lister()