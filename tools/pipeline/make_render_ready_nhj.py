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
import os

from mathutils import Vector

from bpy.types import Operator



def get_output_path():
	fileName = os.path.basename(bpy.data.filepath)
	nameParts = str(fileName).split('_')
	
	dirs = (bpy.data.filepath).split('\\')
	if len(dirs) < 2:
		return ""

	mainDir = dirs[0] + '\\' + dirs[1] + '\\'
	renderDir = mainDir + 'RENDER\\SINEMA_2\\' + nameParts[1] + "\\"

	return renderDir

def get_output_name():
	fileName = os.path.basename(bpy.data.filepath)
	nameParts = str(fileName).split('_')
	return nameParts[0] + "_" + nameParts[1] + "_"


def get_file_path(name):
	return get_output_path() + name + "\\" + get_output_name() + name + "_"



def out_put_setting(ctx, scene):
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

	filepath = get_file_path("Base")
	render.filepath = filepath

	render.use_file_extension = True
	render.use_render_cache = False

	render.image_settings.file_format = 'PNG'
	render.image_settings.color_mode = 'RGB'
	render.image_settings.color_depth = '8'
	render.image_settings.compression = 15
	render.use_overwrite = True
	render.use_placeholder = False
	render.image_settings.color_management = 'FOLLOW_SCENE'



def meta_data_setting(scene):
	render = scene.render
	render.metadata_input = 'SCENE'
	render.use_stamp_date = False
	render.use_stamp_time = False
	render.use_stamp_render_time = True
	render.use_stamp_frame = False
	render.use_stamp_frame_range = False
	render.use_stamp_memory = True
	render.use_stamp_hostname = True
	render.use_stamp_camera = False
	render.use_stamp_lens = False
	render.use_stamp_scene = False
	render.use_stamp_marker = False
	render.use_stamp_filename = False
	render.use_stamp_sequencer_strip = False

	render.use_stamp_note = False
	render.use_stamp = False

	render.use_sequencer = False
	render.use_compositing = True

	scene.render.use_compositing = True



def set_cycle_paraqmeters(scene):
	scene.name = "Cycles"
	scene.render.engine = 'CYCLES'
	cycles = scene.cycles

	# engine
	cycles.device = 'GPU'
	cycles.feature_set = 'SUPPORTED'
	cycles.shading_system = False

	# samples
	cycles.use_adaptive_sampling = True
	cycles.adaptive_threshold = 0.04
	cycles.samples = 512

	# denoise
	cycles.use_denoising = True
	cycles.denoiser = 'OPENIMAGEDENOISE'
	cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
	cycles.denoising_prefilter = 'ACCURATE'

	# Lighgt
	cycles.use_light_tree = True

	cycles.max_bounces = 12
	cycles.diffuse_bounces = 4
	cycles.glossy_bounces = 4
	cycles.transmission_bounces = 12
	cycles.volume_bounces = 0
	cycles.transparent_max_bounces = 8

	cycles.sample_clamp_direct = 0.0
	cycles.sample_clamp_indirect = 10.0

	cycles.blur_glossy = 1.03
	cycles.caustics_reflective = False
	cycles.caustics_refractive = False

	# GI
	cycles.use_fast_gi = False

	# Volum
	cycles.volume_step_rate = 1.0
	cycles.volume_preview_step_rate = 1.0
	cycles.volume_max_steps = 1024

	scene.render.use_motion_blur = False
	cycles.film_exposure = 1.0
	cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
	cycles.filter_width = 1.5
	scene.render.film_transparent = False

	# Color
	scene.display_settings.display_device = 'sRGB'
	scene.view_settings.view_transform = 'Filmic'
	scene.view_settings.look = 'None'
	scene.view_settings.exposure = 0
	scene.view_settings.gamma = 1
	scene.sequencer_colorspace_settings.name = 'sRGB'
	scene.view_settings.use_curve_mapping = False



def clone_scene(ctx):
	if 'EEVEE' in bpy.data.scenes:
		return bpy.data.scenes['EEVEE']
	
	elif 'Cycles' in bpy.data.scenes:
		set_as_active_scene(bpy.data.scenes['Cycles'])
	
	bpy.ops.scene.new(type='LINK_COPY')
	return ctx.scene



