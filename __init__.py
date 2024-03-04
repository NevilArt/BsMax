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
# 2024/02/06

bl_info = {
	'name': 'BsMax',
	'description': 'Package of many tools + other CG apps UI mimic',
	'author': 'Naser Merati (Nevil)',
	'version': (0, 1, 2, 20240304),
	'blender': (3, 3, 0),# 3.3LTS ~ 4.1Beta
	'location': 'Almost Everywhere in Blender',
	'wiki_url': 'https://github.com/NevilArt/BsMax/wiki',
	'doc_url': 'https://github.com/NevilArt/BsMax/wiki',
	'tracker_url': 'https://github.com/NevilArt/BsMax/issues',
	'category': 'Interface'
}


import bpy
import sys
import os

from bpy.props import (EnumProperty, BoolProperty, FloatProperty)
from time import sleep
from _thread import start_new_thread
from bpy.utils import (register_class, unregister_class)

# Add public classes, variables and functions path if not in list.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

from .bsmax import register_bsmax, unregister_bsmax
from .keymaps import register_keymaps, unregister_keymaps
from .menu import register_menu, unregister_menu
from .primitive import register_primitives, unregister_primitives
from .startup import register_startup, unregister_startup
from .tools import register_tools, unregister_tools

# import templates

addons = bpy.context.preferences.addons
wiki = 'https://github.com/NevilArt/BsMax/wiki/'
iniFileName = bpy.utils.user_resource('SCRIPTS') + '\\addons\\BsMax.ini'


# Addon preferences
def update_preferences(self, ctx, action):
	""" Quick Selection """
	if self.mode == 'QUICK' and action == 'aplication':
		if self.aplication != 'Custom':
			self.navigation = self.aplication
			self.keymaps = self.aplication
			self.toolpack = self.aplication

			self.navigation_3d = self.aplication
			self.navigation_2d = self.aplication
			self.viowport = self.aplication
			self.sculpt = self.aplication
			self.uv_editor = self.aplication
			self.node_editor = self.aplication
			self.graph_editor = self.aplication
			self.clip_editor = self.aplication
			self.video_sequencer = self.aplication
			self.text_editor = self.aplication
			self.file_browser = self.aplication
			self.floatmenus = self.aplication

			if self.aplication == '3DsMax':
				self.side_panel='3DsMax'
			else:
				self.side_panel='None'

	""" Simple Selection """
	if self.mode == 'SIMPLE':
		if action == 'navigation':
			if self.navigation != 'Custom':
				self.navigation_3d = self.navigation
				self.navigation_2d = self.navigation
			return

		elif action in {'keymaps', 'transform'}:
			if self.keymaps != 'Custom':
				self.viowport = self.keymaps
				self.sculpt = self.keymaps
				self.uv_editor = self.keymaps
				self.node_editor = self.keymaps
				self.graph_editor = self.keymaps
				self.clip_editor = self.keymaps
				self.video_sequencer = self.keymaps
				self.text_editor = self.keymaps
				self.file_browser = self.keymaps
			return

	""" Custom Selection """
	if action in {
		'navigation_3d', 'navigation_2d','viowport',
		'sculpt', 'uv_editor', 'node_editor', 'text_editopr',
		'graph_editor','clip_editor', 'video_sequencer',
		'text_editor','file_browser', 'floatmenus', 'view_undo'
		}:
		
		global addons
		register_keymaps(addons[__name__].preferences)
  

def draw_simple_panel(self, layout):
	row = layout.row()
	col = row.column()
	col.label(text='Select packages parts separately')
	self.row_prop(col, 'navigation', 'Navigation')
	self.row_prop(col, 'keymaps', 'Keymaps-' + self.keymaps)
	self.row_prop(col, 'floatmenus', 'floatmenus-' + self.floatmenus)
	#TODO update wiki page
	self.row_prop(col, 'side_panel', 'SidePanel-' + self.floatmenus)
	col.label(text='Note: Sometimes need to restart Blender to addon work properly')


