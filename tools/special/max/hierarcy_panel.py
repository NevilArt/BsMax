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


def get_hierarcy_panel(layout, ctx):
	cPanel = ctx.scene.comand_panel
	layout.prop(cPanel, 'hierarcy_type', expand=True)

	if cPanel.hierarcy_type == 'PIVOT':
		get_hierarcy_pivot_ui(layout, ctx)

	elif cPanel.hierarcy_type == 'IK':
		get_hierarcy_ik_ui(layout, ctx)

	elif cPanel.hierarcy_type == 'LINKINFO':
		get_hierarcy_linkinfo_ui(layout, ctx)


class SCENE_OP_BsMax_Hierarchy_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Hierarchy'
	bl_idname = 'VIEW3D_PT_BsMax_hierarchy'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return ctx.scene.comand_panel.main_tab == 'HIERARCHY'
	
	def draw(self, ctx):
		get_hierarcy_panel(self.layout, ctx)


def register_hierarchy_panel():
	register_class(SCENE_OP_BsMax_Hierarchy_Panel)


def unregister_hierarchy_panel():
	unregister_class(SCENE_OP_BsMax_Hierarchy_Panel)


if __name__ == "__main__":
	register_hierarchy_panel()