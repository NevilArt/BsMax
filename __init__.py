############################################################################
#	BsMax, 3D apps inteface simulator and tools pack for Blender
#	Copyright (C) 2020  Naser Merati (Nevil)
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
	"name": "BsMax",
	"description": "BsMax for Blender 2.80 ~ 2.90",
	"author": "Naser Merati (Nevil)",
	"version": (0, 1, 0, 20200425),
	"blender": (2, 80, 0),# 2.80~2.90
	"location": "Almost Everywhere in Blender",
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	"category": "Interface"
}

import bpy,sys,os
from bpy.props import EnumProperty
from bpy.types import Operator, AddonPreferences
from time import sleep
from _thread import start_new_thread

# Add public classes, variables and functions path.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

import templates

from .keymaps import register_keymaps,unregister_keymaps,register_navigation,unregister_navigation
from .menu import register_menu,unregister_menu
from .primitive import register_primitives,unregister_primitives
from .startup import register_startup,unregister_startup
from .tools import register_tools,unregister_tools,register_special

addons = bpy.context.preferences.addons
# Addon preferences
def update_navigation(self, ctx):
	register_navigation(addons[__name__].preferences)

def update_toolpack(self, ctx):
	register_special(addons[__name__].preferences)

def update_floatmenu(self, ctx):
	register_menu(addons[__name__].preferences)

def update_keymaps(self, ctx):
	self.arreng()
	register_keymaps(addons[__name__].preferences)

class BsMax_AddonPreferences(AddonPreferences):
	bl_idname = __name__

	navigation: EnumProperty(name='Navigation',update=update_navigation,
		default='Blender',
		description='select overide navigation mode',
		items=[('3DsMax','3DsMax',''),
			('Maya','Maya',''),
			# ('Softimage','Softimage',''),
			# ('Modo','Modo',''),
			# ('Cinema4D','Cinema4D',''),
			('Blender','Blender',''),
			('None','None','')])

	apppack = [('3DsMax','3DsMax',''),
			('Maya','Maya',''),
			# ('Softimage','Softimage',''),
			# ('Modo','Modo',''),
			# ('Cinema4D','Cinema4D',''),
			('Blender','Blender',''),
			('None','None','')]

	toolpack: EnumProperty(name='Tools Pack',
		default='Blender',
		description='Extera Overide Tools',
		update=update_toolpack,items=apppack)

	floatmenus: EnumProperty(name='Float Menu',update=update_floatmenu,
		default='Blender',
		description='Float menus type',
		items=[('QuadMenu_st_andkey','QuadMenu Standard (with Keymap)',''),
			('QuadMenu_st_nokey','QuadMenu Standard (without Keymap)',''),
			('Blender','Blender',''),
			('None','None','')])

	keymaps: EnumProperty(name='Keymap',
		default='Blender',
		description='Overide Full Keymap',
		update=update_keymaps,items=apppack)
	
	def arreng(self):
		if self.keymaps != "Blender":
			if self.toolpack != self.keymaps:
				self.toolpack = self.keymaps
		if self.floatmenus == 'QuadMenu_st_andkey' or self.floatmenus == 'QuadMenu_st_nokey':
			if self.toolpack != '3DsMax':
				self.toolpack = '3DsMax'

	def draw(self, ctx):
		self.arreng()
		layout = self.layout
		row = layout.row()
		col = row.column()
		col.prop(self, "navigation")
		col.prop(self, "keymaps")
		col.prop(self, "floatmenus")
		col.prop(self, "toolpack")

def register_keymaps_delay(preferences):
	sleep(0.1)
	""" Wait For Load Blender Defualt Keymaps First """
	register_keymaps(preferences)

def register():
	bpy.utils.register_class(BsMax_AddonPreferences)
	preferences = bpy.context.preferences.addons[__name__].preferences
	register_primitives()
	register_tools(preferences)
	register_startup(preferences)
	register_menu(preferences)
	register_navigation(preferences)
	templates.register()
	start_new_thread(register_keymaps_delay,tuple([preferences]))
	
def unregister():
	unregister_keymaps()
	unregister_navigation()
	unregister_menu()
	unregister_tools()
	unregister_primitives()
	unregister_startup()
	bpy.utils.unregister_class(BsMax_AddonPreferences)
	templates.unregister()
	if path not in sys.path:
		sys.path.remove(path)