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
# 2024/01/25

import bpy

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, EnumProperty



def get_create_subtype(createType):
	default = 'STANDARD'
	items = [('STANDARD', 'Standard', '')]

	if createType == "MESH":
		default = 'STANDARD'
		items = [
			('STANDARD', 'Standard Primitives', ''),
			('EXTENDED', 'Extended Primitives', ''),
			('COMPOUND','Compound Objects',''),
			('PARTICLE','Particle System',''),
			('PATHGRIDE','Path Gride',''),
			('BODY','Body Objects',''),
			('DOOR','Door',''),
			('NURBS','Nurbs Surface',''),
			('WINDOWS','Windows',''),
			('AEC','AEC Extended',''),
			('POINTCLOUD','Point Cloud objects',''),
			('DYNAMIC','Dynamic objects',''),
			('STAIRS','Stairs',''),
			('ABC','Alembic',''),
			('FLUIDS','Fluids','')
		]

	elif createType == 'CURVE':
		default = 'SPLINE'
		items = [
			('SPLINE', 'Spline', ''),
			('NURBS', 'NURBS Curvs', ''),
			('COMPOUND', 'Compound Shapes', ''),
			('EXTENDED', 'Extended Shapes', ''),
			# ('CREATIONGRAPH', 'Max Creation Graph', '')
		]

	elif createType == 'LIGHT':
		default = 'STANDARD'
		items = [
			('PHOTOMETRIC','Photometric',''),
			('STANDARD','Standard',''),
			# ('ARNOLD','Arnold','')
		]

	elif createType == 'CAMERA':
		default = 'STANDARD'
		items = [
			('STANDARD','Standard',''),
			# ('ARNOLD','Arnold','')
		]

	elif createType == 'EMPTY':
		default = 'STANDARD'
		items = [
			('STANDARD','Standard',''),
			('ATOMOSPHER','Atomospheric Apparatus',''),
			('CAMERAMATCH','Camera Match',''),
			('ASSEMBLY','Assembly Head',''),
			('MANPULATOR','Manpulator',''),
			('PFLOW','Particle Flow',''),
			('MASSFX','MassFX',''),
			('CAT','Cat Objects',''),
			('VRML97','VRML97',''),
		]

	elif createType == 'SPACEWRAP':
		default = 'FORCE'
		items = [
			('FORCE','Force',''),
			('DEFELECTOR','Defelector',''),
			('DEFORABLE','Geometric/Deformable',''),
			('MODIFIER','Modifier Base',''),
			('PARTICLE','Particle & Dynamics','')
		]

	elif createType =='SETTING':
		default = 'STANDARD'
		items = [('STANDARD','Standard','')]

	return (default, items)



