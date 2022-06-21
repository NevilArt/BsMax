#####################################
#	SMA YN Make Ready for Render
#	Base on EEVEE
#	Version 1.0.8 2021-09-10
#	
#	How to use:
#		Open Blender scene.
#		Open and apply this script.
#	Scene file naming rule:
#	(Short Name) + _ + 'B' + (Episod Number) + _ + (Scene Name) + _ + ('Render') + _ + (Number)
#		Example:
#			YN_B02_S17_Render_07.blend
#			YN_B02_S05Ek2_Render_03.blend
#			YN_B02_S07B_Render_00_rev.blend
#	What the script does:
#		Set Render Preset.
#		Creat out put pathes.
#		Check and Fix light setting and count (Sun).
#		Check and Fix Camera Setting.
#		Check and Fix Meta data setting.
#		Set Passes Mist/Mask.
#		Create Composit node setup and passes out puts.
#####################################

import bpy
import os

from bpy.types import Operator



def render_preset():
	"""
	#	Change render engine and set basic setting of render setting
	#	Mostly are default value
	"""

	""" Render Engine """
	bpy.context.scene.render.engine = 'BLENDER_EEVEE'

	scene = bpy.context.scene
	render = scene.render
	eevee = scene.eevee
		
	""" Sampling """
	eevee.taa_render_samples = 200
	
	""" AO """
	eevee.use_gtao = True
	eevee.gtao_distance = 0.2
	eevee.gtao_factor = 1
	eevee.gtao_quality = 0.25
	
	""" Bloom """
	eevee.use_bloom = False
	eevee.bloom_threshold = 0.8
	eevee.bloom_knee = 0.5
	eevee.bloom_radius = 6.5
	eevee.bloom_color = (1, 1, 1)
	eevee.bloom_intensity = 0.05
	eevee.bloom_clamp = 0
	
	""" Depth of Field """
	eevee.bokeh_max_size = 100
	eevee.bokeh_threshold = 1
	eevee.bokeh_neighbor_max = 10
	eevee.bokeh_denoise_fac = 0.75
	eevee.use_bokeh_high_quality_slight_defocus = False
	eevee.use_bokeh_jittered = False
	eevee.bokeh_overblur = 5

	""" SSS """
	eevee.sss_samples = 7
	eevee.sss_jitter_threshold = 0.3
	
	""" Reflect/refract """
	eevee.use_ssr = True
	eevee.use_ssr_refraction = True
	eevee.use_ssr_halfres = True
	eevee.ssr_quality = 0.25
	eevee.ssr_max_roughness = 0.5
	eevee.ssr_thickness = 0.2
	eevee.ssr_border_fade = 0.075
	eevee.ssr_firefly_fac = 10
	
	""" Mothin blur """
	eevee.use_motion_blur = False
	
	""" Volumetric """
	eevee.volumetric_start = 0.1
	eevee.volumetric_end = 100
	eevee.volumetric_tile_size = '8'
	eevee.volumetric_samples = 64
	eevee.volumetric_sample_distribution = 0.8
	eevee.use_volumetric_lights = True
	eevee.volumetric_light_clamp = 0
	eevee.use_volumetric_shadows = False
	eevee.volumetric_shadow_samples = 16

	""" Performance """
	render.use_high_quality_normals = False
	
	""" Hair """
	render.hair_type = 'STRIP'
	render.hair_subdiv = 0
	
	""" Shadow """
	eevee.shadow_cube_size = '4096'
	eevee.shadow_cascade_size = '4096'
	eevee.use_shadow_high_bitdepth = True
	eevee.use_soft_shadows = True
	eevee.light_threshold = 0.01
	
	""" Light cache """
	
	""" Film """
	render.filter_size = 1.5
	render.film_transparent = False
	eevee.use_overscan = True
	eevee.overscan_size = 3
	
	""" Simplify """
	render.use_simplify = False
	
	""" Color managment """
	scene.display_settings.display_device = 'sRGB'
	scene.view_settings.view_transform = 'Filmic'
	scene.view_settings.look = 'None'
	scene.view_settings.exposure = 0
	scene.view_settings.gamma = 1
	scene.sequencer_colorspace_settings.name = 'sRGB'
	scene.view_settings.use_curve_mapping = False



