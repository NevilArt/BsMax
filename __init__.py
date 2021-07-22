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

bl_info = {
	'name': 'BsMax',
	'description': 'BsMax for Blender 2.80 ~ 3.0',
	'author': 'Naser Merati (Nevil)',
	'version': (0, 1, 0, 20210722),
	'blender': (2, 80, 0),# 2.80 ~ 3.0
	'location': 'Almost Everywhere in Blender',
	'wiki_url': 'https://github.com/NevilArt/BsMax_2_80/wiki',
	'doc_url': 'https://github.com/NevilArt/BsMax_2_80/wiki',
	'tracker_url': 'https://github.com/NevilArt/BsMax_2_80/issues',
	'category': 'Interface'
}

import bpy,sys,os
from bpy.props import EnumProperty, BoolProperty, FloatProperty
from time import sleep
from _thread import start_new_thread

# Add public classes, variables and functions path.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

from .keymaps import register_keymaps, unregister_keymaps
from .menu import register_menu, unregister_menu
from .primitive import register_primitives, unregister_primitives
from .startup import register_startup, unregister_startup
from .tools import register_tools, unregister_tools

# import templates

addons = bpy.context.preferences.addons
wiki = 'https://github.com/NevilArt/BsMax_2_80/wiki/'

# Addon preferences
def update_preferences(self, ctx, action):
	""" Radiobuttons """
	if action == 'quick' and self.quick:
		self.simple = self.custom = False
		self.refine()
	elif action == 'simple'and self.simple:
		self.quick = self.custom = False
		self.refine()
	elif action == 'custom' and self.custom:
		self.simple = self.quick = False
	if not self.quick and not self.simple and not self.custom:
		if action == 'quick':
			self.quick = True
		elif action == 'simple':
			self.simple = True
		elif action == 'custom':
			self.custom = True
		else:
			self.simple = True
	
	if self.active:
		""" Quick Selection """
		if self.quick and action == 'aplication':
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

		""" Simple Selection """
		if self.simple:
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
		if action in {'navigation_3d','navigation_2d','viowport', 'sculpt',
			'uv_editor', 'node_editor', 'text_editopr', 'graph_editor','clip_editor',
			'video_sequencer', 'text_editor','file_browser', 'floatmenus', 'view_undo'}:
			register_keymaps(addons[__name__].preferences)

