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
# 2024/02/18

import bpy

from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty
from bpy.utils import register_class, unregister_class


from bpy.app import version


def get_internals_only(modifierList):
	newList = [
		modifer for modifer in modifierList if modifer[0][0] in ('B', 'O')
	]

	if newList:
		return newList

	return [('N-NONE', 'Empty', '')]


def get_mesh_modifier_list():
	modifierList = [
		# ('MESHSELECT', 'Mesh Select', ''),
		# ('PATCHSELECT', 'Patch Select', ''),
		# ('POLYSELECT', 'Poly Select', ''),
		# ('VOLSELECT', 'Vol. Select', ''),

		# ('CAMERAMAP', 'Camera Map(WSM)', ''),
		# ('DISPLACEMESH', 'Displace Mesh(WSM)', ''),
		# ('HAIRANDFUR', 'Hair and Fur(WSM)', ''),
		# ('MAPSCALLER', 'MapScaler(WSM)', ''),
		# ('PATCHDEFORM', 'PatchDeform(WSM)', ''),
		# ('PATHDEFORM', 'PathDeform(WSM)', ''),
		# ('PFLOWCOLLISION', 'Pflow Collision Shape(WSM)', ''),
		# ('POINTCACHEW', 'Point Cache(WSM)', ''),
		# ('SUBDIVIDE', 'Subdivide(WSM)', ''),
		# ('SURFACEMAPPER', 'Surface Maper(WSM)', ''),
		# ('SURFACECDEFORM', 'Surface Deform(WSM)', ''),

		# ('AFFECTREGION', 'Affect Region', ''),
		# ('ARNOLDPROPERTIES', 'Arnold Properties', ''),
		('B-ARRAY', 'Array', 'ARRAY'),
		# ('G-ARRAY', 'Array (GN)', 'Array'),
		# ('ATTRIBUTEHOLDEDR', 'Attribute Holder', ''),
		('G-BEND', 'Bend (GN)', 'Bend'),
		('B-BEND', 'Bend', 'SIMPLE_DEFORM'),
		('B-BOLLEAN', 'Boolean', 'BOOLEAN'),
		# ('CAMERAMAP', 'Camera Map', ''),
		# ('CAPHOLE', 'Cap Holes', ''),
		('B-CHAMFER', 'Chamfer', 'BEVEL'),
		# ('CLOTH', 'Cloth', ''),
		# ('CONFIRM', 'Confirm', ''),
		# ('CREASE', 'Crease', ''),
		# ('CREASESET', 'CreaseSet', ''),
		('B-DATACHANEL', 'Data Chanel (GN)', 'NODES'),
		('B-DELETEMESH', 'Delete Mesh (Mask)', 'MASK'),
		# ('DELETEPATCH', 'DeletePatch', ''),
		# ('DISPAPPROX', 'Disp Approx', ''),
		('B-DISPLACE', 'Displace', 'DISPLACE'),
		# ('G-DISPLACE', 'Displace (GN)', ''),
		# ('EDITMESH', 'Edit Mesh', ''),
		# ('EDITNORMAL', 'Edit Normal', ''),
		# ('EDITPATCH', 'Edit Patch', ''),
		# ('EDITPOLY', 'Edit Poly', ''),
		# ('FACEEXTRUD', 'Face Extrud', ''),
		('O-FFD2X2X2', 'FFD 2x2x2', 'modifier.ffd_2x2x2_set'),
		('O-FFD3X3X3', 'FFD 3x3x3', 'modifier.ffd_3x3x3_set'),
		('O-FFD4X4X4', 'FFD 4x4x4', 'modifier.ffd_4x4x4_set'),
		# ('FFDBOX', 'FFD(Box)', ''),
		# ('FFDCYL', 'FFD(Cyl)', ''),
		# ('FILTERMESHHUE', 'Filter Mesh Color By Hue', ''),
		# ('FLEX', 'Flex', ''),
		# ('HSHS', 'HSDS', ''),
		('B-LATTICE', 'Lattice', 'WIREFRAME'),
		# ('G-LATTICE', 'Lattice', ''),
		# ('LINKEDXFORM', 'Linked Xform', ''),
		# ('MAPSCALLER', 'MapScaller', ''),
		# ('MASSFXRBODY', 'MassFX RBody', ''),
		# ('MATERIAL', 'Material', ''),
		# ('MATERIALBYELEMENT', 'MaterialByElement', ''),
		# ('MCLOTH', 'mCloth', ''),
		# ('G-MELT', 'Melt', ''),
		# ('MESHCLEANER', 'Mesh Cleaner', ''),
		# ('MESHSELECT', 'Mesh Select', ''),
		# ('MESHSMOMTH', 'Mesh Smooth', ''),
		('B-MIRROR', 'Mirror', 'MIRROR'),
		# ('MORPHER', 'Morpher', ''),
		# ('MULTIRES', 'MultiRes', ''),
		# ('NOISE', 'Noise', ''),
		('B-NORMAL', 'Normal', 'NORMAL_EDIT'),
		('B-OPENSUBDIV', 'OpenSubdiv', 'SUBSURF'),
		# ('OPTIMIZE', 'Optimize', ''),
		# ('PARTICLEFORCE', 'Particle Face Creator', ''),
		# ('PARTICLESKINNER', 'Particle Skinner', ''),
		# ('PATHSELECT', 'Path Select', ''),
		('B-PATHDEFORM', 'Patch Deform (Curve)', 'CURVE'),
		# ('G-PATHDEFORM', 'Patch Deform', ''),
		('B-PHYSIQUE', 'Physique (Armature)', 'ARMATURE'),
		# ('POINTCACHE', 'Point Cache', ''),
		# ('POLYSELECT', 'Poly Select', ''),
		# ('PRESERVE', 'Preserve', ''),
		# ('PROJECTION', 'Projection', ''),
		# ('PROOPTIMIZER', 'ProOptimizer', ''),
		# ('G-PUSH', 'Push', ''),
		# ('QUDIFYMESH', 'Qudify Mesh', ''),
		# ('RELAX', 'Relax', ''),
		# ('RETOPOLOGY', 'Retopology', ''),
		('B-RIPPLE', 'Ripple', 'WAVE'),
		# ('SELECTBYCHANEL', 'Select by Chanel', ''),
		('B-SHELL', 'Shell (Solidify)', 'SOLIDIFY'),
		# ('SKEW', 'Skew', ''),
		('B-SKIN', 'Skin (Armature)', 'ARMATURE'),
		# ('SKINMORPH', 'Skin Morph', ''),
		# ('SKINWRAP', 'Skin Wrap', ''),
		# ('SKINWRAPPATCH', 'Skin Wrap Patch', ''),
		# ('SLICE', 'Slice', ''),
		# ('SMOOTH', 'Smooth', ''),
		('G-SPEREFY', 'Sperefy', 'To Sphere'),
		# ('SQUEEZE', 'Squeeze', ''),
		# ('STLCHECK', 'STL check', ''),
		('G-STRETCH', 'Stretch (GN)', 'Stretch'),
		# ('SUBDIVIDE', 'Subdivide', ''),
		# ('SUBSTITUTE', 'Substitute', ''),
		# ('SURFDEFORM', 'SurfDeform', ''),
		('B-SYMMETRY', 'Symmetry', 'MIRROR'),
		('G-TAPER', 'Taper (GN)', 'Taper'),
		('B-TESSELLATE', 'Tessellate', 'TRIANGULATE'),
		('B-TURBOSMOTH', 'Turbosmooth', 'SUBSURF'),
		# ('TURNMESH', 'Turn to Mesh', ''),
		# ('TURNPATCH', 'Turn to Patch', ''),
		# ('TURNPOLY', 'Turn to Poly', ''),
		('B-TWIST', 'Twist', 'SIMPLE_DEFORM'),
		('G-TWIST', 'Twist (GN)', 'Twist'),
		# ('UNWRAPUVW', 'Unwrap UVW', ''),
		# ('UVASCOLOR', 'UV as Color', ''),
		# ('UVASHSL', 'UV as HSL Color', ''),
		# ('UVASGRADIENT', 'UV as HSL Gradiyent', ''),
		# ('UVASBLABLA', 'UV as HSL Gradient with mid....', ''),
		# ('UVWMAPP', 'UVW Map', ''),
		# ('UVMAPPADD', 'UVW Mapping Add', ''),
		# ('UVWCLEAR', 'UVW Mapping Clear', ''),
		# ('UVWXFORM', 'UVW Xform', ''),
		# ('VERTEXWELD', 'Vertex Weld', ''),
		# ('VERTEXPAINT', 'Vertex Paint', ''),
		# ('VOLSELECT', 'Vol. Select', ''),
		('B-WAVE', 'Wave', 'WAVE'),
		# ('WEGHTEDNORMAL', 'Weghted Normals', ''),
		('B-WELDER', 'Welder', 'WELD'),
		# ('XFORM', 'Xform', '')
	]

	if version >= (3, 6, 0):
		return modifierList

	return get_internals_only(modifierList)


