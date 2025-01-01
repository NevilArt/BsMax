############################################################################
#	BsMax, 3D apps inteface simulator and tools pack for Blender
#	Copyright (C) 2021  Naser Merati (Nevil)
#
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
# 2024/12/27

bl_info = {
	'name': "BsMax",
	'description': "BsMax UI simulations and Tool pack (Blender 3.6LTS ~ 4.3)",
	'author': "Nevil Tan (Naser Merati)",
	'version': (0, 1, 3, 20250101),
	'blender': (3, 6, 0), # Minimum Version
	'location': "Almost Everywhere in Blender",
	'doc_url': 'https://github.com/NevilArt/BsMax/wiki',
	'tracker_url': 'https://github.com/NevilArt/BsMax/issues',
	'category': "Interface"
}

import bpy
import sys
import os

# Add public classes, variables and functions path if not in list.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

from bpy.types import AddonPreferences, Operator
from bpy.props import EnumProperty, BoolProperty, FloatProperty
from time import sleep
from _thread import start_new_thread
from bpy.utils import register_class, unregister_class

from .bsmax import register_bsmax, unregister_bsmax
from .keymaps import register_keymaps, unregister_keymaps
from .menu import register_menu, unregister_menu
from .primitive import register_primitives, unregister_primitives
from .startup import register_startup, unregister_startup
from .tools import register_tools, unregister_tools
from bsmax.data_file import (
	get_datafiles_path,
	write_dictionary_to_json_file,
	read_json_file_to_dictionary,
	open_folder_in_explorer
)

# import templates

def wiki():
	return 'https://github.com/NevilArt/BsMax/wiki/'

# Addon preferences
def update_preferences(cls, _, action):
	addons = bpy.context.preferences.addons
	preferences = addons[__name__].preferences
	""" Quick Selection """
	if cls.mode == 'QUICK' and action == 'APLICATION':
		if cls.aplication != 'CUSTOM':
			cls.navigation = cls.aplication
			cls.keymaps = cls.aplication

			cls.navigation_3d = cls.aplication
			cls.navigation_2d = cls.aplication
			cls.viowport = cls.aplication
			cls.sculpt = cls.aplication
			cls.uv_editor = cls.aplication
			cls.node_editor = cls.aplication
			cls.graph_editor = cls.aplication
			cls.clip_editor = cls.aplication
			cls.video_sequencer = cls.aplication
			cls.text_editor = cls.aplication
			cls.file_browser = cls.aplication
			cls.floatmenus = cls.aplication

			if cls.aplication == '3DSMAX':
				cls.side_panel='3DSMAX'
			else:
				cls.side_panel='NONE'

	""" Simple Selection """
	if cls.mode == 'SIMPLE':
		if action == 'NAVIGATION':
			if cls.navigation != 'CUSTOM':
				cls.navigation_3d = cls.navigation
				cls.navigation_2d = cls.navigation
			return

		elif action in {'KEYMAPS', 'TRANSFORM'}:
			if cls.keymaps != 'CUSTOM':
				cls.viowport = cls.keymaps
				cls.sculpt = cls.keymaps
				cls.uv_editor = cls.keymaps
				cls.node_editor = cls.keymaps
				cls.graph_editor = cls.keymaps
				cls.clip_editor = cls.keymaps
				cls.video_sequencer = cls.keymaps
				cls.text_editor = cls.keymaps
				cls.file_browser = cls.keymaps
			return

	""" Custom Selection """
	if action in {
		'NAVIGATION_3D', 'NAVIGATION_2D','VIEWPORT',
		'SCULPT', 'UV_EDITOR', 'NODE_EDITOR', 'TEXT_EDITOR',
		'GRAPH_EDITOR','CLIP_EDITOR', 'VIDEO_SEQUENCER',
		'FILE_BROWSER', 'FLOATMENUS', 'VIEW_UNDO'
		}:

		register_keymaps(preferences)
	
	if action == 'PANEL':
		pass


def row_prop(cls, col, name, page):
	row = col.row()
	row.prop(cls, name)
	srow = row.row()
	srow.scale_x = 1
	srow.operator('wm.url_open', icon='HELP').url= wiki() + page
  

