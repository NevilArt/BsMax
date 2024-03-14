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
# 2024/03/06

import bpy

from bpy.types import Operator, Panel, UIList
from bpy.props import StringProperty, EnumProperty, IntProperty
from bpy.utils import register_class, unregister_class

from bpy.app import version

from bsmax.state import is_primitive
from bsmax.primitive_ui import get_primitive_edit_panel


def get_internals_only(modifierList):
	newList = [
		modifer for modifer in modifierList if modifer[0][0] in ('B', 'O')
	]

	if newList:
		return newList

	return [('N-NONE', 'Empty', '')]


def get_mesh_modifier_list():
	modifierList = [
		# ('MESHSELECT', 'Mesh Select', ''),1
		# ('PATCHSELECT', 'Patch Select', ''),2
		# ('POLYSELECT', 'Poly Select', ''),3
		# ('VOLSELECT', 'Vol. Select', ''),4

		# ('CAMERAMAP', 'Camera Map(WSM)', ''),5
		# ('DISPLACEMESH', 'Displace Mesh(WSM)', ''),6
		# ('HAIRANDFUR', 'Hair and Fur(WSM)', ''),7
		# ('MAPSCALLER', 'MapScaler(WSM)', ''),8
		# ('PATCHDEFORM', 'PatchDeform(WSM)', ''),9
		# ('PATHDEFORM', 'PathDeform(WSM)', ''),10
		# ('PFLOWCOLLISION', 'Pflow Collision Shape(WSM)', ''),11
		# ('POINTCACHEW', 'Point Cache(WSM)', ''),12
		# ('SUBDIVIDE', 'Subdivide(WSM)', ''),13
		# ('SURFACEMAPPER', 'Surface Maper(WSM)', ''),14
		# ('SURFACECDEFORM', 'Surface Deform(WSM)', ''),15

		# ('AFFECTREGION', 'Affect Region', ''),16
		# ('ARNOLDPROPERTIES', 'Arnold Properties', ''),17
		('B-ARRAY', 'Array', 'ARRAY', 'MOD_ARRAY', 18),
		# ('G-ARRAY', 'Array (GN)', 'Array'),19
		# ('ATTRIBUTEHOLDEDR', 'Attribute Holder', ''),20
		('G-BEND', 'Bend', 'Bend', 'GEOMETRY_NODES', 21),
		('B-BEND', 'Bend', 'SIMPLE_DEFORM', 'MOD_SIMPLEDEFORM', 22),
		('B-BOLLEAN', 'Boolean', 'BOOLEAN', 'MOD_BOOLEAN', 23),
		# ('CAMERAMAP', 'Camera Map', ''),24
		# ('CAPHOLE', 'Cap Holes', ''),25
		('B-CHAMFER', 'Chamfer', 'BEVEL', 'MOD_BEVEL', 26),
		# ('CLOTH', 'Cloth', ''),27
		# ('CONFIRM', 'Confirm', ''),28
		# ('CREASE', 'Crease', ''),29
		# ('CREASESET', 'CreaseSet', ''),30
		('B-DATACHANEL', 'Data Chanel', 'NODES', 'GEOMETRY_NODES', 31),
		('B-DELETEMESH', 'Delete Mesh (Mask)', 'MASK', 'MOD_MASK', 32),
		# ('DELETEPATCH', 'DeletePatch', ''),33
		# ('DISPAPPROX', 'Disp Approx', ''),34
		('B-DISPLACE', 'Displace', 'DISPLACE', 'MOD_DISPLACE', 35),
		# ('G-DISPLACE', 'Displace (GN)', ''),36
		# ('EDITMESH', 'Edit Mesh', ''),37
		# ('EDITNORMAL', 'Edit Normal', ''),38
		# ('EDITPATCH', 'Edit Patch', ''),39
		# ('EDITPOLY', 'Edit Poly', ''),40
		# ('FACEEXTRUD', 'Face Extrud', ''),41
		('O-FFD2X2X2', 'FFD 2x2x2', 'modifier.ffd_2x2x2_set', 'MOD_LATTICE', 42),
		('O-FFD3X3X3', 'FFD 3x3x3', 'modifier.ffd_3x3x3_set', 'MOD_LATTICE', 43),
		('O-FFD4X4X4', 'FFD 4x4x4', 'modifier.ffd_4x4x4_set', 'MOD_LATTICE', 44),
		# ('FFDBOX', 'FFD(Box)', ''),45
		# ('FFDCYL', 'FFD(Cyl)', ''),46
		# ('FILTERMESHHUE', 'Filter Mesh Color By Hue', ''),47
		# ('FLEX', 'Flex', ''),48
		# ('HSHS', 'HSDS', ''),49
		('B-LATTICE', 'Lattice', 'WIREFRAME', 'MOD_WIREFRAME', 50),
		# ('G-LATTICE', 'Lattice', ''),51
		# ('LINKEDXFORM', 'Linked Xform', ''),52
		# ('MAPSCALLER', 'MapScaller', ''),53
		# ('MASSFXRBODY', 'MassFX RBody', ''),54
		# ('MATERIAL', 'Material', ''),55
		# ('MATERIALBYELEMENT', 'MaterialByElement', ''),56
		# ('MCLOTH', 'mCloth', ''),57
		# ('G-MELT', 'Melt', ''),58
		# ('MESHCLEANER', 'Mesh Cleaner', ''),59
		# ('MESHSELECT', 'Mesh Select', ''),60
		# ('MESHSMOMTH', 'Mesh Smooth', ''),61
		('B-MIRROR', 'Mirror', 'MIRROR', 'MOD_MIRROR', 62),
		# ('MORPHER', 'Morpher', ''),63
		# ('MULTIRES', 'MultiRes', ''),64
		# ('NOISE', 'Noise', ''),65
		('B-NORMAL', 'Normal', 'NORMAL_EDIT', 'MOD_NORMALEDIT', 66),
		('B-OPENSUBDIV', 'OpenSubdiv', 'SUBSURF', 'MOD_SUBSURF', 67),
		# ('OPTIMIZE', 'Optimize', ''),68
		# ('PARTICLEFORCE', 'Particle Face Creator', ''),69
		# ('PARTICLESKINNER', 'Particle Skinner', ''),70
		# ('PATHSELECT', 'Path Select', ''),71
		('B-PATHDEFORM', 'Patch Deform (Curve)', 'CURVE', 'MOD_CURVE', 72),
		# ('G-PATHDEFORM', 'Patch Deform', ''),73
		('B-PHYSIQUE', 'Physique (Armature)', 'ARMATURE', 'MOD_ARMATURE', 74),
		# ('POINTCACHE', 'Point Cache', ''),75
		# ('POLYSELECT', 'Poly Select', ''),76
		# ('PRESERVE', 'Preserve', ''),77
		# ('PROJECTION', 'Projection', ''),78
		# ('PROOPTIMIZER', 'ProOptimizer', ''),79
		# ('G-PUSH', 'Push', ''),80
		# ('QUDIFYMESH', 'Qudify Mesh', ''),81
		# ('RELAX', 'Relax', ''),82
		# ('RETOPOLOGY', 'Retopology', ''),83
		('B-RIPPLE', 'Ripple', 'WAVE', 'MOD_WAVE', 84),
		# ('SELECTBYCHANEL', 'Select by Chanel', ''),85
		('B-SHELL', 'Shell (Solidify)', 'SOLIDIFY', 'MOD_SOLIDIFY', 86),
		# ('SKEW', 'Skew', ''),87
		('B-SKIN', 'Skin (Armature)', 'ARMATURE', 'MOD_ARMATURE', 88),
		# ('SKINMORPH', 'Skin Morph', ''),89
		# ('SKINWRAP', 'Skin Wrap', ''),90
		# ('SKINWRAPPATCH', 'Skin Wrap Patch', ''),91
		# ('SLICE', 'Slice', ''),92
		# ('SMOOTH', 'Smooth', ''),93
		('G-SPEREFY', 'Sperefy', 'To Sphere', 'GEOMETRY_NODES', 94),
		# ('SQUEEZE', 'Squeeze', ''),95
		# ('STLCHECK', 'STL check', ''),96
		('G-STRETCH', 'Stretch', 'Stretch', 'GEOMETRY_NODES', 97),
		# ('SUBDIVIDE', 'Subdivide', ''),98
		# ('SUBSTITUTE', 'Substitute', ''),99
		# ('SURFDEFORM', 'SurfDeform', ''),100
		('B-SYMMETRY', 'Symmetry', 'MIRROR', 'MOD_MIRROR', 101),
		('G-TAPER', 'Taper', 'Taper', 'GEOMETRY_NODES', 102),
		('B-TESSELLATE', 'Tessellate', 'TRIANGULATE', 'MOD_TRIANGULATE', 103),
		('B-TURBOSMOTH', 'Turbosmooth', 'SUBSURF', 'MOD_SUBSURF', 104),
		# ('TURNMESH', 'Turn to Mesh', ''),105
		# ('TURNPATCH', 'Turn to Patch', ''),106
		# ('TURNPOLY', 'Turn to Poly', ''),107
		('B-TWIST', 'Twist', 'SIMPLE_DEFORM', 'MOD_SIMPLEDEFORM', 108),
		('G-TWIST', 'Twist', 'Twist', 'GEOMETRY_NODES', 109),
		# ('UNWRAPUVW', 'Unwrap UVW', ''),110
		# ('UVASCOLOR', 'UV as Color', ''),111
		# ('UVASHSL', 'UV as HSL Color', ''),112
		# ('UVASGRADIENT', 'UV as HSL Gradiyent', ''),113
		# ('UVASBLABLA', 'UV as HSL Gradient with mid....', ''),114
		# ('UVWMAPP', 'UVW Map', ''),115
		# ('UVMAPPADD', 'UVW Mapping Add', ''),116
		# ('UVWCLEAR', 'UVW Mapping Clear', ''),117
		# ('UVWXFORM', 'UVW Xform', ''),118
		# ('VERTEXWELD', 'Vertex Weld', ''),119
		# ('VERTEXPAINT', 'Vertex Paint', ''),120
		# ('VOLSELECT', 'Vol. Select', ''),121
		('B-WAVE', 'Wave', 'WAVE', 'MOD_WAVE', 122),
		# ('WEGHTEDNORMAL', 'Weghted Normals', ''),123
		('B-WELDER', 'Welder', 'WELD', 'AUTOMERGE_ON', 124),
		# ('XFORM', 'Xform', '')125
	]

	if version >= (3, 6, 0):
		return modifierList

	return get_internals_only(modifierList)


