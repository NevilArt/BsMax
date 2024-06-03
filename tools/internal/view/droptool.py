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
# 2024/05/29

import bpy

from bpy.types import Operator
from bpy.props import EnumProperty


# This Operator makes free 'X' button in EDIT_TEXT mode
class WM_OT_Search_Operator_Cover(Operator):
	""" Call the regular search operator """
	bl_idname = 'wm.search_operator_cover'
	bl_label = "Search Operator Cover"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode != 'EDIT_TEXT'
	
	def execute(self, ctx):
		bpy.ops.wm.search_operator('INVOKE_DEFAULT')
		return {'FINISHED'}


# This Operator makes free '[' ']' buttons in EDIT_TEXT mode
class WM_OT_Side_Toolbar_Toggle(Operator):
	""" Call the regular search operator """
	bl_idname = "wm.side_toolbar_toggle"
	bl_label = "Side Toolbar Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	side: EnumProperty(
		name="Side",
		default='LEFT',
		items=[
			('LEFT', "Left", "Left toolbar Toggle"),
			('RIGHT', "Right", "Right toolbar Toggle")
		]
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		return ctx.mode != 'EDIT_TEXT'
	
	def execute(self, ctx):
		if self.side == 'LEFT':
			bpy.ops.wm.context_toggle(
				data_path='space_data.show_region_toolbar'
			)

		else:
			bpy.ops.wm.context_toggle(data_path='space_data.show_region_ui')

		return{'FINISHED'}


class View_OT_Blender_Default_Menue_Call(Operator):
	bl_idname = 'bsmax.blenderdefaultmenucall'
	bl_label = "Call Blender Menu"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	def execute(self, ctx):
		mode = ctx.mode
		if mode == 'OBJECT':
			mt = 'VIEW3D_MT_object_context_menu'

		elif mode == 'EDIT_MESH':
			mt = 'VIEW3D_MT_edit_mesh_context_menu'

		elif mode == 'EDIT_CURVE':
			mt = 'VIEW3D_MT_edit_curve_context_menu'

		elif mode == 'EDIT_METABALL':
			mt = 'VIEW3D_MT_edit_metaball_context_menu'

		elif mode == 'EDIT_ARMATURE':
			mt = 'VIEW3D_MT_armature_context_menu'

		elif mode == 'EDIT_LATTICE':
			mt = 'VIEW3D_MT_edit_lattice_context_menu'

		elif mode == 'EDIT_TEXT':
			mt = 'VIEW3D_MT_edit_text_context_menu'

		elif mode == 'POSE':
			mt = 'VIEW3D_MT_pose_context_menu'

		elif mode == 'GPENCIL_EDIT':
			mt = 'VIEW3D_MT_gpencil_edit_context_menu'

		elif mode == 'PARTICLE':
			mt = 'VIEW3D_MT_particle_context_menu'

		bpy.ops.wm.call_menu(name=mt)

		return{'FINISHED'}


class View3D_OT_Drop_Tool(Operator):
	bl_idname = 'view3d.drop_tool'
	bl_label = "Drop Tool"
	bl_options = {'REGISTER', 'INTERNAL'}

	preferences = None

	def drop_tool(self, ctx):
		tools = ctx.workspace.tools
		tool = tools.from_space_view3d_mode(ctx.mode, create=False).idname
		leagals = {
			'builtin.select',
			'builtin.select_box',
			'builtin.select_circle',
			'builtin.select_lasso',
			'builtin.cursor',
			'builtin.move',
			'builtin.rotate',
			'builtin.scale',
			'builtin.scale_cage'
		}
		
		if not tool in leagals:
			bpy.ops.wm.tool_set_by_id(name='builtin.move')
			return True
		
		return False

	def call_menu(self, _):
		if self.preferences != None:
			if self.preferences.floatmenus == "3DSMAX":
				bpy.ops.bsmax.view3dquadmenue('INVOKE_DEFAULT', menu='default')

			else:
				bpy.ops.bsmax.blenderdefaultmenucall('INVOKE_DEFAULT')

		else:
			bpy.ops.bsmax.blenderdefaultmenucall('INVOKE_DEFAULT')

	def execute(self, ctx):
		if not self.drop_tool(ctx):
			self.call_menu(ctx)

		return{'FINISHED'}



classes = {
	WM_OT_Search_Operator_Cover,
	WM_OT_Side_Toolbar_Toggle,
	View_OT_Blender_Default_Menue_Call,
	View3D_OT_Drop_Tool
}


def register_droptool(preferences):
	View3D_OT_Drop_Tool.preferences = preferences

	for cls in classes:
		bpy.utils.register_class(cls)


def unregister_droptool():
	for cls in classes:
		bpy.utils.unregister_class(cls)