def draw_simple_panel(cls, layout):
	row = layout.row()
	col = row.column()
	col.label(text="Select packages parts separately")
	row_prop(cls, col, 'navigation', 'Navigation')
	row_prop(cls, col, 'keymaps', 'Keymaps-' + cls.keymaps)
	row_prop(cls, col, 'floatmenus', 'floatmenus-' + cls.floatmenus)
	#TODO update wiki page
	row_prop(cls, col, 'side_panel', 'SidePanel-' + cls.floatmenus)
	col.label(
		text="Note: Sometimes need to restart Blender to addon work properly"
	)


def draw_custom_panel(cls, layout):
	row = layout.row()
	col = row.column()
	col.label(text="Select packages parts customly")

	row_prop(cls, col, 'navigation_3d', 'navigation_3d-' + cls.navigation_3d)
	row_prop(cls, col, 'navigation_2d',	'navigation_2d-' + cls.navigation_2d)
	row_prop(cls, col, 'viowport', 'viowport-' + cls.viowport)
	row_prop(cls, col, 'sculpt', 'sculpt-' + cls.sculpt)
	row_prop(cls, col, 'uv_editor','uv_editor-' + cls.uv_editor)
	row_prop(cls, col, 'node_editor', 'node_editor-' + cls.node_editor)
	row_prop(cls, col, 'text_editor', 'text_editor-' + cls.text_editor)
	row_prop(cls, col, 'graph_editor', 'graph_editor-' + cls.graph_editor)
	row_prop(cls, col, 'clip_editor', 'clip_editor-' + cls.clip_editor)
	row_prop(cls, 
		col, 'video_sequencer', 'video_sequencer-' + cls.video_sequencer
	)

	row_prop(cls, col, 'file_browser', 'file_browser-' + cls.file_browser)
	row_prop(cls, col, 'floatmenus', 'floatmenus-' + cls.floatmenus)
	row_prop(cls, col, 'side_panel', 'SidePanel-' + cls.floatmenus)

	col.label(
		text="Note: Sometimes need to restart Blender to addon work properly"
	)


def draw_option_panel(cls, layout):
	box = layout.box()
	row = box.row()
	row.prop(cls, 'view_undo')
	row.prop(cls, 'menu_scale')
	row = box.row()
	row.prop(cls, 'blender_transform_type')
	row.prop(cls, 'nevil_stuff')
	row = box.row()
	row.prop(cls, 'geonode_pirimitve')
	row.prop(cls, 'affect_theme')
	row = box.row()
	row.prop(cls, 'experimental')

def get_bsmax_json_file_name():
	return get_datafiles_path() + os.sep + 'BsMax.json'


def save_preferences(preferences):
	file_name = get_bsmax_json_file_name()
	dictionary = {}

	for prop in preferences.bl_rna.properties:
		if prop.is_readonly:
			continue
		
		key = prop.identifier
		if key == 'bl_idname':
			continue
		
		dictionary[key] = getattr(preferences, key)

	write_dictionary_to_json_file(dictionary, file_name)


def load_preferences(preferences):
	file_name = get_bsmax_json_file_name()

	if not os.path.exists(file_name):
		return
	
	dictionary = read_json_file_to_dictionary(file_name)
	
	for key, value in dictionary.items():
		if hasattr(preferences, key):
			current_value = getattr(preferences, key)
			# apply value only if has changed
			if value != current_value:
				setattr(preferences, key, value)