def get_curve_modifier_list():
	modifierList = [
		('B-GEOMETRYNODE', 'Geometry Node', 'NODES', 'GEOMETRY_NODES', 1),
		('B-CACHE', 'Mesh Cache', 'MESH_CACHE', 'MOD_MESHDEFORM', 2),
		('B-SEQUENCECACHE', 'Mesh Sequence Cache', 'MESH_SEQUENCE_CACHE', 'MOD_MESHDEFORM', 3)
	]

	if version >= (3, 6, 0):
		return modifierList

	return get_internals_only(modifierList)
	

def get_modifier_list(_, ctx):
	if not ctx.object:
		return [('N-NONE', 'Empty', '')]
	
	if ctx.object.type == 'MESH':
		return get_mesh_modifier_list()

	if ctx.object.type == 'CURVE':
		return get_curve_modifier_list()


def get_modifier_class(key):
	parts = key.split("-")
	if len(parts) > 1:
		return parts[0]
	return "B"


def get_modifier_name(modidiferList, key):
	for modifier in modidiferList:
		if key == modifier[0]:
			return modifier[1]
	return key


def get_node_group(nodeGroup):
	if nodeGroup in bpy.data.node_groups:
		return bpy.data.node_groups[nodeGroup]

	bpy.ops.scene.import_node_groupe(name=nodeGroup)

	if nodeGroup in bpy.data.node_groups:
		return bpy.data.node_groups[nodeGroup]

	return None


