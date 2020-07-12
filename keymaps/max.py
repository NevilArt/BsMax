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

def create_subobject_mode_keymap(km,space):
	km.new(space,'object.subobject_level','ONE','PRESS',[('level',1)])
	km.new(space,'object.subobject_level','TWO','PRESS',[('level',2)])
	km.new(space,'object.subobject_level','THREE','PRESS',[('level',3)])
	km.new(space,'object.subobject_level','FOUR','PRESS',[('level',4)])
	km.new(space,'object.subobject_level','FIVE','PRESS',[('level',5)])
	km.new(space,'object.subobject_level','SIX','PRESS',[('level',6)])
	# km.new(space,'object.subobject_level','SEVEN','PRESS',[('level',7)])
	# km.new(space,'object.subobject_level','EIGHT','PRESS',[('level',8)])
	# km.new(space,'object.subobject_level','NINE','PRESS',[('level',9)])
	# km.new(space,'object.subobject_level','ZERO','PRESS',[('level',0)])

def create_switch_view_keymap(km,space):
	km.new(space,'view3d.perespective','P','PRESS',[('mode','Perspective')])
	km.new(space,'view3d.perespective','U','PRESS',[('mode','Orthographic')])
	km.new(space,'view3d.view_axis','F','PRESS',[('type','FRONT')])
	km.new(space,'view3d.view_axis','L','PRESS',[('type','LEFT')])
	km.new(space,'view3d.view_axis','T','PRESS',[('type','TOP')])
	km.new(space,'view3d.view_axis','B','PRESS',[('type','BOTTOM')])

def create_view3d_click_celection_keymap(km,space):
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect_all',True)])
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('toggle',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect',True)],alt=True)

def create_view3d_tweak_selection_keymap(km,space):
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )

def create_snap_keymaps(km,space):
	km.new(space,'object.snap_toggle','S','PRESS',[])
	km.new(space,'object.angel_snap','A','PRESS',[])

def create_time_keymaps(km,space):
	km.new(space,'anim.frame_set','HOME','PRESS',[('frame','First')])
	km.new(space,'anim.frame_set','END','PRESS',[('frame','Last')])
	km.new(space,'anim.frame_set','PERIOD','PRESS',[('frame','Next')])
	km.new(space,'anim.frame_set','COMMA','PRESS',[('frame','Previous')])
	km.new(space,'anim.set_key','K','PRESS',[])
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])

def create_side_panel_keymaps(km,space):
	km.new(space,'wm.context_toggle','LEFT_BRACKET','PRESS',[('data_path','space_data.show_region_toolbar')])
	km.new(space,'wm.context_toggle','RIGHT_BRACKET','PRESS',[('data_path','space_data.show_region_ui')])

def create_search_shortkey(km,space):
	if bpy.app.version[1] < 90:
		km.new(space,'wm.search_menu','X','PRESS',[])
	else:
		km.new(space,'wm.search_menu','X','PRESS',[],ctrl=True,shift=True,alt=True)
		km.new(space,'wm.search_operator','X','PRESS',[])

def window(km):
	km.mute('Window','wm.quit_blender','Q','PRESS',ctrl=True)
	space = km.space('Window','EMPTY','WINDOW')
	create_search_shortkey(km,space)

def screen(km):
	space = km.space('Screen','EMPTY','WINDOW')
	km.new(space,'render.render','F9','PRESS',[('use_viewport',True)])
	km.new(space,'render.render','Q','PRESS',[('use_viewport',True),('animation',True)],shift=True)
	km.new(space,'screen.repeat_last','SEMI_COLON','PRESS',[])
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'screen.screen_full_area','X','PRESS',[('use_hide_panels',True)],alt=True,ctrl=True)
	km.new(space,'editor.script_listener','F11','PRESS',[])
	km.new(space,'ed.redo','Y','PRESS',[],ctrl=True)
	km.new(space,'screen.animation_play','SLASH','PRESS',[])

def view2d(km):
	# space = km.space('View2D','EMPTY','WINDOW')
	# km.new(space,'view2d.zoom','MIDDLEMOUSE','PRESS',[],ctrl=True,alt=True)
	pass

