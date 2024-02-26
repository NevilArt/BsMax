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
# 2024/02/25

from bpy.types import Panel, Menu
from bpy.utils import register_class, unregister_class


def is_edit_curve(ctx):
	if 'main_tab' in ctx.scene.comand_panel:
		if ctx.scene.comand_panel['main_tab'] == 2:
			return ctx.mode == 'EDIT_CURVE'
	return False


def get_curve_selection(layout, ctx):
	pass
	

def get_curve_soft_selection(layout, ctx):
	box = layout.box()
	row = box.row()
	row.prop(
		ctx.tool_settings, "use_proportional_edit",
		text="Use Soft Selection"
	)

	box.prop(ctx.scene.tool_settings, "use_proportional_connected")
	box.prop(ctx.scene.tool_settings, "use_proportional_projected")

	row = box.row()
	row.prop(
		ctx.scene.tool_settings, "proportional_distance",
		text=""
	)
	
	row.prop(
		ctx.scene.tool_settings, "proportional_edit_falloff",
		text=""
	)


class BsMax_PT_CP_EditCurve_Selection(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_selection'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Selection'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_selection(layout, ctx)


class BsMax_PT_CP_EditCurve_Soft_Selection(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_soft_selection'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Soft Selection'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_soft_selection(layout, ctx)


# class CURVE_MT_Extrude_Tools(Menu):
# 	bl_idname = "CURVE_MT_extrude_tools"
# 	bl_label = "Extrud"

# 	def draw(self, ctx):
# 		layout = self.layout


classes = (
	BsMax_PT_CP_EditCurve_Selection,
	BsMax_PT_CP_EditCurve_Soft_Selection
)


def register_edit_curve():
	for c in classes:
		register_class(c)


def unregister_edit_curve():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_edit_curve()