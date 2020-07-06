############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from bsmax.keymaps import KeyMaps

def collect_mute_keymaps(km):
	pass

def create_quads(km,space,navigation):
	km.new(space,"bsmax.view3dquadmenue","V","PRESS",[('menu','viewport'),('space','View3D')])
	# This not needed drop tool can call this
	# km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','default'),('space','View3D')])
	# ignore alt + RMB if maya navigation was selected
	if navigation != 'Maya':
		km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','coordinate'),('space','View3D')],alt=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','create'),('space','View3D')],ctrl=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','snap'),('space','View3D')],shift=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','render'),('space','View3D')],alt=True,ctrl=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','fx'),('space','View3D')],alt=True,shift=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','Selection'),('space','View3D')],ctrl=True,shift=True)
	km.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','custom'),('space','View3D')],alt=True,ctrl=True,shift=True)

# Create Keymaps
def create_keymaps(km,navigation):
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# space = km.space('3D View','VIEW_3D','WINDOW')
		# km.new(space,"wm.search_menu","X","PRESS",[])
		
		""" Window """
		# space = km.space('Window','EMPTY','WINDOW')
		
		""" 2D View """
		# space = km.space('View2D','EMPTY','WINDOW')
		
		""" 3D View """
		space = km.space('3D View','VIEW_3D','WINDOW')
		create_quads(km,space,navigation)
		
		""" Object Mode """
		space = km.space('Object Mode','EMPTY','WINDOW')
		create_quads(km,space,navigation)
		
		""" Mesh """
		space = km.space('Mesh','EMPTY','WINDOW')
		create_quads(km,space,navigation)
		
		""" Curve """
		space = km.space('Curve','EMPTY','WINDOW')
		create_quads(km,space,navigation)
		
		""" Armature """
		space = km.space('Armature','EMPTY','WINDOW')
		create_quads(km,space,navigation)
		
		""" Pose """
		space = km.space('Pose','EMPTY','WINDOW')
		create_quads(km,space,navigation)
		
		""" Grease Pencil """
		space = km.space('Grease Pencil','EMPTY','WINDOW')
		create_quads(km,space,navigation)

keymaps = KeyMaps()

def register_keymap(preferences):
	create_keymaps(keymaps,preferences.navigation)
	collect_mute_keymaps(keymaps)
	keymaps.register()

def unregister_keypam():
	keymaps.unregister()