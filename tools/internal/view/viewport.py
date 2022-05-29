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

from random import random

from bpy.types import Operator, Menu
from bpy.props import EnumProperty, BoolProperty


#TODO Open ViewLayer as float dialog for Set State in quad menu


class View3DData:
	def __init__(self):
		self._shading_type = 'SOLID'
v3dd = View3DData()



# new one will cretae for NewStyle mode
class View3D_OT_Wireframe_Toggle(Operator):
	""" Wire Frame toggle """
	bl_idname = "view3d.wireframe_toggle"
	bl_label = "Wireframe Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		global v3dd
		shading = ctx.area.spaces[0].shading
		if shading.type == 'WIREFRAME':
			shading.type = v3dd._shading_type #'SOLID''MATERIAL''RENDERED'
		else:
			v3dd._shading_type = shading.type
			shading.type = 'WIREFRAME'
		return{"FINISHED"}


class Lighting_type:
	def __init__(self):
		self.shading_type = 'SOLID'
lst = Lighting_type()



class View3D_OT_Lighting_Toggle(Operator):
	""" Lighting toggle """
	bl_idname = "view3d.lighting_toggle"
	bl_label = "Lighting Toggle / Attribute Link"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		global lst
		if len(ctx.selected_objects) and ctx.active_object != None:
			bpy.ops.wm.call_menu(name='VIEW3D_MT_make_links')
		else:
			shading = ctx.area.spaces[0].shading
			if shading.type == 'RENDERED':
				shading.type = lst.shading_type
			else:
				lst.shading_type = shading.type
				shading.type = 'RENDERED'
		return{"FINISHED"}



class View3D_OT_Edge_Face_Toggle(Operator):
	""" Edge Face Toggle """
	bl_idname = "view3d.edge_faces_toggle"
	bl_label = "Edge Shaded Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		if overlay.show_wireframes:
			overlay.show_wireframes = False
			overlay.wireframe_threshold = 0.5
		else:
			overlay.show_wireframes = True
			overlay.wireframe_threshold = 1
		return{"FINISHED"}



class View3D_OT_Shade_Selected_Faces(Operator):
	""" Highlight selected faces color toggle """
	bl_idname = "view3d.shade_selected_faces"
	bl_label = "Shade Selected Faces"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		FaceShade = ctx.preferences.themes['Default'].view_3d
		if FaceShade.face_select[3] != 0.0:
			FaceShade.face_select = (0.0, 0.0, 0.0, 0.0)
		else:
			FaceShade.face_select = (0.8156, 0.0, 0.0, 0.5)
		return{"FINISHED"}



class View3D_OT_Show_Statistics(Operator):
	""" Display Statistic Toggle """
	bl_idname = "view3d.show_statistics"
	bl_label = "Show Statistics Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		if not overlay.show_text and not overlay.show_stats:
			overlay.show_text = True
			overlay.show_stats = False

		elif overlay.show_text and not overlay.show_stats:
			overlay.show_text = False
			overlay.show_stats = True

		elif not overlay.show_text and overlay.show_stats:
			overlay.show_text = True
			overlay.show_stats = True

		else:
			overlay.show_text = False
			overlay.show_stats = False
		return{"FINISHED"}



class View3D_OT_Show_Types_Toggle(Operator):
	bl_idname = "view3d.show_types_toggle"
	bl_label = "Show Types Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	mode: EnumProperty(name='Type', default='GEOMETRY', 
					items=[
							('GEOMETRY', 'Geometry', ""),
							('EMPTY', 'Empty', ""),
							('CURVE', 'Curve', ""),
							('LIGHT', 'Light', ""),
							('ARMATURE', 'Armature', ''),
							('CAMERA', 'Camera', ''),
					]
			)

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def geometry_toggle(self, ctx):
		state = ctx.space_data.show_object_viewport_mesh
		ctx.space_data.show_object_viewport_mesh = not state
	
	def empty_toggle(self, ctx):
		data = ctx.space_data
		empty = data.show_object_viewport_empty
		speaker = data.show_object_viewport_speaker
		lightprob = data.show_object_viewport_light_probe
		lattce = data.show_object_viewport_lattice
		state = empty and speaker and lightprob and lattce
		data.show_object_viewport_empty = not state
		data.show_object_viewport_speaker = not state
		data.show_object_viewport_light_probe = not state
		data.show_object_viewport_lattice = not state
	
	def curve_toggle(self, ctx):
		state = ctx.space_data.show_object_viewport_curve
		ctx.space_data.show_object_viewport_curve = not state
	
	def light_toggle(self, ctx):
		state = ctx.space_data.show_object_viewport_light
		ctx.space_data.show_object_viewport_light = not state
	
	def armature_toggle(self, ctx):
		state = ctx.space_data.show_object_viewport_armature
		ctx.space_data.show_object_viewport_armature = not state
	
	def camera_toggle(self, ctx):
		state = ctx.space_data.show_object_viewport_camera
		ctx.space_data.show_object_viewport_camera = not state

	def execute(self, ctx):
		if self.mode == 'GEOMETRY':
			self.geometry_toggle(ctx)

		elif self.mode == 'EMPTY':
			self.empty_toggle(ctx)

		elif self.mode == 'CURVE':
			self.curve_toggle(ctx)

		elif self.mode == 'LIGHT':
			self.light_toggle(ctx)

		elif self.mode == 'ARMATURE':
			self.armature_toggle(ctx)

		elif self.mode == 'CAMERA':
			self.camera_toggle(ctx)

		return{"FINISHED"}



