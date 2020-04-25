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
def public_keymaps(km):
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.zoomincover","WHEELINMOUSE","PRESS",[])
	km.new(space,"view3d.zoomoutcover","WHEELOUTMOUSE","PRESS",[])

# Create Keymaps
def navigation_Blender(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],shift=True)
	km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[])
	km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True)
	km.new(space,"view3d.dollycover","MIDDLEMOUSE","PRESS",[],ctrl=True,shift=True)

def navigation_3dsmax(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[])
	km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)

def navigation_maya(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)

def navigation_modo(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.movecover","LEFTMOUSE","PRESS",[],shift=True)
	km.new(space,"view3d.zoomcover","LEFTMOUSE","PRESS",[],ctrl=True)
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

def navigation_softimage(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)

def navigation_cinema4d(km):
	# 3D View --------------------------------------------------------------
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
	km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)

def create_keymaps(km,app):
	if bpy.context.window_manager.keyconfigs.addon:
		if app == 'Blender':
			navigation_Blender(km)
		elif app == '3DsMax':
			navigation_3dsmax(km)
		elif app == 'Maya':
			navigation_maya(km)
		elif app == 'Modo':
			navigation_modo(km)
		elif app == 'Softimage':
			navigation_softimage(km)
		elif app == 'Cinema4D':
			navigation_cinema4d(km)
		public_keymaps(km)

keymaps = KeyMaps()

def register_navigation(preferences):
	create_keymaps(keymaps,preferences.navigation)
	collect_mute_keymaps(keymaps)
	keymaps.register()

def unregister_navigation():
	keymaps.unregister()