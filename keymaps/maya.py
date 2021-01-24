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

# https://www.autodesk.com/shortcuts/maya
# TODO
# push D edit pivot
# hold D edit pivot
# Timeline
# [] Undo rido only camera

def add_search(km,space):
	if bpy.app.version[1] < 90:
		km.new(space,'wm.search_menu','X','PRESS',[])
	else:
		km.new(space,'wm.search_menu','X','PRESS',[],ctrl=True,shift=True,alt=True)
		km.new(space,'wm.search_operator','X','PRESS',[])

def add_undo(km,space):
	km.new(space,"ed.undo","Z","PRESS",[])
	km.new(space,"ed.undo","Z","PRESS",[],ctrl=True)
	km.new(space,"ed.redo","Z","PRESS",[],shift=True)

#--------------------------------------------------------------------------------------#

def window(km):
	space = km.space('Window','EMPTY','WINDOW')
	add_search(km,space)

def screen(km):
	space = km.space('Screen','EMPTY','WINDOW')
	add_undo(km,space)
	km.new(space,"screen.repeat_last","G","PRESS",[])
	# km.new(space,"render.render","F9","PRESS",[('use_viewport',True)])
	# km.new(space,"render.render","Q","PRESS",[('use_viewport',True),('animation',True)],shift=True)

def view2d(km):
	pass

def view2d_navigation(km,preferences):
	pass

def view3d(km):
	space = km.space( '3D View','VIEW_3D','WINDOW')
	add_search(km,space)
	add_undo(km,space)

	km.new(space,"view3d.select","LEFTMOUSE","CLICK",[])
	km.new(space,"view3d.select","LEFTMOUSE","CLICK",[('extend',True)],ctrl=True)
	km.new(space,"view3d.select","LEFTMOUSE","CLICK",[('deselect',True)],alt=True)
	km.new(space,"wm.tool_set_by_id","Q","PRESS",[('name',"builtin.select_box"),('cycle',True)])
	km.new(space,"wm.tool_set_by_id","W","PRESS",[('name',"builtin.move")])
	km.new(space,"wm.tool_set_by_id","E","PRESS",[('name',"builtin.rotate")])
	km.new(space,"wm.tool_set_by_id","R","PRESS",[('name',"builtin.scale"),('cycle',True)])
	km.new(space,"view3d.view_selected","F","PRESS",[('use_all_regions',False)])
	km.new(space,"view3d.view_all","A","PRESS",[('use_all_regions',False),('center',False)])

	# Display Settings ------------------------------------------
	# 0 	Default quality display setting
	# 1 	Rough quality display setting
	# 2 	Medium quality display setting
	# 3 	Smooth quality display setting
	# 4 	Wireframe
	# 5 	Shaded display
	# 6 	Shaded and Textured display
	# 7 	Use All Lights

