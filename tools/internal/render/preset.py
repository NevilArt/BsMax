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
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, EnumProperty, BoolProperty
from bpy.app.handlers import persistent
from os import path, mkdir, access, W_OK
from glob import glob



# preset_path = bpy.utils.user_resource('SCRIPTS', "presets") + "\\BsMax\\render\\"
preset_path = bpy.utils.user_resource('SCRIPTS') + "\\presets\\BsMax\\render\\"
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



def get_manual_part(ctx, engin_name):
	""" the mising parametes inside the bl_rna.properties adding here manualy """
	script = ""

	if engin_name == 'render':
		render = ctx.scene.render
		bcs = 'bpy.context.scene.render.'
		script += bcs + 'use_high_quality_normals = ' + str(render.use_high_quality_normals) + '\n'
		script += bcs + 'hair_type = "' + render.hair_type + '"\n'
		script += bcs + 'hair_subdiv = ' + str(render.hair_subdiv) + '\n'
		script += bcs + 'film_transparent = ' + str(render.film_transparent) + '\n'
		script += bcs + 'use_simplify = ' + str(render.use_simplify) + '\n'
		script += bcs + 'simplify_subdivision = ' + str(render.simplify_subdivision) + '\n'
		script += bcs + 'simplify_child_particles = ' + str(render.simplify_child_particles) + '\n'
		script += bcs + 'simplify_volumes = ' + str(render.simplify_volumes) + '\n'
		script += bcs + 'simplify_subdivision_render = ' + str(render.simplify_subdivision_render) + '\n'
		script += bcs + 'simplify_child_particles_render = ' + str(render.simplify_child_particles_render) + '\n'
		script += bcs + 'simplify_gpencil = ' + str(render.simplify_gpencil) + '\n'
		script += bcs + 'simplify_gpencil_onplay = ' + str(render.simplify_gpencil_onplay) + '\n'
		script += bcs + 'simplify_gpencil_view_fill = ' + str(render.simplify_gpencil_view_fill) + '\n'
		script += bcs + 'simplify_gpencil_modifier = ' + str(render.simplify_gpencil_modifier) + '\n'
		script += bcs + 'simplify_gpencil_shader_fx = ' + str(render.simplify_gpencil_shader_fx) + '\n'
		script += bcs + 'simplify_gpencil_tint = ' + str(render.simplify_gpencil_tint) + '\n'
		script += bcs + 'simplify_gpencil_antialiasing = ' + str(render.simplify_gpencil_antialiasing) + '\n'
		script += bcs + 'use_freestyle = ' + str(render.use_freestyle) + '\n'
		script += bcs + 'line_thickness_mode = "' + render.line_thickness_mode + '"\n'
		script += bcs + 'line_thickness = ' + str(render.line_thickness) + '\n'
		script += bcs + 'use_save_buffers = ' + str(render.use_save_buffers) + '\n'
		script += bcs + 'use_persistent_data = ' + str(render.use_persistent_data) + '\n'
		script += bcs + 'use_motion_blur = ' + str(render.use_motion_blur) + '\n'
	
	if engin_name == 'eevee':
		eevee = ctx.scene.eevee
		bcs = 'bpy.context.scene.eevee.'
		script += bcs + 'volumetric_light_clamp = ' + str(eevee.volumetric_light_clamp) + '\n'
		script += bcs + 'use_shadow_high_bitdepth = ' + str(eevee.use_shadow_high_bitdepth) + '\n'
		script += bcs + 'use_soft_shadows = ' + str(eevee.use_soft_shadows) + '\n'
		script += bcs + 'gi_auto_bake = ' + str(eevee.gi_auto_bake) + '\n'
		script += bcs + 'gi_glossy_clamp = ' + str(eevee.gi_glossy_clamp) + '\n'
		script += bcs + 'gi_show_cubemaps = ' + str(eevee.gi_show_cubemaps) + '\n'
		script += bcs + 'gi_show_irradiance = ' + str(eevee.gi_show_irradiance) + '\n'
		script += bcs + 'use_overscan = ' + str(eevee.use_overscan) + '\n'
		script += bcs + 'use_gtao = ' + str(eevee.use_gtao) + '\n'
		script += bcs + 'use_bloom = ' + str(eevee.use_bloom) + '\n'
		script += bcs + 'use_ssr = ' + str(eevee.use_ssr) + '\n'
		script += bcs + 'use_motion_blur = ' + str(eevee.use_motion_blur) + '\n'
		script += bcs + 'use_volumetric_shadows = ' + str(eevee.use_volumetric_shadows) + '\n'

	if engin_name == 'cycles':
		cycles = ctx.scene.cycles
		bcs = 'bpy.context.scene.cycles'
		script += bcs + 'shading_system = ' + str(cycles.shading_system) + '\n'
		script += bcs + '.aa_samples = ' + str(cycles.aa_samples) + '\n'
		script += bcs + '.ao_samples = ' + str(cycles.ao_samples) + '\n'
		script += bcs + '.use_adaptive_sampling = ' + str(cycles.use_adaptive_sampling) + '\n'
		script += bcs + '.adaptive_min_samples = ' + str(cycles.adaptive_min_samples) + '\n'
		script += bcs + '.use_denoising = ' + str(cycles.use_denoising) + '\n'
		script += bcs + '.denoiser = "' + cycles.denoiser + '"\n'
		script += bcs + '.seed = ' + str(cycles.seed) + '\n'
		script += bcs + '.use_square_samples = ' + str(cycles.use_square_samples) + '\n'
		script += bcs + '.min_light_bounces = ' + str(cycles.min_light_bounces) + '\n'
		script += bcs + '.min_transparent_bounces = ' + str(cycles.min_transparent_bounces) + '\n'
		script += bcs + '.volume_bounces = ' + str(cycles.volume_bounces) + '\n'
		script += bcs + '.sample_clamp_direct = ' + str(cycles.sample_clamp_direct) + '\n'
		script += bcs + '_curves.shape = "' + ctx.scene.cycles_curves.shape + '"\n'
		script += bcs + '.use_preview_denoising = ' + str(cycles.use_preview_denoising) + '\n'
		script += bcs + '.use_animated_seed = ' + str(cycles.use_animated_seed) + '\n'
		script += bcs + '.ao_bounces_render = ' + str(cycles.ao_bounces_render) + '\n'
		script += bcs + '.use_camera_cull = ' + str(cycles.use_camera_cull) + '\n'
		script += bcs + '.use_distance_cull = ' + str(cycles.use_distance_cull) + '\n'
		script += bcs + '.use_progressive_refine = ' + str(cycles.use_progressive_refine) + '\n'
		script += bcs + '.debug_use_spatial_splits = ' + str(cycles.debug_use_spatial_splits) + '\n'
		script += bcs + '.debug_bvh_time_steps = ' + str(cycles.debug_bvh_time_steps) + '\n'
		script += bcs + '_curves.subdivisions = ' + str(ctx.scene.cycles_curves.subdivisions) + '\n'

	return script



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
	script = preset_kay + '\n'
	script += 'import bpy \n'
	script += get_script(ctx.scene.render, 'render')
	script += get_manual_part(ctx, 'render')
	if ctx.scene.render.engine == 'BLENDER_EEVEE':
		script += get_script(ctx.scene.eevee, 'eevee')
		script += get_manual_part(ctx, 'eevee')
	elif ctx.scene.render.engine == 'CYCLES':
		script += get_script(ctx.scene.cycles, 'cycles')
		script += get_manual_part(ctx, 'cycles')
	elif ctx.scene.render.engine == 'BLENDER_WORKBENCH':
		script += get_script(ctx.scene, 'scene')
		script += get_manual_part(ctx, 'scene')
	#TODO other render engined has to add here
	return script



