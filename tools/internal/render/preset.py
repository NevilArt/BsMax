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
# 2024/02/29

import bpy

from bpy.types import Panel, Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent
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


def pystr_attribute(ctx, space, attribute):
	if not hasattr(space, attribute):
		return ""

	script = 'bpy.context.scene.'

	if space == ctx.scene.render:
		script += 'render.'

	elif space == ctx.scene.cycles:
		script += 'cycles.'

	elif space == ctx.scene.eevee:
		script += 'eevee.'

	script += attribute + " = "
	value = getattr(space, attribute)
	script += '"' + value + '"' if type(value) == str else str(value)
	script += '\n'
	return script


def get_manual_part(ctx, engin_name):
	""" the mising parametes inside the bl_rna.properties adding here manualy """
	script = ""

	if engin_name == 'render':
		render = ctx.scene.render
		attributes = (
			"use_high_quality_normals",
			"hair_type",
			"hair_subdiv",
			"film_transparent",
			"use_simplify",
			"simplify_subdivision",
			"simplify_child_particles",
			"simplify_volumes",
			"simplify_subdivision_render",
			"simplify_child_particles_render",
			"simplify_gpencil",
			"simplify_gpencil_onplay",
			"simplify_gpencil_view_fill",
			"simplify_gpencil_modifier",
			"simplify_gpencil_shader_fx",
			"simplify_gpencil_tint",
			"simplify_gpencil_antialiasing",
			"use_freestyle",
			"line_thickness_mode",
			"line_thickness",
			"use_persistent_data",
			"use_motion_blur"
		)

		for attribute in attributes:
			script += pystr_attribute(ctx, render, attribute)
		
		# script += bcs + 'use_save_buffers = ' + str(render.use_save_buffers) + '\n'
		# TODO find new alternative
	
	if engin_name == 'eevee':
		eevee = ctx.scene.eevee
		attributes = (
			"volumetric_light_clamp",
			"use_shadow_high_bitdepth",
			"use_soft_shadows",
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
		)

		for attribute in attributes:
			script += pystr_attribute(ctx, eevee, attribute)
	
	if engin_name == 'cycles':
		cycles = ctx.scene.cycles
		
		attributes = (
			"aa_samples",
			"ao_samples",
			"use_adaptive_sampling",
			"adaptive_min_samples",
			"use_denoising",
			"seed",
			"use_square_samples",
			"min_light_bounces",
			"min_transparent_bounces",
			"volume_bounces",
			"sample_clamp_direct",
			"use_preview_denoising",
			"use_animated_seed",
			"ao_bounces_render",
			"use_camera_cull",
			"use_distance_cull",
			"use_progressive_refine",
			"debug_use_spatial_splits",
			"debug_bvh_time_steps "
		)

		bcs = 'bpy.context.scene.cycles'
		script += bcs + 'denoiser = "' + cycles.denoiser + '"\n'
		script += bcs + 'curves.shape = "' + ctx.scene.cycles_curves.shape + '"\n'
		script += bcs + 'shading_system = ' + str(cycles.shading_system) + '\n'
		script += bcs + '_curves.subdivisions = ' + str(ctx.scene.cycles_curves.subdivisions) + '\n'

		for attribute in attributes:
			script += pystr_attribute(ctx, cycles, attribute)

	
	if engin_name == 'cycles_x':
		scene = ctx.scene
		cycles = scene.cycles
		world = scene.world
		view_settings = scene.view_settings
		display_settings = scene.display_settings
		sequencer_colorspace_settings = scene.sequencer_colorspace_settings
		grease_pencil_settings = scene.grease_pencil_settings
		
		bcs = 'bpy.context.scene.cycles'
		bcw = 'bpy.context.scene.world'
		bcv = 'bpy.context.scene.view_settings'
		bcd = 'bpy.context.scene.display_settings'
		bcq = 'bpy.context.scene.sequencer_colorspace_settings'
		bcg = 'bpy.context.scene.grease_pencil_settings'

		script += bcs + '.use_preview_adaptive_sampling = ' + \
					 str(cycles.use_preview_adaptive_sampling) + '\n'
		script += bcs + '.use_camera_cull = ' + str(cycles.use_camera_cull) + '\n'
		script += bcs + '.use_distance_cull = ' + str(cycles.use_distance_cull) + '\n'
		script += bcs + '.debug_use_spatial_splits = ' + str(cycles.debug_use_spatial_splits) + '\n'
		script += bcs + '.debug_bvh_time_steps = ' + str(cycles.debug_bvh_time_steps) + '\n'
		script += bcs + '.film_transparent_glass = ' + str(cycles.film_transparent_glass) + '\n'
		script += bcs + '_curves.shape = "' + scene.cycles_curves.shape + '"\n'
		script += bcs + '_curves.subdivisions = ' + str(scene.cycles_curves.subdivisions) + '\n'

		script += bcw + '.light_settings.ao_factor = ' + \
				str(world.light_settings.ao_factor) + '\n'

		script += bcw + '.light_settings.distance = ' + \
				str(world.light_settings.distance) + '\n'

		script += bcv + '.view_transform = "' + \
				str(view_settings.view_transform) + '"\n'

		script += bcv + '.look = "' + str(view_settings.look) + '"\n'
		script += bcv + '.exposure = ' + str(view_settings.exposure) + '\n'
		script += bcv + '.gamma = ' + str(view_settings.gamma) + '\n'

		script += bcv + '.use_curve_mapping = ' + \
				str(view_settings.use_curve_mapping) + '\n'

		script += bcd + '.display_device = "' + \
				str(display_settings.display_device) + '"\n'

		script += bcq + '.name = "' + str(sequencer_colorspace_settings.name) + '"\n'

		script += bcg + '.antialias_threshold = ' + \
				 str(grease_pencil_settings.antialias_threshold) + '\n'
	
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

		if not (name.startswith('__') and name.endswith('__') or name in illegals) :
			""" check is name avlible in properti list """

			if name in engin.bl_rna.properties:
				""" filter read onlys """

				if not engin.bl_rna.properties[name].is_readonly:
					value = getattr(engin, name)
					value = refine_value(value)

					if value:
						script += 'bpy.context.scene.' + engin_name + '.' + name + ' = ' + str(value) + '\n'

	return script


