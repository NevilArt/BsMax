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
from .commands import * # all "c0000" are from here
from .q_items import QuadItem
from bsmax.state import is_active_primitive, get_active_type

# Indexes
# [3] [2]
#    +
# [4] [1]
##########
t,f,n = True,False,None

def seprator():
	return QuadItem(n,f,f,n,n,n)

def get_view3d_transform_convert_to_sub(ctx): #Submenu
	items = []
	#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Convert Curve To Mesh",f,t,n,c0001,n))
	items.append(QuadItem("Convert Mesh To Curve",f,t,n,c0002,n))
	# NOTE Sub menus do not return text and index
	return items

def get_view3d_transform(ctx):
	items = []
	#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Move",f,t,n,c0003,c0004))
	items.append(QuadItem("Rotate",f,t,n,c0005,c0006))
	items.append(QuadItem("Scale", f,t,n,c0007,c0008))
	items.append(QuadItem("Placment",f,t,n,c0172,n))
	items.append(QuadItem("Cursor",f,t,n,c0109,n))
	items.append(seprator())
	items.append(QuadItem("Select",f,t,n,c0009,n))
	items.append(QuadItem("Select Similar",f,t,n,c0010,n))
	items.append(QuadItem("Select Instance",f,t,n,c0001,n))
	items.append(seprator())
	items.append(QuadItem("Clone",f,(len(ctx.selected_objects) > 0),n,c0011,n))
	items.append(QuadItem("Align Objects...",f,(len(ctx.selected_objects) > 0),n,c0144,n))
	items.append(seprator())
	items.append(QuadItem("Object Properties...",f,t,n,c0166,n))
	items.append(seprator())
	items.append(QuadItem("Curve Editor...",f,t,n,c0167,n))
	items.append(QuadItem("Dope sheet...",f,t,n,c0168,n))
	items.append(QuadItem("Driver Editor...",f,t,n,c0170,n))
	items.append(QuadItem("NLA Editor...",f,t,n,c0169,n))
	items.append(QuadItem("Text Editor...",f,t,n,c0171,n))
	items.append(QuadItem(n,f,f,n,n,n))
	submenu = get_view3d_transform_convert_to_sub(ctx)
	items.append(QuadItem("Conver to",f,f,submenu,n,n))
	return "Transform",items,1

def get_view3d_lighting_sub(ctx):
	items = []
	#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Wire Frame",f,t,n,c0176,n))
	items.append(QuadItem("Solid",f,t,n,c0177,n))
	items.append(QuadItem("Material",f,t,n,c0178,n))
	items.append(QuadItem("Rendered",f,t,n,c0179,n))
	items.append(seprator())
	uslr = ctx.space_data.shading.use_scene_lights_render
	items.append(QuadItem("Use Scene Light",uslr,t,n,c0192,n))
	uswr = ctx.space_data.shading.use_scene_world_render
	items.append(QuadItem("Use World Light",uswr,t,n,c0193,n))
	items.append(seprator())
	items.append(QuadItem("Combined (Default)",f,t,n,c0180,n))
	items.append(QuadItem("Emission",f,t,n,c0181,n))
	items.append(QuadItem("Environment",f,t,n,c0182,n))
	items.append(QuadItem("Shadow",f,t,n,c0183,n))
	items.append(seprator())
	items.append(QuadItem("Diffuse Light",f,t,n,c0184,n))
	items.append(QuadItem("Diffuse Color",f,t,n,c0185,n))
	items.append(QuadItem("Specular Light",f,t,n,c0186,n))
	items.append(QuadItem("Specular Color",f,t,n,c0187,n))
	items.append(QuadItem("Volum Transmittance",f,t,n,c0188,n))
	items.append(QuadItem("Volum Scatter",f,t,n,c0189,n))
	items.append(seprator())
	items.append(QuadItem("Normal",f,t,n,c0190,n))
	items.append(QuadItem("Mist",f,t,n,c0191,n))
	return items

