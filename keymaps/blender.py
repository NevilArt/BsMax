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

def window(km):
	pass

def screen(km):
	pass

def view2d(km):
	pass

def view2d_navigation(km,preferences):
	pass

def view3d(km):
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"wm.multi_item_rename","F2","PRESS",[])
	km.new(space,"wm.call_menu","A","PRESS",[('name',"BsMax_MT_Create")],ctrl=True,shift=True)

def view3d_navigation(km,preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	if preferences.view_undo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],shift=True)
		km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True)
		km.new(space,"view3d.dollycover","MIDDLEMOUSE","PRESS",[],ctrl=True,shift=True)
		km.new(space,"view3d.zoomincover","WHEELINMOUSE","PRESS",[])
		km.new(space,"view3d.zoomoutcover","WHEELOUTMOUSE","PRESS",[])

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
	space = km.space('Object Non-modal','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,"bsmax.mode_set",'F9',"PRESS",[])

def mesh(km):
	space = km.space('Mesh','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])

def curve(km):
	space = km.space('Curve','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])

def armature(km):
	space = km.space('Armature','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,"wm.multi_item_rename","F2","PRESS",[])

def metaball(km):
	space = km.space('Metaball','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])

def lattice(km):
	space = km.space('Lattice','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])

def grease_pencil(km):
	pass

def pos(km):
	space = km.space('Pose','EMPTY','WINDOW')
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])

def vertex_paint(km):
	pass

def weight_paint(km):
	pass

def image_paint(km):
	pass

def sculpt(km):
	pass

def node_editor(km):
	space = km.space("Node Editor","NODE_EDITOR",'WINDOW')
	km.new(space,"wm.multi_item_rename","F2","PRESS",[])

def graph_editor(km):
	pass

def dopesheet_editor(km):
	pass

def nla_editor(km):
	pass

def uv_editor(km):
	pass
			
def sequence_editor(km):
	space = km.space('Sequencer','SEQUENCE_EDITOR','WINDOW')
	km.new(space,"wm.multi_item_rename","F2","PRESS",[])

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
km_float_menu = KeyMaps()

def register_blender(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.navigation_3d == "Blender":
			view3d_navigation(km_navigation_3d,preferences)
			km_navigation_3d.register()
		else:
			km_navigation_3d.unregister()

		if preferences.navigation_2d == "Blender":
			view2d_navigation(km_navigation_2d,preferences)
			km_navigation_2d.register()
		else:
			km_navigation_2d.unregister()

		if preferences.viowport == "Blender":
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

		if preferences.sculpt == "Blender":
			vertex_paint(km_sculpt)
			weight_paint(km_sculpt)
			image_paint(km_sculpt)
			sculpt(km_sculpt)
			km_sculpt.register()
		else:
			km_sculpt.unregister()

		if preferences.uv_editor == "Blender":
			uv_editor(km_uv_editor)
			km_uv_editor.register()
		else:
			km_uv_editor.unregister()

		if preferences.node_editor == "Blender":
			node_editor(km_node_editor)
			km_node_editor.register()
		else:
			km_node_editor.unregister()

		if preferences.graph_editor == "Blender":
			graph_editor(km_graph_editor)
			dopesheet_editor(km_graph_editor)
			nla_editor(km_graph_editor)
			km_uv_editor.register()
		else:
			km_graph_editor.unregister()
			
		if preferences.clip_editor == "Blender":
			km_clip_editor.register()
		else:
			km_clip_editor.unregister()

		if preferences.video_sequencer == "Blender":
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

		if preferences.text_editor == "Blender":
			text(km_text_editor)
			km_text_editor.register()
		else:
			km_text_editor.unregister()
		
		if preferences.file_browser == "Blender":
			file_browser(km_file_browser)
			km_file_browser.register()
		else:
			km_file_browser.unregister()

def unregister_blender():
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
	km_float_menu.unregister()