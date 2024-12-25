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
# 2024/12/10

import bpy
import os
import subprocess
import platform
import json

from bpy.types import Panel, Operator, PropertyGroup, UIList
from bpy.utils import register_class, unregister_class
from bpy.app import version
from bpy.props import (
	StringProperty, EnumProperty, BoolProperty,
	CollectionProperty, IntProperty
)

from os import path, mkdir
from glob import glob


def get_datafiles_path():
	user_resource_path = bpy.utils.resource_path('USER')
	datafiles_path = os.path.join(user_resource_path, "datafiles")

	datafiles_path += os.sep + 'BsMax'
	if not path.isdir(datafiles_path):
		mkdir(datafiles_path)

	datafiles_path += os.sep + 'Render_presets'
	if not path.isdir(datafiles_path):
		mkdir(datafiles_path)	

	return datafiles_path


def write_dictionary_to_json_file(data, file_path):
	try:
		with open(file_path, 'w', encoding='utf-8') as json_file:
			json.dump(data, json_file, ensure_ascii=False, indent=4)
		return True
	except:
		return False


def read_json_file_to_dictionary(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as json_file:
			data = json.load(json_file)
		return data
	except:
		return {}


# not a good method but for now works fine
def str_data_path(ctx, data_path):
	scene = ctx.scene
	if data_path == scene:
		return 'scene.'
	if data_path == scene.render:
		return 'scene.render.'
	if data_path == scene.cycles:
		return 'scene.cycles.'
	if data_path == scene.eevee:
		return 'scene.eevee.'
	if data_path == scene.world.light_settings:
		return 'scene.world.light_settings.'
	if data_path == scene.view_settings:
		return 'scene.view_settings.'
	if data_path == scene.display_settings:
		return 'scene.display_settings.'
	if data_path == scene.sequencer_colorspace_settings:
		return 'scene.sequencer_colorspace_settings.'
	if data_path == scene.grease_pencil_settings:
		return 'scene.grease_pencil_settings.'
	if data_path == scene.cycles_curves:
		return 'scene.cycles_curves.'
	return ''


def attribute_list_to_dictionery(ctx, data_path, attribute_list):
	new_dictionary = {}
	for attribute in attribute_list:
		if not hasattr(data_path, attribute):
			continue
		data_path_name = str_data_path(ctx, data_path) + attribute
		new_dictionary[data_path_name] = getattr(data_path, attribute)
	
	return new_dictionary


def get_manual_part_of_dict(ctx, engin_name):
	""" the mising parametes inside the
		bl_rna.properties adding manualy
	"""
	new_dictionary = {}

	if engin_name == 'RENDER':
		attributes = [
			"use_high_quality_normals",
			"hair_subdiv",
			"film_transparent",
			"use_simplify",
			"simplify_gpencil",
			"simplify_gpencil_onplay",
			"use_freestyle",
			"use_persistent_data",
			"use_motion_blur"
		]

		if version >= (4, 2, 0):
			attributes += [
			"use_simplify_normals"
		]

		render = ctx.scene.render
		new_dictionary.update(
			attribute_list_to_dictionery(ctx, render, attributes)
		)

	if engin_name == 'EEVEE':
		attributes = [
			"volumetric_light_clamp",
			"use_shadow_high_bitdepth",
			"gi_auto_bake",
			"gi_glossy_clamp",
			"gi_show_cubemaps",
			"gi_show_irradiance",
			"use_overscan",
			"use_gtao",
			"use_bloom",
			"use_ssr",
			"use_motion_blur",
			"use_volumetric_shadows"
		]

		eevee = ctx.scene.eevee
		new_dictionary.update(
			attribute_list_to_dictionery(ctx, eevee, attributes)
		)

	if engin_name == 'EEVEENEXT':
		# TODO check this list again after 4.2LTS releasee
		attributes = [
			"use_shadow_jitter_viewport",
			"use_shadow_jitter_viewport",
			"clamp_surface_direct",
			"clamp_volume_direct",
			"use_raytracing",
			"ray_tracing_options.resolution_scale",
			"ray_tracing_options.trace_max_roughness",
			"ray_tracing_options.screen_trace_quality",
			"ray_tracing_options.screen_trace_thickness",
			"ray_tracing_options.use_denoise",
			"ray_tracing_options.denoise_bilateral",
			"ray_tracing_options.denoise_temporal",
			"ray_tracing_options.denoise_spatial",
			"fast_gi_distance",
			"use_bokeh_jittered",
			"use_overscan"
		]

		eevee = ctx.scene.eevee
		new_dictionary.update(
			attribute_list_to_dictionery(ctx, eevee, attributes)
		)

	if engin_name == 'CYCLES':
		attributes = [
			"use_camera_cull",
			"use_distance_cull",
			"debug_use_spatial_splits",
			"debug_bvh_time_steps",
			"film_transparent_glass",

			"shading_system",
			"preview_adaptive_min_samples",
			"use_preview_denoising",
			"denoising_use_gpu",
			"use_guiding",
			"use_guiding",
			"use_animated_seed",
			"sample_offset",
			"auto_scrambling_distance",
			"preview_scrambling_distance",
			"min_light_bounces",
			"min_transparent_bounces",
			"sample_clamp_direct",
			"debug_use_compact_bvh"
		]

		cycles = ctx.scene.cycles
		new_dictionary.update(
			attribute_list_to_dictionery(ctx, cycles, attributes)
		)

	if engin_name == 'SCENE':
		scene = ctx.scene
		attributes = [
			[scene.world.light_settings, "ao_factor"],
			[scene.world.light_settings, "distance"],
			[scene.view_settings, "view_transform"],
			[scene.view_settings, "look"],
			[scene.view_settings, "exposure"],
			[scene.view_settings, "gamma"],
			[scene.view_settings, "use_curve_mapping"],
			[scene.display_settings, "display_device"],
			[scene.sequencer_colorspace_settings, "name"],
			[scene.grease_pencil_settings, "antialias_threshold"],
			[scene.cycles_curves, "shape"],
			[scene.cycles_curves, "subdivisions"]
		]

		for data_path, attribute in attributes:
			new_dictionary.update(
				attribute_list_to_dictionery(ctx, data_path, [attribute])
			)

	return new_dictionary


def get_dictionary(ctx, engin, engin_name):
	""" 
	* get render engin and render engin name
	* collect all editable attributes
	* return the list as a dictionary
	"""
	ignore_list = {
		'bl_rna', 'rna_type', 'filepath', '',
		'stamp_background', 'stamp_foreground', 'stamp_note_text'
	}

	dictionary = {}

	for name in dir(engin):
		""" filter none relateds """
		if name in ignore_list:
			continue

		if (name.startswith('__') and name.endswith('__')) :
			continue

		""" check is name avlible in properti list """
		if not name in engin.bl_rna.properties:
			continue

		""" filter read onlys """
		if engin.bl_rna.properties[name].is_readonly:
			continue

		value = getattr(engin, name)

		if value:
			key = 'scene.' + engin_name + '.' + name
			dictionary[key] = value

	return dictionary


def create_preset_dictionary(ctx):
	dictionary = {}

	dictionary.update(get_dictionary(ctx, ctx.scene.render, 'render'))
	dictionary.update(get_manual_part_of_dict(ctx, 'RENDER'))

	engine = ctx.scene.render.engine

	if engine == 'BLENDER_EEVEE':
		dictionary.update(get_dictionary(ctx, ctx.scene.eevee, 'eevee'))
		dictionary.update(get_manual_part_of_dict(ctx, 'EEVEE'))

	if engine == 'BLENDER_EEVEE_NEXT':
		dictionary.update(get_dictionary(ctx, ctx.scene.eevee, 'eevee'))
		dictionary.update(get_manual_part_of_dict(ctx, 'EEVEENEXT'))

	elif engine == 'CYCLES':
		dictionary.update(get_dictionary(ctx, ctx.scene.cycles, 'cycles'))
		dictionary.update(get_manual_part_of_dict(ctx, 'CYCLES'))

	elif engine == 'BLENDER_WORKBENCH':
		dictionary.update(get_dictionary(ctx, ctx.scene, 'scene'))

	dictionary.update(get_manual_part_of_dict(ctx, 'SCENE'))

	#TODO other render engined has to add here
	# Octane
	# Redshift
	# Vray

	return dictionary


def open_folder_in_explorer(path):
	if not os.path.isdir(path):
		return

	if platform.system() == "Windows":
		os.startfile(path)
	
	elif platform.system() == "Darwin":
		subprocess.call(["open", path])
	
	elif platform.system() == "Linux":
		subprocess.call(["xdg-open", path])


def get_list_of_presets():
	preset_path = get_datafiles_path()
	return [
		path.splitext(path.basename(f))[0]
			for f in glob(preset_path+"/*.json")
	]


def render_preset_reload(ctx):
	ctx.scene.render_presets.clear()
	for name in get_list_of_presets():
		ps = ctx.scene.render_presets.add()
		ps.name = name


def render_preset_add(ctx):
	name = ctx.scene.render_preset_name
	file_name = get_datafiles_path() + os.sep + name + ".json"

	if os.path.exists(file_name):
		pass
		#TODO check is name avalible warn or use auto digit

	write_dictionary_to_json_file(
		create_preset_dictionary(ctx), file_name
	)

	render_preset_reload(ctx)


def render_preset_remove(ctx):
	index = ctx.scene.render_presets_index
	name = ctx.scene.render_presets[index].name
	file_name = get_datafiles_path() + os.sep + name + ".json"
	#TODO ask for permition
	os.remove(file_name)
	render_preset_reload(ctx)


def render_preset_name_update(ctx):
	index = ctx.scene.render_presets_index
	new_name = ctx.scene.render_presets[index].name
	old_name = ctx.scene.render_preset_name
	file_path = get_datafiles_path() + os.sep

	os.rename(
		file_path + new_name + ".json",
		file_path + old_name + ".json"
	)

	render_preset_reload(ctx)


def render_preset_load(ctx):
	index = ctx.scene.render_presets_index
	name = ctx.scene.render_presets[index].name
	file_name = get_datafiles_path() + os.sep + name + ".json"
	dictionary = read_json_file_to_dictionary(file_name)
	scope = {'ctx': ctx}
	for key, value in dictionary.items():
		expression = 'ctx.' + key
		try:
			exec(f"{expression} = {value}", {"__builtins__": None}, scope)
		except:
			pass


class Render_Preset(PropertyGroup):
	name: StringProperty(
		name="Preset Name", default="New Preset"
	) # type: ignore


class Render_OT_Preset(Operator):
	bl_idname = "render.preset"
	bl_label = "Render Preset"
	bl_description = "Save/Load or Copy/Past render settings"
	bl_options = {'REGISTER', 'INTERNAL'}

	action: EnumProperty(
		items=[
			('RELOAD', 'Reload', "Save Render Setting to File"),
			('ADD', 'Add', "Save Render Setting to File"),
			('REMOVE', 'Remove', "Remove Active Preset"),
			('UPDATE', 'Update', "Update active preset"),
			('LOAD', 'Load', 'Load Rendert Setting from File'),
			('REVEAL', 'Reveal', 'Reveal Render Presets Folder')
		],
		default='RELOAD'
	) # type: ignore

	def execute(self, ctx):
		if self.action == 'RELOAD':
			render_preset_reload(ctx)

		elif self.action == 'ADD':
			render_preset_add(ctx)

		elif self.action == 'REMOVE':
			render_preset_remove(ctx)

		elif self.action == 'UPDATE':
			render_preset_name_update(ctx)

		elif self.action == 'LOAD':
			render_preset_load(ctx)

		elif self.action == 'REVEAL':
			open_folder_in_explorer(get_datafiles_path())

		return{'FINISHED'}


class RENDER_UI_Preset(UIList):
	def draw_item(self, ctx, layout, data, item, icon,
		active_data, active_property, index = 0, flt_flag = 0):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.label(text=item.name)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			layout.prop(item, "name", text="", emboss=False)


class RENDER_PT_Preset(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = 'Presets'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		layout = self.layout
		scene = ctx.scene

		row = layout.row()
		col = row.column()
		sub_col = col.column(align=True)
		sub_col.template_list(
			"RENDER_UI_Preset", "",
			scene, "render_presets",
			scene, "render_presets_index"
		)
		sub_col.prop(ctx.scene, 'render_preset_name')

		col = row.column()

		sub_col = col.column(align=True)

		sub_col.operator(
			'render.preset', text='', icon='FILE_REFRESH'
		).action='RELOAD'

		sub_col = col.column(align=True)
		sub_col.operator( 
			'render.preset', text='', icon='ADD'
		).action='ADD'

		sub_col.operator( 
			'render.preset', text='', icon='REMOVE'
		).action='REMOVE'

		sub_col.operator( 
			'render.preset', text='', icon='GREASEPENCIL'
		).action='UPDATE'

		sub_col = col.column()
		sub_col.operator(
			'render.preset', text='', icon='FILEBROWSER'
		).action='REVEAL'

		sub_col = col.column()
		sub_col.operator(
			'render.preset', text='', icon='PLAY'
		).action='LOAD'


class Render_PrePostScript(PropertyGroup):
	pre_render_active: BoolProperty(
		name="Active", default=False,
		description='Run the Script befor render start'
	) # type: ignore
	
	description = "The script has to run befor render start\n"
	description += "Just write the name of script on text editor"
	pre_render_script: StringProperty(
		name="Pre", default="", description=description
	) # type: ignore
	
	post_render_active: BoolProperty(
		name="Active", default=False,
		description='Run the Script after render finished'
	) # type: ignore
	
	description = "The script has to run after render finish\n"
	description += "Just write the name of script on text editor"
	post_render_script: StringProperty(
		name="Post", default="", description=description
	) # type: ignore


classes = {
	Render_Preset,
	RENDER_UI_Preset,
	Render_OT_Preset,
	RENDER_PT_Preset
}


def register_preset():
	for cls in classes:
		register_class(cls)

	Scene = bpy.types.Scene
	Scene.render_presets = CollectionProperty(type=Render_Preset)
	Scene.render_presets_index = IntProperty(name="Index", default=0)
	Scene.render_preset_name = StringProperty(name="", default="New Preset")


def unregister_preset():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_preset()