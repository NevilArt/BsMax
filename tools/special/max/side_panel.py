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
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import (
	IntProperty, StringProperty,
	BoolProperty, PointerProperty, EnumProperty
)



def get_modifier_list(self, ctx):
	return [
		('MESHSELECT', 'Mesh Select', ''),
		('PATCHSELECT', 'Patch Select', ''),
		('POLYSELECT', 'Poly Select', ''),
		('VOLSELECT', 'Vol. Select', ''),

		('CAMERAMAP', 'Camera Map()', ''),
		('DISPLACEMESH', 'Displace Mesh()', ''),
		('HAIRANDFUR', 'Hair and Fur()', ''),
		('MAPSCALLER', 'MapScaler()', ''),
		('PATCHDEFORM', 'PatchDeform()', ''),
		('PATHDEFORM', 'PathDeform()', ''),
		('PFLOWCOLLISION', 'Pflow Collision Shape()', ''),
		('POINTCACHEW', 'Point Cache()', ''),
		('SUBDIVIDE', 'Subdivide()', ''),
		('SURFACEMAPPER', 'Surface Maper()', ''),
		('SURFACECDEFORM', 'Surface Deform()', ''),

		('AFFECTREGION', 'Affect Region', ''),
		('ARNOLDPROPERTIES', 'Arnold Properties', ''),
		('ARRAY', 'Array', ''),
		('ATTRIBUTEHOLDEDR', 'Attribute Holder', ''),
		('BEND', 'Bend', ''),
		('BOLLEAN', 'Boolean', ''),
		('CAMERAMAP', 'Camera Map', ''),
		('CAPHOLE', 'Cap Holes', ''),
		('CHAMFER', 'Chamfer', ''),
		('CLOTH', 'Cloth', ''),
		('CONFIRM', 'Confirm', ''),
		('CREASE', 'Crease', ''),
		('CREASESET', 'CreaseSet', ''),
		('DATACHANEL', 'Data Chanel', ''),
		('DELETEMESH', 'Delete Mesh', ''),
		('DELETEPATCH', 'DeletePatch', ''),
		('DISPAPPROX', 'Disp Approx', ''),
		('DISPLACE', 'Displace', ''),
		('EDITMESH', 'Edit Mesh', ''),
		('EDITNORMAL', 'Edit Normal', ''),
		('EDITPATCH', 'Edit Patch', ''),
		('EDITPOLY', 'Edit Poly', ''),
		('FACEEXTRUD', 'Face Extrud', ''),
		('FFD2X2X2', 'FFD 2x2x2', ''),
		('FFD3X3X3', 'FFD 3x3x3', ''),
		('FFD4X4X4', 'FFD 4x4x4', ''),
		('FFDBOX', 'FFD Box', ''),
		#...
		('MELT', 'Melt', ''),
		('MESHCLEANER', 'Mesh Cleaner', ''),
		('MESHSELECT', 'Mesh Select', ''),
		('MESHSMOMTH', 'Mesh Smooth', ''),
		('MIRROR', 'Mirror', ''),
		('MORPHER', 'Morpher', ''),
		('MULTIRES', 'MultiRes', ''),
		('NOISE', 'Noise', ''),
		('NORMAL', 'Normal', ''),
		('OPENSUBDIV', 'OpenSubdiv', ''),
		('OPTIMIZE', 'Optimize', ''),
		('PARTICLEFORCE', 'Particle Face Creator', ''),
		('PARTICLESKINNER', 'Particle Skinner', ''),
		('PATHSELECT', 'Path Select', ''),
		('PATHDEFORM', 'Patch Deform', ''),
		('PHYSIQUE', 'Physique', ''),
		('POINTCACHE', 'Point Cache', ''),
		('POLYSELECT', 'Poly Select', ''),
		('PRESERVE', 'Preserve', ''),
		('PROJECTION', 'Projection', ''),
		('PROOPTIMIZER', 'ProOptimizer', ''),
		('PUSH', 'Push', ''),
		('QUDIFYMESH', 'Qudify Mesh', ''),
		('RELAX', 'Relax', ''),
		('RETOPOLOGY', 'Retopology', ''),
		('RIPPLE', 'Ripple', ''),
		('SELECTBYCHANEL', 'Select by Chanel', ''),
		('SHELL', 'Shell', ''),
		('SKEW', 'Skew', ''),
		('SKIN', 'Skin', ''),
		('SKINMORPH', 'Skin Morph', ''),
		('SKINWRAP', 'Skin Wrap', ''),
		('SKINWRAPPATCH', 'Skin Wrap Patch', ''),
		('SLICE', 'Slice', ''),
		('SMOOTH', 'Smooth', ''),
		('SPEREFY', 'Sperefy', ''),
		# ('', '?????', ''),
		('STLCHECK', 'STL check', ''),
		('STRETCH', 'Stretch', ''),
		('SUBDIVIDE', 'Subdivide', ''),
		# ('', '?????', ''),
		('SURFDEFORM', 'SurfDeform', ''),
		('SYMMETRY', 'Symmetry', ''),
		('TAPE', 'Tape', ''),
		('TURBOSMOTH', 'Turbosmoth', ''),
		('UNWRAPUVW', 'Unwrap UVW', ''),
		('UVASCOLOR', 'UV as Color', ''),
		('UVASHSL', 'UV as HSL Color', ''),
		('UVASGRADIENT', 'UV as HSL Gradiyent', ''),
		('UVASBLABLA', 'UV as HSL Gradient with mid....', ''),
		('UVWMAPP', 'UVW Map', ''),
		('UVMAPPADD', 'UVW Mapping Add', ''),
		('UVWCLEAR', 'UVW Mapping Clear', ''),
		('UVWXFORM', 'UVW Xform', ''),
		('VERTEXWELD', 'Vertex Weld', ''),
		('VERTEXPAINT', 'Vertex Paint', ''),
		('VOLSELECT', 'Vol. Select', ''),
		('WAVE', 'Wave', ''),
		('WEGHTEDNORMAL', 'Weghted Normals', ''),
		('WELDER', 'Welder', ''),
		('XFORM', 'Xform', '')
	]



