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
# 2024/06/09

import bpy
import os
import subprocess
import platform

from bpy.types import Panel, Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent
from bpy.app import version
from bpy.props import (
	PointerProperty, StringProperty, EnumProperty, BoolProperty
)

from os import path, mkdir, access, W_OK
from glob import glob


preset_kay = '""" BsMax Render Preset File """'


def refine_value(value):
	""" get value and return an executable pyton string """
	if type(value).__name__ == 'Color':
		return (value[0], value[1], value[2])

	if type(value).__name__ == 'str':
		return '"' + value + '"'

	if type(value).__name__ in {'float', 'bool', 'int'}:
		return value

	return None


# not a good method but for now is trusted
def str_data_path(ctx, data_path):
	scene = ctx.scene
	if data_path == scene:
		return 'bpy.context.scene.'
	if data_path == scene.render:
		return 'bpy.context.scene.render.'
	if data_path == scene.cycles:
		return 'bpy.context.scene.cycles.'
	if data_path == scene.eevee:
		return 'bpy.context.scene.eevee.'
	if data_path == scene.world.light_settings:
		return 'bpy.context.scene.world.light_settings.'
	if data_path == scene.view_settings:
		return 'bpy.context.scene.view_settings.'
	if data_path == scene.display_settings:
		return 'bpy.context.scene.display_settings.'
	if data_path == scene.sequencer_colorspace_settings:
		return 'bpy.context.scene.sequencer_colorspace_settings.'
	if data_path == scene.grease_pencil_settings:
		return 'bpy.context.scene.grease_pencil_settings.'
	if data_path == scene.cycles_curves:
		return 'bpy.context.scene.cycles_curves.'
	return ''


def pystr_attribute(ctx, data_path, attribute):
	if not hasattr(data_path, attribute):
		return ""

	script = str_data_path(ctx, data_path) + attribute + " = "
	value = getattr(data_path, attribute)
	script += '"' + value + '"' if type(value) == str else str(value)
	script += '\n'
	return script


def get_manual_part(ctx, engin_name):
	""" the mising parametes inside the
		bl_rna.properties adding manualy
	"""
	script = ""

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
		for attribute in attributes:
			script += pystr_attribute(ctx, render, attribute)

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
		for attribute in attributes:
			script += pystr_attribute(ctx, eevee, attribute)

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
		for attribute in attributes:
			script += pystr_attribute(ctx, eevee, attribute)

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
		for attribute in attributes:
			script += pystr_attribute(ctx, cycles, attribute)

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
			script += pystr_attribute(ctx, data_path, attribute)

	return script


def get_preset_path():
	preset_path = bpy.utils.user_resource('CONFIG') + '\\BsMax\\'
	if not path.isdir(preset_path):
		mkdir(preset_path)

	preset_path += 'render_presets\\'
	if not path.isdir(preset_path):
		mkdir(preset_path)

	return preset_path


def get_script(engin, engin_name):
	""" 
	* get render engin and render engin name
	* collect all change able attributes
	* convert the attribute and data to line of python code
	* e.g. bpy.context.scene.eevee.motion_blur_max = 32
	"""

	illegals = {'bl_rna', 'rna_type', 'filepath', ''}
	script = ""
	for name in dir(engin):
		""" filter none relateds """
		if name in illegals:
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
		value = refine_value(value)

		if value:
			script += 'bpy.context.scene.'
			script += engin_name + '.' + name 
			script += ' = ' + str(value) + '\n'

	return script


def create_preset_script(ctx):
	global preset_kay
	script = preset_kay + '\n'
	script += 'import bpy \n'
	script += get_script(ctx.scene.render, 'render')
	script += get_manual_part(ctx, 'RENDER')

	engine = ctx.scene.render.engine

	if engine == 'BLENDER_EEVEE':
		script += get_script(ctx.scene.eevee, 'eevee')
		script += get_manual_part(ctx, 'EEVEE')
	
	if engine == 'BLENDER_EEVEE_NEXT':
		script += get_script(ctx.scene.eevee, 'eevee')
		script += get_manual_part(ctx, 'EEVEENEXT')

	elif engine == 'CYCLES':
		script += get_script(ctx.scene.cycles, 'cycles')
		script += get_manual_part(ctx, 'CYCLES')
		
	elif engine == 'BLENDER_WORKBENCH':
		script += get_script(ctx.scene, 'scene')
	
	script += get_manual_part(ctx, 'SCENE')

	#TODO other render engined has to add here
	return script


def is_script_preset(script):
	global preset_kay
	if type(script).__name__ == 'str':
		lines = script.split('\n')
		if len(lines) == 0:
			return False
		return lines[0] == preset_kay
	else:
		return False


def execute_is_python(script):
	if is_script_preset(script):
		exec(script)