def output_set():
	"""
	#	Check and Set Render image size, Frame rate and Formats
	"""
	scene = bpy.context.scene
	render = scene.render
	
	""" Render Size """
	render.resolution_x = 1920
	render.resolution_y = 1080
	render.resolution_percentage = 100
	render.pixel_aspect_x = 1
	render.pixel_aspect_y = 1
	render.use_border = False

	""" Frame rate """
	scene.render.fps = 25
	
	""" Render File Format """
	render.use_file_extension = True
	render.use_render_cache = False
	render.image_settings.file_format = 'PNG'
	render.image_settings.color_mode = 'RGB'
	render.image_settings.color_depth = '8'
	render.image_settings.compression = 15
	render.use_overwrite = True
	render.use_placeholder = False

	""" Fix Frame Range if start from 1"""
	if scene.frame_start == 1:
		scene.frame_start = 0
	
	""" Post prosse setting """
	render.use_sequencer = True
	render.use_sequencer = False
	render.dither_intensity = 1.0

	render.use_multiview = False




def camera_check():
	"""
	#	Check/Set Camera cliping
	#	Start clip most be bigger than or equal 10cm
	#	End clip most be smaller then 200~300m
	"""
	active_camera = bpy.context.scene.camera
	
	""" pass if camera not exist """
	if not active_camera:
		return

	""" Check Camera Cliping """
	if active_camera.data.clip_start < 0.08:
		active_camera.data.clip_start = 0.1
	if active_camera.data.clip_end > 250:
		active_camera.data.clip_end = 200



def light_check():
	"""
	#	Scene has to have only one sunlight
	#	Create one of not exist
	#	Set if a sunlight is in scene
	#	Delete more sunlights than one
	"""
	""" check sunlight count """
	sun_lights = []
	
	for obj in bpy.data.objects:
		if obj.type == 'LIGHT':
			if obj.data.type == 'SUN':
				sun_lights.append(obj)
				
	""" Keep first sun light """
	if len(sun_lights) > 0:
		sun_light = sun_lights[0]
		sun_lights.pop(0)
	else:
		""" Create a new sun light if no light in scene """
		bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD',
			location=(0, 0, 10), rotation=(0, 0.2, 0.5), scale=(1, 1, 1))
	
		""" Find new created Sun light in scene lights """
		for obj in bpy.data.objects:
			if obj.type == 'LIGHT':
				if obj.data.type == 'SUN':
					sun_light = obj

	""" Delete extera sun lights """
	bpy.ops.object.select_all(action='DESELECT')
	for light in sun_lights:
		light.select_set(True)
	bpy.ops.object.delete({'selected_objects': sun_lights})

	""" Set Sunlight settings """
	if sun_light.name.lower() == 'sun':
		""" Day mode setting """
		sun_light.data.energy = 7
		sun_light.data.diffuse_factor = 1
		sun_light.data.specular_factor = 1
		sun_light.data.volume_factor = 1
		sun_light.data.angle = 0.0349066
	
	elif sun_light.name.lower() == 'moon':
		""" Night mode setting """
		sun_light.data.energy = 1
		sun_light.data.diffuse_factor = 1
		sun_light.data.specular_factor = 1
		sun_light.data.volume_factor = 1
		sun_light.data.angle = 0.174533
	
	""" Shadow """
	sun_light.data.use_shadow = True
	sun_light.data.shadow_buffer_bias = 0.001
	sun_light.data.shadow_cascade_count = 4
	sun_light.data.shadow_cascade_fade = 0.1
	sun_light.data.shadow_cascade_max_distance = 200
	sun_light.data.shadow_cascade_exponent = 0.8
	
	""" Disable contact shadow """
	sun_light.data.use_contact_shadow = False
	


def metadata_set():
	"""
	#	Make sure Burn to Image of meta data is off
	#	Turn on nececery datas only
	"""
	render = bpy.context.scene.render
	render.use_stamp_date = False
	render.use_stamp_time = False
	render.use_stamp_render_time = True
	render.use_stamp_frame = True
	render.use_stamp_frame_range = False
	render.use_stamp_memory = True
	render.use_stamp_hostname = False
	render.use_stamp_camera = False
	render.use_stamp_lens = False
	render.use_stamp_scene = False
	render.use_stamp_marker = False
	render.use_stamp_filename = False
	render.use_stamp_note = False
	render.use_stamp = False



def passes_set():
	"""
	#	Render passes setting
	#	Active the Mist and Crypto matt
	"""
	scene = bpy.context.scene
	world = scene.world
	view_layers = scene.view_layers[0]

	""" Data """
	view_layers.use_pass_combined = True
	view_layers.use_pass_z = False
	view_layers.use_pass_mist = True
	view_layers.use_pass_normal = False

	""" Light 'Reset to default' """
	view_layers.use_pass_diffuse_direct = False
	view_layers.use_pass_diffuse_color = False
	view_layers.use_pass_glossy_direct = False
	view_layers.use_pass_glossy_color = False
	# scene.use_pass_volume_direct = False
	view_layers.use_pass_emit = False
	view_layers.use_pass_environment = False
	view_layers.use_pass_shadow = False
	view_layers.use_pass_ambient_occlusion = False

	""" Mist Setting """
	world.mist_settings.start = 0
	world.mist_settings.depth = 200
	world.mist_settings.falloff = 'LINEAR'

	""" Crypto matte """
	view_layers.use_pass_cryptomatte_material = False
	view_layers.use_pass_cryptomatte_object = False
	view_layers.use_pass_cryptomatte_asset = True