def get_subtype(createType):
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
			('CREATIONGRAPH', 'Max Creation Graph', '')
		]

	elif createType == 'LIGHT':
		default = 'STANDARD'
		items = [
			('PHOTOMETRIC','Photometric',''),
			('STANDARD','Standard',''),
			('ARNOLD','Arnold','')
		]

	elif createType == 'CAMERA':
		default = 'STANDARD'
		items = [
			('STANDARD','Standard',''),
			('ARNOLD','Arnold','')
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

	elif cPanel.mesh_types == 'EXTENDED':
		row = box.row()
		row.operator("create.box", text="ChamferBox")
		row.operator("create.cone", text="ChamferCylinder")
	
	elif cPanel.mesh_types == 'COMPOUND':
		pass

	elif cPanel.mesh_types == 'PARTICLE':
		pass

	elif cPanel.mesh_types == 'PATHGRIDE':
		pass

	elif cPanel.mesh_types == 'BODY':
		pass

	elif cPanel.mesh_types == 'DOOR':
		pass

	elif cPanel.mesh_types == 'NURBS':
		pass
	
	elif cPanel.mesh_types == 'WINDOWS':
		pass

	elif cPanel.mesh_types == 'AEC':
		pass

	elif cPanel.mesh_types == 'POINTCLOUD':
		pass

	elif cPanel.mesh_types == 'DYNAMIC':
		pass

	elif cPanel.mesh_types == 'STAIRS':
		pass

	elif cPanel.mesh_types == 'ABC':
		pass

	elif cPanel.mesh_types == 'FLUIDS':
		pass



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
		# row = box.row()
		# row.operator("create.box", text="Egg")
		# row.operator("create.cone", text="Section")
	
	elif cPanel.curve_types == 'NURBS':
		pass

	elif cPanel.curve_types == 'COMPOUND':
		pass

	elif cPanel.curve_types == 'EXTENDED':
		pass

	elif cPanel.curve_types == 'CREATIONGRAPH':
		pass



def get_create_light_ui(layout, cPanel):
	layout.prop(cPanel, 'light_types', text="")
	box = layout.box()

	if cPanel.light_types == 'PHOTOMETRIC':
		pass
	elif cPanel.light_types == 'STANDARD':
		row = box.row()
		row.operator("create.pointlight", text="Point Light")
		row.operator("create.spotlight", text="Spot Light")
		row = box.row()
		row.operator("create.sunlight", text="Sun Light")
		row.operator("create.arealight", text="Area Light")
	elif cPanel.light_types == 'ARNOLD':
		pass



def get_create_camera_ui(layout, cPanel):
	layout.prop(cPanel, 'camera_types', text="")
	box = layout.box()

	if cPanel.camera_types == 'STANDARD':
		row = box.row()
		row.operator("create.camera", text="Free Camera")
		row.operator("create.camera", text="Target Camera")
	elif cPanel.camera_types == 'ARNOLD':
		pass



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

	elif cPanel.empty_types == 'ATOMOSPHER':
		pass
	elif cPanel.empty_types == 'CAMERAMATCH':
		pass
	elif cPanel.empty_types == 'ASSEMBLY':
		pass
	elif cPanel.empty_types == 'MANPULATOR':
		pass
	elif cPanel.empty_types == 'PFLOW':
		pass
	elif cPanel.empty_types == 'MASSFX':
		pass
	elif cPanel.empty_types == 'CAT':
		pass
	elif cPanel.empty_types == 'VRML97':
		pass



def get_create_spacewrap_ui(layout, cPanel):
	layout.prop(cPanel, 'spacewrap_types', text="")
	box = layout.box()

	if cPanel.empty_types == 'STANDARD':
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
		row = box.row()
		row.operator("create.effector", text="Smoke").effector_type='SMOKE'
	elif cPanel.empty_types == 'ATOMOSPHER':
		pass



def get_create_setting_ui(layout, cPanel):
	layout.prop(cPanel, 'setting_types', text="")
	box = layout.box()

	if cPanel.setting_types == 'STANDARD':
		pass




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
		# update=
	)

	stDefault, stItems = get_subtype('MESH')
	mesh_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('CURVE')
	curve_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('LIGHT')
	light_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('CAMERA')
	camera_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('EMPTY')
	empty_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('SPACEWRAP')
	spacewrap_types: EnumProperty(
		items= stItems,
		default=stDefault
	)

	stDefault, stItems = get_subtype('SETTING')
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



def get_modifier_panel(layout, ctx):
	layout.operator("object.create_modifier", text="Modifier List")
	box = layout.box()
	if ctx.object:
		for modifer in ctx.object.modifiers:
			box.label(text=modifer.name)



def get_hierarcy_panel(layout, ctx):
	box = layout.box()
	if ctx.object:
		box.prop(ctx.object, 'lock_location', text="location")
		box.prop(ctx.object, 'lock_rotation', text="Rotation")
		box.prop(ctx.object, 'rotation_mode')
		box.prop(ctx.object, 'lock_scale', text="Scale")



def get_motion_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



def get_display_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



def get_utility_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")



class Object_OT_Create_Modifier(Operator):
	bl_idname = 'object.create_modifier'
	bl_label = 'Create Modifier'
	bl_property = 'search'
	bl_description = ''

	search: EnumProperty(name='Select Modifier', items=get_modifier_list)
	
	
	def execute(self, ctx):
		print(self.search)
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		ctx.window_manager.invoke_search_popup(self)
		return{'RUNNING_MODAL'}
	
	


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
	Object_OT_Create_Modifier,
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