def is_script_preset(script):
	if type(script).__name__ == 'str':
		lines = script.split('\n')
		if len(lines) == 0:
			return False
		return lines[0] == preset_kay
	else:
		return False



class Render_OT_Save_Preset(Operator):
	""" Save curent render state as a preset """
	bl_idname = "render.save_preset"
	bl_label = "Save Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	preset_name: StringProperty(name='Preset Name', default='New Preset')

	def save_file(self, string):
		if not path.exists(preset_path):
			if access(preset_path, W_OK):
				mkdir(preset_path)
		filename = 	preset_path + self.preset_name + '.py'
		preset_file = open(filename, "w")
		preset_file.write(string)
		preset_file.close()

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'preset_name')

	def execute(self, ctx):
		self.save_file(create_preset_script(ctx))
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)



class Render_OT_Copy_Preset(Operator):
	""" Copy curent render state to clipboard """
	bl_idname = "render.copy_preset"
	bl_label = "Copy Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	preset_name: StringProperty(name='Preset Name', default='New Preset')

	def execute(self, ctx):
		ctx.window_manager.clipboard = create_preset_script(ctx)
		return{"FINISHED"}



class Render_OT_Load_Preset(Operator):
	""" Load and saved render presets """
	bl_idname = "render.load_preset"
	bl_label = "Load Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def get_presets(self, ctx):
		preset_list = [path.splitext(path.basename(f))[0] for f in glob(preset_path+"/*.py")]
		presets = []
		for pl in preset_list:
			presets.append((pl, pl,''))
		return presets

	preset_name: EnumProperty(name='Preset Name', items=get_presets)

	def draw(self, ctx):
		self.layout.prop(self, 'preset_name')

	def read_file(self):
		filename = 	preset_path + self.preset_name + '.py'
		return open(filename).read()

	def execute(self, ctx):
		exec(self.read_file())
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)