def draw_custom_panel(self, layout):
	row = layout.row()
	col = row.column()
	col.label(text='Select packages parts customly')

	self.row_prop(col, 'navigation_3d', 'navigation_3d-' + self.navigation_3d)
	self.row_prop(col, 'navigation_2d',	'navigation_2d-' + self.navigation_2d)
	self.row_prop(col, 'viowport', 'viowport-' + self.viowport)
	self.row_prop(col, 'sculpt', 'sculpt-' + self.sculpt)
	self.row_prop(col, 'uv_editor','uv_editor-' + self.uv_editor)
	self.row_prop(col, 'node_editor', 'node_editor-' + self.node_editor)
	self.row_prop(col, 'text_editor', 'text_editor-' + self.text_editor)
	self.row_prop(col, 'graph_editor', 'graph_editor-' + self.graph_editor)
	self.row_prop(col, 'clip_editor', 'clip_editor-' + self.clip_editor)
	self.row_prop(
		col, 'video_sequencer','video_sequencer-' + self.video_sequencer
	)
	self.row_prop(col, 'file_browser', 'file_browser-' + self.file_browser)
	self.row_prop(col, 'floatmenus', 'floatmenus-' + self.floatmenus)
	self.row_prop(col, 'side_panel', 'SidePanel-' + self.floatmenus)
	col.label(text='Note: Sometimes need to restart Blender to addon work properly')


def draw_option_panel(self, layout):
	box = layout.box()
	row = box.row()
	row.prop(self, 'view_undo')
	row.prop(self, 'menu_scale')
	row = box.row()
	row.prop(self, 'blender_transform_type')
	row.prop(self, 'nevil_stuff')
	row = box.row()
	row.prop(self, 'geonode_pirimitve')
	row.prop(self, 'affect_theme')
	row = box.row()
	row.prop(self, 'experimental')