def get_create_mesh_ui(layout, cPanel):
	layout.prop(cPanel, 'mesh_types', text="")
	box = layout.box()
	if cPanel.mesh_types == 'STANDARD':
		row = box.row()
		row.operator("create.box", text="Box")
		row.operator("create.cone", text="Cone")
		row = box.row()
		row.operator("create.sphere", text="Sphere")
		row.operator("create.sphere", text="GeoSphere")
		row = box.row()
		row.operator("create.cylinder", text="Cylinder")
		row.operator("create.tube", text="Tube")
		row = box.row()
		row.operator("create.torus", text="Torus")
		row.operator("create.pyramid", text="Pyramid")
		row = box.row()
		row.operator("create.teapot", text="Teapot")
		row.operator("create.plane", text="Plane")
		row = box.row()
		row.operator("create.text", text="TextPlus")

	elif cPanel.mesh_types == 'EXTENDED':
		row = box.row()
		row.operator("bsmax.reserved", text="Hedra")
		row.operator("bsmax.reserved", text="Torus Knot")
		row = box.row()
		row.operator("bsmax.reserved", text="ChamferBox")
		row.operator("bsmax.reserved", text="ChamferCyl")
		row = box.row()
		row.operator("create.oiltank", text="OilTank")
		row.operator("create.capsule", text="Capsule")
		row = box.row()
		row.operator("bsmax.reserved", text="Spindle")
		row.operator("bsmax.reserved", text="L-Ext")
		row = box.row()
		row.operator("bsmax.reserved", text="Gengon")
		row.operator("bsmax.reserved", text="C-Ext")
		row = box.row()
		row.operator("bsmax.reserved", text="RingWave")
		row.operator("bsmax.reserved", text="Hose")
		row = box.row()
		row.operator("bsmax.reserved", text="Prism")
	
	elif cPanel.mesh_types == 'COMPOUND':
		row = box.row()
		row.operator("bsmax.reserved", text="Morph")
		row.operator("bsmax.reserved", text="Scatter")
		row = box.row()
		row.operator("bsmax.reserved", text="Conform")
		row.operator("bsmax.reserved", text="Connect")
		row = box.row()
		row.operator("bsmax.reserved", text="BlobMesh")
		row.operator("bsmax.reserved", text="ShapeMerg")
		row = box.row()
		row.operator("bsmax.reserved", text="Terrain")
		row.operator("bsmax.reserved", text="Loft")
		row = box.row()
		row.operator("bsmax.reserved", text="Mesher")
		row.operator("bsmax.reserved", text="ProBooleeean")
		row = box.row()
		row.operator("bsmax.reserved", text="ProCutter")
		row.operator("bsmax.reserved", text="Booleean")

	elif cPanel.mesh_types == 'PARTICLE':
		row = box.row()
		row.operator("bsmax.reserved", text="PF Source")
		row.operator("bsmax.reserved", text="Spray")
		row = box.row()
		row.operator("bsmax.reserved", text="Snow")
		row.operator("bsmax.reserved", text="Super Spray")
		row = box.row()
		row.operator("bsmax.reserved", text="Blizzard")
		row.operator("bsmax.reserved", text="PArray")
		row = box.row()
		row.operator("bsmax.reserved", text="PCloud")

	elif cPanel.mesh_types == 'PATHGRIDE':
		row = box.row()
		row.operator("bsmax.reserved", text="Quad Patch")
		row.operator("bsmax.reserved", text="Tri Patch")

	elif cPanel.mesh_types == 'BODY':
		row = box.row()
		row.operator("bsmax.reserved", text="Body Utility")
		row.operator("bsmax.reserved", text="Body Object")
		row = box.row()
		row.operator("bsmax.reserved", text="Join Bodies")
		row.operator("bsmax.reserved", text="Body Cutter")

	elif cPanel.mesh_types == 'DOOR':
		row = box.row()
		row.operator("bsmax.reserved", text="Pivot")
		row.operator("bsmax.reserved", text="Sliding")
		row = box.row()
		row.operator("bsmax.reserved", text="BiFold")

	elif cPanel.mesh_types == 'NURBS':
		row = box.row()
		row.operator("bsmax.reserved", text="Point Surf")
		row.operator("bsmax.reserved", text="CV Surf")
	
	elif cPanel.mesh_types == 'WINDOWS':
		row = box.row()
		row.operator("bsmax.reserved", text="Awning")
		row.operator("bsmax.reserved", text="Casement")
		row = box.row()
		row.operator("bsmax.reserved", text="Fixed")
		row.operator("bsmax.reserved", text="Pivoted")
		row = box.row()
		row.operator("bsmax.reserved", text="Projected")
		row.operator("bsmax.reserved", text="Sliding")

	elif cPanel.mesh_types == 'AEC':
		row = box.row()
		row.operator("bsmax.reserved", text="Foliage")
		row.operator("bsmax.reserved", text="Railing")
		row = box.row()
		row.operator("bsmax.reserved", text="Wall")

	elif cPanel.mesh_types == 'POINTCLOUD':
		row = box.row()
		row.operator("bsmax.reserved", text="PointCloud")

	elif cPanel.mesh_types == 'DYNAMIC':
		row = box.row()
		row.operator("bsmax.reserved", text="Spring")
		row.operator("bsmax.reserved", text="Damper")

	elif cPanel.mesh_types == 'STAIRS':
		row = box.row()
		row.operator("bsmax.reserved", text="Straight Stair")
		row.operator("bsmax.reserved", text="L-Type Stair")
		row = box.row()
		row.operator("bsmax.reserved", text="U-Type Stair")
		row.operator("bsmax.reserved", text="Spiral Stair")

	elif cPanel.mesh_types == 'ABC':
		row = box.row()
		row.operator("bsmax.reserved", text="Alembic")
		row.operator("bsmax.reserved", text="Procedural")
		row = box.row()
		row.operator("bsmax.reserved", text="Volume")
		row.operator("bsmax.reserved", text="USD")

	elif cPanel.mesh_types == 'FLUIDS':
		row = box.row()
		row.operator("bsmax.reserved", text="Liquid")
		row.operator("bsmax.reserved", text="Fluid Loader")



