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
	if 'main_tab' in ctx.scene.command_panel:
		if ctx.scene.command_panel['main_tab'] == 2:
			return ctx.mode == 'EDIT_CURVE'
	return False


def get_curve_rendering(layout, ctx):
	box = layout.box()
	# box.operator('bsmax.reserved', text='Enable In Render')
	# box.operator('bsmax.reserved', text='Enable In Viewport')

	# box.operator('bsmax.reserved', text='Generate Mapping Coolds.')

	box1 = box.box()
	row = box1.row()
	curve = ctx.object.data
	row.prop(curve, "bevel_mode", expand=True)

	box1.use_property_split = True

	col = box1.column()
	if curve.bevel_mode == 'OBJECT':
		col.prop(curve, "bevel_object", text="Object")
	else:
		col.prop(curve, "bevel_depth", text="Depth")
		col.prop(curve, "bevel_resolution", text="Resolution")
	col.prop(curve, "use_fill_caps")

	if curve.bevel_mode == 'PROFILE':
		col.template_curveprofile(curve, "bevel_profile")
	

def get_curve_surface_properties(layout, ctx):
	ob = ctx.object
	is_sortable = len(ob.material_slots) > 1
	rows = 4 if is_sortable else 3

	row = layout.row()
	row.template_list(
		"MATERIAL_UL_matslots", "", ob,
		"material_slots", ob, "active_material_index", rows=rows
	)

	col = row.column(align=True)
	col.operator("object.material_slot_add", icon='ADD', text="")
	col.operator("object.material_slot_remove_plus", icon='REMOVE', text="")
	col.separator()
	col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")

	if is_sortable:
		col.separator()
		col.operator(
			"object.material_slot_move", icon='TRIA_UP', text=""
		).direction = 'UP'
		
		col.operator(
			"object.material_slot_move", icon='TRIA_DOWN', text=""
		).direction = 'DOWN'

	if ob.mode == 'EDIT':
		row = layout.row(align=True)
		row.operator("object.material_slot_assign", text="Assign")
		row.operator("object.material_slot_select", text="Select")
		row.operator("object.material_slot_deselect", text="Deselect")

	row = layout.row()
	row.template_ID(ob, "active_material", new="material.new")


def get_curve_interpolation(layout, ctx):
	box = layout.box()
	curve = ctx.object.data

	box.prop(curve, "resolution_u", text="Resolution Preview U")
	box.prop(curve, "render_resolution_u", text="Render Resolution")

	row = box.row()
	row.prop(curve, "use_radius", text="Radius")
	row.prop(curve, "use_stretch", text="Stretch")
	row.prop(curve, "use_deform_bounds", text="Bounds Clamp")


def get_curve_selection(layout, ctx):
	box = layout.box()
	row = box.row()
	mesh_option = ctx.scene.mesh_select_option
	row.prop(mesh_option, 'by_element', text="", icon="SNAP_VOLUME")

	box = layout.box()
	row = box.row()
	row.operator('curve.select_less', text="Shrink")

	row1= row.row(align=True)
	row1.operator('curve.select_previous', text="", icon="TRIA_LEFT")
	row1.operator('curve.select_more', text="Grow")
	row1.operator('curve.select_next', text="", icon="TRIA_RIGHT")
	
	row = box.row()
	row.operator('curve.select_linked', text="Linked")
	

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


def get_curve_geometry(layout, ctx):
	pass


class BsMax_PT_CP_EditCurve_Rendering(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_rendering'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Rendering'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_rendering(layout, ctx)


class BsMax_PT_CP_EditCurve_Surface_Properties(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_surface_properties'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Surfacec Properties (Material IDs)'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_surface_properties(layout, ctx)


class BsMax_PT_CP_EditCurve_Interpolation(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_interpolation'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Interpolation'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_interpolation(layout, ctx)


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


class BsMax_PT_CP_EditCurve_Geometry(Panel):
	bl_idname = 'BSMAX_PT_cp_editcurve_geometry'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Geometry'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_curve(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_curve_geometry(layout, ctx)


# class CURVE_MT_Extrude_Tools(Menu):
# 	bl_idname = "CURVE_MT_extrude_tools"
# 	bl_label = "Extrud"

# 	def draw(self, ctx):
# 		layout = self.layout


classes = (
	BsMax_PT_CP_EditCurve_Rendering,
	BsMax_PT_CP_EditCurve_Surface_Properties,
	BsMax_PT_CP_EditCurve_Interpolation,
	BsMax_PT_CP_EditCurve_Selection,
	BsMax_PT_CP_EditCurve_Soft_Selection,
	BsMax_PT_CP_EditCurve_Geometry
)


def register_edit_curve():
	for c in classes:
		register_class(c)


def unregister_edit_curve():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_edit_curve()