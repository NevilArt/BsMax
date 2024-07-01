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
# 2022/06/29

import bpy
import os

from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class

def get_output_path():
	file_name = os.path.basename(bpy.data.filepath)
	name_parts = str(file_name).split('_')
	
	directories = (bpy.data.filepath).split('\\')
	if len(directories) < 2:
		return

	main_folder = directories[0] + '\\' + directories[1] + '\\'
	
	render_path = main_folder + 'OUTPUT\\RENDER\\'
	if not os.path.isdir(render_path):
		return
	
	if not os.access(render_path, os.W_OK):
		return
	
	render_path += name_parts[1] + "\\"

	if not os.path.isdir(render_path):
		os.mkdir(render_path)

	return render_path


def get_render_file_name():
	file_name = os.path.basename(bpy.data.filepath)
	name_parts = str(file_name).split('_')
	return name_parts[1]


def get_render_extention(scene):
	file_format = scene.render.image_settings.file_format
	if file_format in {'OPEN_EXR_MULTILAYER', 'OPEN_EXR'}:
		return ".exr"
	if file_format in {'JPEG', 'JPG'}:
		return ".jpg"
	return "." + file_format.lower()


def set_output_path(scene, chanel):
	render_path = get_output_path()
	if not render_path:
		return
	render_path += chanel + '\\'
	if not os.path.isdir(render_path):
		os.mkdir(render_path)
	file_name = get_render_file_name()
	file_name += "_" + chanel + "_"
	# file_name += get_render_extention(scene)
	scene.render.filepath = render_path + file_name


def get_main_scene():
	for scene in bpy.data.scenes:
		if scene.name in {'Scene', 'Main'}:
			return scene
	return None


def get_scene(ctx, name:str):
	for scene in bpy.data.scenes:
		if scene.name == name:
			ctx.window.scene = scene
			return scene
	
	main_scene = get_main_scene()
	if not main_scene:
		return
	
	# Clone the main Scene
	ctx.window.scene = main_scene
	bpy.ops.scene.new(type='LINK_COPY')
	ctx.scene.name = name
	return ctx.scene


def set_output_format(render, format:str):
	image_settings = render.image_settings
	format, mode = format.split('_')
	if format == 'EXR':
		image_settings.file_format = 'OPEN_EXR'
		image_settings.color_mode = mode #'RGB''RGBA''BW'
		image_settings.exr_codec = 'DWAA'
		image_settings.use_preview = True

	elif format == 'PNG':
		image_settings.file_format = 'PNG'
		image_settings.color_mode = mode #'RGB''RGBA''BW'
		image_settings.color_depth = '8'
		image_settings.compression = 15

	elif format == 'JPGE':
		image_settings.file_format = 'JPEG'
		image_settings.color_mode = mode
		image_settings.quality = 90


def set_output_setting(scene, format:str, chanel_name:str):
	render = scene.render
	render.resolution_x = 2048
	render.resolution_y = 1152
	render.resolution_percentage = 100
	render.pixel_aspect_x = 1.0
	render.pixel_aspect_y = 1.0
	render.use_border = False

	scene.frame_start = 0
	scene.frame_step = 1
	render.use_multiview = False

	render.use_file_extension = True
	render.use_render_cache = False
	render.use_overwrite = True
	render.use_placeholder = False
	render.image_settings.color_management = 'FOLLOW_SCENE'

	set_output_format(render, format)
	set_output_path(scene, chanel_name)


def set_outliner_setting(ctx):
	space_data = None
	for area in ctx.screen.areas:
		if area.type == 'OUTLINER':
			for space in area.spaces:
				if space.type == 'OUTLINER':
					space_data = space

	if not space_data:
		return

	space_data.show_restrict_column_enable = True
	space_data.show_restrict_column_select = True
	space_data.show_restrict_column_hide = True
	space_data.show_restrict_column_viewport = True
	space_data.show_restrict_column_render = True
	space_data.show_restrict_column_holdout = True
	space_data.show_restrict_column_indirect_only = True


