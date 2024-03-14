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
# 2024/03/03

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


def get_draw_alignment_ui(ctx, layout):
	box = layout.box()
	row = box.row()
	row.label(text='Drawing Gride')
	row.prop(
		ctx.scene.primitive_setting, 'draw_mode',
		text='', expand=True
	)


def get_create_mesh_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'mesh_types', text="")
	get_draw_alignment_ui(ctx, layout)
	
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

	elif cPanel.mesh_types == 'NURBS':
		row = box.row()
		row.operator("bsmax.reserved", text="Point Surf")
		row.operator("bsmax.reserved", text="CV Surf")
	
	elif cPanel.mesh_types == 'ARCHITECTURE':
		row = box.row()
		row.operator("bsmax.reserved", text="AEC Foliage")
		row.operator("bsmax.reserved", text="AEC Railing")
		# Wall
		row = box.row()
		row.operator("bsmax.reserved", text="Wall")
		row = box.row()
		# Doors
		row = box.row()
		row.operator("bsmax.reserved", text="Pivot Door")
		row.operator("bsmax.reserved", text="Sliding Door")
		row = box.row()
		row.operator("bsmax.reserved", text="BiFold Door")
		row = box.row()
		# Stairs
		row = box.row()
		row.operator("bsmax.reserved", text="Straight Stair")
		row.operator("bsmax.reserved", text="L-Type Stair")
		row = box.row()
		row.operator("bsmax.reserved", text="U-Type Stair")
		row.operator("bsmax.reserved", text="Spiral Stair")
		row = box.row()
		# Windows
		row = box.row()
		row.operator("bsmax.reserved", text="Awning Window")
		row.operator("bsmax.reserved", text="Casement Window")
		row = box.row()
		row.operator("bsmax.reserved", text="Fixed Window")
		row.operator("bsmax.reserved", text="Pivoted Window")
		row = box.row()
		row.operator("bsmax.reserved", text="Projected Window")
		row.operator("bsmax.reserved", text="Sliding Window")

	elif cPanel.mesh_types == 'POINTCLOUD':
		row = box.row()
		row.operator("bsmax.reserved", text="PointCloud")

	elif cPanel.mesh_types == 'DYNAMIC':
		row = box.row()
		row.operator("bsmax.reserved", text="Spring")
		row.operator("bsmax.reserved", text="Damper")

	elif cPanel.mesh_types == 'ABC':
		row = box.row()
		row.operator("bsmax.reserved", text="Alembic")
		row.operator("bsmax.reserved", text="Procedural")
		row = box.row()
		row.operator("bsmax.reserved", text="Volume")
		row.operator("bsmax.reserved", text="USD")

	elif cPanel.mesh_types == 'FLUIDS':
		row = box.row()
		row.operator("object.quick_smoke", text="ُQuick Smoke")
		row.operator("object.quick_fur", text="ُQuick Fur")
		row = box.row()
		row.operator("object.quick_explode", text="ُQuick Explod")
		row.operator("object.quick_liquid", text="ُQuick Liquid")
		row = box.row()
		row.operator("bsmax.reserved", text="Fluid Loader")


def get_create_curve_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'curve_types', text="")
	get_draw_alignment_ui(ctx, layout)
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
		row.operator("create.torusknot", text="Tors Knot")
	
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


def get_create_light_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'light_types', text="")
	get_draw_alignment_ui(ctx, layout)
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
		row.operator("create.arealight", text="Area").free=True
		row.operator("create.arealight", text="Area Target")
		row = box.row()
		row.operator("create.sunlight", text="Sun")

	elif cPanel.light_types == 'ARNOLD':
		row = box.row()
		row.operator("bsmax.reserved", text="Arnold")


def get_create_camera_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'camera_types', text="")
	get_draw_alignment_ui(ctx, layout)
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


def get_create_empty_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'empty_types', text="")
	get_draw_alignment_ui(ctx, layout)
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


def get_create_spacewrap_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'spacewrap_types', text="")
	get_draw_alignment_ui(ctx, layout)
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


def get_create_setting_ui(ctx, layout, cPanel):
	layout.prop(cPanel, 'setting_types', text="")
	get_draw_alignment_ui(ctx, layout)
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


def create_next_ui(ctx, layout):
	row = layout.row()
	primitive_setting = ctx.scene.primitive_setting
	if primitive_setting.active_tool:
		row.prop(primitive_setting, 'next_name', text='')
		row.prop(primitive_setting, 'next_color', text='')


def get_create_panel(layout, ctx):
	cPanel = ctx.scene.command_panel
	layout.prop(cPanel, 'create_type', expand=True)
		
	if cPanel.create_type == 'MESH':
		get_create_mesh_ui(ctx, layout, cPanel)

	elif cPanel.create_type == 'CURVE':
		get_create_curve_ui(ctx, layout, cPanel)
		
	elif cPanel.create_type == 'LIGHT':
		get_create_light_ui(ctx, layout, cPanel)

	elif cPanel.create_type == 'CAMERA':
		get_create_camera_ui(ctx, layout, cPanel)

	elif cPanel.create_type == 'EMPTY':
		get_create_empty_ui(ctx, layout, cPanel)
	
	elif cPanel.create_type == 'SPACEWRAP':
		get_create_spacewrap_ui(ctx, layout, cPanel)

	elif cPanel.create_type == 'SETTING':
		get_create_setting_ui(ctx, layout, cPanel)
	
	create_next_ui(ctx, layout.box())


class SCENE_OP_BsMax_Create_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Create'
	bl_idname = 'VIEW3D_PT_BsMax_create'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'CREATE'
	
	def draw(self, ctx):
		get_create_panel(self.layout, ctx)


def register_create_panel():
	register_class(SCENE_OP_BsMax_Create_Panel)


def unregister_create_panel():
	unregister_class(SCENE_OP_BsMax_Create_Panel)


if __name__ == "__main__":
	register_create_panel()