def get_create_curve_ui(layout, cPanel):
	layout.prop(cPanel, 'curve_types', text="")
	box = layout.box()

	if cPanel.curve_types == 'SPLINE':
		row = box.row()
		row.operator("create.line", text="Line")
		row.operator("create.rectangle", text="Rectangle")
		row = box.row()
		row.operator("create.circle", text="Circle")
		row.operator("create.ellipse", text="Elipse")
		row = box.row()
		row.operator("create.arc", text="Arc")
		row.operator("create.donut", text="Donut")
		row = box.row()
		row.operator("create.ngon", text="NGon")
		row.operator("create.star", text="Star")
		row = box.row()
		row.operator("create.text", text="Text")
		row.operator("create.helix", text="Helix")
		row = box.row()
		row.operator("bsmax.reserved", text="Egg")
		row.operator("bsmax.reserved", text="Section")
		row = box.row()
		row.operator("bsmax.reserved", text="Freehand")
	
	elif cPanel.curve_types == 'NURBS':
		row = box.row()
		row.operator("bsmax.reserved", text="Point Curve")
		row.operator("bsmax.reserved", text="CV Curve")

	elif cPanel.curve_types == 'COMPOUND':
		row = box.row()
		row.operator("bsmax.reserved", text="ShpBoolean")

	elif cPanel.curve_types == 'EXTENDED':
		row = box.row()
		row.operator("bsmax.reserved", text="WRectangle")
		row.operator("bsmax.reserved", text="Chanel")
		row = box.row()
		row.operator("bsmax.reserved", text="Angle")
		row.operator("bsmax.reserved", text="Tee")
		row = box.row()
		row.operator("bsmax.reserved", text="Wide Flange")

	elif cPanel.curve_types == 'CREATIONGRAPH':
		pass



def get_create_light_ui(layout, cPanel):
	layout.prop(cPanel, 'light_types', text="")
	box = layout.box()

	if cPanel.light_types == 'PHOTOMETRIC':
		row = box.row()
		row.operator("bsmax.reserved", text="Target Light")
		row.operator("bsmax.reserved", text="Free Light")
		row = box.row()
		row.operator("bsmax.reserved", text="Sun Positioner")

	elif cPanel.light_types == 'STANDARD':
		row = box.row()
		row.operator("create.pointlight", text="Point")
		row.operator("create.spotlight", text="Spot")
		row = box.row()
		row.operator("create.arealight", text="Area")
		row.operator("create.arealight", text="Area Target").free=True
		row = box.row()
		row.operator("create.sunlight", text="Sun")

	elif cPanel.light_types == 'ARNOLD':
		row = box.row()
		row.operator("bsmax.reserved", text="Arnold")



def get_create_camera_ui(layout, cPanel):
	layout.prop(cPanel, 'camera_types', text="")
	box = layout.box()

	if cPanel.camera_types == 'STANDARD':
		row = box.row()
		row.operator("create.camera", text="Camera")

	elif cPanel.camera_types == 'ARNOLD':
		row = box.row()
		row.operator("bsmax.reserved", text="Vr Camera")
		row.operator("bsmax.reserved", text="Fisheye")
		row = box.row()
		row.operator("bsmax.reserved", text="Spherical")
		row.operator("bsmax.reserved", text="Cylindrical")