class Render_OT_Paste_Preset(Operator):
	""" Paste Preset from clipboard """
	bl_idname = "render.paste_preset"
	bl_label = "Paste Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		script = ctx.window_manager.clipboard
		if is_script_preset(script):
			exec(script)
		return{"FINISHED"}



class Render_OT_Open_Renderpreset_folder(Operator):
	bl_idname = "render.open_renderpreset_folder"
	bl_label = "Open Renderpreset Folder"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		return{"FINISHED"}



class RENDER_PT_Preset(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = 'Presets'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.operator('render.save_preset', text='Save', icon='ADD')
		row.operator('render.load_preset', text='Load', icon='FILE_TICK')
		row.operator('render.copy_preset', text='', icon='COPYDOWN')
		row.operator('render.paste_preset', text='', icon='PASTEDOWN')



class Render_PrePostScript(PropertyGroup):
	pre_render_active: BoolProperty (name='Active', default=False,
		description='Run the Script befor render start')
	
	pre_render_script: StringProperty(name='Pre', default='',
		description='The script has to run befor render start\n Just write the name of script on text editor')
	
	post_render_active: BoolProperty (name='Active', default=False,
		description='Run the Script after render finished')
	
	post_render_script: StringProperty(name='Post', default='',
		description='The script has to run after render finish\n Just write the name of script on text editor')



class RENDER_PT_Script(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	bl_label = 'Script'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		rpps = ctx.scene.render_prepost_script
		layout = self.layout
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


classes = [	Render_OT_Save_Preset,
			Render_OT_Copy_Preset,
			Render_OT_Load_Preset,
			Render_OT_Paste_Preset,
			Render_PrePostScript,
			RENDER_PT_Preset,
			RENDER_PT_Script]



def register_preset():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.Scene.render_prepost_script = PointerProperty(type=Render_PrePostScript,
		name='Pre/Post Render Script')
	
	bpy.app.handlers.render_init.append(pre_render)
	bpy.app.handlers.render_complete.append(post_render)
	

def unregister_preset():
	[bpy.utils.unregister_class(c) for c in classes]

	bpy.app.handlers.render_init.remove(pre_render)
	bpy.app.handlers.render_complete.remove(post_render)

if __name__ == '__main__':
	register_preset()