def get_curve_modifier_list():
	modifierList = [
		('N-NONE', 'Empty', '')
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


def get_modifier_name(key):
	parts = key.split("-")
	if len(parts) > 1:
		return parts[1]
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


def add_modifier(ctx, obj, index, key):
	category = get_modifier_class(key)

	if category == "B": # Blender Internal
		modifierType = get_modifier_node_group_name(ctx, key)
		modifierName = get_modifier_name(key)
		for obj in ctx.selected_objects:
			obj.modifiers.new(name=modifierName, type=modifierType)

	if category == "G": # Geometry Node
		nodeGroupName = get_modifier_node_group_name(ctx, key)
		nodeGroup = get_node_group(nodeGroupName)
		modifier = obj.modifiers.new(name=nodeGroupName, type='NODES')
		modifier.node_group = nodeGroup
	
	if category == "O": # Operator
		operatorIdName = get_modifier_node_group_name(ctx, key)
		exec("bpy.ops." + operatorIdName + "()")

	if category == "T": # Geometry Tool
		pass

	if category == "N": # None
		pass


class Object_OT_Create_Modifier(Operator):
	bl_idname = 'object.create_modifier'
	bl_label = 'Create Modifier'
	bl_property = 'search'
	bl_description = ''

	search: EnumProperty(name='Select Modifier', items=get_modifier_list)
	
	
	def execute(self, ctx):
		idName = self.search
		obj = ctx.object
		index = 1
		add_modifier(ctx, obj, index, idName)
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		ctx.window_manager.invoke_search_popup(self)
		return{'RUNNING_MODAL'}


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


classes = (
	Object_OT_Create_Modifier,
	Object_OT_Reset_Xform
)


def register_modifier():
	for c in classes:
		register_class(c)


def unregister_modifier():
	for c in classes:
		if hasattr(bpy.types, c.bl_idname):
			unregister_class(c)


if __name__ == "__main__":
	register_modifier()