def get_view3d_display(ctx):
	items = []
				#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Manage State Sets...",f,f,n,"",n))
	items.append(QuadItem("State Sets",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Hide Selection",f,t,n,c0012,n))
	items.append(QuadItem("Hide Unselected",f,t,n,c0013,n))
	items.append(QuadItem("Unhide All",f,t,n,c0014,n))
	items.append(QuadItem("Unhide by Name",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Freeze Selection",f,t,n,c0015,n))
	items.append(QuadItem("Unfreeze All",f,t,n,c0016,n))
	items.append(seprator())
	items.append(QuadItem("Isolate Toggle",f,t,n,c0017,n))
	items.append(seprator())
	submenu = get_view3d_lighting_sub(ctx)
	items.append(QuadItem("Viewport Lighting",f,t,submenu,n,n))
	return "Display",items,2

def get_view3d_tool1(ctx):
	items = []
	V,E,F = ctx.tool_settings.mesh_select_mode
	if ctx.mode == 'OBJECT':
		V,E,F = False,False,False
	if get_active_type(ctx) == 'MESH':
		if not is_active_primitive(ctx):
			#  text, check, enabled,menu,action,setting
			items.append(QuadItem("Top-level",(ctx.mode=='OBJECT'),t,n,c0018,n))
			items.append(QuadItem("Vertex",V,t,n,c0019,n))
			items.append(QuadItem("Edge",E,t,n,c0020,n))
			items.append(QuadItem("Border",f,t,n,c0021,n))
			items.append(QuadItem("Polygon",F,t,n,c0022,n))
			items.append(QuadItem("Element",f,t,n,c0023,n))
			items.append(seprator())
			items.append(QuadItem("Repeat",f,t,n,c0024,n))
			IsEditMode = (ctx.mode=="EDIT_MESH")
			items.append(seprator())
			items.append(QuadItem("Quickslice",f,IsEditMode,n,c0025,n))
			items.append(QuadItem("Cut",f,IsEditMode,n,c0026,n))
			items.append(seprator())
			items.append(QuadItem("Attach",f,t,n,c0098,c0099))
			items.append(QuadItem("Collaps",f,IsEditMode,n,c0027,n))
			items.append(QuadItem("Hide Unselected",f,IsEditMode,n,c0028,n))
			items.append(seprator())
			items.append(QuadItem("Ignore Backfacing",f,t,n,c0029,n))
			items.append(QuadItem("NURMS Toggle",f,f,n,"",n))
	elif get_active_type(ctx) == 'CURVE':
		items.append(QuadItem("Extrude",f,t,n,c0134,n))
		if not is_active_primitive(ctx):
			items.append(seprator())
			items.append(QuadItem("Top-level",(ctx.mode=='OBJECT'),t,n,c0018,n))
			items.append(QuadItem("Vertex",f,t,n,c0019,n))
			items.append(QuadItem("Segment",f,f,n,c0020,n))
			items.append(QuadItem("Spline",f,f,n,c0021,n))
			if ctx.mode == 'EDIT_CURVE':
				items.append(seprator())
				items.append(QuadItem("Reset Tangents",f,f,n,"",n))
				items.append(QuadItem("Smooth",f,t,n,c0030,n))
				items.append(QuadItem("Corner",f,t,n,c0031,n))
				items.append(QuadItem("Bezier",f,t,n,c0032,n))
				items.append(QuadItem("Bezier Corner",f,t,n,c0033,n))
				items.append(seprator())
				items.append(QuadItem("Unbined",f,f,n,"",n))
				items.append(QuadItem("Bined",f,f,n,"",n))
				items.append(seprator())
				items.append(QuadItem("Divide",f,t,n,c0034,c0159))
				items.append(seprator())
				items.append(QuadItem("Make First",f,t,n,c0161,n))
				items.append(QuadItem("Revarse Spline",f,t,n,c0160,n))
	if get_active_type(ctx) == 'ARMATURE':
		items.append(QuadItem("Octahedral",f,t,n,c0150,n))
		items.append(QuadItem("Stick",f,t,n,c0151,n))
		items.append(QuadItem("BndiBone",f,t,n,c0152,n))
		items.append(QuadItem("Envelope",f,t,n,c0153,n))
		items.append(QuadItem("Wire",f,t,n,c0154,n))
		if ctx.mode == 'EDIT_ARMATURE':
			pass
		elif ctx.mode == 'POSE':
			pass
	return "Tool1",items,3

def get_view3d_tool2(ctx):
	items = []
	if ctx.mode == 'OBJECT':
		items.append(QuadItem("Link To",f,t,n,c0173,n))
		items.append(QuadItem("Unlink Selection",f,t,n,c0174,n))
		items.append(seprator())
		dac = ctx.scene.tool_settings.use_transform_skip_children
		items.append(QuadItem("Don`t Affect Children",dac,t,n,c0175,n))
		
	if get_active_type(ctx) == 'MESH':
		V,E,F = ctx.tool_settings.mesh_select_mode
		if ctx.mode == "EDIT_MESH" and not is_active_primitive(ctx):
			#  text, check, enabled,menu,action,setting
			items.append(QuadItem("Create",f,t,n,c0035,n))
			items.append(seprator())
			if V:
				items.append(QuadItem("Remove",f,t,n,c0036,n))
				items.append(QuadItem("Break",f,f,n,c0037,n))
				items.append(QuadItem("Connect",f,t,n,c0038,""))
				items.append(seprator())
				items.append(QuadItem("Extrude",f,t,n,c0039,""))
				items.append(QuadItem("Chamfer",f,t,n,c0040,""))
				items.append(seprator())
				items.append(QuadItem("Weld",f,t,n,c0041,c0042))
				items.append(QuadItem("Target Weld",f,t,n,c0130,n))
				items.append(seprator())
				items.append(QuadItem("Remove Isolated Vertexs",f,t,n,c0135,n))
			if E:
				items.append(QuadItem("Remove",f,t,n,c0043,n))
				items.append(QuadItem("Split",f,t,n,c0165,n))
				items.append(QuadItem("Connect",f,t,n,c0045,n))
				items.append(QuadItem("Bridge",f,t,n,c0143,n))
				items.append(seprator())
				items.append(QuadItem("Extrude",f,t,n,c0046,""))
				items.append(QuadItem("Chamfer",f,t,n,c0047,""))
				items.append(seprator())
				items.append(QuadItem("Weld",f,t,n,c0048,""))
				items.append(QuadItem("Target Weld",f,f,n,"",n))
				items.append(seprator())
				items.append(QuadItem("Edit Triangulation",f,f,n,"",n))
				items.append(QuadItem("Create Shape",f,t,n,c0049,n))
				items.append(seprator())
				items.append(QuadItem("Remove Isolated Edges",f,t,n,c0135,n))
			if F:
				items.append(QuadItem("Remove",f,t,n,c0050,n))
				items.append(QuadItem("Detach",f,t,n,c0051,n))
				items.append(QuadItem("Bridge",f,t,n,c0143,n))
				items.append(seprator())
				items.append(QuadItem("Extrude",f,t,n,c0052,""))
				items.append(QuadItem("Bevel",f,f,n,"",""))
				items.append(QuadItem("Outline",f,t,n,"",""))
				items.append(QuadItem("Inset",f,t,n,c0053,""))
				items.append(seprator())
				items.append(QuadItem("Edit Triangulation",f,f,n,"",n))
				items.append(QuadItem("Flip Normal",f,t,n,c0054,n))
				items.append(seprator())
				items.append(QuadItem("Remove Isolated Faces",f,t,n,c0135,n))
	elif get_active_type(ctx) == 'CURVE' and ctx.mode == 'EDIT_CURVE':
		items.append(QuadItem("Create Line",f,f,n,"",n))
		items.append(QuadItem("Attach",f,f,n,"",""))
		items.append(QuadItem("Detach Segment",f,f,n,"",n))
		items.append(seprator())
		items.append(QuadItem("Chamfer",f,t,n,c0055,c0145))
		items.append(QuadItem("Fillet",f,t,n,c0056,c0146))
		items.append(seprator())
		items.append(QuadItem("Connect",f,f,n,"",n))
		items.append(QuadItem("Refine Connect",f,f,n,"",n))
		items.append(seprator())
		items.append(QuadItem("Cycle Vertices",f,f,n,"",n))
		items.append(QuadItem("Break Vertices",f,f,n,"",n))
		items.append(QuadItem("Weld Vertices",f,f,n,"",n))
		items.append(QuadItem("Fuse Vertices",f,f,n,"",n))
	elif get_active_type(ctx) == 'LIGHT':
		l_type = ctx.object.data.type
		items.append(QuadItem("Point",(l_type == 'POINT'),t,n,c0057,n))
		items.append(QuadItem("Sun",(l_type == 'SUN'),t,n,c0058,n))
		items.append(QuadItem("Spot",(l_type == 'SPOT'),t,n,c0059,n))
		items.append(QuadItem("Area",(l_type == 'AREA'),t,n,c0060,n))
		items.append(seprator())
		shadow = ctx.object.data.use_shadow
		items.append(QuadItem("Shadow",shadow,t,n,c0061 + str(not shadow),n))
		items.append(seprator())
		items.append(QuadItem("Make Target Light",f,t,n,c0141,n))
		items.append(QuadItem("Make Free Light",f,t,n,c0142,n))
		items.append(seprator())
		items.append(QuadItem("Select Light Target",f,t,n,c0147,n))
	elif get_active_type(ctx) == 'CAMERA':
		items.append(QuadItem("Set View to selected Camera",f,t,n,c0133,n))
		items.append(QuadItem("Set as Active Camera",f,t,n,c0077,n))
		items.append(seprator())
		items.append(QuadItem("Make Target Camera",f,t,n,c0131,n))
		items.append(QuadItem("Make Free Camera",f,t,n,c0132,n))
		items.append(seprator())
		items.append(QuadItem("Select Camera Target",f,t,n,c0147,n))
		items.append(seprator())
		items.append(QuadItem("Lock Camera to View",ctx.space_data.lock_camera,t,n,c0162,n))
		items.append(QuadItem("Lock to 3D Cursor",ctx.space_data.lock_cursor,t,n,c0163,n))
		items.append(seprator())
		items.append(QuadItem("Lock Camera Transform",f,t,n,c0164,n))
		
	if get_active_type(ctx) == 'ARMATURE':
		if ctx.mode == 'EDIT_ARMATURE':
			items.append(QuadItem("Divide Bone",f,t,n,c0148,c0149))
		elif ctx.mode == 'POSE':
			pass
	return "Tool2",items,4

def get_view3D_create(ctx):
	items = []
	enabled = ctx.mode == 'OBJECT'
	#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Sphere",f,enabled,n,c0062,n))
	items.append(QuadItem("Box",f,enabled,n,c0063,n))
	items.append(QuadItem("Cylinder",f,enabled,n,c0064,n))
	items.append(QuadItem("Plane",f,enabled,n,c0065,n))
	items.append(seprator())
	items.append(QuadItem("Line",f,enabled,n,c0066,n))
	items.append(QuadItem("Circle",f,enabled,n,c0067,n))
	items.append(QuadItem("Rectangle",f,enabled,n,c0068,n))
	items.append(QuadItem("Arc",f,t,n,c0069,n))
	return "Primitives",items,2

def get_view3D_viewport(ctx):
	items = []
	items.append(QuadItem("Front View",f,t,n,c0070,n))
	items.append(QuadItem("Back View",f,t,n,c0071,n))
	items.append(seprator())
	items.append(QuadItem("Top View",f,t,n,c0072,n))
	items.append(QuadItem("Bottom View",f,t,n,c0073,n))
	items.append(seprator())
	items.append(QuadItem("Left View",f,t,n,c0074,n))
	items.append(QuadItem("Right View",f,t,n,c0075,n))
	items.append(seprator())
	items.append(QuadItem("Prespective/Isometric",f,t,n,c0076,n))
	items.append(QuadItem("Camera View",f,t,n,c0077,n))
	items.append(seprator())
	items.append(QuadItem("Create Camera From View",f,t,n,c0078,n))
	return "Viewports",items,1

def get_view3d_camera(ctx):
	items = []
	lock = ctx.space_data.lock_camera
	items.append(QuadItem("Lock Camera to View",lock,t,n,c0137,n))
	items.append(seprator())
	items.append(QuadItem("Select Active Camera",f,t,n,c0138,n))
	items.append(QuadItem("Select Active Cameras target ",f,t,n,c0139,n))
	items.append(QuadItem("Select Active Camera and target",f,t,n,c0140,n))
	return "Camera",items,2

def get_view3d_set(ctx):
	items = []
	items.append(QuadItem("Set Keyframe",f,t,n,c0079,n))
	items.append(QuadItem("Set Key Filter",f,t,n,c0080,n))
	items.append(seprator())
	items.append(QuadItem("Motion path",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Delete Selected Animation",f,t,n,c0081,n))
	items.append(seprator())
	items.append(QuadItem("Driver Editor...",f,f,n,"",n))
	items.append(QuadItem("Dope Sheet...",f,f,n,"",n))
	items.append(QuadItem("Curve Editor...",f,f,n,"",n))
	return "Set",items,1

def get_view3d_coordinates(ctx):
	items = []
	items.append(QuadItem("Cursor",f,t,n,c0082,n))
	# Object Mode
	if ctx.mode == 'OBJECT':
		items.append(QuadItem("Local",f,t,n,c0083,n))
		items.append(QuadItem("Normal",f,t,n,c0084,n))
	# Pose Mode
	if ctx.mode == 'POSE':
		items.append(QuadItem("Local",f,t,n,c0136,n))
	# Edit Mode
	if 'EDIT' in ctx.mode:
		items.append(QuadItem("Local",f,t,n,c0084,n))
		items.append(QuadItem("Parent",f,t,n,c0083,n))
	items.append(QuadItem("Gimbal",f,t,n,c0085,n))
	items.append(QuadItem("Screen",f,t,n,c0086,n))
	items.append(QuadItem("World",f,t,n,c0087,n))
	return "Coordinates",items,2

def get_view3d_transform2(ctx):
	items = []
	#  text, check, enabled,menu,action,setting
	items.append(QuadItem("Rotation To Zero",f,t,n,c0158,n))
	items.append(QuadItem("Transform To Zero",f,t,n,c0157,n))
	items.append(seprator())
	items.append(QuadItem("Freeze Rotation",f,t,n,c0156,n))
	items.append(QuadItem("Freeze Transform",f,t,n,c0155,n))
	return "Transform",items,3

def get_view3d_pose(ctx):
	items = []
	items.append(QuadItem("Set Perf Angles",f,f,n,"",n))
	items.append(QuadItem("Assume Perf Angles",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Set as Skin Pose",f,f,n,"",n))
	items.append(QuadItem("Assume Skin Pose",f,f,n,"",n))
	return "Pose",items,4

def get_view3d_snap_toggles(ctx):
	items = []
	tool_settings = ctx.scene.tool_settings
	snaps = tool_settings.snap_elements
	items.append(QuadItem("Gride Points",('INCREMENT' in snaps),t,n,c0088,n))
	items.append(QuadItem("Pivot",f,f,n,"",n))
	items.append(QuadItem("Vertex",('VERTEX' in snaps),t,n,c0089,n))
	items.append(QuadItem("Midpoint",('VOLUME' in snaps),t,n,c0090,n))
	items.append(QuadItem("Edge/Segment",('EDGE' in snaps),t,n,c0091,n))
	items.append(QuadItem("Face",('FACE' in snaps),t,n,c0092,n))
	items.append(seprator())
	targets = tool_settings.snap_target
	items.append(QuadItem("Closest",('CLOSEST' in targets),t,n,c0093,n))
	items.append(QuadItem("Center",('CENTER' in targets),t,n,c0094,n))
	items.append(QuadItem("Median",('MEDIAN' in targets),t,n,c0095,n))
	items.append(QuadItem("Active",('ACTIVE' in targets),t,n,c0096,n))
	items.append(seprator())
	move = tool_settings.use_snap_translate
	rotate = tool_settings.use_snap_rotate
	scale = tool_settings.use_snap_scale
	items.append(QuadItem("Move",move,t,n,c0110 + str(not move),n))
	items.append(QuadItem("Rotate",rotate,t,n,c0111 + str(not rotate),n))
	items.append(QuadItem("Scale",scale,t,n,c0112 + str(not scale),n))
	return "Snap Toggles",items,1

def get_view3d_snap_override(ctx):
	items = []
	items.append(QuadItem("Pivot to Geometry",f,t,n,c0108,n))
	items.append(QuadItem("Pivot to Center",f,t,n,c0107,n))
	items.append(QuadItem("Pivot to 3D Cursor",f,t,n,c0106,n))
	items.append(QuadItem("Pivot to Object",f,t,n,c0105,n))
	items.append(QuadItem("Object to Pivot",f,t,n,c0104,n))
	#items.append(seprator())
	#items.append(QuadItem("Last",f,f,n,"",n))
	#items.append(QuadItem("None",f,f,n,"",n))
	#items.append(seprator())
	#items.append(QuadItem("Standard",f,f,n,"",n))
	#items.append(QuadItem("Body Snaps",f,f,n,"",n))
	#items.append(QuadItem("NURBS",f,f,n,"",n))
	#items.append(QuadItem("Point Cloud Objects",f,f,n,"",n))
	return "Snap Override",items,2

def get_view3d_snap_options(ctx):
	items = []
	items.append(QuadItem("Enable Axis Constrants in Snap",f,f,n,"",n))
	items.append(QuadItem("Snap To Frozen Objects",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Gride and Snap Setting...",f,f,n,"",n))
	return "Snap Options",items,3

def get_view3d_rendering_properties(ctx):
	items = []
	scene = ctx.scene
	eevee = scene.eevee
	render = scene.render
	engine = render.engine
	# items.append(QuadItem("Renderable",f,f,n,"",n))
	# items.append(QuadItem("Inherit Visiblity",f,f,n,"",n))
	# items.append(QuadItem("Visable to Camera",f,f,n,"",n))
	# items.append(QuadItem("Visable to Reflection",f,f,n,"",n))
	# items.append(QuadItem("Cast Shadow",f,f,n,"",n))
	# items.append(QuadItem("Apply Atmospherics",f,f,n,"",n))
	# items.append(QuadItem("Render Occluded Objects",f,f,n,"",n))
	# items.append(seprator())
	# items.append(QuadItem("Motion Blur",f,f,n,"",n))
	# items.append(seprator())
	# items.append(QuadItem("Object Properties...",f,f,n,"",n))
	if engine == 'BLENDER_EEVEE':
		items.append(QuadItem("Ambient Occlusion",eevee.use_gtao,t,n,c0116,n))
		items.append(QuadItem("Bloom",eevee.use_bloom,t,n,c0117,n))
		items.append(QuadItem("Screen Space Reflection",eevee.use_ssr,t,n,c0118,n))
		items.append(QuadItem("Motion Blur",eevee.use_motion_blur,t,n,c0119,n))
		items.append(QuadItem("Simplify",render.use_simplify,t,n,c0120,n))
		items.append(QuadItem("Freesryle",render.use_freestyle,t,n,c0121,n))
	elif engine == 'BLENDER_WORKBENCH':
		pass
		#items.append(QuadItem("Backface culling",scene.shading.show_backface_culling,t,n,c0123,n))
		#items.append(QuadItem("X-Ray",scene.shading.show_xray,t,n,c0125,n))
		#items.append(QuadItem("Shadow",scene.shading.show_shadows,t,n,c0126,n))
		#items.append(QuadItem("Cavity",scene.shading.show_cavity,t,n,c0127,n))
		#items.append(QuadItem("Depth Of Field",scene.shading.use_dof,t,n,c0128,n))
		#items.append(QuadItem("Outline",scene.shading.show_object_outline,t,n,c0129,n))
		#items.append(QuadItem("Simplify",scene.render.use_simplify,t,n,c0120,n))
		#items.append(seprator())
		# scene.shading.color_type = 'MATERIAL'
		# scene.shading.color_type = 'OBJECT'
		# scene.shading.color_type = 'VERTEX'
		# scene.shading.color_type = 'SINGLE'
		# scene.shading.color_type = 'RANDOM'
		# scene.shading.color_type = 'TEXTURE'
		#items.append(seprator())
		# scene.shading.light = 'STUDIO'
		# scene.shading.light = 'MATCAP'
		# scene.shading.light = 'FLAT'
	elif engine == 'CYCLES':
		items.append(QuadItem("Hair",scene.cycles_curves.use_curves,t,n,c0122,n))
		items.append(QuadItem("Simplify",render.use_simplify,t,n,c0120,n))
		items.append(QuadItem("Motion Blur",render.use_motion_blur,t,n,c0124,n))
		items.append(QuadItem("Freesryle",render.use_freestyle,t,n,c0121,n))
	return "Rendering Properties",items,1

def get_view3d_render(ctx):
	items = []
	items.append(QuadItem("Render",f,t,n,c0097,n))
	#items.append(QuadItem("Render Animation",f,f,n,"",n))
	items.append(QuadItem("Render Setup...",f,f,n,"",n))
	items.append(QuadItem("Rendered Frame Window",f,f,n,"",n))
	items.append(seprator())
	engine = ctx.scene.render.engine
	items.append(QuadItem("Eevee",engine == 'BLENDER_EEVEE',t,n,c0113,n))
	items.append(QuadItem("Workbench",engine == 'BLENDER_WORKBENCH',t,n,c0114,n))
	items.append(QuadItem("Cycles",engine == 'CYCLES',t,n,c0115,n))
	return "Render",items,2

def get_view3d_rendering_tools(ctx):
	items = []
	items.append(QuadItem("Radiosity...",f,f,n,"",n))
	items.append(QuadItem("Light Tracer",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Exposure Control...",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Environment...",f,f,n,"",n))
	items.append(QuadItem("Effects...",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Raytracer Setting",f,f,n,"",n))
	items.append(QuadItem("Raytracer Include/Exclude...",f,f,n,"",n))
	items.append(QuadItem("Render Message Window...",f,f,n,"",n))
	return "Rendering Tools",items,3

def get_view3d_selection1(ctx):
	items = []
	items.append(QuadItem("Select Instance",f,f,n,"",n))
	items.append(QuadItem("Select Similar",f,f,n,"",n))
	items.append(seprator())
	return "Selection",items,1

def get_view3d_selection2(ctx):
	items = []
	return "Selection",items,2

def get_view3d_selection3(ctx):
	items = []
	return "Selection",items,3

def get_view3d_selection4(ctx):
	items = []
	return "Selection",items,4

def get_view3d_fx_tools(ctx):
	items = []
	items.append(QuadItem("Quick Smoke", f,t,n,c0100,n))
	items.append(QuadItem("Quick Fur",   f,t,n,c0101,n))
	items.append(QuadItem("Quick Explod",f,t,n,c0102,n))
	items.append(QuadItem("Quick Fluid", f,t,n,c0103,n))
	items.append(seprator())
	return "FX Tools",items,1

def get_view3d_fx_objects(ctx):
	items = []
	items.append(QuadItem("FXObjects",f,f,n,"",n))
	items.append(seprator())
	return "FX Objects",items,2

def get_view3d_fx_simulation(ctx):
	items = []
	items.append(QuadItem("FXSimulation",f,f,n,"",n))
	items.append(seprator())
	return "FX Simulation",items,3

def get_view3d_fx_constraints(ctx):
	items = []
	items.append(QuadItem("FXConstraints",f,f,n,"",n))
	items.append(seprator())
	return "FX Constraints",items,4

def get_grapheditor_trackview(ctx):
	items = []
	items.append(QuadItem("Move Keys",f,f,n,"",n))
	items.append(QuadItem("Add Keys",f,f,n,"",n))
	items.append(QuadItem("Isolate Curve",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Auto",f,f,n,"",n))
	items.append(QuadItem("Spline",f,f,n,"",n))
	items.append(QuadItem("Liner",f,f,n,"",n))
	items.append(QuadItem("Stepped",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Break Tangents",f,f,n,"",n))
	items.append(QuadItem("Unify Tangents",f,f,n,"",n))
	return "Track View",items,1

def get_uv_editor_transform(ctx):
	items = []
	items.append(QuadItem("Move",f,f,n,"",n))
	items.append(QuadItem("Rotate",f,f,n,"",n))
	items.append(QuadItem("Scale",f,f,n,"",n))
	items.append(QuadItem("Freeform Gizmo",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Flip Horizontal",f,f,n,"",n))
	items.append(QuadItem("Flip Vertical",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Mirror Horizontal",f,f,n,"",n))
	items.append(QuadItem("Mirror Vertical",f,f,n,"",n))
	return "Track View",items,1

def get_uv_editor_display(ctx):
	items = []
	items.append(QuadItem("Hide Selected",f,f,n,"",n))
	items.append(QuadItem("Unhide All",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Freeze Selected",f,f,n,"",n))
	items.append(QuadItem("Unfreeze All",f,f,n,"",n))
	return "Track View",items,2

def get_uv_editor_tools1(ctx):
	items = []
	items.append(QuadItem("Top-level",f,f,n,"",n))
	items.append(QuadItem("Vertex",f,f,n,"",n))
	items.append(QuadItem("Edge",f,f,n,"",n))
	items.append(QuadItem("Polygon",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Copy",f,f,n,"",n))
	items.append(QuadItem("Past",f,f,n,"",n))
	items.append(QuadItem("Past Weld",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Pack UVs",f,f,n,"",""))
	items.append(seprator())
	items.append(QuadItem("Render UVW Template...",f,f,n,"",n))
	return "Track View",items,3

def get_uv_editor_tools2(ctx):
	items = []
	items.append(QuadItem("Weld Selected",f,f,n,"",n))
	items.append(QuadItem("Target Weld",f,f,n,"",n))
	items.append(QuadItem("Break",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Detach Edge Verts",f,f,n,"",n))
	items.append(seprator())
	items.append(QuadItem("Stitch Selected",f,f,n,"",""))  
	items.append(seprator())
	items.append(QuadItem("Stitch Vertices",f,f,n,"",""))
	items.append(seprator())
	items.append(QuadItem("Relax",f,f,n,"",""))
	return "Track View",items,4

__all__ = [ "get_view3d_display",
			"get_view3d_transform",
			"get_view3d_tool1",
			"get_view3d_tool2",
			"get_view3D_create",
			"get_view3D_viewport",
			"get_view3d_camera",
			"get_view3d_set",
			"get_view3d_coordinates",
			"get_view3d_transform2",
			"get_view3d_pose",
			"get_view3d_snap_toggles",
			"get_view3d_snap_override",
			"get_view3d_snap_options",
			"get_view3d_rendering_properties",
			"get_view3d_render",
			"get_view3d_rendering_tools",
			"get_view3d_fx_tools",
			"get_view3d_fx_objects",
			"get_view3d_fx_simulation",
			"get_view3d_fx_constraints",
			"get_view3d_selection1",
			"get_view3d_selection2",
			"get_view3d_selection3",
			"get_view3d_selection4",
			"get_grapheditor_trackview",
			"get_uv_editor_transform",
			"get_uv_editor_display",
			"get_uv_editor_tools1",
			"get_uv_editor_tools2" ]