def get_create_empty_ui(layout, cPanel):
	layout.prop(cPanel, 'empty_types', text="")
	box = layout.box()

	if cPanel.empty_types == 'STANDARD':
		row = box.row()
		row.operator("create.empty", text="Point axis").empty_type='PLAIN_AXES'
		row.operator("create.empty", text="Arrows").empty_type='ARROWS'
		row = box.row()
		row.operator("create.empty", text="Single Arrow").empty_type='SINGLE_ARROW'
		row.operator("create.empty", text="Circle").empty_type='CIRCLE'
		row = box.row()
		row.operator("create.empty", text="Cube").empty_type='CUBE'
		row.operator("create.empty", text="Sphere").empty_type='SPHERE'
		row = box.row()
		row.operator("create.empty", text="Cone").empty_type='CONE'
		row.operator("create.empty", text="Image").empty_type='IMAGE'

		row = box.row()
		row.operator("bsmax.reserved", text="Dummy")
		row.operator("bsmax.reserved", text="Containeer")
		row = box.row()
		row.operator("bsmax.reserved", text="Crowd")
		row.operator("bsmax.reserved", text="Delegate")
		row = box.row()
		row.operator("bsmax.reserved", text="ExposeeeTm")
		row.operator("bsmax.reserved", text="Grid")
		row = box.row()
		row.operator("bsmax.reserved", text="Point")
		row.operator("bsmax.reserved", text="Tape")
		row = box.row()
		row.operator("bsmax.reserved", text="Protractor")
		row.operator("bsmax.reserved", text="Influencer")
		row = box.row()
		row.operator("bsmax.reserved", text="Arrow")
		row.operator("bsmax.reserved", text="Volume")
		row = box.row()
		row.operator("bsmax.reserved", text="Compass")

	elif cPanel.empty_types == 'ATOMOSPHER':
		row = box.row()
		row.operator("bsmax.reserved", text="BoxGizmo")
		row.operator("bsmax.reserved", text="ShpereGizmo")
		row = box.row()
		row.operator("bsmax.reserved", text="CylGizmo")

	elif cPanel.empty_types == 'CAMERAMATCH':
		row = box.row()
		row.operator("bsmax.reserved", text="CamPoint")

	elif cPanel.empty_types == 'ASSEMBLY':
		row = box.row()
		row.operator("bsmax.reserved", text="Luminair")

	elif cPanel.empty_types == 'MANPULATOR':
		row = box.row()
		row.operator("bsmax.reserved", text="Cone Angle")
		row.operator("bsmax.reserved", text="Plane Angle")
		row = box.row()
		row.operator("bsmax.reserved", text="Slider")

	elif cPanel.empty_types == 'PFLOW':
		row = box.row()
		row.operator("bsmax.reserved", text="Find Target")
		row.operator("bsmax.reserved", text="SpeedByIcon")
		row = box.row()
		row.operator("bsmax.reserved", text="Initial State")
		row.operator("bsmax.reserved", text="Group Select")
		row = box.row()
		row.operator("bsmax.reserved", text="Particle Paint")
		row.operator("bsmax.reserved", text="Birth Texture")
		row = box.row()
		row.operator("bsmax.reserved", text="mP Solver")
		row.operator("bsmax.reserved", text="mP Buoyancy")
		row = box.row()
		row.operator("bsmax.reserved", text="BrithGrid")
		row.operator("bsmax.reserved", text="BirthStream")
		row = box.row()
		row.operator("bsmax.reserved", text="mP World")
		row.operator("bsmax.reserved", text="BlurWind")
		row = box.row()
		row.operator("bsmax.reserved", text="Data Icon")
		row.operator("bsmax.reserved", text="RandomWalk")
		row = box.row()
		row.operator("bsmax.reserved", text="Test Icon")

	elif cPanel.empty_types == 'MASSFX':
		row = box.row()
		row.operator("bsmax.reserved", text="UConstraint")

	elif cPanel.empty_types == 'CAT':
		row = box.row()
		row.operator("bsmax.reserved", text="CATMuscle")
		row.operator("bsmax.reserved", text="Muscle Strand")
		row = box.row()
		row.operator("bsmax.reserved", text="CATParent")

	elif cPanel.empty_types == 'VRML97':
		row = box.row()
		row.operator("bsmax.reserved", text="Anchor")
		row.operator("bsmax.reserved", text="TouchSensor")
		row = box.row()
		row.operator("bsmax.reserved", text="ProxSensor")
		row.operator("bsmax.reserved", text="TimeSensor")
		row = box.row()
		row.operator("bsmax.reserved", text="NavInfo")
		row.operator("bsmax.reserved", text="Background")
		row = box.row()
		row.operator("bsmax.reserved", text="Fog")
		row.operator("bsmax.reserved", text="AudioClip")
		row = box.row()
		row.operator("bsmax.reserved", text="Sound")
		row.operator("bsmax.reserved", text="BilBoard")
		row = box.row()
		row.operator("bsmax.reserved", text="LOD")
		row.operator("bsmax.reserved", text="Inline")