def composit_setup():
	""" Create/Fix Composit node setup """
	scene = bpy.context.scene
	render_path = os.path.dirname(scene.render.filepath)
	parent_dir = os.path.dirname(render_path) + '\\'

	""" Create FileName from Render out """
	file_name = os.path.basename(scene.render.filepath)
	names = file_name.split('_')
	if len(names) == 5:
		render_file = names[0] + '_' + names[1] + '_' + names[2] + '_'
	else:
		render_file = 'XX_B00_S00'

	""" Enable Composite node tree """
	scene.use_nodes = True

	node_tree = scene.node_tree
	nodes = node_tree.nodes

	""" Detect Render Node """
	if 'Render Layers' in nodes:
		render_node = nodes['Render Layers']
		render_node.location.x = -400
		render_node.location.y = 500
	else:
		render_node = nodes.new('CompositorNodeRLayers')
		render_node.location.x = -400
		render_node.location.y = 500
	
	if 'Composite' in nodes:
		composite_node = nodes['Composite']
	else:
		composite_node = nodes.new('CompositorNodeComposite')
		composite_node.location.x = 100
		composite_node.location.y = 400

	node_tree.links.new(render_node.outputs['Image'], composite_node.inputs[0])

	""" Create Cryptomatt node """
	if 'Cryptomatte' in nodes:
		cryptomatt_node = nodes['Cryptomatte']
	else:
		cryptomatt_node = nodes.new('CompositorNodeCryptomatteV2')
		cryptomatt_node.width = 300
		cryptomatt_node.location.x = -400
		cryptomatt_node.location.y = -50
		cryptomatt_node.matte_id = ''

	""" Create Mist output node """   
	if 'File Output Mist' in nodes:
		mist_output = nodes['File Output Mist']
	else:
		mist_output = nodes.new('CompositorNodeOutputFile')
		mist_output.name = 'File Output Mist'
		mist_output.label = 'File Output Mist'
		mist_output.width = 400
		mist_output.location.x = 100
		mist_output.location.y = 200
		mist_output.format.file_format = 'PNG'
		mist_output.format.color_mode = 'RGB'
		mist_output.format.color_depth = '8'
		mist_output.format.compression = 15
		mist_output.base_path = parent_dir + 'Mist\\'
		mist_output.file_slots[0].path = render_file + 'Mist_'

	""" Connet Mist output node """
	node_tree.links.new(render_node.outputs['Mist'], mist_output.inputs[0])

	""" Create Mask output node """
	if 'File Output Mask' in nodes:
		mask_output = nodes['File Output Mask']
	else:
		mask_output = nodes.new('CompositorNodeOutputFile')
		mask_output.name = 'File Output Mask'
		mask_output.label = 'File Output Mask'
		mask_output.width = 400
		mask_output.location.x = 100
		mask_output.location.y = 0
		mask_output.format.file_format = 'PNG'
		mask_output.format.color_mode = 'RGB'
		mask_output.format.color_depth = '8'
		mask_output.format.compression = 15
		mask_output.base_path = parent_dir + 'Mask\\'
		mask_output.file_slots[0].path = render_file + 'Mask_'

	""" Connect Mask output node """
	node_tree.links.new(cryptomatt_node.outputs['Matte'], mask_output.inputs[0])

	""" Create Viewer node """
	if 'Viewer' in nodes:
		viewer_output = nodes['Viewer']
	else:
		viewer_output = nodes.new('CompositorNodeViewer')
		viewer_output.location.x = 100
		viewer_output.location.y = -150

	""" Connect Viewer Nnde """
	node_tree.links.new(cryptomatt_node.outputs['Pick'], viewer_output.inputs[0])

	""" Create list of characters and Set Matt IDs """
	armatures = [char for char in bpy.data.objects if char.type == 'ARMATURE']
	emptyes = [empty for empty in bpy.data.objects if empty.type == 'EMPTY']
	char_names = []
	
	""" Collect Armature names and make unique array """
	for armature in armatures:
		is_unique = not armature.name in char_names
		has_mesh = len(armature.children) > 0
		if is_unique and has_mesh:
			char_names.append(armature.name)
	
	""" 
	#	Collect Alembic Parent Helper
	#	Emptys with mesh child that has sequence cache
	"""
	for empty in emptyes:
		has_abc = False
		if empty.empty_display_type == 'SINGLE_ARROW':
			for child in empty.children:
				if child.type == 'MESH':
					for modifier in child.modifiers:
						if modifier.type == 'MESH_SEQUENCE_CACHE':
							has_abc = True

						""" Do not countinue search modifiers if found one """
						if has_abc:
							break

				""" Do not check other children if found any """
				if has_abc:
					break
		
		""" Get empty as owner of ABC Charcter """
		if has_abc:
			if not empty.name in char_names:
				char_names.append(empty.name)
	
	""" Collect extera objects in Character collection 
	*	if mesh or empty without parent and renderable
	"""
	for collection in  bpy.data.collections:
		if collection.name.lower() in {'character', 'characters'}:
			for obj in collection.objects:
				if obj.type in {'MESH', 'EMPTY'}:
					if obj.parent == None and not obj.hide_render:
						if not obj.name in char_names:
							char_names.append(obj.name)
		break
	
	matt_id, count = '', len(char_names)
	
	for index, name in enumerate(char_names):
		matt_id += name
		if index < count:
			matt_id += ','
	
	cryptomatt_node.matte_id = matt_id



