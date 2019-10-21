import bpy, rna_keymap_ui

KeyMaps = []

# https://www.autodesk.com/shortcuts/maya
#TODO
# push D edit pivot
# hold D edit pivot
# Timeline
# [] Undo rido only camera

def create_maya_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon

	if kcfg:
		# Window ---------------------------------------------------------------
		km = kcfg.keymaps.new(name ='Window', space_type ='EMPTY')

		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')

		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))

		# Navigation
		#kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS", alt = True)
		#KeyMaps.append((km, kmi))
		#kmi = km.keymap_items.new("view3d.rotate", "LEFTMOUSE", "PRESS", alt = True)
		#KeyMaps.append((km, kmi))
		#kmi = km.keymap_items.new("view3d.zoom", "RIGHTMOUSE", "PRESS", alt = True)
		#KeyMaps.append((km, kmi))

		# selection
		kmi = km.keymap_items.new("view3d.select", "LEFTMOUSE", "CLICK")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.select", "LEFTMOUSE", "CLICK", ctrl = True)
		kmi.properties.extend = True
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.select", "LEFTMOUSE", "CLICK", alt = True)
		kmi.properties.deselect = True
		KeyMaps.append((km, kmi))

		# Set tools
		kmi = km.keymap_items.new("wm.tool_set_by_id", "Q", "PRESS")
		kmi.properties.name = "builtin.select_box"
		kmi.properties.cycle = True
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id", "W", "PRESS")
		kmi.properties.name = "builtin.move"
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id", "E", "PRESS")
		kmi.properties.name = "builtin.rotate"
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("wm.tool_set_by_id", "R", "PRESS")
		kmi.properties.name = "builtin.scale"
		kmi.properties.cycle = True
		KeyMaps.append((km, kmi))

		# Undo/Rido
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Tools From Maya
		kmi = km.keymap_items.new("view3d.view_selected", "F", "PRESS")
		kmi.properties.use_all_regions = False
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.view_all", "A", "PRESS")
		kmi.properties.use_all_regions = False
		kmi.properties.center = False
		KeyMaps.append((km, kmi))

		# Object Non-modal --------------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Object Non-modal', space_type = 'EMPTY', region_type = 'WINDOW')

		kmi = km.keymap_items.new("bsmax.mode_set", 'TAB', "PRESS")
		KeyMaps.append((km, kmi))

		# Object Mode ----------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Object Mode', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Hide/Unhide
		kmi = km.keymap_items.new("object.hide_view_set", "H", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("object.hide_view_set", "H", "PRESS", alt = True)
		kmi.properties.unselected = True
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("object.hide_view_clear", "H", "PRESS", ctrl = True, shift = True)
		KeyMaps.append((km, kmi))

		# SetKey
		kmi = km.keymap_items.new("object.hide_view_clear", "S", "PRESS")
		KeyMaps.append((km, kmi))
		# kmi = km.keymap_items.new("anim.keyframe_insert_menu", "W", "PRESS", shift = True)
		# kmi.properties.type = 'Location'
		# KeyMaps.append((km, kmi))
		# kmi = km.keymap_items.new("anim.keyframe_insert_menu", "E", "PRESS", shift = True)
		# kmi.properties.type = 'Rotation'
		# KeyMaps.append((km, kmi))
		# kmi = km.keymap_items.new("anim.keyframe_insert_menu", "R", "PRESS", shift = True)
		# kmi.properties.type = 'Scaling'
		# KeyMaps.append((km, kmi))

		# Pivot tools
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("object.modifypivotpoint", "INSERT", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("wm.call_menu", "INSERT", "PRESS", ctrl = True)
		kmi.properties.name = "BSMAX_MT_SetPivotPoint"
		KeyMaps.append((km, kmi))

		# Mesh -----------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Mesh', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Curve ----------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Curve', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Armature -------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Armature', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Metaball -------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Metaball', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Lattice --------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Lattice', space_type = 'EMPTY')

		# Global
		kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

		# Font -----------------------------------------------------------------

		# Pose -----------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Pose', space_type = 'EMPTY')

		# GRAPH_EDITOR ----------------------------------------------------------------

		# DOPESHEET_EDITOR (Timeline)--------------------------------------------------
		km = kcfg.keymaps.new(name = "Dopesheet", space_type = "DOPESHEET_EDITOR")

		# Screen ----------------------------------------------------------------------
		km = kcfg.keymaps.new(name = 'Screen', space_type = 'EMPTY')

		kmi = km.keymap_items.new("screen.repeat_last", "G", "PRESS")
		KeyMaps.append((km, kmi))

		"""
		kmi = km.keymap_items.new("render.render", "F9", "PRESS")
		kmi.properties.use_viewport = True
		BsMax_KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("render.render", "Q", "PRESS", shift = True)
		kmi.properties.use_viewport = True
		kmi.properties.animation = True
		BsMax_KeyMaps.append((km, kmi))
		"""
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.undo", "Z", "PRESS", ctrl = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("ed.redo", "Z", "PRESS", shift = True)
		KeyMaps.append((km, kmi))

def remove_maya_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def maya_keys(register):
	if register:
		remove_maya_keymaps()
		create_maya_keymaps()
	else:
		remove_maya_keymaps()

if __name__ == '__main__':
	maya_keys(True)

__all__=["maya_keys"]


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

Display Settings ------------------------------------------
0 	Default quality display setting
1 	Rough quality display setting
2 	Medium quality display setting
3 	Smooth quality display setting
4 	Wireframe
5 	Shaded display
6 	Shaded and Textured display
7 	Use All Lights

Displaying Objects (Show, Hide)----------------------------
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
, 	Go to Previous key
Alt + , 	Move backward one frame in time
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
Shift + J 	Move, Rotate, Scale Tool relative snapping (press and release)
J 	Move, Rotate, Scale Tool snapping (press and release)
C 	Snap to curves (press and release)
X 	Snap to grids (press and release)
V 	Snap to points (press and release)


Tool Operations --------------------------------
Return 	Complete current tool
- 	Decrease manipulator size
Insert 	Enter tool Edit mode
=, + 	Increase manipulator size
W 	Move Tool, or with left mouse button for Move Tool marking menu
J 	Move, Rotate, Scale Tool Snapping (press and release)
E 	Rotate Tool, or with left mouse button for Rotate Tool marking menu
R 	Scale Tool, or with left mouse button for Scale Tool marking menu
Shift + Q 	Select Tool, or with left mouse button for Component marking menu
Alt + Q 	Select Tool, or with left mouse button for Polygon marking menu
Q 	Select Tool, or with left mouse button for Selection Mask marking menu
Y 	Selects the last used tool that is not one of Select, Move, Rotate, or Scale
T 	Show manipulator tool
Ctrl + T 	Show universal manipulator tool
Insert 	Switches between move pivot and move object (Move Tool)
D 	With left mouse button move pivot (Move Tool)

Tumble, Track or Dolly ---------------------------------
Alt + Right mouse button 	Dolly Tool (press and release)
Alt + Middle mouse button 	Track Tool (press and release)
Alt + Left mouse button 	Tumble Tool (press and release)

Window and View Operations ------------------------
Space 	(When tapped) Switch between the active window in multi-pane display and single pane display
Alt + Ctrl + Middle mouse button 	Fast pan in the Outliner
A 	Frame All in active panel, or with left mouse button for History Operations marking menu
Shift + A 	Frame All in all views
F 	Frame Selected in active panel
Shift + F 	Frame Selected in all views
F1 	Maya Help
Alt + Middle mouse button 	Pan in the Attribute Editor
Alt + Middle mouse button 	Pan in the Outliner
] 	Redo view change
Alt + B 	Switch between a gradient, black, dark gray, or light gray background color
Ctrl + Space 	Switch between the standard view and full-screen view of the current panels
Ctrl + A 	Switches between Attribute Editor or Channel Box–displays the Attribute Editor if neither is shown
[ 	Undo view change
Shift + } 	View next layout
Shift + { 	View previous layout

## Pane Specific Commands ##
Graph Editor ------------------------

1 	Absolute View
A 	Frame All
T 	Frame Center View
G 	Frame Playback Range
F 	Frame Selected
H 	Lock Channel
3 	Normalized View
2 	Stacked View
D 	Tangents Auto
M 	Toggle Curve Selection
J 	Unlock Channel

HyperGraph Panel-------------------
Alt + T 	Decrease Depth
Alt + G 	Increase Depth

Hypershade ------------------------
> 	Graph Downstream
Ctrl + . 	Graph Remove Downstream
Ctrl + L 	Graph Remove Selected
Ctrl + / 	Graph Remove Unselected
Ctrl + , 	Graph Remove Upstream
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
, 	Select Up Stream
3 	Show All Attrs
2 	Show Connected Attrs
4 	Show Custom Attrs
! 	Solo Last Output
@ 	Solo Material
5 	Toggle Node Title Mode
= 	Toggle Zoom In
- 	Toggle Zoom Out

Node Editor ------------------------
Up Arrow 	Back to Parent
Enter 	Dive Into Compound
> 	Graph Downstream
Ctrl + . 	Graph Remove Downstream
Ctrl + L 	Graph Remove Selected
Ctrl + , 	Graph Remove Upsream
? 	Graph Up Downstream
< 	Graph Upstream
X 	Grid Toggle Snap
1 	Hide Attributes
Down Arrow 	Pick Walk Down
Left Arrow 	Pick Walk Left
Right Arrow 	Pick Walk Right
Up Arrow 	Pick Walk Up
Ctrl + / 	Remove Unselected
/ 	Select Connected
. 	Select Down Stream
3 	Show All Attrs
2 	Show Connected Attrs
4 	Show Custom Attrs
S 	Toggle Attr Filter
P 	Toggle Node Selected Pins
V 	Toggle Node Swatch Size
5 	Toggle Node Title Mode
C 	Toggle Synced Selection
= 	Toggle Zoom In
- 	Toggle Zoom Out
, 	Up Stream

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