def get_create_spacewrap_ui(layout, cPanel):
	layout.prop(cPanel, 'spacewrap_types', text="")
	box = layout.box()

	if cPanel.spacewrap_types == 'FORCE':
		row = box.row()
		row.operator("create.effector", text="Force").effector_type='FORCE'
		row.operator("create.effector", text="Wind").effector_type='WIND'
		row = box.row()
		row.operator("create.effector", text="Vortex").effector_type='VORTEX'
		row.operator("create.effector", text="Magnet").effector_type='MAGNET'
		row = box.row()
		row.operator("create.effector", text="Harmonic").effector_type='HARMONIC'
		row.operator("create.effector", text="Charge").effector_type='CHARGE'
		row = box.row()
		row.operator("create.effector", text="Lennard-jones").effector_type='LENNARDJ'
		row.operator("create.effector", text="Texture").effector_type='TEXTURE'
		row = box.row()
		row.operator("create.effector", text="Guide").effector_type='GUIDE'
		row.operator("create.effector", text="Boid").effector_type='BOID'
		row = box.row()
		row.operator("create.effector", text="Turbulence").effector_type='TURBULENCE'
		row.operator("create.effector", text="Drag").effector_type='DRAG'
		# row = box.row()
		# row.operator("create.effector", text="Smoke").effector_type='SMOKE'

	elif cPanel.spacewrap_types == 'DEFELECTOR':
		row = box.row()
		row.operator("bsmax.reserved", text="POmniFlect")
		row.operator("bsmax.reserved", text="SOminiFlect")
		row = box.row()
		row.operator("bsmax.reserved", text="UOmniFlect")
		row.operator("bsmax.reserved", text="UDefelector")
		row = box.row()
		row.operator("bsmax.reserved", text="SDefelector")
		row.operator("bsmax.reserved", text="Defelector")
	
	elif cPanel.spacewrap_types == 'DEFORABLE':
		row = box.row()
		row.operator("bsmax.reserved", text="FFD(BOX)")
		row.operator("bsmax.reserved", text="FFD(Cyl)")
		row = box.row()
		row.operator("bsmax.reserved", text="Wave")
		row.operator("bsmax.reserved", text="Ripple")
		row = box.row()
		row.operator("bsmax.reserved", text="Displace")
		row.operator("bsmax.reserved", text="Confirm")
		row = box.row()
		row.operator("bsmax.reserved", text="Bomb")
	
	elif cPanel.spacewrap_types == 'MODIFIER':
		row = box.row()
		row.operator("bsmax.reserved", text="Bend")
		row.operator("bsmax.reserved", text="Twist")
		row = box.row()
		row.operator("bsmax.reserved", text="Taper")
		row.operator("bsmax.reserved", text="Skew")
		row = box.row()
		row.operator("bsmax.reserved", text="Noise")
		row.operator("bsmax.reserved", text="Stretch")
	
	elif cPanel.spacewrap_types == 'PARTICLE':
		row = box.row()
		row.operator("bsmax.reserved", text="Vector Field")