def set_eevee_parameters(scene):
	scene.name = "EEVEE"
	scene.render.engine = 'BLENDER_EEVEE'
	eevee = scene.eevee

	eevee.taa_render_samples = 64
	eevee.use_gtao = False
	eevee.use_bloom = False

	eevee.bokeh_max_size = 100
	eevee.bokeh_threshold = 1
	eevee.bokeh_neighbor_max = 10
	eevee.bokeh_denoise_fac = 0.75
	eevee.use_bokeh_high_quality_slight_defocus = False
	eevee.use_bokeh_jittered = False
	# post effect
	eevee.sss_samples = 1
	eevee.use_ssr = False
	eevee.use_motion_blur = False
	# shadow
	eevee.shadow_cube_size = '64'
	eevee.shadow_cascade_size = '64'
	eevee.use_shadow_high_bitdepth = False
	eevee.use_soft_shadows = False
	# Film
	scene.render.filter_size = 1.38
	scene.render.film_transparent = False
	eevee.use_overscan = False
	# Simplify
	scene.render.use_simplify = False
	# Composit
	scene.use_nodes = False



def set_view_layer(scene):
	scene.render.use_single_layer = False
	view_layer = scene.view_layers[0]
	view_layer.use = True

	# Data
	view_layer.use_pass_combined = True
	view_layer.use_pass_z = False
	view_layer.use_pass_mist = False
	view_layer.use_pass_position = False
	view_layer.use_pass_normal = False
	view_layer.use_pass_vector = False
	view_layer.use_pass_uv = False

	view_layer.use_pass_object_index = True
	view_layer.use_pass_material_index = True
	view_layer.pass_alpha_threshold = 0.5

	# Light
	view_layer.use_pass_diffuse_direct = False
	view_layer.use_pass_diffuse_indirect = False
	view_layer.use_pass_diffuse_color = False
	view_layer.use_pass_glossy_direct = False
	view_layer.use_pass_glossy_indirect = False
	view_layer.use_pass_glossy_color = False
	view_layer.use_pass_transmission_direct = False
	view_layer.use_pass_transmission_indirect = False
	view_layer.use_pass_transmission_color = False
	view_layer.use_pass_emit = False
	view_layer.use_pass_environment = False
	view_layer.use_pass_ambient_occlusion = False

	# Crypto matt
	view_layer.use_pass_cryptomatte_asset = True



def get_max_mist_distance(scene):
	return 250



def set_mist(scene):
	scene.view_layers[0].use_pass_mist = True
	mist_settings = scene.world.mist_settings
	mist_settings.start = 0
	mist_settings.depth = get_max_mist_distance(scene)
	mist_settings.falloff = 'INVERSE_QUADRATIC'



def set_as_active_scene(ctx, scene):
	ctx.window.scene = scene



