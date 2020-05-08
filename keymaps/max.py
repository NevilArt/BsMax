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
	# Disable/Enable Unwanted Default ShortKeys
	km.mute('3D View Generic','wm.context_toggle','T','PRESS')
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK')
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('3D View','view3d.select','LEFTMOUSE','CLICK',shift=True)
	km.mute('3D View','view3d.view_center_pick','MIDDLEMOUSE','CLICK',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','NORTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','SOUTH',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','EAST',alt=True)
	km.mute('3D View','view3d.view_axis','EVT_TWEAK_M','WEST',alt=True)
	km.mute('3D View Tool: Select Box','view3d.select_box','EVT_TWEAK_L','ANY',ctrl=True)
	km.mute('3D View Tool: Select Circle','view3d.select_circle','LEFTMOUSE','PRESS',ctrl=True)
	km.mute('3D View Tool: Select Lasso','view3d.select_lasso','EVT_TWEAK_L','ANY',ctrl=True)
	km.mute('3D View Generic','wm.context_toggle','T','ANY')
	km.mute('Mesh','mesh.shortest_path_pick','LEFTMOUSE','CLICK',ctrl=True)
	km.mute('Mesh','mesh.loop_select','LEFTMOUSE','CLICK',alt=True)
	km.mute('Window','wm.quit_blender','Q','PRESS',ctrl=True)

def create_subobject_mode_keymap(km,space):
	km.new(space,'bsmax.subobjectlevel','ONE','PRESS',[('level',1)])
	km.new(space,'bsmax.subobjectlevel','TWO','PRESS',[('level',2)])
	km.new(space,'bsmax.subobjectlevel','THREE','PRESS',[('level',3)])
	km.new(space,'bsmax.subobjectlevel','FOUR','PRESS',[('level',4)])
	km.new(space,'bsmax.subobjectlevel','FIVE','PRESS',[('level',5)])
	km.new(space,'bsmax.subobjectlevel','SIX','PRESS',[('level',6)])
	km.new(space,'bsmax.subobjectlevel','SEVEN','PRESS',[('level',7)])
	km.new(space,'bsmax.subobjectlevel','EIGHT','PRESS',[('level',8)])
	km.new(space,'bsmax.subobjectlevel','NINE','PRESS',[('level',9)])
	km.new(space,'bsmax.subobjectlevel','ZERO','PRESS',[('level',0)])

def create_switch_view_keymap(km,space):
	# km.new(space,'view3d.view_persportho','P','PRESS',[])
	km.new(space,'view3d.perespective_toggle','P','PRESS',[])
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

