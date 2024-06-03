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


def get_display_color_panel(layout, ctx):
	box = layout.box()
	box.label(text="Coming soon")


def get_display_hide_category_panel(layout, ctx):
	space_data = ctx.space_data
	layout.prop(
		space_data.overlay, 'show_overlays', text="Show Renderable Only"
	)

	box = layout.box()
	col = box.column()
	col.prop(space_data, 'show_object_viewport_speaker')
	col.prop(space_data, 'show_object_viewport_camera')
	col.prop(space_data, 'show_object_viewport_light_probe')
	col.prop(space_data, 'show_object_viewport_light')
	col.prop(space_data, 'show_object_viewport_empty')
	col.prop(space_data, 'show_object_viewport_lattice')
	col.prop(space_data, 'show_object_viewport_armature')
	col.prop(space_data, 'show_object_viewport_grease_pencil')
	col.prop(space_data, 'show_object_viewport_volume')
	col.prop(space_data, 'show_object_viewport_pointcloud')
	col.prop(space_data, 'show_object_viewport_curves')
	col.prop(space_data, 'show_object_viewport_font')
	col.prop(space_data, 'show_object_viewport_meta')
	col.prop(space_data, 'show_object_viewport_surf')
	col.prop(space_data, 'show_object_viewport_curve')
	col.prop(space_data, 'show_object_viewport_mesh')

	row = layout.row()
	row.operator('bsmax.reserved', text="All")
	row.operator('bsmax.reserved', text="None")
	row.operator('bsmax.reserved', text="Invert")


def get_display_hide_panel(layout, ctx):
	box = layout.box()
	col = box.column()
	col.operator("object.hide", text="Hide Selected").mode='SELECTION'
	col.operator("object.hide", text="Hide Unselected").mode='UNSELECTED'
	col.operator('bsmax.reserved', text="Hide By Name")
	col.operator('bsmax.reserved', text="Hide by Hit")

	col = box.column()
	col.operator("object.hide", text="Unhide all").mode='CLEAR'
	col.operator('bsmax.reserved', text="Unhide by name")

	layout.operator('bsmax.reserved', text="Hide Frozen Objects")


def get_display_freeze_panel(layout, ctx):
	space_data = ctx.space_data
	box = layout.box()
	col = box.column()
	col.prop(space_data, 'show_object_select_mesh')
	col.prop(space_data, 'show_object_select_curve')
	col.prop(space_data, 'show_object_select_surf')
	col.prop(space_data, 'show_object_select_meta')
	col.prop(space_data, 'show_object_select_font')
	col.prop(space_data, 'show_object_select_curves')
	col.prop(space_data, 'show_object_select_pointcloud')
	col.prop(space_data, 'show_object_select_volume')
	col.prop(space_data, 'show_object_select_grease_pencil')
	col.prop(space_data, 'show_object_select_armature')
	col.prop(space_data, 'show_object_select_lattice')
	col.prop(space_data, 'show_object_select_empty')
	col.prop(space_data, 'show_object_select_light')
	col.prop(space_data, 'show_object_select_light_probe')
	col.prop(space_data, 'show_object_select_camera')
	col.prop(space_data, 'show_object_select_speaker')

	row = layout.row()
	row.operator('bsmax.reserved', text="All")
	row.operator('bsmax.reserved', text="None")
	row.operator('bsmax.reserved', text="Invert")


def get_display_properties_panel(layout, ctx):
	space_data = ctx.space_data
	box = layout.box()
	col = box.column()
	col.operator('bsmax.reserved', text="Display as Box")
	col.prop(
		space_data.shading, 'show_backface_culling', text="Backfacec Cull"
	)

	col.operator('bsmax.reserved', text="Edge Only")
	col.operator('bsmax.reserved', text="Vertex Ticks")
	col.prop(space_data.overlay,  'show_motion_paths', text="Motion Path")
	col.prop(space_data.shading,  'show_xray', text="See-Through")
	col.operator('bsmax.reserved', text="Ignore Extents")
	col.operator('bsmax.reserved', text="Show Frozen in Gray")
	col.operator('bsmax.reserved', text="Never Degrade")



def get_display_links_panel(layout, ctx):
	col = layout.column()
	col.prop(
		ctx.space_data.overlay, 'show_relationship_lines', text="Display Links"
	)
	col.operator('bsmax.reserved', text="Link Replace Objects")
	

class SCENE_OP_BsMax_Display_Color_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Display Color"
	bl_idname = 'VIEW3D_PT_BsMax_display_color'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_color_panel(self.layout, ctx)


class SCENE_OP_BsMax_Display_Hide_category_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Hide by Category"
	bl_idname = 'VIEW3D_PT_BsMax_display_hide_category'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_hide_category_panel(self.layout, ctx)


class SCENE_OP_BsMax_Display_Hide_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Hide"
	bl_idname = 'VIEW3D_PT_BsMax_display_hide'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_hide_panel(self.layout, ctx)


class SCENE_OP_BsMax_Display_Freeze_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Freeze"
	bl_idname = 'VIEW3D_PT_BsMax_display_freeze'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_freeze_panel(self.layout, ctx)


class SCENE_OP_BsMax_Display_Properties_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Display Properties"
	bl_idname = 'VIEW3D_PT_BsMax_display_properties'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_properties_panel(self.layout, ctx)


class SCENE_OP_BsMax_Display_Links_Panel(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Display Properties"
	bl_idname = 'VIEW3D_PT_BsMax_display_links'
	bl_category = "BsMax"

	@classmethod
	def poll(self, ctx):
		return ctx.scene.command_panel.main_tab == 'DISPLAY'
	
	def draw(self, ctx):
		get_display_links_panel(self.layout, ctx)


classes = {
	SCENE_OP_BsMax_Display_Color_Panel,
	SCENE_OP_BsMax_Display_Hide_category_Panel,
	SCENE_OP_BsMax_Display_Hide_Panel,
	SCENE_OP_BsMax_Display_Freeze_Panel,
	SCENE_OP_BsMax_Display_Properties_Panel,
	SCENE_OP_BsMax_Display_Links_Panel
}


def register_display_panel():
	for cls in classes:
	    register_class(cls)


def unregister_display_panel():
	for cls in classes:
		if cls.is_registered:
			unregister_class(cls)


if __name__ == '__main__':
	register_display_panel()