def get_modifier_node_group_name(ctx, key):
	for pack in get_modifier_list(None, ctx):
		if pack[0] == key:
			return pack[2]
	return None


def add_modifier(ctx, obj, modiferList, key):
	category = get_modifier_class(key)
	modifierName = get_modifier_name(modiferList, key)

	if category == "B": # Blender Internal
		modifierType = get_modifier_node_group_name(ctx, key)
		for obj in ctx.selected_objects:
			obj.modifiers.new(name=modifierName, type=modifierType)

	if category == "G": # Geometry Node
		nodeGroupName = get_modifier_node_group_name(ctx, key)
		nodeGroup = get_node_group(nodeGroupName)
		modifier = obj.modifiers.new(name=nodeGroupName, type='NODES')
		modifier.node_group = nodeGroup
		modifier.name = modifierName
	
	if category == "O": # Operator
		operatorIdName = get_modifier_node_group_name(ctx, key)
		exec("bpy.ops." + operatorIdName + "()")

	if category == "T": # Geometry Tool
		pass

	if category == "N": # None
		pass


def get_base_object_name(ctx):
	obj = ctx.object
	if not obj:
		return ""

	if is_primitive(ctx):
		return obj.data.primitivedata.classname
	elif obj.type == 'MESH':
		return "Editable Mesh/Poly"
	elif obj.type == 'CURVE':
		return "Editable Curve"

	return obj.name