def get_create_setting_ui(layout, cPanel):
	layout.prop(cPanel, 'setting_types', text="")
	box = layout.box()

	if cPanel.setting_types == 'STANDARD':
		row = box.row()
		row.operator("create.bone", text="Bones")
		row.operator("bsmax.reserved", text="Ring Array")
		row = box.row()
		row.operator("bsmax.reserved", text="Biped")
		row.operator("bsmax.reserved", text="Sunlight")
		row = box.row()
		row.operator("bsmax.reserved", text="Daylight")



def get_hierarcy_pivot_ui(layout, ctx):
	box = layout.box()
	# Move/Rotate/Scale
	box.prop(
		ctx.scene.tool_settings, "use_transform_data_origin",
		text="Affect Pivot Only", toggle=True
	)

	box.prop(
		ctx.scene.tool_settings, "use_transform_pivot_point_align",
		text="Affect Object Only", toggle=True
	)

	box.operator("bsmax.reserved", text="Affect Hierarcy Only")
	
	box = layout.box()
	# Alignment
	box.operator("bsmax.reserved", text="Center to Object")
	box.operator("bsmax.reserved", text="Align to Object")
	box.operator("bsmax.reserved", text="Align to world")
	# Pivot
	box.operator("bsmax.reserved", text="Reset")

	box = layout.box()
	# Working pivot
	box.operator("bsmax.reserved", text="Edit working pivot")
	box.operator("bsmax.reserved", text="Use working pivot")
	box.operator("bsmax.reserved", text="Alight ti view")
	box.operator("bsmax.reserved", text="Reset")

	box = layout.box()
	# adjust Transform
	box.prop(
		ctx.scene.tool_settings, "use_transform_skip_children",
		text="Dont Affect Children", toggle=True
	)

	box.operator("bsmax.reserved", text="Reset Transform")
	box.operator("bsmax.reserved", text="Reset Scale")



def get_hierarcy_ik_ui(layout, ctx):
	box = layout.box()



def get_hierarcy_linkinfo_ui(layout, ctx):
	if not ctx.object:
		return 

	box = layout.box()
	box.prop(ctx.object, 'lock_location', text="location")
	box.prop(ctx.object, 'lock_rotation', text="Rotation")
	box.prop(ctx.object, 'rotation_mode')
	box.prop(ctx.object, 'lock_scale', text="Scale")



class BsMax_Scene_Side_Panel(PropertyGroup):
	main_tab: EnumProperty(
		default='CREATE',
		items =[
			('CREATE', 'Create', '', 'ADD', 1),
			('MODIFY', 'Modify', '', 'FULLSCREEN_ENTER', 2),
			('HIERARCHY', 'Hierarchy', '', 'PARTICLES', 3),
			('MOTION', 'Motion', '', 'PHYSICS', 4),
			('DISPLAY', 'Display', '', 'WORKSPACE', 5),
			('UTILITIES', 'Utilities', '', 'MODIFIER', 6)
		]
	)

	create_type: EnumProperty(
		items =[
			('MESH', 'Mesh', '', 'NODE_MATERIAL', 1),
			('CURVE', 'Curve', '', 'MOD_SUBSURF', 2),
			('LIGHT', 'Light', '', 'LIGHT_DATA', 3),
			('CAMERA', 'Camera', '', 'CAMERA_DATA', 4),
			('EMPTY', 'Empty', '', 'MODIFIER_DATA', 5),
			('SPACEWRAP', 'Spacewrap', '', 'FORCE_FORCE', 6),
			('SETTING', 'Setting', '', 'SETTINGS', 7),
		],
		default='MESH',
	)

	hierarcy_type: EnumProperty(
		items =[
			('PIVOT', 'Pivot', ''),
			('IK', 'IK', ''),
			('LINKINFO', 'Link Info', ''),
		],
		default='LINKINFO',
	)

	stDefault, stItems = get_create_subtype('MESH')
	mesh_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('CURVE')
	curve_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('LIGHT')
	light_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('CAMERA')
	camera_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('EMPTY')
	empty_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('SPACEWRAP')
	spacewrap_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('SETTING')
	setting_types: EnumProperty(
		items= stItems,
		default=stDefault
	)