def set_composit_up(sceneCycles, sceneEevee):
	sceneCycles.use_nodes = True
	node_tree = sceneCycles.node_tree
	nodes = node_tree.nodes

	""" Detect Nodes """
	cyclesRenderLayer = None
	eeveeRenderLayer = None
	compositeNode = None
	cryptomattNode = None
	mistOutputNode = None
	maskOutputNode = None
	MattOutputNode = None
	viewerNode = None

	for node in nodes:
		# render layer nodes
		if node.type == 'R_LAYERS':
			if node.scene.name == 'Cycles':
				cyclesRenderLayer = node
			elif node.scene.name == 'EEVEE':
				eeveeRenderLayer = node
		
		# composit node
		elif node.type == 'COMPOSITE':
			compositeNode = node

		elif node.type == 'CRYPTOMATTE_V2':
			cryptomattNode = node
		
		# File outpout
		elif node.type == 'OUTPUT_FILE':
			if node.name == 'Mist':
				mistOutputNode = node
			elif node.name == 'Mask':
				maskOutputNode = node
			elif node.name == 'Matt':
				MattOutputNode = node
		
		# viewer
		elif node.type == 'VIEWER':
			viewerNode = node


	if not cyclesRenderLayer:
		cyclesRenderLayer = nodes.new('CompositorNodeRLayers')
		cyclesRenderLayer.scene = sceneCycles
		cyclesRenderLayer.name = cyclesRenderLayer.label = "Cycles"
		cyclesRenderLayer.location = Vector((0, 400))
	
	if not eeveeRenderLayer:
		eeveeRenderLayer = nodes.new('CompositorNodeRLayers')
		eeveeRenderLayer.scene = sceneEevee
		eeveeRenderLayer.name = eeveeRenderLayer.label = "EEVEE"
		eeveeRenderLayer.location = Vector((0, 0))

	if not compositeNode:
		compositeNode = nodes.new('CompositorNodeComposite')
		compositeNode.location = Vector((400, 400))

	if not cryptomattNode:
		cryptomattNode = nodes.new('CompositorNodeCryptomatteV2')
		cryptomattNode.location = Vector((0, -400))
	
	if not MattOutputNode:
		MattOutputNode = nodes.new('CompositorNodeOutputFile')
		MattOutputNode.name = MattOutputNode.label = "Matt"
		MattOutputNode.location = Vector((400, -0))
		MattOutputNode.width = 400
		MattOutputNode.format.file_format = 'PNG'
		MattOutputNode.format.color_mode = 'RGBA'
		MattOutputNode.format.color_depth = '8'
		MattOutputNode.format.compression = 15
		MattOutputNode.base_path = get_output_path() + 'Matt\\'
		MattOutputNode.file_slots[0].path = get_output_name() + "Matt_"

	if not mistOutputNode:
		mistOutputNode = nodes.new('CompositorNodeOutputFile')
		mistOutputNode.name = mistOutputNode.label = "Mist"
		mistOutputNode.location = Vector((400, -200))
		mistOutputNode.width = 400
		mistOutputNode.format.file_format = 'PNG'
		mistOutputNode.format.color_mode = 'RGB'
		mistOutputNode.format.color_depth = '16'
		mistOutputNode.format.compression = 15
		mistOutputNode.base_path = get_output_path() + 'Mist\\'
		mistOutputNode.file_slots[0].path = get_output_name() + "Mist_"

	if not maskOutputNode:
		maskOutputNode = nodes.new('CompositorNodeOutputFile')
		maskOutputNode.name = maskOutputNode.label = "Mask"
		maskOutputNode.location = Vector((400, -400))
		maskOutputNode.width = 400
		maskOutputNode.format.file_format = 'PNG'
		maskOutputNode.format.color_mode = 'RGB'
		maskOutputNode.format.color_depth = '8'
		maskOutputNode.format.compression = 15
		maskOutputNode.base_path = get_output_path() + 'Mask\\'
		maskOutputNode.file_slots[0].path = get_output_name() + "Mask_"
	
	if not viewerNode:
		viewerNode = nodes.new('CompositorNodeViewer')
		viewerNode.location = Vector((400, -600))
		
	node_tree.links.new(cyclesRenderLayer.outputs['Image'], compositeNode.inputs[0])
	node_tree.links.new(cryptomattNode.outputs['Matte'], maskOutputNode.inputs[0])
	node_tree.links.new(eeveeRenderLayer.outputs['Mist'], mistOutputNode.inputs[0])
	node_tree.links.new(eeveeRenderLayer.outputs['Image'], MattOutputNode.inputs[0])
	node_tree.links.new(cryptomattNode.outputs['Image'], viewerNode.inputs[0])



def get_cycles_scene(ctx):
	if 'Cycles' in bpy.data.scenes:
		return bpy.data.scenes['Cycles']
	return ctx.scene



def setup_render_setting(ctx):
	cyclesScene = get_cycles_scene(ctx)
	set_cycle_paraqmeters(cyclesScene)

	eeveeScene = clone_scene(ctx)
	set_eevee_parameters(eeveeScene)
	set_mist(eeveeScene)

	set_as_active_scene(ctx, cyclesScene)
	
	out_put_setting(ctx, cyclesScene)
	meta_data_setting(cyclesScene)

	set_composit_up(cyclesScene, eeveeScene)



class Render_OT_Make_Ready_Render_v2(Operator):
	bl_idname = "nevil.make_ready_render_v2"
	bl_label = "Make Ready Render V2 (Nevil)"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		setup_render_setting(ctx)
		return{"FINISHED"}



def register_make_ready_render_v2():
	try:
		bpy.utils.register_class(Render_OT_Make_Ready_Render_v2)
	except:
		pass



def unregister_make_ready_render_v2():
	if hasattr(bpy.types, Render_OT_Make_Ready_Render_v2.bl_idname):
		bpy.utils.unregister_class(Render_OT_Make_Ready_Render_v2)



if __name__ == "__main__":
	setup_render_setting(bpy.context)