def set_eevee(scene):
	render = scene.render
	eevee = scene.eevee
	render.engine = 'BLENDER_EEVEE_NEXT'

	eevee.taa_render_samples = 512
	eevee.use_raytracing = True
	eevee.use_shadows = True


def set_eevee_volum(scene):
	render = scene.render
	eevee = scene.eevee
	render.engine = 'BLENDER_EEVEE_NEXT'

	eevee.taa_render_samples = 512
	eevee.use_raytracing = True
	eevee.use_shadows = True


def set_eevee_sky(scene):
	render = scene.render
	eevee = scene.eevee
	render.engine = 'BLENDER_EEVEE_NEXT'

	eevee.taa_render_samples = 1
	eevee.use_shadows = False
	eevee.use_raytracing = False


def set_eevee_mist(scene):
	render = scene.render
	eevee = scene.eevee
	render.engine = 'BLENDER_EEVEE_NEXT'

	eevee.taa_render_samples = 1
	eevee.use_shadows = False
	eevee.use_raytracing = False


def set_cycles(scene):
	render = scene.render
	render.engine = 'CYCLES'
	cycles = scene.cycles
	cycles.device = 'GPU'

	cycles.use_adaptive_sampling = True
	cycles.samples = 512
	cycles.adaptive_threshold = 0.01
	cycles.denoiser = 'OPENIMAGEDENOISE'
	cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
	cycles.denoising_prefilter = 'ACCURATE'
	cycles.denoising_quality = 'HIGH'
	cycles.denoising_use_gpu = True

	render.hair_type = 'STRIP'
	render.hair_subdiv = 2
	render.film_transparent = True
	render.use_persistent_data = True #need to test

	render.use_simplify = True
	render.use_simplify = True


def get_viewlayer_collections(view_layer, collections):
	all_layer_collections = []

	def collect(layer_collection):
		all_layer_collections.append(layer_collection)
		for child in layer_collection.children:
			collect(child)
	
	collect(view_layer.layer_collection)

	layer_collections = []
	for collection in collections:
		for layer_collection in all_layer_collections:
			if collection.name == layer_collection.name:
				layer_collections.append(layer_collection)
				continue

	return layer_collections


def set_collection_setting(view_layer, collections, action, state):
	if not view_layer or not collections:
		return

	layer_collections = get_viewlayer_collections(view_layer, collections)

	if action == 'exclude':
		for collection in layer_collections:
			collection.exclude = state

	elif action == 'holdout':
		for collection in layer_collections:
			collection.holdout = state

	elif action == 'indirect_only':
		for collection in layer_collections:
			collection.indirect_only = state


def get_collection_by_name(collections, name):
	for collection in collections:
		if collection.name == name:
			return collection
	return None


def get_collections(scene, name):
	Main_collections = scene.collection.children_recursive
	collection = get_collection_by_name(Main_collections, name)
	if not collection:
		return None
	return [collection] + collection.children_recursive


def set_scene_char(ctx):
	scene = get_scene(ctx, "Char")
	set_cycles(scene)
	set_output_setting(scene, 'EXR_RGBA', "Char")
	set_outliner_setting(ctx)
	view_layer = scene.view_layers[0]

	render = get_collections(scene, "Char")
	render += get_collections(scene, "Prop")
	holdout = get_collections(scene, "Env")
	exclude = get_collections(scene, "Env_Layout")

	set_collection_setting(view_layer, holdout, 'holdout', True)
	set_collection_setting(view_layer, exclude, 'exclude', True)


def set_scene_env(ctx):
	scene = get_scene(ctx, "Env")
	set_cycles(scene)
	set_output_setting(scene, 'EXR_RGBA', "Env")
	set_outliner_setting(ctx)
	view_layer = scene.view_layers[0]

	indirect_only = get_collections(scene, "Char")
	indirect_only += get_collections(scene, "Prop")
	exclude = get_collections(scene, "Env_Layout")

	set_collection_setting(view_layer, indirect_only, 'indirect_only', True)
	set_collection_setting(view_layer, exclude, 'exclude', True)


