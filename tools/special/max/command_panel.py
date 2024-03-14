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

import bpy

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, IntProperty
from bpy.utils import register_class, unregister_class


def get_create_subtype(createType):
	default = 'STANDARD'
	items = [('STANDARD', 'Standard', '')]

	if createType == "MESH":
		default = 'STANDARD'
		items = [
			('STANDARD', 'Standard Primitives', ''),
			('EXTENDED', 'Extended Primitives', ''),
			('COMPOUND', 'Compound Objects', ''),
			('PARTICLE', 'Particle System', ''),
			('PATHGRIDE', 'Path Gride', ''),
			('BODY', 'Body Objects', ''),
			('ARCHITECTURE', 'Architecture', ''),
			('NURBS', 'Nurbs Surface',  ''),
			('POINTCLOUD', 'Point Cloud objects', ''),
			('DYNAMIC', 'Dynamic objects', ''),
			('ABC', 'Alembic', ''),
			('FLUIDS', 'Fluids', '')
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


def modifer_panel_update(self, _):
	bpy.ops.object.active_modifier(index=self.active_modifier)


class BsMax_Command_Panel(PropertyGroup):
	main_tab: EnumProperty(
		default='CREATE',
		items=[
			('CREATE', 'Create', '', 'ADD', 1),
			('MODIFY', 'Modify', '', 'FULLSCREEN_ENTER', 2),
			('HIERARCHY', 'Hierarchy', '', 'PARTICLES', 3),
			('MOTION', 'Motion', '', 'PHYSICS', 4),
			('DISPLAY', 'Display', '', 'WORKSPACE', 5),
			('UTILITIES', 'Utilities', '', 'MODIFIER', 6)
		]
	)

	create_type: EnumProperty(
		items=[
			('MESH', 'Mesh', '', 'NODE_MATERIAL', 1),
			('CURVE', 'Curve', '', 'MOD_SUBSURF', 2),
			('LIGHT', 'Light', '', 'LIGHT_DATA', 3),
			('CAMERA', 'Camera', '', 'CAMERA_DATA', 4),
			('EMPTY', 'Empty', '', 'MODIFIER_DATA', 5),
			('SPACEWRAP', 'Spacewrap', '', 'FORCE_FORCE', 6),
			('SETTING', 'Setting', '', 'SETTINGS', 7)
		],
		default='MESH',
	)

	hierarcy_type: EnumProperty(
		items=[
			('PIVOT', 'Pivot', ''),
			('IK', 'IK', ''),
			('LINKINFO', 'Link Info', ''),
		],
		default='LINKINFO',
	)

	stDefault, stItems = get_create_subtype('MESH')
	mesh_types: EnumProperty(
		items=stItems, default=stDefault
	)

	stDefault, stItems = get_create_subtype('CURVE')
	curve_types: EnumProperty(
		items=stItems, default=stDefault
	)

	stDefault, stItems = get_create_subtype('LIGHT')
	light_types: EnumProperty(
		items=stItems, default=stDefault
	)

	stDefault, stItems = get_create_subtype('CAMERA')
	camera_types: EnumProperty(
		items=stItems,
		default=stDefault
	)

	stDefault, stItems = get_create_subtype('EMPTY')
	empty_types: EnumProperty(
		items=stItems, default=stDefault
	)

	stDefault, stItems = get_create_subtype('SPACEWRAP')
	spacewrap_types: EnumProperty(
		items=stItems, default=stDefault
	)

	stDefault, stItems = get_create_subtype('SETTING')
	setting_types: EnumProperty(
		items=stItems, default=stDefault
	)

	active_modifier: IntProperty(update=modifer_panel_update)


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
		cPanel = ctx.scene.command_panel

		layout.prop(cPanel, 'main_tab', expand=True)


classes = (
	BsMax_OT_Reserved,
	BsMax_Command_Panel,
	SCENE_OP_BsMax_Side_Panel
)


def register_command_panel():
	for c in classes:
		register_class(c)
	
	bpy.types.Scene.command_panel = PointerProperty(type=BsMax_Command_Panel)


def unregister_command_panel():
	#TODO check is class exist before remove
	for c in classes:
		try:
			unregister_class(c)
		except:
			pass


if __name__ == "__main__":
	register_command_panel()