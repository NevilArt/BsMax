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

def add_subobject(km, space):
	km.new(space,'object.subobject_level','ONE','PRESS',[('level',1)])
	km.new(space,'object.subobject_level','TWO','PRESS',[('level',2)])
	km.new(space,'object.subobject_level','THREE','PRESS',[('level',3)])
	km.new(space,'object.subobject_level','FOUR','PRESS',[('level',4)])
	# km.new(space,'object.subobject_level','FIVE','PRESS',[('level',5)])
	# km.new(space,'object.subobject_level','SIX','PRESS',[('level',6)])
	# km.new(space,'object.subobject_level','SEVEN','PRESS',[('level',7)])
	# km.new(space,'object.subobject_level','EIGHT','PRESS',[('level',8)])
	# km.new(space,'object.subobject_level','NINE','PRESS',[('level',9)])
	# km.new(space,'object.subobject_level','ZERO','PRESS',[('level',0)])

def add_switch_view(km, space):
	km.new(space,'view3d.perespective','P','PRESS',[('mode','Perspective')])
	km.new(space,'view3d.perespective','U','PRESS',[('mode','Orthographic')])
	km.new(space,'view3d.view_axis','F','PRESS',[('type','FRONT')])
	km.new(space,'view3d.view_axis','L','PRESS',[('type','LEFT')])
	km.new(space,'view3d.view_axis','T','PRESS',[('type','TOP')])
	km.new(space,'view3d.view_axis','B','PRESS',[('type','BOTTOM')])

def add_view3d_click_selection(km, space):
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect_all',True)])
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('toggle',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect',True)],alt=True)

def add_view3d_tweak_selection(km, space):
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
	km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )

def add_transform_tool(km, space, preferences, smax=False):
	if preferences.blender_transform_type:
		km.new(space,'transform.translate','W','PRESS',[])
		km.new(space,'transform.rotate','E','PRESS',[])
		km.new(space,'transform.resize','R','PRESS',[])
	else:
		if smax:
			km.new(space,'object.move','W','PRESS',[('smax',True)])
			km.new(space,'object.rotate','E','PRESS',[('smax',True)])
			km.new(space,'object.scale','R','PRESS',[('cage',False)])
		else:
			km.new(space,'object.move','W','PRESS',[])
			km.new(space,'object.rotate','E','PRESS',[])
			km.new(space,'object.scale','R','PRESS',[])

def add_snap(km, space):
	km.new(space,'object.snap_toggle','S','PRESS',[])
	km.new(space,'object.angel_snap','A','PRESS',[])

def add_time(km, space):
	km.new(space,'anim.frame_set','HOME','PRESS',[('frame','First')])
	km.new(space,'anim.frame_set','END','PRESS',[('frame','Last')])
	km.new(space,'anim.frame_set','PERIOD','PRESS',[('frame','Next')])
	km.new(space,'anim.frame_set','COMMA','PRESS',[('frame','Previous')])
	km.new(space,'anim.set_key','K','PRESS',[])
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])

def add_side_panel(km, space):
	km.new(space,'wm.context_toggle','LEFT_BRACKET','PRESS',[('data_path','space_data.show_region_toolbar')])
	km.new(space,'wm.context_toggle','RIGHT_BRACKET','PRESS',[('data_path','space_data.show_region_ui')])

def add_search(km, space):
	if bpy.app.version[1] < 90:
		km.new(space,'wm.search_menu','X','PRESS',[])
	else:
		km.new(space,'wm.search_menu','X','PRESS',[],ctrl=True,shift=True,alt=True)
		km.new(space,'wm.search_operator','X','PRESS',[])

def add_show_types(km, space):
	km.new(space,'view3d.show_geometry_toggle','G','PRESS',[],shift=True)
	km.new(space,'view3d.show_helper_toggle','H','PRESS',[],shift=True)
	km.new(space,'view3d.show_shape_toggle','S','PRESS',[],shift=True)
	km.new(space,'view3d.show_light_toggle','L','PRESS',[],shift=True)
	km.new(space,'view3d.show_bone_toggle','B','PRESS',[],shift=True)
	km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)

def add_float_editors(km, space):
	km.new(space,'editor.float','M','PRESS',[('ui_type','ShaderNodeTree'),('shader_type','OBJECT')])
	km.new(space,'editor.float','EIGHT','PRESS',[('ui_type','ShaderNodeTree'),('shader_type','WORLD')])
	# km.new(space,'editor.float','SIX','PRESS',[('ui_type','particle')])
	# km.new(space,'editor.float','H','PRESS',[('ui_type','OUTLINER')])