def set_scene_hair(ctx):
	scene = get_scene(ctx, "Hair")
	set_eevee(scene)
	set_output_setting(scene, 'EXR_RGBA', "Hair")
	set_outliner_setting(ctx)


def set_scene_bg_cycles(ctx):
	scene = get_scene(ctx, "BG (Cycles)")
	set_cycles(scene)
	set_output_setting(scene, 'EXR_RGBA', "BG")
	set_outliner_setting(ctx)


def set_scene_bg_eevee(ctx):
	scene = get_scene(ctx, "BG (EEVEE)")
	set_eevee(scene)
	set_output_setting(scene, 'EXR_RGBA', "BG")
	set_outliner_setting(ctx)


def set_scene_crowds(ctx):
	scene = get_scene(ctx, "Crowds") 
	set_eevee(scene)
	set_output_setting(scene, 'EXR_RGBA', "Crowds")
	set_outliner_setting(ctx)


def set_scene_mist(ctx):
	scene = get_scene(ctx, "Mist") 
	set_eevee_mist(scene)
	set_output_setting(scene, 'EXR_RGB', "Mist")
	set_outliner_setting(ctx)


def set_scene_volum(ctx):
	scene = get_scene(ctx, 'Volum')
	set_eevee_volum(scene)
	set_output_setting(scene, 'EXR_RGB', "Volum")
	set_outliner_setting(ctx)


def set_scene_sky(ctx):
	scene = get_scene(ctx, "sky")
	set_eevee_sky(scene)
	set_output_setting(scene, 'EXR_RGB', "Sky")
	set_outliner_setting(ctx)


class Render_OT_Make_Ready_Render_V3(Operator):
	bl_idname = 'nevil.make_ready_render_v3'
	bl_label = "Make Ready Render V3 (Nevil)"
	bl_description = ""
	bl_options = {'REGISTER'}

	char: BoolProperty(
		name="Character", default=True,
		description=""
	) # type: ignore
	
	hair:  BoolProperty(
		name="Hair", default=True,
		description=""
	) # type: ignore

	env: BoolProperty(
		name="Environment", default=True,
		description=""
	) # type: ignore

	bg_eevee: BoolProperty(
		name="BG (EEVEE)", default=True,
		description=""
	) # type: ignore

	bg_cycles: BoolProperty(
		name="BG (CYCLES)", default=False,
		description=""
	) # type: ignore

	crowds: BoolProperty(
		name="Crowds", default=False,
		description=""
	) # type: ignore

	mist:  BoolProperty(
		name="Mist", default=True, 
		description=""
	) # type: ignore

	sky: BoolProperty(
		name="Sky", default=True,
		description=""
	) # type: ignore

	volum:  BoolProperty(
		name="Volum", default=False,
		description=""
	) # type: ignore

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.prop(self, 'char')
		row.prop(self, 'hair')
		row.prop(self, 'env')

		row = layout.row()
		row.prop(self, 'bg_eevee')
		row.prop(self, 'bg_cycles')
		row.prop(self, 'crowds')

		row = layout.row()
		row.prop(self, 'mist')
		row.prop(self, 'sky')
		row.prop(self, 'volum')

	def execute(self, ctx):
		if self.char:
			set_scene_char(ctx)

		if self.env:
			set_scene_env(ctx)

		if self.hair:
			set_scene_hair(ctx)
		
		if self.bg_cycles:
			set_scene_bg_cycles(ctx)

		if self.bg_eevee:
			set_scene_bg_eevee(ctx)

		if self.crowds:
			set_scene_crowds(ctx)
		
		if self.mist:
			set_scene_mist(ctx)
		
		if self.volum:
			set_scene_volum(ctx)

		if self.sky:
			set_scene_sky(ctx)

		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)


classes ={
	Render_OT_Make_Ready_Render_V3
}


def register_make_ready_render_v3():
	for cls in classes:
		register_class(cls)


def unregister_make_ready_render_v3():
	for cls in classes:
		if cls.is_registered:
			unregister_class(cls)


if __name__ == '__main__':
	unregister_make_ready_render_v3()
	register_make_ready_render_v3()