class OBJECT_UL_modifier_list(UIList):

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
		scene = data
		ob = item

		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(ob, "name", text="", emboss=False, icon_value=layout.icon(ob))


def get_modifier_panel(layout, ctx):
	layout.operator("object.create_modifier", text="Modifier List")

	col = layout.box().column()

	col.template_list(
			"OBJECT_UL_modifier_list",
			"",
			ctx.object,
			"modifiers",
			ctx.scene.command_panel,
			"active_modifier")

	col.operator('object.edit_mode_toggle', text=get_base_object_name(ctx))
	
	if is_primitive(ctx):
		box =layout.box()
		box.operator("primitive.cleardata", text="Collaps Primitive Data")
		get_primitive_edit_panel(ctx.object.data.primitivedata, box)


class Object_OT_Create_Modifier(Operator):
	bl_idname = 'object.create_modifier'
	bl_label = 'Create Modifier'
	bl_property = 'search'
	bl_description = ''

	search: EnumProperty(name='Select Modifier', items=get_modifier_list)
	
	def execute(self, ctx):
		modifierList = get_modifier_list(None, ctx) 
		add_modifier(ctx, ctx.object, modifierList, self.search)
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		ctx.window_manager.invoke_search_popup(self)
		return{'RUNNING_MODAL'}


class Object_OT_Active_Modifier(Operator):
	bl_idname = 'object.active_modifier'
	bl_label = 'Active Modifier'
	bl_options = {'REGISTER', 'INTERNAL'}

	index: IntProperty()
	
	def execute(self, ctx):
		if self.index < len(ctx.object.modifiers):
			ctx.object.modifiers[self.index].is_active = True
		return{'FINISHED'}


class Object_OT_Edit_Mode_Toggle(Operator):
	bl_idname = 'object.edit_mode_toggle'
	bl_label = 'Edit Mode Toggle'
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		if not is_primitive(ctx):
			bpy.ops.bsmax.mode_set()
		return{'FINISHED'}
	

class Modifier_OT_Add_Geodifier(Operator):
	bl_idname = "modifier.add_geodifier"
	bl_label = "ADD Geodifier"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	idname: StringProperty()

	def execute(self, ctx):
		return{"FINISHED"}


class Object_OT_Reset_Xform(Operator):
	bl_idname = "object.reset_xform"
	bl_label = "Reset Xform"

	@classmethod
	def poll(self, ctx):
		return ctx.object

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			ctx.view_layer.objects.active = obj
			bpy.ops.object.transform_apply(
				location=False,rotation=True,scale=True
			)

		ctx.view_layer.objects.active = obj
		return{"FINISHED"}


class SCENE_OP_BsMax_Modifier_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Modifier'
	bl_idname = 'VIEW3D_PT_BsMax_modifier'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'MODIFY'
	
	def draw(self, ctx):
		get_modifier_panel(self.layout, ctx)


classes = (
	Object_OT_Create_Modifier,
	Object_OT_Active_Modifier,
	Object_OT_Edit_Mode_Toggle,

	Object_OT_Reset_Xform,

	OBJECT_UL_modifier_list,
	SCENE_OP_BsMax_Modifier_Panel
)


def register_modifier_panel():
	for c in classes:
		register_class(c)


def unregister_modifier_panel():
	for c in classes:
		if hasattr(bpy.types, c.bl_idname):
			unregister_class(c)


if __name__ == "__main__":
	# unregister_modifier_panel()
	register_modifier_panel()