def open_folder_in_explorer(path):
	if not os.path.isdir(path):
		return

	if platform.system() == "Windows":
		os.startfile(path)
	
	elif platform.system() == "Darwin":
		subprocess.call(["open", path])
	
	elif platform.system() == "Linux":
		subprocess.call(["xdg-open", path])


def save_file(presetName, string):
	presetPath = get_preset_path()
	if not path.exists(presetPath):
		if access(presetPath, W_OK):
			mkdir(presetPath)

	fileName = 	presetPath + presetName + '.py'
	presetFile = open(fileName, "w")
	presetFile.write(string)
	presetFile.close()


def get_presets_list():
	preset_path = get_preset_path()
	preset_list = [
		path.splitext(path.basename(f))[0]
			for f in glob(preset_path+"/*.py")
	]
	return [(pl, pl, "") for pl in preset_list]


def read_preset_file(presetName):
	fileName = 	get_preset_path() + presetName + '.py'
	return open(fileName).read()


class Render_OT_Preset(Operator):
	bl_idname = "render.preset"
	bl_label = "Render Preset"
	bl_description = "Save/Load or Copy/Past render settings"
	bl_options = {'REGISTER', 'INTERNAL'}

	def get_presets(self, _):
		return get_presets_list()

	name: StringProperty(
		name='Preset Name', default='New Preset'
	) # type: ignore
	
	names: EnumProperty(
		name='Preset Name', items=get_presets
	) # type: ignore
	
	action: EnumProperty(
		items=[
			('COPY', 'Copy', 'Copy Render Setting to Clipboard'),
			('PASTE', 'Paste', 'Paste Render Setting from Clipboard'),
			('SAVE', 'Save', 'Save Render Setting to File'),
			('LOAD', 'Load', 'Load Rendert Setting from File'),
			('REVEAL', 'Reveal', 'Reveal Render Presets Folder')
		],
		default='SAVE'
	) # type: ignore

	def draw(self, ctx):
		layout = self.layout
		if self.action == 'SAVE':
			layout.prop(self, 'name')
		elif self.action == 'LOAD':
			layout.prop(self, 'names')

	def execute(self, ctx):
		if self.action == 'COPY':
			ctx.window_manager.clipboard = create_preset_script(ctx)

		elif self.action == 'PASTE':
			execute_is_python(ctx.window_manager.clipboard)

		elif self.action == 'SAVE':
			save_file(self.name, create_preset_script(ctx))

		elif self.action == 'LOAD':
			exec(read_preset_file(self.names))

		elif self.action == 'REVEAL':
			open_folder_in_explorer(get_preset_path())

		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		if self.action in ('SAVE', 'LOAD'):
			return ctx.window_manager.invoke_props_dialog(self)
		else:
			return self.execute(ctx)


class RENDER_PT_Preset(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = 'Presets'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.operator(
			'render.preset', text='Save', icon='ADD'
		).action='SAVE'
		
		row.operator(
			'render.preset', text='Load', icon='FILE_TICK'
		).action='LOAD'
		
		row.operator(
			'render.preset', text='', icon='COPYDOWN'
		).action='COPY'
		
		row.operator(
			'render.preset', text='', icon='PASTEDOWN'
		).action='PASTE'

		row.operator(
			'render.preset', text='', icon='FILEBROWSER'
		).action='REVEAL'


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


class RENDER_PT_Script(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = "Script"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		layout = self.layout
		rpps = ctx.scene.render_prepost_script

		row = layout.row()
		row.prop(rpps, 'pre_render_active', text="", icon='PLAY')
		row.prop(rpps, 'pre_render_script')
		
		row = layout.row()
		row.prop(rpps, 'post_render_active', text="", icon='PLAY')
		row.prop(rpps, 'post_render_script')


@persistent
def pre_render(scene):
	if scene.render_prepost_script.pre_render_active:
		script_name = scene.render_prepost_script.pre_render_script
		if script_name in bpy.data.texts:
			script = bpy.data.texts[script_name].as_string()
			try:
				exec(script)
			except:
				pass


@persistent
def post_render(scene):
	if scene.render_prepost_script.post_render_active:
		script_name = scene.render_prepost_script.post_render_script
		if script_name in bpy.data.texts:
			script = bpy.data.texts[script_name].as_string()
			try:
				exec(script)
			except:
				pass


classes = {
	Render_PrePostScript,
	Render_OT_Preset,
	RENDER_PT_Preset,
	RENDER_PT_Script
}


def register_preset():
	for cls in classes:
		register_class(cls)

	bpy.types.Scene.render_prepost_script = PointerProperty(
		type=Render_PrePostScript,
		name="Pre/Post Render Script"
	)
	
	bpy.app.handlers.render_init.append(pre_render)
	bpy.app.handlers.render_complete.append(post_render)


def unregister_preset():
	for cls in classes:
		unregister_class(cls)

	bpy.app.handlers.render_init.remove(pre_render)
	bpy.app.handlers.render_complete.remove(post_render)


if __name__ == '__main__':
	register_preset()