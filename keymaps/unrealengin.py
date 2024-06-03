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

def view2d_navigation(km, preferences):
	pass

def view3d(km):
	pass

def view3d_navigation(km,preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.view_undo:
		km.new(space, 'view3d.movecover', 'MIDDLEMOUSE', 'PRESS', [], alt=True)
		km.new(space, 'view3d.rotatecover', 'LEFTMOUSE', 'PRESS', [], alt=True)
		km.new(space, 'view3d.zoomcover', 'RIGHTMOUSE', 'PRESS', [], alt=True)
	else:
		km.new(space, 'view3d.move', 'MIDDLEMOUSE', 'PRESS', [], alt=True)
		km.new(space, 'view3d.rotate', 'LEFTMOUSE', 'PRESS', [], alt=True)
		km.new(space, 'view3d.zoom', 'RIGHTMOUSE', 'PRESS', [], alt=True)

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


def register_unreal(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.navigation_3d == 'UNREAL':
			view3d_navigation(km_navigation_3d,preferences)
			km_navigation_3d.register()
		else:
			km_navigation_3d.unregister()

		if preferences.navigation_2d == 'UNREAL':
			view2d_navigation(km_navigation_2d,preferences)
			km_navigation_2d.register()
		else:
			km_navigation_2d.unregister()

		if preferences.viowport == 'UNREAL':
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

		if preferences.sculpt == 'UNREAL':
			vertex_paint(km_sculpt)
			weight_paint(km_sculpt)
			image_paint(km_sculpt)
			sculpt(km_sculpt)
			km_sculpt.register()
		else:
			km_sculpt.unregister()

		if preferences.uv_editor == 'UNREAL':
			uv_editor(km_uv_editor)
			km_uv_editor.register()
		else:
			km_uv_editor.unregister()

		if preferences.node_editor == 'UNREAL':
			node_editor(km_node_editor)
			km_node_editor.register()
		else:
			km_node_editor.unregister()

		if preferences.graph_editor == 'UNREAL':
			graph_editor(km_graph_editor)
			dopesheet_editor(km_graph_editor)
			nla_editor(km_graph_editor)
			km_uv_editor.register()
		else:
			km_graph_editor.unregister()
			
		if preferences.clip_editor == 'UNREAL':
			km_clip_editor.register()
		else:
			km_clip_editor.unregister()

		if preferences.video_sequencer == 'UNREAL':
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

		if preferences.text_editor == 'UNREAL':
			# console(km_text_editor)
			text(km_text_editor)
			km_text_editor.register()
		else:
			km_text_editor.unregister()
		
		if preferences.file_browser == 'UNREAL':
			file_browser(km_file_browser)
			km_file_browser.register()
		else:
			km_file_browser.unregister()

def unregister_unreal():
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