class BsMax_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	active = BoolProperty(name='Active',default=False)
	
	quick: BoolProperty(name='Quick',default=False,
		update= lambda self,ctx: update_preferences(self,ctx,'quick'))
	simple: BoolProperty(name='Simple',default=True,
		update= lambda self,ctx: update_preferences(self,ctx,'simple'))
	custom: BoolProperty(name='Custom',default=False,
		update= lambda self,ctx: update_preferences(self,ctx,'custom'))
	
	apps = [('3DsMax', '3DsMax', 'Try to simulate 3DsMax HotKeys and Menus'),
		('Maya', 'Maya', 'Try to simulate Maya HotKeys'),
		('None', 'Blender (Default)', 'Do not makes any changes on Keymaps'),
		('Blender', 'Blender (Adapted)', 'Some Keymaps change to work with Bsmax')]
	custom = [('Custom', 'Custom','')]
	menus = [('3DsMax', '3DsMax (QuadMenu)','Simulate 3DsMax Quad menu'),
		('Maya','Maya (Not ready yet)',''),
		('Blender','Blender (Default)','')]
	
	""" Quick select mode """
	aplication: EnumProperty(name='Aplication', items=apps+custom, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'aplication'),
		description='select a package')

	""" Simple select mode """
	navigation: EnumProperty(name='Navigation', items=apps+custom, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'navigation'),
		description='select overide navigation mode')

	toolpack: EnumProperty(name='Tools Pack', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'toolpack'),
		description='Extera Overide Tools')

	floatmenus: EnumProperty(name='Float Menu', items=menus, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'floatmenus'),
		description='Float menus type')

	keymaps: EnumProperty(name='Keymap', items=apps+custom, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'keymaps'),
		description='Overide Full Keymap')
	
	""" Custom select mode """
	navigation_3d: EnumProperty(name='Navigation 3D', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'navigation_3d'),
		description='Overide navigation on 3D View')
	navigation_2d: EnumProperty(name='Navigation 2D', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'navigation_2d'),
		description='Overide navigation in 2D Views')
	viowport: EnumProperty(name='View 3D', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'viowport'),
		description='Overide keymaps in 3D view')
	sculpt: EnumProperty(name='Sculp/Paint', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'sculpt'),
		description='Overide keymaps in sculpt and paint mode')
	uv_editor: EnumProperty(name='UV Editor', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'uv_editor'),
		description='Overide keymaps in UV editor')
	node_editor: EnumProperty(name='Node Editor', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'node_editor'),
		description='Overide keymaps in Node editors')
	graph_editor: EnumProperty(name='Graph Editor', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'graph_editor'),
		description='Overide keymaps in Time ediotrs')
	clip_editor: EnumProperty(name='Clip Editor', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'clip_editor'),
		description='Overide keymaps in Clip editor')
	video_sequencer: EnumProperty(name='Video Sequencer', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'video_sequencer'),
		description='Overide keymaps in Video sequencer')
	text_editor: EnumProperty(name='Text Editor', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'text_editopr'),
		description='Overide keymaps in text editor')
	file_browser: EnumProperty(name='File Browser', items=apps, default='Blender',
		update= lambda self,ctx: update_preferences(self,ctx,'file_browser'),
		description='Overide keymaps in File Browser')

	""" Global options """
	options: BoolProperty(default=False)
	view_undo: BoolProperty(name='View Undo',default=False,
		update= lambda self, ctx: update_preferences(self,ctx,'view_undo'),
		description='undo the only view angle')
	menu_scale: FloatProperty(name='Float Menu Scale', min=1, max=3, description='')

	blender_transform_type: BoolProperty(name='Blender Transform Type', default=False,
		update= lambda self,ctx: update_preferences(self,ctx,'transform'),
		description='Make "W E R" work as "G R S", Need to restart to See effect')

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
		row = col.row()
		row.prop(self,name)
		srow = row.row()
		srow.scale_x = 1
		srow.operator('wm.url_open', icon='HELP').url= wiki + page

	def draw(self, ctx):
		layout = self.layout
		
		box = layout.box()
		row = box.row(align=True)
		row.prop(self, 'quick', icon='MESH_CIRCLE')
		row.prop(self, 'simple', icon='MESH_UVSPHERE')
		row.prop(self, 'custom', icon='MESH_ICOSPHERE')

		if self.quick:
			row = box.row()
			col = row.column()
			self.row_prop(col, 'aplication', 'applications')

		if self.simple:	
			row = box.row()
			col = row.column()
			self.row_prop(col, 'navigation', 'Navigation')
			self.row_prop(col, 'keymaps', 'Keymaps-' + self.keymaps)
			self.row_prop(col, 'floatmenus', 'floatmenus-' + self.floatmenus)
		
		if self.custom:
			row = box.row()
			col = row.column()

			self.row_prop(col, 'navigation_3d', 'navigation_3d-' + self.navigation_3d)
			self.row_prop(col, 'navigation_2d', 'navigation_2d-' + self.navigation_2d)
			self.row_prop(col, 'viowport', 'viowport-' + self.viowport)
			self.row_prop(col, 'sculpt', 'sculpt-' + self.sculpt)
			self.row_prop(col, 'uv_editor', 'uv_editor-' + self.uv_editor)
			self.row_prop(col, 'node_editor', 'node_editor-' + self.node_editor)
			self.row_prop(col, 'text_editor', 'text_editor-' + self.text_editor)
			self.row_prop(col, 'graph_editor', 'graph_editor-' + self.graph_editor)
			self.row_prop(col, 'clip_editor', 'clip_editor-' + self.clip_editor)
			self.row_prop(col, 'video_sequencer', 'video_sequencer-' + self.video_sequencer)
			self.row_prop(col, 'file_browser', 'file_browser-' + self.file_browser)
			self.row_prop(col, 'floatmenus', 'floatmenus-' + self.floatmenus)
		
		box = layout.box()
		row = box.row()
		icon = 'DOWNARROW_HLT' if self.options else 'RIGHTARROW'
		row.prop(self, 'options', text='Options', icon=icon)
		row.operator('bsmax.save_preferences', text='Save Preferences Setting', icon='FILE_TICK')
		
		if self.options:
			box = box.box()
			row = box.row()
			row.prop(self, 'view_undo')
			row.prop(self, 'menu_scale')
			row = box.row()
			row.prop(self, 'blender_transform_type')
		if self.menu_scale < 1:
			self.menu_scale = 1

def save_preferences(preferences):
	filename = bpy.utils.user_resource('SCRIPTS', 'addons') + '/BsMax.ini'
	string = ''
	for prop in preferences.bl_rna.properties:
		if not prop.is_readonly:
			key = prop.identifier
			if key != 'bl_idname':
				val = str(getattr(preferences, key))
				string += key + '=' + val + os.linesep
	ini = open(filename, 'w')
	ini.write(string)
	ini.close()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def load_preferences(preferences):
	# filename = bpy.utils.user_resource('SCRIPTS', 'addons') + '/BsMax.ini'
	filename = bpy.utils.user_resource('SCRIPTS') + '\\addons\\BsMax.ini'
	if os.path.exists(filename):
		string = open(filename).read()
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
					pass

class BsMax_OT_Save_Preferences(bpy.types.Operator):
	bl_idname = 'bsmax.save_preferences'
	bl_label = 'Save BsMax Preferences'
	bl_options = {'REGISTER', 'INTERNAL'}
	def execute(self, ctx):
		save_preferences(addons[__name__].preferences)
		return{'FINISHED'}

def register_delay(preferences):
	sleep(0.2)
	register_keymaps(preferences)
	register_startup(preferences)

def register():
	bpy.utils.register_class(BsMax_OT_Save_Preferences)
	bpy.utils.register_class(BsMax_AddonPreferences)
	preferences = addons[__name__].preferences
	load_preferences(preferences)
	preferences.active = True
	register_primitives()
	register_tools(preferences)
	register_menu(preferences)
	# templates.register()
	start_new_thread(register_delay,tuple([preferences]))
	
def unregister():
	save_preferences(addons[__name__].preferences)
	unregister_keymaps()
	unregister_menu()
	unregister_tools()
	unregister_primitives()
	unregister_startup()
	bpy.utils.unregister_class(BsMax_AddonPreferences)
	bpy.utils.unregister_class(BsMax_OT_Save_Preferences)
	# templates.unregister()
	if path in sys.path:
		sys.path.remove(path)