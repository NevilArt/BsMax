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

""" Note: this file is not active yet """

import bpy
from bpy.types import WorkSpaceTool

class CurveFilletTool(WorkSpaceTool):
	bl_space_type='VIEW_3D'
	bl_context_mode='EDIT_CURVE'
	bl_options = {'REGISTER', 'UNDO'}

	""" The prefix of the idname should be your add-on name """
	bl_idname = "bsmax.curvefillet"
	bl_label = "Fillet (Curve)"
	bl_description = ( "This is a tooltip")
	#bl_icon = "ops.generic.select_circle"
	bl_widget = None

	def draw_settings(ctx, layout, tool):
		props = tool.operator_properties("curve.chamfer")

class CurveChamferTool(WorkSpaceTool):
	bl_space_type='VIEW_3D'
	bl_context_mode='EDIT_CURVE'

	bl_idname = "bsmax.curvechamfer"
	bl_label = "Chamfer (Curve)"
	bl_description = ("This is a tooltip")
	#bl_icon = "ops.generic.select_lasso"
	bl_widget = None

	def draw_settings(ctx, layout, tool):
		# props = tool.operator_properties("view3d.select_lasso")
		# layout.prop(props, "mode")
		pass

def panel_cls(register):
	if register:
		bpy.utils.register_tool(CurveFilletTool, after={"builtin.randomize"}, separator=True, group=True)
		bpy.utils.register_tool(CurveChamferTool, after={CurveFilletTool.bl_idname})
	else:
		bpy.utils.unregister_tool(CurveFilletTool)
		bpy.utils.unregister_tool(CurveChamferTool)

if __name__ == '__main__':
	panel_cls(True)

__all__ = ["panel_cls"]