def create_render_file_name():
	"""
	#	Genarate Render out path via Blender File name and Path
	#	Naming rolls
	#	(Short Name) + _ + 'B' + (Episod Number) + _ + (Scene Name) + _ + ('Render') + _ + (Number)
	#	Example:
	#		YN_B02_S17_Render_07
	#		YN_B02_S05Ek2_Render_03
	"""
	file_name = os.path.basename(bpy.data.filepath)

	""" Get project directory (Drive Name + First Folder Name) """
	dirs = (bpy.data.filepath).split('\\')
	if len(dirs) < 2:
		return
	main_dir = dirs[0] + '\\' + dirs[1] + '\\'

	""" Split file name to parts """
	keys = str(file_name).split('_')
	
	""" 
	#	Ignore if naming is not regular name
	#	[0]  [1]   [2]   [3]      [n]
	#	YN _ B02 _ S17 _ Render _ 07
	"""
	if len(keys) < 4:
		return
	
	""" Unpack Keys """
	short_name = keys[0]
	episode = keys[1]
	scene = keys[2]
	render = keys[3]

	""" second check for make sure naming is right """
	if render.lower() != 'render':
		return

	""" Get Episode number from second part of name """
	episode_index_name = ''
	for digit in episode:
		if digit in '0123456789':
			episode_index_name += digit
	if len(episode_index_name) == 0:
		return
	episode_index = int(episode_index_name)

	""" Create Render File name and Path """
	main_render_path = main_dir + 'RENDER\\'
	episod_path = main_render_path + str(episode_index) + '.BOLUM\\'
	
	scene_name = short_name + '_'
	scene_name += episode + '_'
	scene_name += scene + '\\'

	file_name = short_name + '_'
	file_name += episode + '_'
	file_name += scene + '_'
	file_name += 'Base_'

	scene_path = episod_path + scene_name

	""" Create Needed Folders if not exist """
	if not os.path.isdir(main_render_path):
		os.mkdir(main_render_path)
	
	if not os.path.isdir(episod_path):
		os.mkdir(episod_path)
	
	if not os.path.isdir(scene_path):
		os.mkdir(scene_path)
	
	if not os.path.isdir(scene_path + 'Base'):
		os.mkdir(scene_path + 'Base')
	
	if not os.path.isdir(scene_path + 'Mist'):
		os.mkdir(scene_path + 'Mist')
	
	if not os.path.isdir(scene_path + 'Mask'):
		os.mkdir(scene_path + 'Mask')
	
	""" Set output path """
	bpy.context.scene.render.filepath = scene_path + 'Base\\' + file_name


class Sequencer_OT_Make_Ready_Render(Operator):
	bl_idname = "nevil.make_ready_render"
	bl_label = "Make Ready Render (Nevil)"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		render_preset()
		output_set()
		create_render_file_name()
		camera_check()
		light_check()
		metadata_set()
		passes_set()
		composit_setup()
		return{"FINISHED"}


def register_make_ready_render():
	try:
		bpy.utils.register_class(Sequencer_OT_Make_Ready_Render)
	except:
		pass

def unregister_make_ready_render():
	if hasattr(bpy.types, Sequencer_OT_Make_Ready_Render.bl_idname):
		bpy.utils.unregister_class(Sequencer_OT_Make_Ready_Render)

if __name__ == '__main__':
	register_make_ready_render()