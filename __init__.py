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
	"version": (0, 1, 0, 20200421),
	"blender": (2, 80, 0),# 2.80~2.90
	"location": "Almost Everywhere in Blender",
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	"category": "Interface"
}

import bpy, sys, os
from bpy.props import EnumProperty
from bpy.types import Operator, AddonPreferences

# Add public classes, variables and functions path.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

import templates

from .keymaps import keymaps_keys,navigation_keys,public_keys
from .menu import menu_cls
from .primitive import primitive_cls
from .startup import startup_cls
from .tools import tools_cls,special_cls

# Addon preferences
def fix_option(self):
	if self.keymaps != "Blender":
		if self.toolpack != self.keymaps:
			self.toolpack = self.keymaps

def update_navigation(self, ctx):
	navigation_keys(True, get_pref())

def update_toolpack(self, ctx):
	special_cls(True, get_pref())

def update_floatmenu(self, ctx):
	menu_cls(True, get_pref())

def update_keymaps(self, ctx):
	fix_option(self)
	keymaps_keys(True, get_pref())

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

	def draw(self, ctx):
		layout = self.layout
		fix_option(self)
		row = layout.row()
		col = row.column()
		col.prop(self, "navigation")
		col.prop(self, "keymaps")
		col.prop(self, "floatmenus")
		col.prop(self, "toolpack")

def get_pref():
	return bpy.context.preferences.addons[__name__].preferences

def register():
	bpy.utils.register_class(BsMax_AddonPreferences)
	pref = get_pref()
	primitive_cls(True, pref)
	tools_cls(True,pref)
	startup_cls(True, pref)
	menu_cls(True, pref)
	navigation_keys(True, pref)
	keymaps_keys(True, pref)
	public_keys(True, pref)
	templates.register()
	
def unregister():
	pref = get_pref()
	navigation_keys(False, pref)
	keymaps_keys(False, pref)
	public_keys(False, pref)
	menu_cls(False, pref)
	primitive_cls(False, pref)
	tools_cls(False,pref)
	startup_cls(False, pref)
	bpy.utils.unregister_class(BsMax_AddonPreferences)
	templates.unregister()
	if path not in sys.path:
		sys.path.remove(path)