class BsMax_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	mode: EnumProperty(
		items=[
			# (
			# 	'QUICK', 'Quick',
			# 	'Select full package at once',
			# 	'MESH_CIRCLE', 1
			# ),
			(
				'SIMPLE', 'Simple',
				'Select Package by main parts',
				'MESH_UVSPHERE', 2
			),
			(
				'CUSTOM', 'Custom',
				'Select Package part by part',
				'MESH_ICOSPHERE', 3
			)
		],
		default='SIMPLE',
		update= lambda self,ctx: update_preferences(self, ctx, 'aplication'),
		description='select a package'
	)

	active = BoolProperty(name='Active', default=False)
	
	quick: BoolProperty(
		name='Quick',
		default=False,
		update= lambda self,ctx: update_preferences(self,ctx,'quick')
	)

	simple: BoolProperty(
		name='Simple',
		default=True,
		update= lambda self,ctx: update_preferences(self,ctx,'simple')
	)

	custom: BoolProperty(
		name='Custom',
		default=False,
		update= lambda self,ctx: update_preferences(self,ctx,'custom')
	)
	
	apps = [
		(
			'3DsMax',
			'3DsMax',
			'Try to simulate 3DsMax HotKeys and Menus'
		),
		
		(
			'Maya',
			'Maya',
			'Try to simulate Maya HotKeys'
		),
		
		(
			'None',
			'Blender (Default)',
			'Do not makes any changes on Keymaps'
		),
		
		(
			'Blender',
			'Blender (Adapted)',
			'Some Keymaps change to work with Bsmax'
		)
	]

	custom = [('Custom', 'Custom','')]

	menus = [
		(
			'3DsMax',
			'3DsMax (Quad Menu)',
			'Simulate 3DsMax Quad menu'
		),
		
		(	'PieMax',
   			'3DsMax (Pie Menu) (Under Construction)',
			'Simulate 3DsMax Quad menu as Pie Menu'
		),
		
		(
			'Maya',
			'Maya (Not ready yet)',
			''
		),
		
		(
			'Blender',
			'Blender (Default)',
			'Do not make any changes.'
		)
	]

	panels = [
		('3DsMax', '3DsMax (Command Panel)', ''),
		('None', 'None', '')
	]
	
	""" Quick select mode """
	aplication: EnumProperty(
		name='Aplication',
		items=apps+custom,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'aplication'),
		description='select a package'
	)

	""" Simple select mode """
	navigation: EnumProperty(
		name='Navigation',
		items=apps+custom,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'navigation'),
		description='select overide navigation mode'
	)

	toolpack: EnumProperty(
		name='Tools Pack',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'toolpack'),
		description='Extera Overide Tools'
	)

	keymaps: EnumProperty(
		name='Keymap',
		items=apps+custom,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'keymaps'),
		description='Overide Full Keymap'
	)

	floatmenus: EnumProperty(
		name='Float Menu',
		items=menus,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'floatmenus'),
		description='Float menus type'
	)


	side_panel: EnumProperty(
		name='Side Panel',
		items=panels,
		default='None',
		# upadate= lambda self,ctx: update_preferences(self, ctx, 'panel'),
		description='panel in right side of target software'
	)
	
	
	""" Custom select mode """
	navigation_3d: EnumProperty(
		name='Navigation 3D',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'navigation_3d'),
		description='Overide navigation on 3D View'
	)

	navigation_2d: EnumProperty(
		name='Navigation 2D',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'navigation_2d'),
		description='Overide navigation in 2D Views'
	)

	viowport: EnumProperty(
		name='View 3D',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'viowport'),
		description='Overide keymaps in 3D view'
	)

	sculpt: EnumProperty(
		name='Sculp / Paint',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'sculpt'),
		description='Overide keymaps in sculpt and paint mode'
	)

	uv_editor: EnumProperty(
		name='UV Editor',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'uv_editor'),
		description='Overide keymaps in UV editor'
	)

	node_editor: EnumProperty(
		name='Node Editor',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'node_editor'),
		description='Overide keymaps in Node editors'
	)

	graph_editor: EnumProperty(
		name='Graph Editor',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'graph_editor'),
		description='Overide keymaps in Time ediotrs'
	)

	clip_editor: EnumProperty(
		name='Clip Editor',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'clip_editor'),
		description='Overide keymaps in Clip editor'
	)
	
	video_sequencer: EnumProperty(
		name='Video Sequencer',
		items=apps + [('Premiere','Premiere','')],
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'video_sequencer'),
		description='Overide keymaps in Video sequencer'
	)

	text_editor: EnumProperty(
		name='Text Editor',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'text_editopr'),
		description='Overide keymaps in text editor'
	)

	file_browser: EnumProperty(
		name='File Browser',
		items=apps,
		default='Blender',
		update= lambda self,ctx: update_preferences(self, ctx, 'file_browser'),
		description='Overide keymaps in File Browser'
	)

	""" Global options """
	options: BoolProperty(default=False)

	view_undo: BoolProperty(
		name='View Undo',
		default=False,
		update= lambda self, ctx: update_preferences(self, ctx, 'view_undo'),
		description='undo the only view angle'
	)

	menu_scale: FloatProperty(
		name='Float Menu Scale', min=1, max=3, description=''
	)

	menu_auto_scale: BoolProperty(
		name='Auto',
		default=False,
		description='Link float menu size to thema scale value'
	)

	blender_transform_type: BoolProperty(
		name='Blender Transform Type',
		default=False,
		update= lambda self,ctx: update_preferences(self, ctx, 'transform'),
		description='Make "W E R" work as "G R S", Need to restart to See effect'
	)

	nevil_stuff: BoolProperty(
		name='Developer Exteras',
		default=False,
		description='This tools may not usefull for theres, just keep it off'
	)

	affect_theme: BoolProperty(
		name='Affect Theme',
		default=True,
		description='Let addon change some part of theme'
	)

	experimental: BoolProperty(
		name='Experimental',
		default=False,
		description='Enable unfinished tools too'
	)

	geonode_pirimitve: BoolProperty(
		name='GeoNode primitive',
		default=False,
		description='Convert Primitives to geometry node modfier'
	)

	def refine(self):
		""" Disactive keymap update """
		self.active = False

		""" Simple mode navigation """
		if self.navigation_3d == self.navigation_2d:
			if self.navigation == 'Custom':
				self.navigation = self.navigation_3d

		elif self.navigation != 'Custom':
			self.navigation = 'Custom'

		""" Simple mode keymap """
		if self.viowport == self.sculpt and\
			self.viowport == self.uv_editor and\
			self.viowport == self.node_editor and\
			self.viowport == self.text_editor and\
			self.viowport == self.graph_editor and\
			self.viowport == self.clip_editor and\
			self.viowport == self.video_sequencer and\
			self.viowport == self.file_browser:
			if self.keymaps == 'Custom':
				self.keymaps = self.viowport
		elif self.keymaps != 'Custom':
			self.keymaps = 'Custom'

		""" Quick select mode """
		if self.navigation == self.keymaps and\
			self.navigation == self.floatmenus:
			if self.aplication == 'Custom':
				self.aplication = self.navigation
		elif self.aplication != 'Custom':
			self.aplication = 'Custom'

		""" Reactive keymap update """
		self.active = True

	def row_prop(self, col, name, page):
		global wiki
		row = col.row()
		row.prop(self,name)
		srow = row.row()
		srow.scale_x = 1
		srow.operator('wm.url_open', icon='HELP').url= wiki + page

	def draw(self, ctx):
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
		row.prop(self, 'options', text='Options', icon=icon)

		row.operator(
			'bsmax.save_preferences',
			text='Save Preferences Setting',
			icon='FILE_TICK'
		)
		
		if self.options:
			draw_option_panel(self, box)

		if self.menu_scale < 1:
			self.menu_scale = 1


