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
from bsmax.keymaps import KeyMaps

def collect_mute_keymaps(km):
	pass

# public Keymaps added anyway
def public_keymaps(km,preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.zoomincover","WHEELINMOUSE","PRESS",[])
		km.new(space,"view3d.zoomoutcover","WHEELOUTMOUSE","PRESS",[])
	else:
		km.new(space,"view3d.zoom","WHEELINMOUSE","PRESS",[('delta',1)])
		km.new(space,"view3d.zoom","WHEELOUTMOUSE","PRESS",[('delta',-1)])

# Create Keymaps
def navigation_Blender(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],shift=True)
		km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True)
		km.new(space,"view3d.dollycover","MIDDLEMOUSE","PRESS",[],ctrl=True,shift=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],shift=True)
		km.new(space,"view3d.rotate","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.zoom","MIDDLEMOUSE","PRESS",[],ctrl=True)
		km.new(space,"view3d.dolly","MIDDLEMOUSE","PRESS",[],ctrl=True,shift=True)

def navigation_3dsmax(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotate","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)

def navigation_maya(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","RIGHTMOUSE","PRESS",[],alt=True)

def navigation_modo(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.movecover","LEFTMOUSE","PRESS",[],shift=True)
		km.new(space,"view3d.zoomcover","LEFTMOUSE","PRESS",[],ctrl=True)
	else:
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.move","LEFTMOUSE","PRESS",[],shift=True)
		km.new(space,"view3d.zoom","LEFTMOUSE","PRESS",[],ctrl=True)

	#km.new(space,"view3d.rotate","MIDDLEMOUSE","PRESS",[],alt=True) #roll
	# Orbit mode
	#km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True) #rotate camera
	
	#https://www.youtube.com/watch?v=SDvv34owpV0
	#x.view.use_mouse_depth_navigate=True # enable: Auto Depth
	#x.view.use_zoom_to_mouse=True # enable: Zoom To Mouse Position
	#x.inputs.use_mouse_emulate_3_button=True # enable: Emulate 3 Button Mouse
	#x.inputs.view_rotate_method=‘TRACKBALL’ # Orbit Style: Trackball
	#x.inputs.view_zoom_axis=‘HORIZONTAL’ # Zoom Style: Horizontal
	#x.view.use_auto_perspective=True # enable: Auto Perspective (auto orthographic views)
	#x.system.use_region_overlap=True # enable: Region Overlap (makes Tool Shelf transparent)
	#bpy.ops.wm.save_userpref()

def navigation_softimage(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","RIGHTMOUSE","PRESS",[],alt=True)

def navigation_cinema4d(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","RIGHTMOUSE","PRESS",[],alt=True)


def navigation_unrealengin(km,preferences):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.viewundo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","RIGHTMOUSE","PRESS",[],alt=True)

		# because of some API limitation not possble for now but planed 
		# lmb + twaak up move forward
		# lmb + tweak down move backward
		# lmb + tweak left turn left
		# lmb + tweak right turn right

		# rmb + tweak up look up
		# rmb + twead down look down
		# rmb + twead left look left
		# rmb + twead right look right

		# mmb + tweak up move up (pan)
		# mmb + tweak left and right look left and right
	
		# w move forward
		# s move backward
		# a move left
		# d move rigth

		# e move up (z up)
		# q move down (z down)
		# c fov to zoom in (release mouse back to origen)
		# z fov zoom back (release mouse back to origen)

		# mwb changes movment speed

		# f zoom extended

def create_keymaps(km,preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		app = preferences.navigation
		if app == 'Blender':
			navigation_Blender(km,preferences)
		elif app == '3DsMax':
			navigation_3dsmax(km,preferences)
		elif app == 'Maya':
			navigation_maya(km,preferences)
		elif app == 'Modo':
			navigation_modo(km,preferences)
		elif app == 'Softimage':
			navigation_softimage(km,preferences)
		elif app == 'Cinema4D':
			navigation_cinema4d(km,preferences)
		elif app == 'UnrealEngin':
			navigation_unrealengin(km,preferences)
		public_keymaps(km,preferences)

keymaps = KeyMaps()

def register_navigation(preferences):
	keymaps.unregister()
	create_keymaps(keymaps,preferences)
	collect_mute_keymaps(keymaps)
	keymaps.register()

def unregister_navigation():
	keymaps.unregister()