def view3d_navigation(km,preferences):
	space = km.space('3D View','VIEW_3D','WINDOW')
	if preferences.view_undo:
		km.new(space,"view3d.movecover","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotatecover","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoomcover","RIGHTMOUSE","PRESS",[],alt=True)
	else:
		km.new(space,"view3d.move","MIDDLEMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.rotate","LEFTMOUSE","PRESS",[],alt=True)
		km.new(space,"view3d.zoom","RIGHTMOUSE","PRESS",[],alt=True)

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
	space = km.space( 'Object Non-modal','EMPTY','WINDOW')
	km.new(space,"bsmax.mode_set",'TAB',"PRESS",[])

	space = km.space( 'Object Mode','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)
	km.new(space,"object.hide_view_set","H","PRESS",[],ctrl=True)
	km.new(space,"object.hide_view_set","H","PRESS",[('unselected',True)],alt=True)
	km.new(space,"object.hide_view_clear","H","PRESS",[],ctrl=True,shift=True)
	km.new(space,"object.hide_view_clear","S","PRESS",[])
	# km.new(space,"anim.keyframe_insert_menu","W","PRESS",[('type','Location')],shift=True)
	# km.new(space,"anim.keyframe_insert_menu","E","PRESS",[('type','Rotation')],shift=True)
	# km.new(space,"anim.keyframe_insert_menu","R","PRESS",[('type','Scaling')],shift=True)
	km.new(space,"object.modify_pivotpoint","INSERT","PRESS",[])
	km.new(space,"wm.call_menu","INSERT","PRESS",[('name',"BSMAX_MT_SetPivotPoint")],ctrl=True)

def mesh(km):
	space = km.space('Mesh','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)

def curve(km):
	space = km.space('Curve','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)

def armature(km):
	space = km.space('Armature','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)

def metaball(km):
	space = km.space('Metaball','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)

def lattice(km):
	space = km.space('Lattice','EMPTY','WINDOW')
	add_search(km,space)
	add_undo(km,space)

def grease_pencil(km):
	pass

def pos(km):
	# space = km.space('Pose','EMPTY','WINDOW')
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
	# Node Editor ------------------------
	# Up Arrow 	Back to Parent
	# Enter 	Dive Into Compound
	# > 	Graph Downstream
	# Ctrl + . 	Graph Remove Downstream
	# Ctrl + L 	Graph Remove Selected
	# Ctrl + ,	Graph Remove Upsream
	# ? 	Graph Up Downstream
	# < 	Graph Upstream
	# X 	Grid Toggle Snap
	# 1 	Hide Attributes
	# Down Arrow 	Pick Walk Down
	# Left Arrow 	Pick Walk Left
	# Right Arrow 	Pick Walk Right
	# Up Arrow 	Pick Walk Up
	# Ctrl + / 	Remove Unselected
	# / 	Select Connected
	# . 	Select Down Stream
	# 3 	Show All Attrs
	# 2 	Show Connected Attrs
	# 4 	Show Custom Attrs
	# S 	Toggle Attr Filter
	# P 	Toggle Node Selected Pins
	# V 	Toggle Node Swatch Size
	# 5 	Toggle Node Title Mode
	# C 	Toggle Synced Selection
	# = 	Toggle Zoom In
	# - 	Toggle Zoom Out
	# ,	Up Stream

def graph_editor(km):
	# space = km.space("Dopesheet","DOPESHEET_EDITOR,'WINDOW'")
	# Graph Editor ------------------------
	# 1 	Absolute View
	# A 	Frame All
	# T 	Frame Center View
	# G 	Frame Playback Range
	# F 	Frame Selected
	# H 	Lock Channel
	# 3 	Normalized View
	# 2 	Stacked View
	# D 	Tangents Auto
	# M 	Toggle Curve Selection
	# J 	Unlock Channel
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
km_float_menu = KeyMaps()

def register_maya(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.navigation_3d == "Maya":
			view3d_navigation(km_navigation_3d,preferences)
			km_navigation_3d.register()
			bpy.context.preferences.inputs.view_zoom_axis = 'HORIZONTAL'
		else:
			km_navigation_3d.unregister()

		if preferences.navigation_2d == "Maya":
			view2d_navigation(km_navigation_2d,preferences)
			km_navigation_2d.register()
		else:
			km_navigation_2d.unregister()

		if preferences.viowport == "Maya":
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

		if preferences.sculpt == "Maya":
			vertex_paint(km_sculpt)
			weight_paint(km_sculpt)
			image_paint(km_sculpt)
			sculpt(km_sculpt)
			km_sculpt.register()
		else:
			km_sculpt.unregister()

		if preferences.uv_editor == "Maya":
			uv_editor(km_uv_editor)
			km_uv_editor.register()
		else:
			km_uv_editor.unregister()

		if preferences.node_editor == "Maya":
			node_editor(km_node_editor)
			km_node_editor.register()
		else:
			km_node_editor.unregister()

		if preferences.graph_editor == "Maya":
			graph_editor(km_graph_editor)
			dopesheet_editor(km_graph_editor)
			nla_editor(km_graph_editor)
			km_uv_editor.register()
		else:
			km_graph_editor.unregister()
			
		if preferences.clip_editor == "Maya":
			km_clip_editor.register()
		else:
			km_clip_editor.unregister()

		if preferences.video_sequencer == "Maya":
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

		if preferences.text_editor == "Maya":
			# console(km_text_editor)
			text(km_text_editor)
			km_text_editor.register()
		else:
			km_text_editor.unregister()
		
		if preferences.file_browser == "Maya":
			file_browser(km_file_browser)
			km_file_browser.register()
		else:
			km_file_browser.unregister()

def unregister_maya():
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

"""
2D Pan/Zoom
#\\ + Middle mouse button 	2D Pan tool
#\\ + Right mouse button 	2D Zoom tool
#\\ Enable/disable 2D Pan/Zoom

Animation Operations --------------------------------------
I 	Insert Keys Tool (for Graph Editor) (press and release)
S 	Set Key
Shift + E 	Set key for Rotate
Shift + R 	Set key for Scale
Shift + W 	Set key for Translate
Alt + J 	Toggle Multicolor Feedback
Shift + S 	With left mouse button for Keyframe marking menu



Displaying Objects (Show,Hide)----------------------------
Ctrl + H 	Hide > Hide Selection
Alt + H 	Hide > Hide Unselected Objects
Shift + l 	Isolate Select > View Selected (in the panel menus)
Ctrl + Shift + H 	Show > Show Last Hidden
Shift + H 	Show > Show Selection

Edit Operations -----------------------------------------
Ctrl (or Cmd) + C 	Copy
Ctrl (or Cmd) + X 	Cut
Ctrl + D 	Duplicate
Ctrl + Shift + D 	Duplicate Special
Shift + D 	Duplicate with Transform
Ctrl + G 	Group
P 	Parent
Ctrl (or Cmd) + V 	Paste
Shift + Z 	Redo
G 	Repeat
Shift + G 	Repeat command at mouse position
Z 	Undo (also Ctrl+z/+z)
Shift + P 	Unparent
Ctrl + R 	Create file reference
Ctrl + Q 	Exit
Ctrl + N 	New Scene
Ctrl + O 	Open Scene
Ctrl + S 	Save Scene
Ctrl + Shift + S 	Save Scene As

Hotbox Display -------------------------------------------------
Space 	(When pressed down) Show the hotbox

Modeling Operations ---------------------------------------------
2 	Cage + smooth polygon mesh display
Ctrl + F10 	Convert polygon selection to Edges
Ctrl + F9 	Convert polygon selection to Vertices
Ctrl + F11 	Covert polygon selection to Faces
Ctrl + F12 	Covert polygon selection to UVs
Page Down 	Decreases Division Levels for Smooth Mesh Preview or Subdiv Proxy
1 	Default polygon mesh display (no smoothing)
~ 	Displays both the original (proxy) and the smoothed mesh
Page Up 	Increases Division Levels for Smooth Mesh Preview or Subdiv Proxy
l 	Lock/unlock length of curve (press and hold)
3 	Smooth polygon mesh display


Moving Selected Objects --------------------------------------
Alt + Down 	Move down one pixel
Alt + Left 	Move left one pixel
Alt + Right 	Move right one pixel
Alt + Up 	Move up one pixel


Painting Operations -----------------------------------------
Ctrl + B 	Edit Paint Effects template brush settings
Alt + F 	Flood with the current value
Shift + B 	Modify lower brush radius (press and release)
M 	Modify maximum displacement (Sculpt Surfaces and Sculpt Polygons Tool)
N 	Modify paint value
B 	Modify upper brush radius (press and release)
O + Left mouse button 	Poly Brush Tool marking menu
O + Middle mouse button 	Poly UV Tool marking menu
/ 	Switch to pick color mode (press and release)
Alt + R 	Toggle Reflection on or off
Alt + C 	Turn Color Feedback on or off
Alt + A 	Turn Show Wireframe on or off
U 	With left mouse button for Artisan Paint Operation marking menu

Pick Walk* --------------------------------------------
Down 	Walk down current
Left 	Walk left in current
Right 	Walk right in current
Up 	Walk up current


Playback Control ----------------------------------------
Alt+Shift + V 	Go to Min Frame
. 	Go to Next key
,	Go to Previous key
Alt + ,	Move backward one frame in time
Alt + . 	Move forward one frame in time
Alt + V 	Turn Playback on or off
K + Middle mouse button 	Virtual Time Slider mode (press and hold and scrub timeline)

Rendering -------------------------------------------
Ctrl + Left 	Render view next image
Ctrl + Right 	Render view previous image

Selecting Menus ------------------------------------
F2 	Show Animation menu set
F5 	Show Dynamics menu set
F4 	Show Modeling menu set
F3 	Show Polygons menu set
F6 	Show Rendering menu set
Ctrl + M 	Show/hide main menu bar
Shift + M 	Show/hide panel menu bar
Ctrl + Shift + M 	Show/hide panel toolbar


Selecting Objects and Components -----------------------------------
F10 	Edge
F11 	Face
> 	Grow polygon selection region
F8 	Object/Component (Switch between object and component editing)
Ctrl + I 	Select next intermediate object
< 	Shrink polygon selection region
F12 	UV
F9 	Vertex
Alt + F9 	Vertex Face


Snapping Operations ----------------------------------------
Shift + J 	Move,Rotate,Scale Tool relative snapping (press and release)
J 	Move,Rotate,Scale Tool snapping (press and release)
C 	Snap to curves (press and release)
X 	Snap to grids (press and release)
V 	Snap to points (press and release)


Tool Operations --------------------------------
Return 	Complete current tool
- 	Decrease manipulator size
Insert 	Enter tool Edit mode
=,+ 	Increase manipulator size
W 	Move Tool,or with left mouse button for Move Tool marking menu
J 	Move,Rotate,Scale Tool Snapping (press and release)
E 	Rotate Tool,or with left mouse button for Rotate Tool marking menu
R 	Scale Tool,or with left mouse button for Scale Tool marking menu
Shift + Q 	Select Tool,or with left mouse button for Component marking menu
Alt + Q 	Select Tool,or with left mouse button for Polygon marking menu
Q 	Select Tool,or with left mouse button for Selection Mask marking menu
Y 	Selects the last used tool that is not one of Select,Move,Rotate,or Scale
T 	Show manipulator tool
Ctrl + T 	Show universal manipulator tool
Insert 	Switches between move pivot and move object (Move Tool)
D 	With left mouse button move pivot (Move Tool)

Tumble,Track or Dolly ---------------------------------
Alt + Right mouse button 	Dolly Tool (press and release)
Alt + Middle mouse button 	Track Tool (press and release)
Alt + Left mouse button 	Tumble Tool (press and release)

Window and View Operations ------------------------
Space 	(When tapped) Switch between the active window in multi-pane display and single pane display
Alt + Ctrl + Middle mouse button 	Fast pan in the Outliner
A 	Frame All in active panel,or with left mouse button for History Operations marking menu
Shift + A 	Frame All in all views
F 	Frame Selected in active panel
Shift + F 	Frame Selected in all views
F1 	Maya Help
Alt + Middle mouse button 	Pan in the Attribute Editor
Alt + Middle mouse button 	Pan in the Outliner
] 	Redo view change
Alt + B 	Switch between a gradient,black,dark gray,or light gray background color
Ctrl + Space 	Switch between the standard view and full-screen view of the current panels
Ctrl + A 	Switches between Attribute Editor or Channel Box–displays the Attribute Editor if neither is shown
[ 	Undo view change
Shift + } 	View next layout
Shift + { 	View previous layout

## Pane Specific Commands ##


HyperGraph Panel-------------------
Alt + T 	Decrease Depth
Alt + G 	Increase Depth

Hypershade ------------------------
> 	Graph Downstream
Ctrl + . 	Graph Remove Downstream
Ctrl + L 	Graph Remove Selected
Ctrl + / 	Graph Remove Unselected
Ctrl + ,	Graph Remove Upstream
? 	Graph Up Downstream
< 	Graph Upstream
1 	Hypdershade Hide Attributes
Down Arrow 	Pick Walk Down
Left Arrow 	Pick Walk Left
Right Arrow 	Pick Walk Right
Up Arrow 	Pick Walk Up
P 	Pin Selected
# 	Remove Material Soloing
/ 	Select Connected
. 	Select Down Stream
,	Select Up Stream
3 	Show All Attrs
2 	Show Connected Attrs
4 	Show Custom Attrs
! 	Solo Last Output
@ 	Solo Material
5 	Toggle Node Title Mode
= 	Toggle Zoom In
- 	Toggle Zoom Out



Outliner -------------------------------
Enter 	Rename Selected Item
F 	Reveal Selected

Pose Editor ----------------------------
Ctrl + G 	Pose Interpolator New Group

Profiler -------------------------------
1 	Category View
2 	CPU View
3 	Thread View
Ctrl + R 	Toggle Recording

Shape Editor ---------------------------
Ctrl + D 	Duplicate Target
Ctrl + G 	New Group
Alt + D 	Select None

Time Editor ----------------------------
L 	Additive Layer
Y 	Clip Hold Toggle
T 	Clip Loop Toggle
W 	Clip Razor
Shift + H 	Clip Scale End
Shift + G 	Clip Scale Start
R 	Clip Scale Toggle
H 	Clip Trim End
G 	Clip Trim Start
E 	Clip Trim Toggle
Shift + I 	Create Audio Clip
O 	Create Clip
Ctrl + G 	Create Group From Selection
Shift + L 	Create Override Layer
P 	Create Pose Clip
Ctrl + X 	Cut Clips
Ctrl + Shift + G 	Explode Group
Ctrl + E 	Export Selection
A 	Frame All
F 	Frame Selected
B 	Ghost Track Toggle
I 	Import Animation
U 	Ripple Edit Toggle Press
U 	Ripple Edit Toggle Release
Q 	Scene Authoring Toggle
S 	Set Key
D 	Set Zero Key
M 	Toggle Mute Selected Tracks
X 	Toggle Snap to Clip Press
X 	Toggle Snap to Clip Release
N 	Toggle Solo Selected Tracks
K 	Toggle Time Cursor Press
K 	Toggle Time Cursor Release

"""