class BsMax_AddonPreferences(AddonPreferences):
	bl_idname = __name__

	mode: EnumProperty(
		items=[
			(
				'SIMPLE',
				"Simple",
				"Select Package by main parts",
				'MESH_UVSPHERE', 2
			),
			(
				'CUSTOM',
				"Custom",
				"Select Package part by part",
				'MESH_ICOSPHERE', 3
			)
		],
		default='SIMPLE',
		update= lambda self, ctx: update_preferences(self, ctx, 'aplication'),
		description="select a package"
	) # type: ignore
	
	apps = [
		(
			'3DSMAX',
			"3DsMax",
			"Try to simulate 3DsMax HotKeys and Menus"
		),
		
		(
			'MAYA',
			"Maya",
			"Try to simulate Maya HotKeys"
		),
		
		(
			'NONE',
			"Blender (Default)",
			"Do not makes any changes on Keymaps"
		),
		
		(
			'BLENDER',
			"Blender (Adapted)",
			"Some Keymaps change to work with Bsmax"
		)
	]

	custom = [('CUSTOM', "Custom", "")]

	menus = [
		(
			'3DSMAX',
			"3DsMax (Quad Menu)",
			"Simulate 3DsMax Quad menu"
		),
		
		(	'PIEMAX',
   			"3DsMax (Pie Menu) (Under Construction)",
			"Simulate 3DsMax Quad menu as Pie Menu"
		),
		
		(
			'MAYA',
			"Maya (Not ready yet)",
			""
		),
		
		(
			'BLENDER',
			"Blender (Default)",
			"Do not make any changes."
		)
	]

	panels = [
		('3DSMAX', "3DsMax (Command Panel)", ""),
		('NONE', "None", "")
	]
	
	""" Quick select mode """
	aplication: EnumProperty(
		name="Aplication",
		items=apps+custom,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'APLICATION'),
		description="select a package"
	) # type: ignore

	""" Simple select mode """
	navigation: EnumProperty(
		name="Navigation",
		items=apps+custom,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'NAVIGATION'),
		description="select overide navigation mode"
	) # type: ignore

	keymaps: EnumProperty(
		name="Keymap",
		items=apps+custom,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'KEYMAPS'),
		description="Overide Full Keymap"
	) # type: ignore

	floatmenus: EnumProperty(
		name="Float Menu",
		items=menus,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'FLOATMENUS'),
		description="Float menus type"
	) # type: ignore


	side_panel: EnumProperty(
		name="Side Panel",
		items=panels,
		default='NONE',
		update= lambda self, ctx: update_preferences(self, ctx, 'PANEL'),
		description="panel in right side of target software"
	) # type: ignore
	
	
	""" Custom select mode """
	navigation_3d: EnumProperty(
		name="Navigation 3D",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'NAVIGATION_3D'
		),

		description="Overide navigation on 3D View"
	) # type: ignore

	navigation_2d: EnumProperty(
		name="Navigation 2D",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'NAVIGATION_2D'
		),

		description="Overide navigation in 2D Views"
	) # type: ignore

	viowport: EnumProperty(
		name="View 3D",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'VIEWPORT'),
		description="Overide keymaps in 3D view"
	) # type: ignore

	sculpt: EnumProperty(
		name="Sculpt / Paint",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'SCULPT'),
		description="Overide keymaps in sculpt and paint mode"
	) # type: ignore

	uv_editor: EnumProperty(
		name="UV Editor",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'UV_EDITOR'),
		description="Overide keymaps in UV editor"
	) # type: ignore

	node_editor: EnumProperty(
		name="Node Editor",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'NODE_EDITOR'),
		description="Overide keymaps in Node editors"
	) # type: ignore

	graph_editor: EnumProperty(
		name="Graph Editor",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'GRAPH_EDITOR'
		),
		description="Overide keymaps in Time ediotrs"
	) # type: ignore

	clip_editor: EnumProperty(
		name="Clip Editor",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(self, ctx, 'CLIP_EDITOR'),
		description="Overide keymaps in Clip editor"
	) # type: ignore
	
	video_sequencer: EnumProperty(
		name="Video Sequencer",
		items=apps + [('Premiere', "Premiere", "")],
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'VIDEO_SEQUENCER'
		),
		description="Overide keymaps in Video sequencer"
	) # type: ignore

	text_editor: EnumProperty(
		name="Text Editor",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'TEXT_EDITOR'
		),
		description="Overide keymaps in text editor"
	) # type: ignore

	file_browser: EnumProperty(
		name="File Browser",
		items=apps,
		default='BLENDER',
		update= lambda self, ctx: update_preferences(
			self, ctx, 'FILE_BROWSER'
		),
		description="Overide keymaps in File Browser"
	) # type: ignore

	""" Global options """
	options: BoolProperty(default=False) # type: ignore

	view_undo: BoolProperty(
		name="View Undo",
		default=False,
		update= lambda self, ctx: update_preferences(self, ctx, 'VIEW_UNDO'),
		description="undo the only view angle"
	) # type: ignore

	menu_scale: FloatProperty(
		name="Float Menu Scale", min=1, max=3,
		description=""
	) # type: ignore

	menu_auto_scale: BoolProperty(
		name="Auto",
		default=False,
		description="Link float menu size to thema scale value"
	) # type: ignore

	blender_transform_type: BoolProperty(
		name="Blender Transform Type",
		default=False,
		update= lambda self, ctx: update_preferences(self, ctx, 'TRANSFORM'),
		description="Make 'W E R' work as 'G R S', Need to restart to See effect"
	) # type: ignore

	nevil_stuff: BoolProperty(
		name="Developer Exteras",
		default=False,
		description="This tools may not usefull for theres, just keep it off"
	) # type: ignore

	affect_theme: BoolProperty(
		name="Affect Theme",
		default=True,
		description="Let addon change some part of theme"
	) # type: ignore

	experimental: BoolProperty(
		name="Experimental",
		default=False,
		description="Enable unfinished tools too"
	) # type: ignore

	geonode_pirimitve: BoolProperty(
		name="GeoNode primitive",
		default=False,
		description="Convert Primitives to geometry node modfier"
	) # type: ignore

	def draw(self, _):
		layout = self.layout

		box = layout.box()
		row = box.row(align=True)
		row.prop(self, 'mode', expand=True)
		
		if self.mode == 'SIMPLE':
			draw_simple_panel(self, box)

		elif self.mode == 'CUSTOM':
			draw_custom_panel(self, box)

		box = layout.box()
		row = box.row()
		icon = 'DOWNARROW_HLT' if self.options else 'RIGHTARROW'
		row.prop(self, 'options', text="Options", icon=icon)

		row.operator(
			'bsmax.save_preferences',
			text="Save Preferences Setting",
			icon='FILE_TICK'
		)

		row.operator(
			'bsmax.open_data_file_directory',
			text="", icon='FILEBROWSER'
		)
		
		if self.options:
			draw_option_panel(self, box)

		if self.menu_scale < 1:
			self.menu_scale = 1