def save_preferences(preferences):
	global iniFileName
	string = ''

	for prop in preferences.bl_rna.properties:
		if not prop.is_readonly:
			key = prop.identifier
			if key != 'bl_idname':
				val = str(getattr(preferences, key))
				string += key + '=' + val + os.linesep

	ini = open(iniFileName, 'w')
	ini.write(string)
	ini.close()


def isfloat(value):
	try:
		float(value)
		return True

	except ValueError:
		return False


def load_preferences(preferences):
	global iniFileName

	if os.path.exists(iniFileName):
		string = open(iniFileName).read()
		props = string.splitlines()

		for prop in props:
			key = prop.split('=')

			if len(key) == 2:
				if isfloat(key[1]):
					value = float(key[1])
				elif key[1] in {'True', 'False'}:
					value = key[1] == 'True'
				else:
					value = key[1]

				try:
					if hasattr(preferences, key[0]):
						setattr(preferences, key[0], value)
				except:
					# ignore if there is not the attribute
					pass


class BsMax_OT_Save_Preferences(bpy.types.Operator):
	bl_idname = 'bsmax.save_preferences'
	bl_label = 'Save BsMax Preferences'
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		global addons
		save_preferences(addons[__name__].preferences)
		return{'FINISHED'}


def register_delay(preferences):
	sleep(0.2)
	register_keymaps(preferences)
	register_startup(preferences)


classes = (
	BsMax_OT_Save_Preferences,
	BsMax_AddonPreferences
)


def register():
	for c in classes:
		register_class(c)

	global addons
	preferences = addons[__name__].preferences
	load_preferences(preferences)
	preferences.active = True

	register_bsmax()
	register_primitives(preferences)
	register_tools(preferences)
	register_menu(preferences)

	# templates.register()
	start_new_thread(register_delay, tuple([preferences]))
	

def unregister():
	global addons
	save_preferences(addons[__name__].preferences)

	unregister_keymaps()
	unregister_menu()
	unregister_tools()
	unregister_primitives()
	unregister_startup()
	unregister_bsmax()

	for c in classes:
		unregister_class(c)

	# templates.unregister()
	if path in sys.path:
		sys.path.remove(path)