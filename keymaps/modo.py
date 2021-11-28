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

def window(km):
	pass

def screen(km):
	pass

def view2d(km):
	pass

def view2d_navigation(km,preferences):
	pass

def view3d(km):
	pass

def view3d_navigation(km,preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.view_undo:
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

def view3d_generic(km):
	pass

def view3d_select(km):
	pass

def view3d_transform(km):
	pass

def view3d_move(km):
	pass

def view3d_rotate(km):
	pass

def view3d_scale(km):
	pass

def view3d_select_box(km):
	pass

def view3d_select_circle(km):
	pass

def view3d_select_lasso(km):
	pass

def transform(km):
	pass

def object_mode(km):
	pass

def mesh(km):
	pass

def curve(km):
	pass

def armature(km):
	pass

def metaball(km):
	pass

def lattice(km):
	pass

def grease_pencil(km):
	pass

def pos(km):
	pass

def vertex_paint(km):
	pass

def weight_paint(km):
	pass

def image_paint(km):
	pass

def sculpt(km):
	pass

def node_editor(km):
	pass

def graph_editor(km):
	pass

def dopesheet_editor(km):
	pass

def nla_editor(km):
	pass

def uv_editor(km):
	pass
			
def sequence_editor(km):
	pass

def text(km):
	pass

def file_browser(km):
	pass
		
km_navigation_3d = KeyMaps()
km_navigation_2d = KeyMaps()
km_viowport = KeyMaps()
km_sculpt = KeyMaps()
km_uv_editor = KeyMaps()
km_node_editor = KeyMaps()
km_text_editor = KeyMaps()
km_graph_editor = KeyMaps()
km_clip_editor = KeyMaps()
km_video_sequencer = KeyMaps()
km_file_browser = KeyMaps()


def register_modo(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.navigation_3d == "Modo":
			view3d_navigation(km_navigation_3d,preferences)
			km_navigation_3d.register()
		else:
			km_navigation_3d.unregister()

		if preferences.navigation_2d == "Modo":
			view2d_navigation(km_navigation_2d,preferences)
			km_navigation_2d.register()
		else:
			km_navigation_2d.unregister()

		if preferences.viowport == "Modo":
			window(km_viowport)
			screen(km_viowport)
			view3d(km_viowport)
			view2d(km_viowport)
			view3d_generic(km_viowport)
			view3d_select(km_viowport)
			view3d_transform(km_viowport)
			view3d_move(km_viowport)
			view3d_rotate(km_viowport)
			view3d_scale(km_viowport)
			view3d_select_box(km_viowport)
			view3d_select_circle(km_viowport)
			view3d_select_lasso(km_viowport)
			transform(km_viowport)
			object_mode(km_viowport)
			mesh(km_viowport)
			curve(km_viowport)
			armature(km_viowport)
			metaball(km_viowport)
			lattice(km_viowport)
			grease_pencil(km_viowport)
			pos(km_viowport)
			km_viowport.register()
		else:
			km_viowport.unregister()

		if preferences.sculpt == "Modo":
			vertex_paint(km_sculpt)
			weight_paint(km_sculpt)
			image_paint(km_sculpt)
			sculpt(km_sculpt)
			km_sculpt.register()
		else:
			km_sculpt.unregister()

		if preferences.uv_editor == "Modo":
			uv_editor(km_uv_editor)
			km_uv_editor.register()
		else:
			km_uv_editor.unregister()

		if preferences.node_editor == "Modo":
			node_editor(km_node_editor)
			km_node_editor.register()
		else:
			km_node_editor.unregister()

		if preferences.graph_editor == "Modo":
			graph_editor(km_graph_editor)
			dopesheet_editor(km_graph_editor)
			nla_editor(km_graph_editor)
			km_uv_editor.register()
		else:
			km_graph_editor.unregister()
			
		if preferences.clip_editor == "Modo":
			km_clip_editor.register()
		else:
			km_clip_editor.unregister()

		if preferences.video_sequencer == "Modo":
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

		if preferences.text_editor == "Modo":
			# console(km_text_editor)
			text(km_text_editor)
			km_text_editor.register()
		else:
			km_text_editor.unregister()
		
		if preferences.file_browser == "Modo":
			file_browser(km_file_browser)
			km_file_browser.register()
		else:
			km_file_browser.unregister()

def unregister_modo():
	km_navigation_3d.unregister()
	km_navigation_2d.unregister()
	km_viowport.unregister()
	km_sculpt.unregister()
	km_uv_editor.unregister()
	km_node_editor.unregister()
	km_text_editor.unregister()
	km_graph_editor.unregister()
	km_clip_editor.unregister()
	km_video_sequencer.unregister()
	km_file_browser.unregister()