def view3d(km):
	km.mute('3D View','view3d.view_center_pick','MIDDLEMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','NORTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','SOUTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','EAST',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','WEST',alt=True)
	km.mute('3D View','view3d.localview_remove_from','M','PRESS',ctrl=True)
	km.mute('3D View','wm.call_menu_pie','Z','PRESS')

	space = km.space('3D View','VIEW_3D','WINDOW')
	create_search_shortkey(km,space)
	create_snap_keymaps(km,space)
	create_time_keymaps(km,space)
	create_switch_view_keymap(km,space)
	create_view3d_tweak_selection_keymap(km,space)

	km.new(space,'screen.header','SIX','PRESS',[],alt=True)
	km.new(space,'screen.region_quadview','W','PRESS',[],alt=True)
	km.new(space,'view3d.transform_gizmosize','EQUAL','PRESS',[('step',10)])
	km.new(space,'view3d.transform_gizmosize','MINUS','PRESS',[('step',-10)])
	km.new(space,'view3d.localview','Q','PRESS',[],alt=True)
	km.new(space,'wm.tool_set_by_id','Q','PRESS',[('name','builtin.select_box'),('cycle',True)])
	km.new(space,'object.move','W','PRESS',[('smax',True)])
	km.new(space,'object.rotate','E','PRESS',[('smax',True)])
	km.new(space,'object.scale','R','PRESS',[('cage',False)])
	km.new(space,'object.scale','E','PRESS',[('cage',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('extend',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect',True)],alt=True)
	km.new(space,'view3d.zoom_extended','Z','PRESS',[])
	km.new(space,'camera.set_active','C','PRESS',[])
	km.new(space,'view3d.show_hide_gride','G','PRESS',[])
	km.new(space,'view3d.show_statistics','SEVEN','PRESS',[])
	km.new(space,'object.batch_rename','F2','PRESS',[])
	km.new(space,'view3d.wireframe_toggle','F3','PRESS',[])
	km.new(space,'view3d.edge_faces_toggle','F4','PRESS',[])
	km.new(space,'view3d.lighting_toggle','L','PRESS',[],ctrl=True)
	km.new(space,'view3d.background','B','PRESS',[],alt=True)
	km.new(space,'object.subobject_level','B','PRESS',[('level',6)],ctrl=True)
	km.new(space,'camera.show_safe_areas','F','PRESS',[],shift=True)
	km.new(space,'scene.hold','H','PRESS',[],ctrl=True,alt=True)
	km.new(space,'scene.fetch','F','PRESS',[],ctrl=True,alt=True)
	km.new(space,'wm.call_menu','A','PRESS',[('name','BSMAX_MT_createmenu')],ctrl=True,shift=True)
	km.new(space,'view3d.homeview','HOME','PRESS',[],alt=True)
	km.new(space,'screen.animation_play','SLASH','PRESS',[])
	km.new(space,'editor.open_node_ditor','M','PRESS',[('mode','Material')])
	km.new(space,'editor.open_node_ditor','EIGHT','PRESS',[('mode','Environment')])
	km.new(space,'view.undoredo','Z','PRESS',[('redo',False)],shift=True)
	km.new(space,'view.undoredo','Y','PRESS',[('redo',True)],shift=True)

def view3d_generic(km):
	km.mute('3D View Generic','wm.context_toggle','T','PRESS')
	km.mute('3D View Generic','wm.context_toggle','N','PRESS')

	space = km.space('3D View Generic','VIEW_3D','WINDOW')
	km.new(space,'view3d.properties','LEFT_BRACKET','PRESS',[])
	km.new(space,'view3d.toolshelf','RIGHT_BRACKET','PRESS',[])

def view3d_select(km):
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK')
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',shift=True)

	space = km.space('3D View Tool: Select','VIEW_3D','WINDOW')
	create_view3d_tweak_selection_keymap(km,space)
	km.new(space,'view3d.tweak_better','EVT_TWEAK_L','ANY',[])
	
def view3d_transform(km):
	space = km.space('3D View Tool: Transform','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])

def view3d_move(km):
	space = km.space('3D View Tool: Move','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])

def view3d_rotate(km):
	space = km.space('3D View Tool: Rotate','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])

def view3d_scale(km):
	space = km.space('3D View Tool: Scale','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])

def view3d_select_box(km):
	km.mute('3D View Tool: Select Box','view3d.select_box','EVT_TWEAK_L','ANY',ctrl=True)
	space = km.space('3D View Tool: Select Box','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)

def view3d_select_circle(km):
	km.mute('3D View Tool: Select Circle','view3d.select_circle','LEFTMOUSE','PRESS',ctrl=True)
	space = km.space('3D View Tool: Select Circle','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_circle','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	km.new(space,'view3d.select_circle','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)

def view3d_select_lasso(km):
	km.mute('3D View Tool: Select Lasso','view3d.select_lasso','EVT_TWEAK_L','ANY',ctrl=True)
	space = km.space('3D View Tool: Select Lasso','VIEW_3D','WINDOW')
	km.new(space,'view3d.select_lasso','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	km.new(space,'view3d.select_lasso','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)

def transform(km):
	pass
	# space = km.space('Transform Modal Map','EMPTY','WINDOW',modal=True)

def object_mode(km):
	space = km.space('Object Non-modal','EMPTY','WINDOW')
	km.new(space,'bsmax.mode_set','TAB','PRESS',[])

	space = km.space('Object Mode','EMPTY','WINDOW')
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	create_view3d_tweak_selection_keymap(km,space)
	create_view3d_click_celection_keymap(km,space)
	create_snap_keymaps(km,space)
	create_subobject_mode_keymap(km,space)
	
	km.new(space,'view3d.select','LEFTMOUSE','RELEASE',[('enumerate',True)],shift=True)
	km.new(space,'object.select_all','A','PRESS',[('action','SELECT')],ctrl=True )
	km.new(space,'object.select_all','D','PRESS',[('action','DESELECT')],ctrl=True )
	km.new(space,'object.select_all','I','PRESS',[('action','INVERT')],ctrl=True )
	km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
	km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
	km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',False)])
	km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',True)],ctrl=True)
	km.new(space,'object.select_similar','Q','PRESS',[],ctrl=True)
	# Hide/Unhide #
	km.new(space,'object.hide','H','PRESS',[('mode','selection')],alt=True)
	km.new(space,'object.hide','I','PRESS',[('mode','unselected')],alt=True)
	km.new(space,'object.hide','U','PRESS',[('mode','clear')],alt=True)
	km.new(space,'view3d.show_geometry_toggle','G','PRESS',[],shift=True)
	km.new(space,'view3d.show_helper_toggle','H','PRESS',[],shift=True)
	km.new(space,'view3d.show_shape_toggle','S','PRESS',[],shift=True)
	km.new(space,'view3d.show_light_toggle','L','PRESS',[],shift=True)
	km.new(space,'view3d.show_bone_toggle','B','PRESS',[],shift=True)
	km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)

	km.new(space,'object.modify_pivotpoint','INSERT','PRESS',[])
	km.new(space,'wm.call_menu','INSERT','PRESS',[('name','BSMAX_MT_SetPivotPoint')],ctrl=True)
	# Float Editors #
	km.new(space,'editor.open_node_ditor','M','PRESS',[('mode','Material')])
	km.new(space,'editor.open_node_ditor','EIGHT','PRESS',[('mode','Environment')])
	# km.new(space,'editor.open_node_ditor','SIX','PRESS',[('mode','Environment')]) # function editor
	# Tools #
	km.new(space,'object.align_selected_to_target','A','PRESS',[],alt=True)
	km.new(space,'object.transform_type_in','F12','PRESS',[])
	km.new(space,'view3d.lighting_toggle','L','PRESS',[],ctrl=True)
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'modifier.edit_multi','TAB','PRESS',[],ctrl=True)

def mesh(km):
	km.mute('Mesh','mesh.shortest_path_pick','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('Mesh','mesh.loop_select','LEFTMOUSE','CLICK',alt=True)
	km.mute('Mesh','mesh.select_all','A','PRESS')

	space = km.space('Mesh','EMPTY','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	# Selection #
	km.new(space,'mesh.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'mesh.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'mesh.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	create_view3d_click_celection_keymap(km,space)
	create_view3d_tweak_selection_keymap(km,space)
	km.new(space,'mesh.shortest_path_pick','LEFTMOUSE','PRESS',[],shift=True)
	km.new(space,'mesh.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'mesh.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'mesh.select_element','LEFTMOUSE','DOUBLE_CLICK',[])
	km.new(space,'mesh.smart_select_loop','L','PRESS',[],alt=True)
	km.new(space,'mesh.smart_select_ring','R','PRESS',[],alt=True)
	km.new(space,'mesh.select_similar','Q','PRESS',[],ctrl=True)
	# View #
	create_switch_view_keymap(km,space)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	# Hide/Unhide #
	km.new(space,'mesh.hide','H','PRESS',[],alt=True)
	km.new(space,'mesh.hide','I','PRESS',[('unselected',True)],alt=True)
	km.new(space,'mesh.reveal','U','PRESS',[],alt=True)
	# Edit #
	km.new(space,'mesh.connect','E','PRESS',[],ctrl=True,shift=True)
	km.new(space,'view3d.edit_mesh_extrude_move_normal','E','PRESS',[],shift=True)
	km.new(space,'mesh.knife_tool','C','PRESS',[('use_occlude_geometry',True)],alt=True)
	km.new(space,'mesh.bevel','C','PRESS',[('vertex_only',False)],ctrl=True,shift=True)
	km.new(space,'transform.vert_slide','X','PRESS',[],shift=True)
	km.new(space,'mesh.merge','C','PRESS',[('type','CENTER')],alt=True,ctrl=True)
	#km.new(space,'mesh.edge_face_add','P','PRESS',[],alt=True)
	km.new(space,'mesh.smart_create','P','PRESS',[],alt=True)
	#km.new(space,'Bevel','B','PRESS',[],ctrl=True,shift=True)
	#km.new(space,'spline extrud ','E','PRESS',[],alt=True)
	km.new(space,'wm.context_toggle','I','PRESS',[('data_path','space_data.shading.show_xray')],shift=True,ctrl=True)
	#km.new(space,'smooth','M','PRESS',[],ctrl=True)
	#km.new(space,'wm.tool_set_by_name','Q','PRESS',[('name','Bisect')],shift=True,ctrl=True)
	#km.new(space,'mesh.remove_doubles','W','PRESS',[],shift=True,ctrl=True)
	km.new(space,'mesh.target_weld','W','PRESS',[],shift=True,ctrl=True)
	km.new(space,'mesh.remove','BACK_SPACE','PRESS',[('vert',False)])
	km.new(space,'mesh.remove','BACK_SPACE','PRESS',[('vert',True)],ctrl=True)
	km.new(space,'mesh.delete_auto','DEL','PRESS',[])
	km.new(space,'object.transform_type_in','F12','PRESS',[])
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# Tools #
	km.new(space,'view3d.shade_selected_faces','F2','PRESS',[])
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
	km.new(space,'wm.tool_set_by_id','R','PRESS',[('name','builtin.scale'),('cycle',True)])
	km.new(space,'anim.set_key','K','PRESS',[])

def curve(km):
	space = km.space('Curve','EMPTY','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	# Selection #
	km.new(space,'curve.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'curve.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'curve.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	create_view3d_click_celection_keymap(km,space)
	create_view3d_tweak_selection_keymap(km,space)
	km.new(space,'curve.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'curve.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'curve.select_similar','Q','PRESS',[],ctrl=True)
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# View #
	create_switch_view_keymap(km,space)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	# Tools #
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
	km.new(space,'curve.chamfer','C','PRESS',[('fillet',True),('typein',False)],ctrl=True,shift=True)
	# km.new(space,'curve.chamfer','C','DOUBLE_CLICK',[('fillet',True),('typein',True)],ctrl=True,shift=True)

def armature(km):
	space = km.space('Armature','EMPTY','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	# Selection #
	create_view3d_click_celection_keymap(km,space)
	km.new(space,'armature.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'armature.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'armature.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'armature.select_more','PAGE_UP','PRESS',[],ctrl=True,shift=True)
	km.new(space,'armature.select_less','PAGE_DOWN','PRESS',[],ctrl=True,shift=True)
	km.new(space,'armature.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
	km.new(space,'armature.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
	km.new(space,'armature.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',False)])
	km.new(space,'armature.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',True)],ctrl=True)
	km.new(space,'armature.select_similar','Q','PRESS',[],ctrl=True)
	# Hide/Unhide #
	km.new(space,'armature.hide','H','PRESS',[],alt=True)
	km.new(space,'armature.hide','I','PRESS',[('unselected',True)],alt=True)
	km.new(space,'armature.reveal','U','PRESS',[],alt=True)
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# View #
	create_switch_view_keymap(km,space)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'armature.batch_rename','F2','PRESS',[])
	# Tools #
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])

def metaball(km):
	space = km.space('Metaball','EMPTY','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	# Selection #
	km.new(space,'mball.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'mball.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'mball.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'mball.select_similar','Q','PRESS',[],ctrl=True)
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# View #
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	# Tools #
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])

def lattice(km):
	space = km.space('Lattice','EMPTY','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	# Selection #
	km.new(space,'lattice.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'lattice.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'lattice.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'lattice.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'lattice.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'lattice.select_similar','Q','PRESS',[],ctrl=True)
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# View #
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	# Tools #
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])

# def font(km):
# 	pass

def grease_pencil(km):
	space = km.space('Grease Pencil','EMPTY','WINDOW')
	# Global
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)

def pos(km):
	space = km.space('Pose','EMPTY','WINDOW')
	# Global #
	# create_side_panel_keymaps(km,space)
	# Selection #
	create_view3d_click_celection_keymap(km,space)
	km.new(space,'pose.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'pose.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'pose.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'pose.select_more','PAGE_UP','PRESS',[],ctrl=True,shift=True)
	km.new(space,'pose.select_less','PAGE_DOWN','PRESS',[],ctrl=True,shift=True)
	km.new(space,'pose.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
	km.new(space,'pose.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
	km.new(space,'pose.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',False)])
	km.new(space,'pose.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',True)],ctrl=True)
	km.new(space,'pose.select_similar','Q','PRESS',[],ctrl=True)
	# Set Subobject Mode #
	create_subobject_mode_keymap(km,space)
	# View #
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	# Tools #
	# km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	# km.new(space,'anim.set_key','K','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	create_time_keymaps(km,space)

def vertex_paint(km):
	space = km.space('Vertex Paint','EMPTY','WINDOW')
	create_switch_view_keymap(km,space)
	km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)

def weight_paint(km):
	space = km.space('Weight Paint','EMPTY','WINDOW')
	create_switch_view_keymap(km,space)
	km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)
	# Whight Paint Vertex Selection
	# Face Mask

def image_paint(km):
	space = km.space('Image Paint','EMPTY','WINDOW')
	create_side_panel_keymaps(km,space)

def sculpt(km):
	space = km.space('Sculpt','EMPTY','WINDOW')
	create_switch_view_keymap(km,space)
	km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)

def particle(km):
	pass
	# Particle

def outliner(km):
	space = km.space('Outliner','OUTLINER','WINDOW')
	create_search_shortkey(km,space)
	# upper than 2.80 do not need this part
	if bpy.app.version[1] < 81:
		# Selection #
		km.new(space,'outliner.item_activate','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
		km.new(space,'outliner.select_box','EVT_TWEAK_L','EAST',[('mode','SET')])
		km.new(space,'outliner.select_box','EVT_TWEAK_L','SOUTH_EAST',[('mode','SET')])
		km.new(space,'outliner.select_box','EVT_TWEAK_L','NORTH_EAST',[('mode','SET')])
		km.new(space,'outliner.select_box','EVT_TWEAK_L','EAST',[('mode','ADD')],ctrl=True )
		km.new(space,'outliner.select_box','EVT_TWEAK_L','SOUTH_EAST',[('mode','ADD')],ctrl=True )
		km.new(space,'outliner.select_box','EVT_TWEAK_L','NORTH_EAST',[('mode','ADD')],ctrl=True)
		km.new(space,'outliner.select_box','EVT_TWEAK_L','EAST',[('mode','SUB')],alt=True)
		km.new(space,'outliner.select_box','EVT_TWEAK_L','SOUTH_EAST',[('mode','SUB')],alt=True)
		km.new(space,'outliner.select_box','EVT_TWEAK_L','NORTH_EAST',[('mode','SUB')],alt=True)
		km.new(space,'outliner.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'outliner.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'outliner.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		km.new(space,'outliner.collection_objects_select','LEFTMOUSE','DOUBLE_CLICK',[])
		# Tools #
		km.new(space,'outliner.item_rename','F2','PRESS',[])
		km.new(space,'outliner.collection_new','N','PRESS',[],ctrl=True)
		km.new(space,'object.delete','DEL','PRESS',[('confirm',False)],ctrl=True)
		km.new(space,'outliner.hide','H','PRESS',[],alt=True)
		km.new(space,'outliner.unhide_all','U','PRESS',[],alt=True)
	else:
		km.new(space,'outliner.show_active','Z','PRESS',[])

def node_editor(km):
	space = km.space('Node Editor','NODE_EDITOR','WINDOW')
	# Global #
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	km.new(space,'node.batch_rename','F2','PRESS',[])
	# Selection #
	km.new(space,'node.select','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
	km.new(space,'node.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'node.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'node.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	# tools #
	km.new(space,'node.view_selected','Z','PRESS',[])
	km.new(space,'wm.call_menu','RIGHTMOUSE','PRESS',[('name','NODE_MT_add')])
	km.new(space,'node.duplicate_move','EVT_TWEAK_L','ANY',[],shift=True)
	# node.links_cut

def text(km):
	""" script editor """
	space = km.space('Text','TEXT_EDITOR','WINDOW')
	km.new(space,'text.run_script','E','PRESS',[],ctrl=True)
	km.new(space,'text.run_script','F5','PRESS',[]) # From MVS
	km.new(space,'text.autocomplete','RET','PRESS',[],ctrl=True)
	km.new(space,'text.new','N','PRESS',[],ctrl=True)
	km.new(space,'text.open','O','PRESS',[],ctrl=True)
	km.new(space,'text.save','S','PRESS',[],ctrl=True)
	km.new(space,'text.save_as','S','PRESS',[],ctrl=True,shift=True)
	km.new(space,'text.reload','R','PRESS',[],ctrl=True)
	km.new(space,'text.unlink','W','PRESS',[],ctrl=True)

def console(km):
	space = km.space('Console','CONSOLE','WINDOW')
	km.new(space,'text.new','N','PRESS',[],ctrl=True)
	km.new(space,'text.open','O','PRESS',[],ctrl=True)
	km.new(space,'text.save','S','PRESS',[],ctrl=True)
	km.new(space,'console.autocomplete','RET','PRESS',[],ctrl=True)
	km.new(space,'console.autocomplete','SPACE','PRESS',[],ctrl=True)
	km.new(space,'console.paste','INSERT','PRESS',[],shift=True)
	km.new(space,'console.copy','INSERT','PRESS',[],ctrl=True)
	km.new(space,'console.cut','DEL','PRESS',[],shift=True)
	km.new(space,'console.cut','X','PRESS',[],ctrl=True)
	km.new(space,'console.delete','DEL','PRESS',[])
	km.new(space,'console.clear','D','PRESS',[],shift=True)

""" Clip """

def info(km):
	space = km.space('Info','INFO','WINDOW')
	create_search_shortkey(km,space)
	km.new(space,'text.new','N','PRESS',[],ctrl=True)
	km.new(space,'text.open','O','PRESS',[],ctrl=True)
	km.new(space,'text.save','S','PRESS',[],ctrl=True)
	km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
	km.new(space,'info.select_all_toggle','A','PRESS',[],ctrl=True)
	km.new(space,'info.clear','D','PRESS',[('scrollback',True)],ctrl=True)

# def frames(km):
# 	space = km.space('Frames','EMPTY','WINDOW')

def graph_editor(km):
	space = km.space('Graph Editor','GRAPH_EDITOR','WINDOW')
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	create_time_keymaps(km,space)
	km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','ADD'),('tweak',True)],ctrl=True)
	km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','SUB'),('tweak',True)],alt=True)
	km.new(space,'graph.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'graph.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'graph.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'graph.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'graph.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'graph.view_selected','Z','PRESS',[])
	# km.new(space,'graph.view_all','??','PRESS',[])

def dopesheet_editor(km):
	""" (Timeline) """
	space = km.space('Dopesheet','DOPESHEET_EDITOR','WINDOW')
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	create_time_keymaps(km,space)

	km.new(space,'anim.set_timeline_range','LEFTMOUSE','PRESS',[('mode','First')],alt=True,ctrl=True)
	km.new(space,'anim.set_timeline_range','RIGHTMOUSE','PRESS',[('mode','End')],alt=True,ctrl=True)
	km.new(space,'anim.set_timeline_range','MIDDLEMOUSE','PRESS',[('mode','Shift')],alt=True,ctrl=True)

	km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
	km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )
	km.new(space,'action.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'action.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'action.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'action.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'action.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'action.zoom_extended','Z','PRESS',[])

def nla_editor(km):
	space = km.space('NLA Editor','NLA_EDITOR','WINDOW')
	create_search_shortkey(km,space)
	create_side_panel_keymaps(km,space)
	create_time_keymaps(km,space)
	# km.new(space,'nla.view_all','Z','PRESS',[])
	km.new(space,'nla.view_selected','Z','PRESS',[])

def uv_editor(km):
	space = km.space('UV Editor','EMPTY','WINDOW')
	# Selection #
	km.new(space,'object.move','W','PRESS',[])
	km.new(space,'object.rotate','E','PRESS',[])
	km.new(space,'object.scale','R','PRESS',[])
	create_view3d_tweak_selection_keymap(km,space)
	create_snap_keymaps(km,space)
	create_side_panel_keymaps(km,space)
	km.new(space,'wm.tool_set_by_id','Q','PRESS',[('name','builtin.select_box'),('cycle',True)])
	km.new(space,'uv.select','EVT_TWEAK_L','ANY',[('extend',True)])
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )
	km.new(space,'uv.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'uv.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'uv.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'uv.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'uv.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	# Note: multi loop command not working on uv yet
	# km.new(space,'bsmax.uvloopselect','L','PRESS',[],alt=True)
	# km.new(space,'bsmax.uvringselect','R','PRESS',[],alt=True)
	# Hide/Unhide #
	km.new(space,'uv.hide','H','PRESS',[],alt=True)
	km.new(space,'uv.hide','I','PRESS',[('unselected',True)],alt=True)
	km.new(space,'uv.reveal','U','PRESS',[],alt=True)
	km.new(space,'uv.select_split','B','PRESS',[],ctrl=True)
	km.new(space,'uv.weld','W','PRESS',[],ctrl=True)

def sequence_editor(km):
	space = km.space('Sequencer','SEQUENCE_EDITOR','WINDOW')
	km.new(space,'sequencer.batch_rename','F2','PRESS',[])
	create_side_panel_keymaps(km,space)

def file_browser(km):
	space = km.space('File Browser','FILE_BROWSER','WINDOW')
	km.new(space,'filebrowser.scaleicons','WHEELUPMOUSE','PRESS',[('up',True)],ctrl=True)
	km.new(space,'filebrowser.scaleicons','WHEELDOWNMOUSE','PRESS',[('up',False)],ctrl=True)
	km.new(space,'file.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'file.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	create_side_panel_keymaps(km,space)

def modals(km):
	# space = km.space('Knife Tool Modal Map','EMPTY','WINDOW',modal=True)
	# km.new(space,'CONFIRM','RIGHTMOUSE','PRESS',[],any=True)
	pass

def create_keymaps(km):
	if bpy.context.window_manager.keyconfigs.addon:
		window(km)
		screen(km)
		view2d(km)
		view3d(km)
		view3d_generic(km)
		view3d_select(km)
		view3d_transform(km)
		view3d_move(km)
		view3d_rotate(km)
		view3d_scale(km)
		view3d_select_box(km)
		view3d_select_circle(km)
		view3d_select_lasso(km)
		transform(km)
		object_mode(km)
		mesh(km)
		curve(km)
		armature(km)
		metaball(km)
		lattice(km)
		# font(km)
		grease_pencil(km)
		pos(km)
		vertex_paint(km)
		weight_paint(km)
		image_paint(km)
		sculpt(km)
		particle(km)
		outliner(km)
		node_editor(km)
		text(km)
		console(km)
		info(km)
		# frames(km)
		graph_editor(km)
		dopesheet_editor(km)
		nla_editor(km)
		uv_editor(km)
		sequence_editor(km)
		file_browser(km)
		modals(km)

keymaps = KeyMaps()

def register_max():
	create_keymaps(keymaps)
	keymaps.register()

def unregister_max():
	keymaps.unregister()