def get_create_panel(layout, ctx):
	cPanel = ctx.scene.comand_panel
	layout.prop(cPanel, 'create_type', expand=True)
		
	if cPanel.create_type == 'MESH':
		get_create_mesh_ui(layout, cPanel)

	elif cPanel.create_type == 'CURVE':
		get_create_curve_ui(layout, cPanel)
		
	elif cPanel.create_type == 'LIGHT':
		get_create_light_ui(layout, cPanel)

	elif cPanel.create_type == 'CAMERA':
		get_create_camera_ui(layout, cPanel)

	elif cPanel.create_type == 'EMPTY':
		get_create_empty_ui(layout, cPanel)
	
	elif cPanel.create_type == 'SPACEWRAP':
		get_create_spacewrap_ui(layout, cPanel)

	elif cPanel.create_type == 'SETTING':
		get_create_setting_ui(layout, cPanel)
	
	box = layout.box()
	row = box.row()
	row.label(text=ctx.scene.primitive_setting.active_tool)
	



def get_modifier_panel(layout, ctx):
	layout.operator("object.create_modifier", text="Modifier List")
	box = layout.box()
	if ctx.object:
		for modifer in ctx.object.modifiers:
			box.label(text=modifer.name)



def get_hierarcy_panel(layout, ctx):
	cPanel = ctx.scene.comand_panel
	layout.prop(cPanel, 'hierarcy_type', expand=True)

	if cPanel.hierarcy_type == 'PIVOT':
		get_hierarcy_pivot_ui(layout, ctx)

	elif cPanel.hierarcy_type == 'IK':
		get_hierarcy_ik_ui(layout, ctx)

	elif cPanel.hierarcy_type == 'LINKINFO':
		get_hierarcy_linkinfo_ui(layout, ctx)



def get_motion_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



def get_display_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



def get_utility_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



class BsMax_OT_Reserved(Operator):
	bl_idname = 'bsmax.reserved'
	bl_label = 'Reserveed'
	bl_description = ''

	@classmethod
	def poll(self, ctx):
		return False

	def execute(self, ctx):
		return{'FINISHED'}
	
	


class SCENE_OP_BsMax_Side_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'BsMax (Under Construction)'
	bl_idname = 'VIEW3D_PT_BsMax'
	bl_category = 'BsMax'

	def draw(self, ctx):
		layout = self.layout
		cPanel = ctx.scene.comand_panel

		layout.prop(cPanel, 'main_tab', expand=True)

		if cPanel.main_tab == 'CREATE':
			get_create_panel(layout, ctx)

		elif cPanel.main_tab == 'MODIFY':
			get_modifier_panel(layout, ctx)

		elif cPanel.main_tab == 'HIERARCHY':
			get_hierarcy_panel(layout, ctx)

		elif cPanel.main_tab == 'MOTION':
			get_motion_panel(layout, ctx)

		elif cPanel.main_tab == 'DISPLAY':
			get_display_panel(layout, ctx)

		elif cPanel.main_tab == 'UTILITIES':
			get_utility_panel(layout, ctx)
	


classes = (
	BsMax_OT_Reserved,
	BsMax_Scene_Side_Panel,
	SCENE_OP_BsMax_Side_Panel
)



def register_side_panel():
	for c in classes:
		bpy.utils.register_class(c)
	
	bpy.types.Scene.comand_panel = PointerProperty(type=BsMax_Scene_Side_Panel)



def unregister_side_panel():
	#TODO check is class exist before remove
	for c in classes:
		try:
			bpy.utils.unregister_class(c)
		except:
			pass


if __name__ == "__main__":
	register_side_panel()