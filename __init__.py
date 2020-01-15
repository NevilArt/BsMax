############################################################################
#    BsMax, 3D apps inteface simulator and tools pack for Blender
#    Copyright (C) 2020  Naser Merati (Nevil)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

bl_info = {
	"name": "BsMax",
	"description": "BsMax Updated on 15.january.2020",
	"author": "Naser Merati (Nevil)",
	"version": (0, 1, 0, 20200115),
	"blender": (2, 80, 0),# 2.80~2.83
	#"location": "Every where",
	#"warning": "", # used for warning icon and text in addons panel
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	#"support": "COMMUNITY",
	"category": "User Interface"
}

import bpy, sys, os
from bpy.props import EnumProperty
from bpy.types import Operator, AddonPreferences

# Add public classes, variables and functions path.
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

from .keymaps.init import keymaps_keys,navigation_keys,public_keys
from .menu.init import menu_cls
from .primitive.init import primitive_cls
from .startup.init import startup_cls
from .tools.init import public_cls,assistant_cls,special_cls

# Addon preferences
def fix_option(self):
	if self.keymaps != "Blender":
		if self.toolpack != self.keymaps:
			self.toolpack = self.keymaps

def update_navigation(self, ctx):
	navigation_keys(True, get_pret())

def update_toolpack(self, ctx):
	special_cls(True, get_pret())

def update_floatmenu(self, ctx):
	menu_cls(True, get_pret())

def update_keymaps(self, ctx):
	fix_option(self)
	keymaps_keys(True, get_pret())

def update_assistpack(self, ctx):
	assistant_cls(True, get_pret())

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
			('Blender','Blender','')])

	apppack = [('3DsMax','3DsMax',''),
			('Maya','Maya',''),
			# ('Softimage','Softimage',''),
			# ('Modo','Modo',''),
			# ('Cinema4D','Cinema4D',''),
			('Blender','Blender','')]

	toolpack: EnumProperty(name='Tools Pack',
		default='Blender',
		description='Extera Overide Tools',
		update=update_toolpack,items=apppack)

	floatmenus: EnumProperty(name='Float Menu',update=update_floatmenu,
		default='Blender',
		description='Float menus type',
		items=[('QuadMenu_st_andkey','QuadMenu Standard (with Keymap)',''),
			('QuadMenu_st_nokey','QuadMenu Standard (without Keymap)',''),
			('Blender','Blender','')])

	keymaps: EnumProperty(name='Keymap',
		default='Blender',
		description='Overide Full Keymap',
		update=update_keymaps,items=apppack)

	assistpack: EnumProperty(name='Assistance Pack',update=update_assistpack,
		default='None',
		description='More Tools',
		items=[('Rigg','Rigg',''),
			#('Animate','Animate',''),
			#('Model','Model',''),
			('None','None','')])

	def draw(self, ctx):
		layout = self.layout
		fix_option(self)
		row = layout.row()
		col = row.column()
		col.prop(self, "navigation")
		col.prop(self, "keymaps")
		col.prop(self, "floatmenus")
		col.prop(self, "toolpack")
		col.prop(self, "assistpack")

def get_pret():
	return bpy.context.preferences.addons[__name__].preferences

def bsmax_cls(register, pref):
	navigation_keys(register, pref)
	menu_cls(register, pref)
	primitive_cls(register, pref)
	special_cls(register, pref)
	assistant_cls(register, pref)
	public_cls(register, pref)
	keymaps_keys(register, pref)
	public_keys(register, pref)
	startup_cls(register, pref)

def register():
	bpy.utils.register_class(BsMax_AddonPreferences)
	bsmax_cls(True, get_pret())
	
def unregister():
	bsmax_cls(False, get_pret())
	bpy.utils.unregister_class(BsMax_AddonPreferences)

if __name__ == "__main__":
	register()