def add_float_menu(km, space, preferences):
	fm = km_float_menu
	if preferences.floatmenus == "3DsMax":
		fm.new(space,"bsmax.view3dquadmenue","V","PRESS",[('menu','viewport'),('space','View3D')])
		""" This not needed drop tool can call this """
		# fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','default'),('space','View3D')])
		""" Ignore Alt + RMB in Maya navigation enabled """
		if preferences.navigation_3d != 'Maya':
			fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','coordinate'),('space','View3D')],alt=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','create'),('space','View3D')],ctrl=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','snap'),('space','View3D')],shift=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','render'),('space','View3D')],alt=True,ctrl=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','fx'),('space','View3D')],alt=True,shift=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','Selection'),('space','View3D')],ctrl=True,shift=True)
		fm.new(space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",[('menu','custom'),('space','View3D')],alt=True,ctrl=True,shift=True)
#------------------------------------------------------------------------------------------------------#

def window(km):
	km.mute('Window','wm.quit_blender','Q','PRESS',ctrl=True)
	space = km.space('Window','EMPTY','WINDOW')
	add_search(km, space)

def screen(km):
	space = km.space('Screen','EMPTY','WINDOW')
	km.new(space,'render.render','F9','PRESS',[('use_viewport',True)])
	# km.new(space,'render.quick_render','F9','PRESS',[])
	km.new(space,'render.render','Q','PRESS',[('use_viewport',True),('animation',True)],shift=True)
	km.new(space,'screen.repeat_last','SEMI_COLON','PRESS',[])
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'screen.screen_full_area','X','PRESS',[('use_hide_panels',True)],alt=True,ctrl=True)
	km.new(space,'editor.script_listener','F11','PRESS',[])
	km.new(space,'ed.redo','Y','PRESS',[],ctrl=True)
	km.new(space,'screen.animation_play','SLASH','PRESS',[])

def view2d(km):
	# space = km.space('View2D','EMPTY','WINDOW')
	pass

def view2d_navigation(km,preferences):
	space = km.space('View2D','EMPTY','WINDOW')
	km.new(space,'view2d.zoom','MIDDLEMOUSE','PRESS',[],ctrl=True,alt=True)
	pass