# Create Keymaps
def create_keymaps(km):
	if bpy.context.window_manager.keyconfigs.addon:
		# Window ---------------------------------------------------------------
		space = km.space('Window','EMPTY','WINDOW')
		km.new(space,'wm.search_menu','X','PRESS',[])
		# 2D View --------------------------------------------------------------
		# space = km.space('View2D','EMPTY','WINDOW')
		# km.new(space,'view2d.zoom','MIDDLEMOUSE','PRESS',[],ctrl=True,alt=True)
		# 3D View --------------------------------------------------------------
		space = km.space('3D View','VIEW_3D','WINDOW')
		km.new(space,'wm.search_menu','X','PRESS',[])
		km.new(space,'screen.header','SIX','PRESS',[],alt=True)
		km.new(space,'screen.region_quadview','W','PRESS',[],alt=True)
		km.new(space,'bsmax.transformgizmosize','EQUAL','PRESS',[('step',10)])
		km.new(space,'bsmax.transformgizmosize','MINUS','PRESS',[('step',-10)])
		# View
		create_switch_view_keymap(km,space)
		# Display
		km.new(space,'view3d.localview','Q','PRESS',[],alt=True)
		# Set tools
		km.new(space,'wm.tool_set_by_id','Q','PRESS',[('name','builtin.select_box'),('cycle',True)])
		km.new(space,'bsmax.move','W','PRESS',[])
		km.new(space,'bsmax.rotate','E','PRESS',[])
		km.new(space,'bsmax.scale','R','PRESS',[])
		km.new(space,'bsmax.scale','E','PRESS',[],ctrl=True)
		# selection
		km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('extend',True)],ctrl=True)
		km.new(space,'view3d.select','LEFTMOUSE','CLICK',[('deselect',True)],alt=True)
		create_view3d_tweak_selection_keymap(km,space)
		# Tools From BsMax
		km.new(space,'view3d.zoomextended','Z','PRESS',[])
		km.new(space,'bsmax.setasactivecamera','C','PRESS',[])
		km.new(space,'bsmax.showhidegride','G','PRESS',[])
		km.new(space,'bsmax.showstatistics','Y','PRESS',[]) #Temprary
		km.new(space,'object.batchrename','F2','PRESS',[])
		km.new(space,'view3d.wireframetoggle','F3','PRESS',[])
		km.new(space,'view3d.edgefacestoggle','F4','PRESS',[])
		km.new(space,'bsmax.lightingtoggle','L','PRESS',[],ctrl=True)
		km.new(space,'bsmax.snaptoggle','S','PRESS',[])
		km.new(space,'bsmax.angelsnap','A','PRESS',[])
		km.new(space,'bsmax.viewport_background','B','PRESS',[],alt=True)
		km.new(space,'bsmax.subobjectlevel','B','PRESS',[('level',6)],ctrl=True)
		km.new(space,'bsmax.show_safe_areas','F','PRESS',[],shift=True)
		km.new(space,'bsmax.setframe','HOME','PRESS',[('frame','First')])
		km.new(space,'bsmax.setframe','END','PRESS',[('frame','Last')])
		km.new(space,'bsmax.setframe','PERIOD','PRESS',[('frame','Next')])
		km.new(space,'bsmax.setframe','COMMA','PRESS',[('frame','Previous')])
		km.new(space,'bsmax.hold','H','PRESS',[],ctrl=True,alt=True)
		km.new(space,'bsmax.fetch','F','PRESS',[],ctrl=True,alt=True)
		km.new(space,'wm.call_menu','A','PRESS',[('name','BSMAX_MT_createmenu')],ctrl=True,shift=True)
		km.new(space,'view3d.homeview','HOME','PRESS',[],alt=True)
		km.new(space,'view.undoredo','Z','PRESS',[('redo',False)],shift=True)
		km.new(space,'view.undoredo','Y','PRESS',[('redo',True)],shift=True)
		# Float Editors
		km.new(space,'bsmax.openmaterialeditor','M','PRESS',[])
		# 3D View Tool: Select ------------------------------------------------
		space = km.space('3D View Tool: Select','VIEW_3D','WINDOW')
		km.new(space,'bsmax.tweakbetter','EVT_TWEAK_L','ANY',[])
		create_view3d_tweak_selection_keymap(km,space)
		# 3D View Tool: Transform ---------------------------------------------
		space = km.space('3D View Tool: Transform','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		# 3D View Tool: Move ---------------------------------------------------
		space = km.space('3D View Tool: Move','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		# 3D View Tool: Rotate -------------------------------------------------
		space = km.space('3D View Tool: Rotate','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		# 3D View Tool: Scale --------------------------------------------------        
		space = km.space('3D View Tool: Scale','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		# 3D View Tool: Select Box ---------------------------------------------
		space = km.space('3D View Tool: Select Box','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
		# 3D View Tool: Select Circle ------------------------------------------
		space = km.space('3D View Tool: Select Circle','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_circle','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
		km.new(space,'view3d.select_circle','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
		# 3D View Tool: Select Lasso -------------------------------------------
		space = km.space('3D View Tool: Select Lasso','VIEW_3D','WINDOW')
		km.new(space,'view3d.select_lasso','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
		km.new(space,'view3d.select_lasso','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
		# Transform Modal Map --------------------------------------------------
		space = km.space('Transform Modal Map','EMPTY','WINDOW',modal=True)
		# km.new(space,'AXIS_X','F5','ANY',[])
		'''
		('AXIS_X',{'type': 'X','value': 'PRESS','ctrl': True},None),
		('AXIS_Y',{'type': 'Y','value': 'PRESS'},None),
		('AXIS_Z',{'type': 'Z','value': 'PRESS'},None),
		('PLANE_X',{'type': 'X','value': 'PRESS','shift': True,'ctrl': True},None),
		('PLANE_Y',{'type': 'Y','value': 'PRESS','shift': True},None),
		('PLANE_Z',{'type': 'Z','value': 'PRESS','shift': True},None),
		{'type': 'F12','value': 'PRESS','ctrl': True},
		'''
		# Object Non-modal --------------------------------------------------------------------
		space = km.space('Object Non-modal','EMPTY','WINDOW')
		km.new(space,'bsmax.mode_set','TAB','PRESS',[])
		# Object Mode -------------------------------------------------------------------------
		space = km.space('Object Mode','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# selection
		create_view3d_tweak_selection_keymap(km,space)
		create_view3d_click_celection_keymap(km,space)
		km.new(space,'view3d.select','LEFTMOUSE','RELEASE',[('enumerate',True)],shift=True)
		km.new(space,'object.select_all','A','PRESS',[('action','SELECT')],ctrl=True )
		km.new(space,'object.select_all','D','PRESS',[('action','DESELECT')],ctrl=True )
		km.new(space,'object.select_all','I','PRESS',[('action','INVERT')],ctrl=True )
		km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',False)])
		km.new(space,'object.select_hierarchy','PAGE_UP','PRESS',[('direction','PARENT'),('extend',True)],ctrl=True)
		km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',False)])
		km.new(space,'object.select_hierarchy','PAGE_DOWN','PRESS',[('direction','CHILD'),('extend',True)],ctrl=True)
		#km.new(space,'object.select_similar','Q','PRESS',ctrl=True)
		km.new(space,'bsmax.select_similar','Q','PRESS',[],ctrl=True)
		# Hide/Unhide
		km.new(space,'object.hide_view_set','H','PRESS',[],alt=True)
		km.new(space,'object.hide_view_set','I','PRESS',[('unselected',True)],alt=True)
		km.new(space,'object.hide_view_clear','U','PRESS',[],alt=True)
		km.new(space,'bsmax.showgeometrytoggle','G','PRESS',[],shift=True)
		km.new(space,'bsmax.showhelpertoggle','H','PRESS',[],shift=True)
		km.new(space,'bsmax.showshapetoggle','S','PRESS',[],shift=True)
		km.new(space,'bsmax.showlighttoggle','L','PRESS',[],shift=True)
		km.new(space,'bsmax.showbonetoggle','B','PRESS',[],shift=True)
		km.new(space,'bsmax.showcameratoggle','C','PRESS',[],shift=True)
		km.new(space,'object.modifypivotpoint','INSERT','PRESS',[])
		km.new(space,'wm.call_menu','INSERT','PRESS',[('name','BSMAX_MT_SetPivotPoint')],ctrl=True)
		# Float Editors
		km.new(space,'bsmax.openmaterialeditor','M','PRESS',[])
		# Tools
		km.new(space,'bsmax.alignselectedobjects','A','PRESS',[],alt=True)
		km.new(space,'bsmax.setkeys','K','PRESS',[])
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.transformtypein','F12','PRESS',[])
		km.new(space,'bsmax.angelsnap','A','PRESS',[])
		km.new(space,'bsmax.lightingtoggle','L','PRESS',[],ctrl=True)
		km.new(space,'bsmax.jumptofirstframe','HOME','PRESS',[])
		km.new(space,'bsmax.jumptolastframe','END','PRESS',[])
		km.new(space,'bsmax.nextframe','PERIOD','PRESS',[])
		km.new(space,'bsmax.previousframe','COMMA','PRESS',[])
		km.new(space,'screen.animation_play','SLASH','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		# Mesh -----------------------------------------------------------------
		space = km.space('Mesh','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
		km.new(space,'mesh.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'mesh.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'mesh.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		create_view3d_click_celection_keymap(km,space)
		create_view3d_tweak_selection_keymap(km,space)
		km.new(space,'mesh.shortest_path_pick','LEFTMOUSE','PRESS',[],shift=True)
		km.new(space,'mesh.select_more','PAGE_UP','PRESS',[],ctrl=True)
		km.new(space,'mesh.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
		km.new(space,'mesh.selectelement','LEFTMOUSE','DOUBLE_CLICK',[])
		km.new(space,'mesh.smart_select_loop','L','PRESS',[],alt=True)
		km.new(space,'mesh.smart_select_ring','R','PRESS',[],alt=True)
		km.new(space,'mesh.select_similar','Q','PRESS',[],ctrl=True)
		# View
		create_switch_view_keymap(km,space)
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		# Hide/Unhide
		km.new(space,'mesh.hide','H','PRESS',[],alt=True)
		km.new(space,'mesh.hide','I','PRESS',[('unselected',True)],alt=True)
		km.new(space,'mesh.reveal','U','PRESS',[],alt=True)
		# Edit
		km.new(space,'bsmax.connectpoly','E','PRESS',[],ctrl=True,shift=True)
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
		km.new(space,'bsmax.targetweld','W','PRESS',[],shift=True,ctrl=True)
		km.new(space,'bsmax.removemesh','BACK_SPACE','PRESS',[('vert',False)])
		km.new(space,'bsmax.removemesh','BACK_SPACE','PRESS',[('vert',True)],ctrl=True)
		km.new(space,'bsmax.deletemesh','DEL','PRESS',[])
		km.new(space,'bsmax.transformtypein','F12','PRESS',[])
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		# Tools
		km.new(space,'bsmax.shadeselectedfaces','F2','PRESS',[])
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
		km.new(space,'wm.tool_set_by_id','R','PRESS',[('name','builtin.scale'),('cycle',True)])
		
		# Curve ----------------------------------------------------------------
		space = km.space('Curve','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
		km.new(space,'curve.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'curve.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'curve.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		create_view3d_click_celection_keymap(km,space)
		create_view3d_tweak_selection_keymap(km,space)
		km.new(space,'curve.select_more','PAGE_UP','PRESS',[],ctrl=True)
		km.new(space,'curve.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
		km.new(space,'curve.select_similar','Q','PRESS',[],ctrl=True)
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		# View
		create_switch_view_keymap(km,space)
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		# Tools
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
		
		# Armature -------------------------------------------------------------
		space = km.space('Armature','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
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
		# Hide/Unhide
		km.new(space,'armature.hide','H','PRESS',[],alt=True)
		km.new(space,'armature.hide','I','PRESS',[('unselected',True)],alt=True)
		km.new(space,'armature.reveal','U','PRESS',[],alt=True)
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		# View
		create_switch_view_keymap(km,space)
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		km.new(space,'armature.batchrename','F2','PRESS',[])
		# Tools
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		km.new(space,'wm.tool_set_by_id','E','PRESS',[('name','builtin.rotate')])
		
		# Metaball -------------------------------------------------------------
		space = km.space('Metaball','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
		km.new(space,'mball.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'mball.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'mball.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		km.new(space,'mball.select_similar','Q','PRESS',[],ctrl=True)
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		#View
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		# Tools
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		
		# Lattice --------------------------------------------------------------
		space = km.space('Lattice','EMPTY','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
		km.new(space,'lattice.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'lattice.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'lattice.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		km.new(space,'lattice.select_more','PAGE_UP','PRESS',[],ctrl=True)
		km.new(space,'lattice.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
		km.new(space,'lattice.select_similar','Q','PRESS',[],ctrl=True)
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		#View
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		# Tools
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		
		# Font -----------------------------------------------------------------
		# Pose -----------------------------------------------------------------
		space = km.space('Pose','EMPTY','WINDOW')
		# Selection
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
		# Set Subobject Mode
		create_subobject_mode_keymap(km,space)
		#View
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		# Tools
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.selectcamera','C','PRESS',[])
		km.new(space,'bsmax.setkeys','K','PRESS',[])
		
		# Vertex Paint
		space = km.space('Vertex Paint','EMPTY','WINDOW')
		create_switch_view_keymap(km,space)
		km.new(space,'bsmax.showcameratoggle','C','PRESS',[],shift=True)
		# Weight Paint
		space = km.space('Weight Paint','EMPTY','WINDOW')
		create_switch_view_keymap(km,space)
		km.new(space,'bsmax.showcameratoggle','C','PRESS',[],shift=True)
		# Whight Paint Vertex Selection
		# Face Mask
		# Image Paint
		# Sculpt
		space = km.space('Sculpt','EMPTY','WINDOW')
		create_switch_view_keymap(km,space)
		km.new(space,'bsmax.showcameratoggle','C','PRESS',[],shift=True)
		# Particle
		# 3D View Generic ------------------------------------------------------------
		space = km.space('3D View Generic','VIEW_3D','WINDOW')
		km.new(space,'view3d.properties','LEFT_BRACKET','PRESS',[])
		km.new(space,'view3d.toolshelf','RIGHT_BRACKET','PRESS',[])
		# Outliner --------------------------------------------------------------------
		space = km.space('Outliner','OUTLINER','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# upper than 2.80 do not need this part
		if bpy.app.version[1] == 80:
			# Selection
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
			# Tools
			km.new(space,'outliner.item_rename','F2','PRESS',[])
			km.new(space,'outliner.collection_new','N','PRESS',[],ctrl=True)
			km.new(space,'object.delete','DEL','PRESS',[('confirm',False)],ctrl=True)
			km.new(space,'outliner.hide','H','PRESS',[],alt=True)
			# km.new(space,'outliner.hide_unselected','I','PRESS',[],alt=True)
			km.new(space,'outliner.unhide_all','U','PRESS',[],alt=True)
		# Node Editor -----------------------------------------------------------------
		space = km.space('Node Editor','NODE_EDITOR','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		km.new(space,'node.batchrename','F2','PRESS',[])
		# Selection
		km.new(space,'node.select','LEFTMOUSE','PRESS',[('extend',True)],ctrl=True)
		km.new(space,'node.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'node.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'node.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		# tools
		km.new(space,'node.view_selected','Z','PRESS',[])
		km.new(space,'wm.call_menu','RIGHTMOUSE','PRESS',[('name','NODE_MT_add')])
		km.new(space,'node.duplicate_move','EVT_TWEAK_L','ANY',[],shift=True)
		#node.links_cut
		# Screen ----------------------------------------------------------------------
		space = km.space('Screen','EMPTY','WINDOW')
		km.new(space,'render.render','F9','PRESS',[('use_viewport',True)])
		km.new(space,'render.render','Q','PRESS',[('use_viewport',True),('animation',True)],shift=True)
		km.new(space,'screen.repeat_last','SEMI_COLON','PRESS',[])
		km.new(space,'screen.screen_full_area','X','PRESS',[],ctrl=True)
		km.new(space,'screen.screen_full_area','X','PRESS',[('use_hide_panels',True)],alt=True,ctrl=True)
		km.new(space,'bsmax.scriptlistener','F11','PRESS',[])
		km.new(space,'ed.redo','Y','PRESS',[],ctrl=True)
		# Text ----------------------------------------------------------------------
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
		# Console ---------------------------------------------------------------------
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
		# Info ------------------------------------------------------------------------
		space = km.space('Info','INFO','WINDOW')
		km.new(space,'wm.search_menu','X','PRESS',[])
		km.new(space,'text.new','N','PRESS',[],ctrl=True)
		km.new(space,'text.open','O','PRESS',[],ctrl=True)
		km.new(space,'text.save','S','PRESS',[],ctrl=True)
		km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True)
		km.new(space,'info.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True)
		km.new(space,'info.select_all_toggle','A','PRESS',[],ctrl=True)
		km.new(space,'info.clear','D','PRESS',[('scrollback',True)],ctrl=True)
		# Frames ----------------------------------------------------------------------
		space = km.space('Frames','EMPTY','WINDOW')
		km.new(space,'bsmax.jumptofirstframe','HOME','PRESS',[])
		km.new(space,'bsmax.jumptolastframe','END','PRESS',[])
		km.new(space,'bsmax.nextframe','PERIOD','PRESS',[])
		km.new(space,'bsmax.previousframe','COMMA','PRESS',[])
		# GRAPH_EDITOR ----------------------------------------------------------------
		space = km.space('Graph Editor','GRAPH_EDITOR','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Selection
		km.new(space,'graph.clickselect','LEFTMOUSE','PRESS',[])
		km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
		km.new(space,'graph.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )
		km.new(space,'graph.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'graph.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'graph.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		km.new(space,'graph.select_more','PAGE_UP','PRESS',[],ctrl=True)
		km.new(space,'graph.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
		# Translate 
		km.new(space,'transform.translate','EVT_TWEAK_L','ANY',[])
		# Tools
		km.new(space,'bsmax.setkeys','K','PRESS',[])
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		# DOPESHEET_EDITOR (Timeline)--------------------------------------------------
		space = km.space('Dopesheet','DOPESHEET_EDITOR','WINDOW')
		# Global
		km.new(space,'wm.search_menu','X','PRESS',[])
		# Tools
		km.new(space,'bsmax.setkeys','K','PRESS',[])
		km.new(space,'bsmax.autokeymodetoggle','N','PRESS',[])
		km.new(space,'bsmax.settimelinerange','LEFTMOUSE','PRESS',[('mode','First')],alt=True,ctrl=True)
		km.new(space,'bsmax.settimelinerange','RIGHTMOUSE','PRESS',[('mode','End')],alt=True,ctrl=True)
		km.new(space,'bsmax.settimelinerange','MIDDLEMOUSE','PRESS',[('mode','Shift')],alt=True,ctrl=True)
		# Menu
		# km.new(space,'wm.call_menu','RIGHTMOUSE','PRESS',,[('name','bsmax.coordinatesmenu')],alt=True)
		# Selection
		km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','SET')])
		km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','ADD')],ctrl=True )
		km.new(space,'action.select_box','EVT_TWEAK_L','ANY',[('mode','SUB')],alt=True )
		km.new(space,'action.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'action.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		km.new(space,'action.select_all','I','PRESS',[('action','INVERT')],ctrl=True)
		km.new(space,'action.select_more','PAGE_UP','PRESS',[],ctrl=True)
		km.new(space,'action.select_less','PAGE_DOWN','PRESS',[],ctrl=True)
		km.new(space,'screen.animation_play','SLASH','PRESS',[])
		# UV Editor--------------------------------------------------------------------
		space = km.space('UV Editor','EMPTY','WINDOW')
		# Selection
		km.new(space,'bsmax.move','W','PRESS',[])
		km.new(space,'bsmax.rotate','E','PRESS',[])
		km.new(space,'bsmax.scale','R','PRESS',[])
		#create_view3d_click_celection_keymap(space)
		create_view3d_tweak_selection_keymap(km,space)
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
		#Note: multi loop command not working on uv yet
		#km.new(space,'bsmax.uvloopselect','L','PRESS',[],alt=True)
		#km.new(space,'bsmax.uvringselect','R','PRESS',[],alt=True)
		# Hide/Unhide
		km.new(space,'uv.hide','H','PRESS',[],alt=True)
		km.new(space,'uv.hide','I','PRESS',[('unselected',True)],alt=True)
		km.new(space,'uv.reveal','U','PRESS',[],alt=True)
		km.new(space,'uv.select_split','B','PRESS',[],ctrl=True)
		km.new(space,'uv.weld','W','PRESS',[],ctrl=True)
		# SEQUENCE_EDITOR--------------------------------------------------------------------
		space = km.space('Sequencer','SEQUENCE_EDITOR','WINDOW')
		km.new(space,'sequencer.batchrename','F2','PRESS',[])
		# File Browser ----------------------------------------------------------------
		space = km.space('File Browser','FILE_BROWSER','WINDOW')
		km.new(space,'filebrowser.scaleicons','WHEELUPMOUSE','PRESS',[('up',True)],ctrl=True)
		km.new(space,'filebrowser.scaleicons','WHEELDOWNMOUSE','PRESS',[('up',False)],ctrl=True)
		km.new(space,'file.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
		km.new(space,'file.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)
		# Knife Tool Modal Map --------------------------------------------------------
		#space = km.space('Knife Tool Modal Map','EMPTY','WINDOW',modal=True)
		#km.new(space,'CONFIRM','RIGHTMOUSE','PRESS',[],any=True)
		#------------------------------------------------------------------------------

keymaps = KeyMaps()

def register_max():
	create_keymaps(keymaps)
	collect_mute_keymaps(keymaps)
	keymaps.register()

def unregister_max():
	keymaps.unregister()