def create_preset_script(ctx):
	global preset_kay
	script = preset_kay + '\n'
	script += 'import bpy \n'
	script += get_script(ctx.scene.render, 'render')
	script += get_manual_part(ctx, 'render')

	if ctx.scene.render.engine == 'BLENDER_EEVEE':
		script += get_script(ctx.scene.eevee, 'eevee')
		script += get_manual_part(ctx, 'eevee')

	elif ctx.scene.render.engine == 'CYCLES':
		script += get_script(ctx.scene.cycles, 'cycles')
		script += get_manual_part(ctx, 'cycles_x')

	elif ctx.scene.render.engine == 'BLENDER_WORKBENCH':
		script += get_script(ctx.scene, 'scene')
		script += get_manual_part(ctx, 'scene')

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
	return [(pl, pl,'') for pl in preset_list]


def read_preset_file(presetName):
	fileName = 	get_preset_path() + presetName + '.py'
	return open(fileName).read()


class Render_OT_Preset(Operator):
	""" Save/Load or Copy/Past render settings """
	bl_idname = "render.preset"
	bl_label = "Copy Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def get_presets(self, ctx):
		return get_presets_list()

	name: StringProperty(name='Preset Name', default='New Preset')
	names: EnumProperty(name='Preset Name', items=get_presets)
	action: EnumProperty(
		items=[
			('COPY', 'Copy', 'Copy Render Setting to Clipboard'),
			('PASTE', 'Paste', 'Paste Render Setting from Clipboard'),
			('SAVE', 'Save', 'Save Render Setting to File'),
			('LOAD', 'Load', 'Load Rendert Setting from File'),
			('REVEAL', 'Reveal', 'Reveal Render Presets Folder')
		],
		default='SAVE'
	)

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
			pass

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


class Render_PrePostScript(PropertyGroup):
	pre_render_active: BoolProperty(
		name='Active', default=False,
		description='Run the Script befor render start'
	)
	
	description = "The script has to run befor render start\n"
	description += "Just write the name of script on text editor"
	pre_render_script: StringProperty(
		name='Pre', default='', description=description
	)
	
	post_render_active: BoolProperty(
		name='Active', default=False,
		description='Run the Script after render finished'
	)
	
	description = "The script has to run after render finish\n"
	description += "Just write the name of script on text editor"
	post_render_script: StringProperty(
		name='Post', default='', description=description
	)


class RENDER_PT_Script(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = 'Script'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		layout = self.layout
		rpps = ctx.scene.render_prepost_script

		row = layout.row()
		row.prop(rpps, 'pre_render_active', text='', icon='PLAY')
		row.prop(rpps, 'pre_render_script')
		
		row = layout.row()
		row.prop(rpps, 'post_render_active', text='', icon='PLAY')
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
		name='Pre/Post Render Script'
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