def view3d(km,preferences):
	km.mute('3D View','view3d.view_center_pick','MIDDLEMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','NORTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','SOUTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','EAST',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','WEST',alt=True)
	km.mute('3D View','view3d.move','MIDDLEMOUSE','PRESS',shift=True)
	km.mute('3D View','view3d.localview_remove_from','M','PRESS',ctrl=True)
	km.mute('3D View','wm.call_menu_pie','Z','PRESS')
	
	space = km.space('3D View','VIEW_3D','WINDOW')
	add_search(km, space)
	add_snap(km, space)
	add_time(km, space)
	add_switch_view(km, space)
	add_view3d_tweak_selection(km, space)
	add_float_editors(km, space)
	add_float_menu(km, space, preferences)
	add_transform_tool(km, space, preferences, smax=True)

	if preferences.view_undo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)
		km.new(space,"view3d.zoomincover","WHEELINMOUSE","PRESS",[])
		km.new(space,"view3d.zoomoutcover","WHEELOUTMOUSE","PRESS",[])
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotate","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)
		km.new(space,"view3d.zoom","WHEELINMOUSE","PRESS",[('delta',1)])
		km.new(space,"view3d.zoom","WHEELOUTMOUSE","PRESS",[('delta',-1)])
	
	km.new(space,'view3d.drop_tool','RIGHTMOUSE','PRESS',[])

	km.new(space,'view3d.view_axis','EVT_TWEAK_M','NORTH',[('type','TOP'),('relative',True)],shift=True)
	km.new(space,'view3d.view_axis','EVT_TWEAK_M','SOUTH',[('type','BOTTOM'),('relative',True)],shift=True)
	km.new(space,'view3d.view_axis','EVT_TWEAK_M','EAST',[('type','RIGHT'),('relative',True)],shift=True)
	km.new(space,'view3d.view_axis','EVT_TWEAK_M','WEST',[('type','LEFT'),('relative',True)],shift=True)

	# km.new(space,'screen.header','SIX','PRESS',[],alt=True)
	km.new(space,'screen.region_quadview','W','PRESS',[],alt=True)
	km.new(space,'view3d.transform_gizmosize','EQUAL','PRESS',[('step',10)])
	km.new(space,'view3d.transform_gizmosize','MINUS','PRESS',[('step',-10)])
	km.new(space,'view3d.localview','Q','PRESS',[],alt=True)
	km.new(space,'wm.tool_set_by_id','Q','PRESS',[('name','builtin.select_box'),('cycle',True)])
	# km.new(space,'object.move','W','PRESS',[('smax',True)])
	# km.new(space,'object.rotate','E','PRESS',[('smax',True)])
	# km.new(space,'object.scale','R','PRESS',[('cage',False)])
	km.new(space,'object.scale','E','PRESS',[('cage',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('extend',True),('center',True),('enumerate',True),('object',True)],ctrl=True)
	km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect',True)],alt=True)
	km.new(space,'view3d.zoom_extended','Z','PRESS',[])
	km.new(space,'camera.set_active','C','PRESS',[])
	km.new(space,'view3d.show_hide_gride','G','PRESS',[])
	km.new(space,'view3d.show_statistics','SEVEN','PRESS',[])
	km.new(space,'wm.multi_item_rename','F2','PRESS',[])
	km.new(space,'view3d.wireframe_toggle','F3','PRESS',[])
	km.new(space,'view3d.edge_faces_toggle','F4','PRESS',[])
	km.new(space,'view3d.lighting_toggle','L','PRESS',[],ctrl=True)
	km.new(space,'view3d.background','B','PRESS',[],alt=True)
	km.new(space,'object.subobject_level','B','PRESS',[('level',6)],ctrl=True)
	km.new(space,'camera.show_safe_areas','F','PRESS',[],shift=True)
	# km.new(space,'scene.hold','H','PRESS',[],ctrl=True,alt=True)
	# km.new(space,'scene.fetch','F','PRESS',[],ctrl=True,alt=True)
	km.new(space,'wm.call_menu','A','PRESS',[('name','BSMAX_MT_createmenu')],ctrl=True,shift=True)
	km.new(space,'wm.call_menu','T','PRESS',[('name','TOPBAR_MT_file_external_data')],shift=True)
	km.new(space,'view3d.homeview','HOME','PRESS',[],alt=True)
	km.new(space,'screen.animation_play','SLASH','PRESS',[])
	km.new(space,'view.undoredo','Z','PRESS',[('redo',False)],shift=True)
	km.new(space,'view.undoredo','Y','PRESS',[('redo',True)],shift=True)

def view3d_navigation(km, preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.view_undo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotatecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[])
		km.new(space,"view3d.rotate","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","MIDDLEMOUSE","PRESS",[],ctrl=True,alt=True)

def view3d_generic(km):
	km.mute('3D View Generic','wm.context_toggle','T','PRESS')
	km.mute('3D View Generic','wm.context_toggle','N','PRESS')

	space = km.space('3D View Generic','VIEW_3D','WINDOW')
	km.new(space,'view3d.properties','LEFT_BRACKET','PRESS',[])
	km.new(space,'view3d.toolshelf','RIGHT_BRACKET','PRESS',[])


def view3d_tweak(km):
	# space = km.space('3D View Tool: Tweak','VIEW_3D','WINDOW')
	pass

def view3d_select(km):
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK')
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',shift=True)

	space = km.space('3D View Tool: Select','VIEW_3D','WINDOW')
	add_view3d_tweak_selection(km, space)
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
	# space = km.space('Transform Modal Map','EMPTY','WINDOW',modal=True)
	pass

def object_mode(km, preferences):
	km.mute('Object Mode','object.hide_collection','SEVEN','PRESS',any=True)
	
	space = km.space('Object Non-modal','EMPTY','WINDOW')
	km.new(space,'bsmax.mode_set','TAB','PRESS',[])

	space = km.space('Object Mode','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_view3d_tweak_selection(km, space)
	add_view3d_click_selection(km, space)
	add_snap(km, space)
	add_subobject(km, space)
	add_float_editors(km, space)
	add_float_menu(km, space, preferences)
	add_show_types(km, space)
	
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'view3d.select','LEFTMOUSE','RELEASE',[('enumerate',True)],shift=True)
	km.new(space,'object.select_all','A','PRESS',[('action','SELECT')],ctrl=True )
	km.new(space,'object.select_all','D','PRESS',[('action','DESELECT')],ctrl=True )
	km.new(space,'object.select_all','I','PRESS',[('action','INVERT')],ctrl=True )
	km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
	km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
	km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',False)])
	km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',True)],ctrl=True)
	km.new(space,'object.select_similar','Q','PRESS',[],ctrl=True)

	km.new(space,'object.hide','H','PRESS',[('mode','selection')],alt=True)
	km.new(space,'object.hide','I','PRESS',[('mode','unselected')],alt=True)
	km.new(space,'object.hide','U','PRESS',[('mode','clear')],alt=True)
	# km.new(space,'view3d.show_geometry_toggle','G','PRESS',[],shift=True)
	# km.new(space,'view3d.show_helper_toggle','H','PRESS',[],shift=True)
	# km.new(space,'view3d.show_shape_toggle','S','PRESS',[],shift=True)
	# km.new(space,'view3d.show_light_toggle','L','PRESS',[],shift=True)
	# km.new(space,'view3d.show_bone_toggle','B','PRESS',[],shift=True)
	# km.new(space,'view3d.show_camera_toggle','C','PRESS',[],shift=True)

	km.new(space,'object.modify_pivotpoint','INSERT','PRESS',[])
	km.new(space,'wm.call_menu','INSERT','PRESS',[('name','OBJECT_MT_Set_Pivot_Point')],ctrl=True)

	km.new(space,'object.align_selected_to_target','A','PRESS',[],alt=True)
	km.new(space,'object.transform_type_in','F12','PRESS',[])
	km.new(space,'view3d.lighting_toggle','L','PRESS',[],ctrl=True)
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'modifier.edit_multi','TAB','PRESS',[],ctrl=True)
	km.new(space,'object.viewoport_display','X','PRESS',[],alt=True)
	km.new(space,'object.join_plus','J','PRESS',[],ctrl=True)
	km.new(space,'object.select_children','LEFTMOUSE','DOUBLE_CLICK',[('full',True)])
	km.new(space,'object.select_children','LEFTMOUSE','DOUBLE_CLICK',[('full',True),('extend',True)],ctrl=True)
	km.new(space,'object.delete_plus','DEL','PRESS',[])