class BsMax_OT_Save_Preferences(Operator):
	bl_idname = 'bsmax.save_preferences'
	bl_label = "Save BsMax Preferences"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, _):
		addons = bpy.context.preferences.addons
		save_preferences(addons[__name__].preferences)
		return{'FINISHED'}


class BsMax_OT_Open_Data_File_Directory(Operator):
	bl_idname = 'bsmax.open_data_file_directory'
	bl_label = "Open datafile directory"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, _):
		open_folder_in_explorer(get_datafiles_path() + os.sep)
		return{'FINISHED'}


def register_delay(preferences):
	sleep(0.2)
	register_keymaps(preferences)
	register_startup(preferences)


classes = {
	BsMax_OT_Save_Preferences,
	BsMax_OT_Open_Data_File_Directory,
	BsMax_AddonPreferences
}


def register():
	global classes
	
	addons = bpy.context.preferences.addons
	for cls in classes:
		register_class(cls)

	preferences = addons[__name__].preferences
	load_preferences(preferences)

	register_bsmax()
	register_primitives(preferences)
	register_tools(preferences)
	register_menu(preferences)

	# templates.register()
	start_new_thread(register_delay, tuple([preferences]))
	

def unregister():
	global classes
	addons = bpy.context.preferences.addons
	save_preferences(addons[__name__].preferences)

	unregister_keymaps()
	unregister_menu()
	unregister_tools()
	unregister_primitives()
	unregister_startup()
	unregister_bsmax()

	for cls in classes:
		unregister_class(cls)

	# templates.unregister()
	if path in sys.path:
		sys.path.remove(path)