class View3D_OT_Random_Object_Color(Operator):
	""" Give a random objectt color to selected/all mesh objects """
	bl_idname = "view3d.random_object_color"
	bl_label = "Random Object Color"
	bl_options = {'REGISTER', 'UNDO'}

	selected: BoolProperty(name="Selected only", default=False)
	mode: EnumProperty(name="Mode", default="RAND", 
						items=[
							('RAND', 'Random', ''),
							('UNIQ', 'Unique', '')
							]
					)

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def get_objects(self, ctx):
		types = {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}
		if self.selected:
			return [obj for obj in ctx.selected_objects if obj.type in types]
		return [obj for obj in bpy.data.objects if obj.type in types]

	def execute(self, ctx):
		if self.mode == 'RAND':
			for obj in self.get_objects(ctx):
				r = random() * 0.75 + 0.25
				g = random() * 0.75 + 0.25
				b = random() * 0.75 + 0.25
				obj.color = (r, g, b, 1)

		else:
			for obj in self.get_objects(ctx):
				obj.color = (1, 1, 1, 1)

		return{"FINISHED"}



class View3D_OT_Setting(Operator):
	bl_idname = 'view3d.setting'
	bl_label = 'Setting'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	name: EnumProperty(name='Name', default='SHADOW',
		items=[('SHADOW', 'Shadow',''),
			('WIREFRAME', 'Wireframe',''),
			('SOLID', 'Solid',''),
			('MATERIAL', 'Material',''),
			('RENDERED', 'Rendered',''),
			('COMBINED', 'Combined',''),
			('EMISSION', 'emission',''),
			('ENVIRONMENT', 'Environment',''),
			('DIFFUSE_LIGHT', 'Diffuse Light',''),
			('DIFFUSE_COLOR', 'Diffuse Color',''),
			('SPECULAR_LIGHT', 'Specular Light',''),
			('VOLUME_TRANSMITTANCE', 'Volum Transmittance',''),
			('VOLUME_SCATTER', 'Volum Scater',''),
			('NORMAL', 'Normal',''),
			('MIST', 'Mist',''),
			('use_transform_skip_children', 'Use transform skip children',''),
			('use_scene_lights_render', 'Use scene lights render',''),
			('use_scene_world_render', 'Use scene world render','')])

	def execute(self, ctx):
		if self.name in {'WIREFRAME', 'SOLID', 'MATERIAL', 'RENDERED'}:
			ctx.space_data.shading.type = self.name
		
		elif self.name in {'COMBINED', 'EMISSION', 'ENVIRONMENT', 'SHADOW',
			'DIFFUSE_LIGHT', 'DIFFUSE_COLOR', 'SPECULAR_LIGHT', 'SPECULAR_COLOR',
			'VOLUME_TRANSMITTANCE', 'VOLUME_SCATTER', 'NORMAL', 'MIST'}:
			ctx.space_data.shading.render_pass = self.name
		
		elif self.name == 'use_transform_skip_children':
			ctx.scene.tool_settings.use_transform_skip_children = not ctx.scene.tool_settings.use_transform_skip_children
		elif self.name == 'use_scene_lights_render':
			ctx.space_data.shading.use_scene_lights_render = not ctx.space_data.shading.use_scene_lights_render
		elif self.name == 'use_scene_world_render':
			ctx.space_data.shading.use_scene_world_render = not ctx.space_data.shading.use_scene_world_render

		return {'FINISHED'}



class VIEW3D_MT_Preview(Menu):
	bl_idname = "VIEW3D_MT_preview"
	bl_label = "Preview"

	def draw(self, ctx):
		layout=self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("render.opengl",
						text="Viewport Render Image",
						icon='RENDER_STILL')

		layout.operator("render.opengl",
						text="Viewport Render Animation",
						icon='RENDER_ANIMATION').animation = True

		props = layout.operator("render.opengl",
								text="Viewport Render Keyframes",
								icon='RENDER_ANIMATION').animation = True

		props.render_keyed_only = True



class VIEW3D_MT_ViewLayer(Menu):
	bl_idname = "VIEW3D_MT_viewlayer"
	bl_label = "View Layer"

	def draw(self, ctx):
		layout=self.layout
		window = ctx.window
		scene = window.scene
		layout.template_search(
			window, "view_layer",
			scene, "view_layers",
			new="scene.view_layer_add",
			unlink="scene.view_layer_remove")



def random_object_color_menu(self, ctx):
	self.layout.separator()
	self.layout.operator('view3d.random_object_color')



classes = [
		View3D_OT_Edge_Face_Toggle,
		View3D_OT_Lighting_Toggle,
		View3D_OT_Random_Object_Color,
		View3D_OT_Shade_Selected_Faces,
		View3D_OT_Show_Statistics,
		View3D_OT_Show_Types_Toggle,
		View3D_OT_Setting,
		View3D_OT_Wireframe_Toggle,

		VIEW3D_MT_Preview,
		VIEW3D_MT_ViewLayer	
	]


def register_viewport():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.VIEW3D_MT_object_showhide.append(random_object_color_menu)


def unregister_viewport():
	bpy.types.VIEW3D_MT_object_showhide.remove(random_object_color_menu)

	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register_viewport()