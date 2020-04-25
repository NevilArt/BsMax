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

def create_keymaps(km):
	kc = bpy.context.window_manager.keyconfigs

	""" ignore this if right click select mode active """
	try:
		rcsm = kc['blender'].preferences['select_mouse'] == 0
	except:
		rcsm = kc['blender'].preferences.select_mouse != 'RIGHT'

	if kc.addon and rcsm:
		# 3D View --------------------------------------------------------------
		space = km.space('3D View','VIEW_3D','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Object Mode -------------------------------------------------------------------------
		space = km.space('Object Mode','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Mesh -----------------------------------------------------------------
		space = km.space('Mesh','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Curve ----------------------------------------------------------------
		space = km.space('Curve','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Armature -------------------------------------------------------------
		space = km.space('Armature','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Metaball -------------------------------------------------------------
		space = km.space('Metaball','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Lattice --------------------------------------------------------------
		space = km.space('Lattice','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])
		# Pose -----------------------------------------------------------------
		space = km.space('Pose','EMPTY','WINDOW')
		km.new(space,"bsmax.droptool","RIGHTMOUSE","PRESS",[])

keymaps = KeyMaps()

def register_public():
	create_keymaps(keymaps)
	collect_mute_keymaps(keymaps)
	keymaps.register()

def unregister_public():
	keymaps.unregister()