def mesh(km, preferences):
	km.mute('Mesh','mesh.shortest_path_pick','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('Mesh','mesh.loop_select','LEFTMOUSE','CLICK',alt=True)
	km.mute('Mesh','mesh.select_all','A','PRESS')

	space = km.space('Mesh','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_view3d_tweak_selection(km, space)
	add_switch_view(km, space)
	add_float_menu(km, space, preferences)
	add_subobject(km, space)

	km.new(space,'mesh.select_element_toggle','FIVE','PRESS',[('mode','SET')])
	km.new(space,'mesh.select_element_setting','FIVE','PRESS',[('mode','SET')],ctrl=True)
	km.new(space,'mesh.select_max','LEFTMOUSE','CLICK',[('mode','SET')])
	km.new(space,'mesh.select_max','LEFTMOUSE','CLICK',[('mode','ADD')],ctrl=True)
	km.new(space,'mesh.select_max','LEFTMOUSE','CLICK',[('mode','SUB')],alt=True)
	# km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	# km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	# km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)

	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'mesh.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'mesh.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'mesh.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'mesh.shortest_path_pick','LEFTMOUSE','PRESS',[],shift=True)
	km.new(space,'mesh.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'mesh.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'mesh.smart_select_loop','LEFTMOUSE','DOUBLE_CLICK',[])
	km.new(space,'mesh.smart_select_loop','L','PRESS',[],alt=True)
	km.new(space,'mesh.smart_select_ring','R','PRESS',[],alt=True)
	km.new(space,'mesh.select_similar','Q','PRESS',[],ctrl=True)
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
	# km.new(space,'mesh.chamfer','C','PRESS',[],ctrl=True,shift=True)
	km.new(space,'transform.vert_slide','X','PRESS',[],shift=True)
	km.new(space,'mesh.merge','C','PRESS',[('type','CENTER')],alt=True,ctrl=True)
	km.new(space,'mesh.edge_face_add','P','PRESS',[],alt=True)
	# km.new(space,'mesh.smart_create','P','PRESS',[],alt=True)
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
	km.new(space,'mesh.subdivide','M','PRESS',[],ctrl=True)
	km.new(space,'transform.skin_resize','A','PRESS',[],ctrl=True,shift=True)
	# Tools #
	km.new(space,'view3d.shade_selected_faces','F2','PRESS',[])
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
	km.new(space,'wm.tool_set_by_id','R','PRESS',[('name','builtin.scale'),('cycle',True)])
	km.new(space,'anim.set_key','K','PRESS',[])
	# TEST #
	km.new(space,'mesh.drag','EVT_TWEAK_L','ANY',[])

def curve(km, preferences):
	space = km.space('Curve','EMPTY','WINDOW')
	add_search(km, space)
	add_snap(km, space)
	add_side_panel(km, space)
	# add_view3d_click_selection(km, space)
	add_view3d_tweak_selection(km, space)
	add_subobject(km, space)
	add_switch_view(km, space)
	add_float_menu(km, space, preferences)

	km.new(space,'mesh.select_element_toggle','FIVE','PRESS',[('mode','SET')])
	km.new(space,'curve.select_max','LEFTMOUSE','CLICK',[('mode','SET')])
	km.new(space,'curve.select_max','LEFTMOUSE','CLICK',[('mode','ADD')],ctrl=True)
	km.new(space,'curve.select_max','LEFTMOUSE','CLICK',[('mode','SUB')],alt=True)

	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'curve.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'curve.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'curve.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'curve.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'curve.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'curve.select_similar','Q','PRESS',[],ctrl=True)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	
	km.new(space,'curve.break','B','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'curve.extrude_move','E','PRESS',[('action','DESELECT')],ctrl=True,shift=True)

	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
	km.new(space,'curve.chamfer','C','PRESS',[('fillet',True),('typein',False)],ctrl=True,shift=True)
	# km.new(space,'curve.chamfer','C','DOUBLE_CLICK',[('fillet',True),('typein',True)],ctrl=True,shift=True)


def armature(km, preferences):
	space = km.space('Armature','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_subobject(km, space)
	add_switch_view(km, space)
	add_view3d_click_selection(km, space)
	add_float_menu(km, space, preferences)

	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
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
	# View #
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'wm.multi_item_rename','F2','PRESS',[])
	# Tools #
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])

def metaball(km):
	space = km.space('Metaball','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_subobject(km, space)
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'mball.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'mball.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'mball.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'mball.select_similar','Q','PRESS',[],ctrl=True)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])

def lattice(km):
	space = km.space('Lattice','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_subobject(km, space)
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'lattice.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'lattice.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'lattice.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'lattice.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'lattice.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'lattice.select_similar','Q','PRESS',[],ctrl=True)
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])
	km.new(space,'camera.select','C','PRESS',[])

def grease_pencil(km, preferences):
	space = km.space('Grease Pencil','EMPTY','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_float_menu(km, space, preferences)

def pos(km, preferences):
	space = km.space('Pose','EMPTY','WINDOW')
	add_view3d_click_selection(km, space)
	add_subobject(km, space)
	add_time(km, space)
	add_float_menu(km, space, preferences)
	km.new(space,"view3d.drop_tool","RIGHTMOUSE","PRESS",[])
	km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
	km.new(space,'pose.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'pose.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'pose.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'pose.select_more','PAGE_UP','PRESS',[],ctrl=True,shift=True)
	km.new(space,'pose.select_less','PAGE_DOWN','PRESS',[],ctrl=True,shift=True)
	km.new(space,'pose.select_hierarchy_plus','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
	km.new(space,'pose.select_hierarchy_plus','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
	km.new(space,'pose.select_hierarchy_plus','PAGE_DOWN','PRESS',[('direction','CHILDREN'),('full',False),('extend',False)])
	km.new(space,'pose.select_hierarchy_plus','PAGE_DOWN','PRESS',[('direction','CHILDREN'),('full',False),('extend',True)],ctrl=True)
	km.new(space,'pose.select_hierarchy_plus','LEFTMOUSE','DOUBLE_CLICK',[('direction','CHILDREN'),('full',True),('extend',True)])
	km.new(space,'camera.select','C','PRESS',[])
	km.new(space,'pose.hide','H','PRESS',[],alt=True)
	km.new(space,'pose.hide','I','PRESS',[('unselected',True)],alt=True)
	km.new(space,'pose.reveal','U','PRESS',[],alt=True)

def vertex_paint(km):
	space = km.space('Vertex Paint','EMPTY','WINDOW')
	add_switch_view(km, space)
	add_show_types(km, space)
	km.new(space,'camera.set_active','C','PRESS',[])

def weight_paint(km):
	space = km.space('Weight Paint','EMPTY','WINDOW')
	add_switch_view(km, space)
	add_show_types(km, space)
	add_view3d_click_selection(km, space)
	add_view3d_tweak_selection(km, space)
	
	km.new(space,'camera.set_active','C','PRESS',[])
	km.new(space,'wm.context_toggle','ONE','PRESS',[('data_path','weight_paint_object.data.use_paint_mask_vertex')])
	km.new(space,'wm.context_toggle','TWO','PRESS',[('data_path','weight_paint_object.data.use_paint_mask')])
	km.new(space,'paint.vert_select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'paint.vert_select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'paint.vert_select_all','I','PRESS',[('action','INVERT')],ctrl=True)

def image_paint(km):
	space = km.space('Image Paint','EMPTY','WINDOW')
	add_side_panel(km, space)

def sculpt(km, preferences):
	km.mute('Sculpt','wm.radial_control','F','PRESS')

	space = km.space('Sculpt','EMPTY','WINDOW')
	add_switch_view(km, space)
	add_show_types(km, space)
	add_transform_tool(km, space, preferences)

	km.new(space,'camera.set_active','C','PRESS',[])
	# km.new(space,'object.move','W','PRESS',[])
	# km.new(space,'object.rotate','E','PRESS',[])
	# km.new(space,'object.scale','R','PRESS',[])

	# props = [("data_path_primary", 'tool_settings.sculpt.brush.strength'),
	# 	("data_path_secondary", 'tool_settings.unified_paint_settings.strength'),
	# 	("use_secondary", 'tool_settings.unified_paint_settings.use_unified_strength'),
	# 	("rotation_path", 'tool_settings.sculpt.brush.texture_slot.angle'),
	# 	("color_path", 'tool_settings.sculpt.brush.cursor_color_add'),
	# 	("fill_color_path", ''),
	# 	("fill_color_override_path", ''),
	# 	("fill_color_override_test_path", ''),
	# 	("zoom_path", ''),
	# 	("image_id", 'tool_settings.sculpt.brush'),
	# 	("secondary_tex", False)]
	# km.new(space,'wm.radial_control','LEFTMOUSE','PRESS',props, shift=True, ctrl=True)

def particle(km):
	space = km.space('Particle','EMPTY','WINDOW')
	add_switch_view(km, space)
	km.new(space,'camera.set_active','C','PRESS',[])
	km.new(space,'mesh.select_element_toggle','FIVE','PRESS',[('mode','SET')])
	km.new(space,'particle.select_max','LEFTMOUSE','CLICK',[('mode','SET')])
	km.new(space,'particle.select_max','LEFTMOUSE','CLICK',[('mode','ADD')],ctrl=True)
	km.new(space,'particle.select_max','LEFTMOUSE','CLICK',[('mode','SUB')],alt=True)
	km.new(space,'particle.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'particle.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'particle.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'particle.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'particle.select_less','PAGE_DOWN','PRESS',[],ctrl=True)

def outliner(km):
	# km.mute('Outliner','outliner.item_rename','F2','PRESS')
	
	space = km.space('Outliner','OUTLINER','WINDOW')
	add_search(km, space)
	if bpy.app.version[1] < 81:
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
		km.new(space,'outliner.item_rename','F2','PRESS',[])
		km.new(space,'outliner.collection_new','N','PRESS',[],ctrl=True)
		km.new(space,'object.delete','DEL','PRESS',[('confirm',False)],ctrl=True)
		km.new(space,'outliner.hide','H','PRESS',[],alt=True)
		km.new(space,'outliner.unhide_all','U','PRESS',[],alt=True)

	km.new(space,'outliner.show_active','Z','PRESS',[])
	# km.new(space,'outliner.rename_selection','F2','PRESS',[])

def node_editor(km):
	km.mute('Node Editor','node.select','LEFTMOUSE','PRESS',shift=True)
	km.mute('Node Editor','node.select','LEFTMOUSE','PRESS',ctrl=True)
	km.mute('Node Editor','node.select','LEFTMOUSE','PRESS',alt=True)
	space = km.space('Node Editor','NODE_EDITOR','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	km.new(space,'wm.multi_item_rename','F2','PRESS',[])
	km.new(space,'node.select','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
	km.new(space,'node.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
	km.new(space,'node.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )
	km.new(space,'node.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'node.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'node.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'wm.save_as_mainfile','S','PRESS',[],ctrl=True,shift=True)
	# km.new(space,'node.view_selected','Z','PRESS',[])
	km.new(space,'node.zoom_extended','Z','PRESS',[])
	km.new(space,'wm.call_menu','RIGHTMOUSE','PRESS',[('name','NODE_MT_add')])
	# km.new(space,'node.duplicate_move','EVT_TWEAK_L','ANY',[('keep_inputs',True)],shift=True)
	km.new(space,'node.duplicate_move_keep_inputs','EVT_TWEAK_L','ANY',[],shift=True)
	km.new(space,'node.hide_socket_toggle','H','PRESS',[])
	km.new(space,'node.hide_toggle','H','PRESS',[],ctrl=True)
	km.new(space,'node.links_cut','MIDDLEMOUSE','PRESS',[],alt=True)
	km.new(space,'node.link','EVT_TWEAK_L','ANY',[('detach',True)],alt=True)
	km.new(space,'node.select_linked_from','T','PRESS',[],ctrl=True)
	km.new(space,'material.assign_to_selection','A','PRESS',[])
	

def text(km):
	""" script editor """
	space = km.space('Text','TEXT_EDITOR','WINDOW')
	km.new(space,'text.run_script','E','PRESS',[],ctrl=True)
	km.new(space,'text.run_script','F5','PRESS',[]) # From MVS
	km.new(space,'text.autocomplete','RET','PRESS',[],ctrl=True)
	km.new(space,'text.autocomplete','SPACE','PRESS',[],ctrl=True)
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
	km.new(space,'console.clear','D','PRESS',[],ctrl=True)

def info(km):
	space = km.space('Info','INFO','WINDOW')
	add_search(km, space)
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
	add_search(km, space)
	add_side_panel(km, space)
	add_time(km, space)
	km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','ADD'),('tweak',True)],ctrl=True)
	km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','SUB'),('tweak',True)],alt=True)
	km.new(space,'graph.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'graph.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	km.new(space,'graph.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	km.new(space,'graph.select_more','PAGE_UP','PRESS',[],ctrl=True)
	km.new(space,'graph.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
	km.new(space,'graph.view_selected','Z','PRESS',[])
	# km.new(space,'graph.view_all','??','PRESS',[])
	km.new(space,'anim.delete_key','DEL','PRESS',[])

def dopesheet_editor(km):
	""" (Timeline) """
	space = km.space('Dopesheet','DOPESHEET_EDITOR','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	add_time(km, space)

	km.new(space,'anim.set_timeline_range','LEFTMOUSE','PRESS',[('mode','First')],alt=True,ctrl=True)
	km.new(space,'anim.set_timeline_range','RIGHTMOUSE','PRESS',[('mode','End')],alt=True,ctrl=True)
	km.new(space,'anim.set_timeline_range','MIDDLEMOUSE','PRESS',[('mode','Shift')],alt=True,ctrl=True)
	km.new(space,'anim.delete_key','DEL','PRESS',[])

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
	add_search(km, space)
	add_side_panel(km, space)
	add_time(km, space)
	# km.new(space,'nla.view_all','Z','PRESS',[])
	km.new(space,'nla.view_selected','Z','PRESS',[])

def clip_editor(km):
	km.mute('Clip Editor','transform.translate','EVT_TWEAK_L','ANY')
	km.mute('Clip Editor','clip.add_marker_slide','LEFTMOUSE','PRESS',ctrl=True)
	
	space = km.space('Clip Editor','CLIP_EDITOR','WINDOW')
	add_side_panel(km, space)
	add_time(km, space)
	
	km.new(space,'clip.select','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
	# TODO need a Alt click diselect operator
	km.new(space,'clip.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'clip.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	km.new(space,'clip.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
	km.new(space,'clip.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'clip.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
	# km.new(space,'clip.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
	# km.new(space,'clip.delete_marker','DEL','PRESS',[]) TODO replace by instan delete operator
	# TODO replace by automatic one
	# km.new(space,'clip.view_all','Z','PRESS',[('fit_view', True)])
	# km.new(space,'clip.view_selected','Z','PRESS',[])
	km.new(space,'clip.autoframe','Z','PRESS',[])

def uv_editor(km, preferences):
	space = km.space('UV Editor','EMPTY','WINDOW')
	add_snap(km, space)
	add_side_panel(km, space)
	add_transform_tool(km, space, preferences)
	
	# km.new(space,'object.move','W','PRESS',[])
	# km.new(space,'object.rotate','E','PRESS',[])
	# km.new(space,'object.scale','R','PRESS',[])
	
	km.new(space,'wm.tool_set_by_id','Q','PRESS',[('name','builtin.select_box'),('cycle',True)])

	km.new(space,'uv.select','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
	# km.new(space,'uv.select','LEFTMOUSE','PRESS',[('extend',True)],alt=True)
	km.new(space,'uv.shortest_path_pick','LEFTMOUSE','PRESS',[],shift=True)
	km.new(space,'uv.shortest_path_pick','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True,shift=True)
	km.new(space,'uv.select_loop','LEFTMOUSE','DOUBLE_CLICK',[])
	km.new(space,'uv.select_loop','LEFTMOUSE','DOUBLE_CLICK',[('extend',True)],ctrl=True)

	km.new(space,'uv.select','EVT_TWEAK_L','ANY',[('extend',True)])
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
	km.new(space,'uv.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
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
	add_search(km, space)
	add_side_panel(km, space)
	km.new(space,'wm.multi_item_rename','F2','PRESS',[])

def file_browser(km):
	space = km.space('File Browser','FILE_BROWSER','WINDOW')
	add_side_panel(km, space)
	km.new(space,'file.refresh','F5','PRESS',[])
	km.new(space,'file.parent','BACK_SPACE','PRESS',[])
	km.new(space,'file.parent','UP_ARROW','PRESS',[],alt=True)
	km.new(space,'file.next','RIGHT_ARROW','PRESS',[],alt=True)
	km.new(space,'file.previous','LEFT_ARROW','PRESS',[],alt=True)
	km.new(space,'file.directory_new','N','PRESS',[],ctrl=True,shift=True)
	km.new(space,'filebrowser.scaleicons','WHEELUPMOUSE','PRESS',[('up',True)],ctrl=True)
	km.new(space,'filebrowser.scaleicons','WHEELDOWNMOUSE','PRESS',[('up',False)],ctrl=True)
	km.new(space,'file.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'file.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)

def modals(km):
	# space = km.space('Knife Tool Modal Map','EMPTY','WINDOW',modal=True)
	# km.new(space,'CONFIRM','RIGHTMOUSE','PRESS',[],any=True,modal=True)
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

def register_max(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.navigation_3d == "3DsMax":
			view3d_navigation(km_navigation_3d, preferences)
			km_navigation_3d.register()
			bpy.context.preferences.inputs.view_zoom_axis = 'VERTICAL'
		else:
			km_navigation_3d.unregister()

		if preferences.navigation_2d == "3DsMax":
			view2d_navigation(km_navigation_2d, preferences)
			km_navigation_2d.register()
		else:
			km_navigation_2d.unregister()

		if preferences.viowport == "3DsMax":
			window(km_viowport)
			screen(km_viowport)
			view3d(km_viowport, preferences)
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
			object_mode(km_viowport, preferences)
			mesh(km_viowport, preferences)
			curve(km_viowport, preferences)
			armature(km_viowport, preferences)
			metaball(km_viowport)
			lattice(km_viowport)
			grease_pencil(km_viowport, preferences)
			pos(km_viowport, preferences)
			outliner(km_viowport)
			km_viowport.register()
		else:
			km_viowport.unregister()

		if preferences.sculpt == "3DsMax":
			vertex_paint(km_sculpt)
			weight_paint(km_sculpt)
			image_paint(km_sculpt)
			particle(km_sculpt)
			sculpt(km_sculpt, preferences)
			km_sculpt.register()
		else:
			km_sculpt.unregister()

		if preferences.uv_editor == "3DsMax":
			uv_editor(km_uv_editor, preferences)
			km_uv_editor.register()
		else:
			km_uv_editor.unregister()

		if preferences.node_editor == "3DsMax":
			node_editor(km_node_editor)
			km_node_editor.register()
		else:
			km_node_editor.unregister()

		if preferences.graph_editor == "3DsMax":
			graph_editor(km_graph_editor)
			dopesheet_editor(km_graph_editor)
			nla_editor(km_graph_editor)
			km_graph_editor.register()
		else:
			km_graph_editor.unregister()
			
		if preferences.clip_editor == "3DsMax":
			clip_editor(km_clip_editor)
			km_clip_editor.register()
		else:
			km_clip_editor.unregister()

		if preferences.video_sequencer == "3DsMax":
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

		if preferences.text_editor == "3DsMax":
			console(km_text_editor)
			text(km_text_editor)
			info(km_text_editor)
			km_text_editor.register()
		else:
			km_text_editor.unregister()
		
		if preferences.file_browser == "3DsMax":
			file_browser(km_file_browser)
			km_file_browser.register()
		else:
			km_file_browser.unregister()

		if preferences.floatmenus == "3DsMax":
			km_float_menu.register()
		else:
			km_float_menu.unregister()

def unregister_max():
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