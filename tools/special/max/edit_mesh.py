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


def is_edit_mesh(ctx):
	if 'main_tab' in ctx.scene.comand_panel:
		if ctx.scene.comand_panel['main_tab'] == 2:
			return ctx.mode == 'EDIT_MESH'
	return False


def get_mesh_selection(layout, ctx):
	box = layout.box()
	row = box.row()

	row.template_header_3D_mode()
	mesh_option = ctx.scene.mesh_select_option
	row.prop(mesh_option, 'by_element', text="", icon="SNAP_VOLUME")

	if mesh_option.by_element:
		box = box.box()
		row = box.row()
		row.prop(mesh_option, 'normal', text="", icon="SNAP_NORMAL")
		row.prop(mesh_option, 'material', text="", icon="MATERIAL")
		row.prop(mesh_option, 'seam', text="", icon="META_BALL")
		row.prop(mesh_option, 'sharp', text="", icon="MOD_SOLIDIFY")
		row.prop(mesh_option, 'uv', text="", icon="UV")

	box = layout.box()
	row = box.row()
	row.operator("view3d.toggle_xray", text="Backface")
	row.operator("bsmax.reserved", text="Occluded")
	
	box = layout.box()
	row = box.row()
	row.operator('mesh.select_less', text="Shrink")
	row.operator('mesh.select_more', text="Grow")

	row = box.row()
	row.operator('mesh.smart_select_ring', text="Ring")
	row.operator('mesh.smart_select_loop', text="Loop")


def get_mesh_soft_selection(layout, ctx):
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


def get_mesh_edit_vertex_mode(layout, ctx):
	row = layout.row()
	row.operator('mesh.remove', text="Remove").vert=False
	row.operator('bsmax.reserved', text="Break")
	
	row = layout.row()
	row1 = row.row(align=True)
	row1.operator(
		'mesh.tool_set_by_id', text="Extrude"
	).name="builtin.extrude_region"
	row1.operator(
		'wm.call_menu', text='', icon='TOPBAR'
	).name = "MESH_MT_extrude_tools"

	row.operator('mesh.remove_doubles', text="Weld")

	row = layout.row()
	row.operator('mesh.tool_set_by_id', text="Chamfer").name="builtin.bevel"
	row.operator('mesh.target_weld', text="Target Weld")

	row = layout.row()
	row.operator('mesh.connect', text="Connect")

	layout.operator('mesh.delete_loose', text="Remove Isolated Vertices")
	layout.operator('bsmax.reserved', text="Remove Unused Map Verts")

	box = layout.box()
	box.operator('bsmax.reserved', text="Weight")
	box.operator('bsmax.reserved', text="Crease")


def get_mesh_edit_edge_mode(layout, ctx):
	layout.operator('bsmax.reserved', text="Insert Vertex")

	row = layout.row()
	row.operator('mesh.remove', text="Remove").vert=False
	row.operator('bsmax.reserved', text="Split")

	row = layout.row()
	row1 = row.row(align=True)
	row1.operator(
		'mesh.tool_set_by_id', text="Extrude"
	).name="builtin.extrude_region"
	row1.operator(
		'wm.call_menu', text='', icon='TOPBAR'
	).name = "MESH_MT_extrude_tools"

	row.operator('bsmax.reserved', text="Weld")

	row = layout.row()
	row.operator('mesh.tool_set_by_id', text="Chamfer").name="builtin.bevel"
	row.operator('bsmax.reserved', text="Target Weld")

	row = layout.row()
	row.operator('mesh.bridge_edge_loops', text="Bridge")
	row.operator('mesh.connect', text="Connect")

	layout.operator(
		'mesh.create_curve_from_edge', text="Creat Shape From Selection"
	)

	box = layout.box()
	box.operator('bsmax.reserved', text="Weight")
	box.operator('bsmax.reserved', text="Crease")
	box.operator('bsmax.reserved', text="Depth")

	row = layout.row()
	row.operator('mesh.faces_shade_flat', text="Hard")
	row.operator('mesh.faces_shade_smooth', text="Smooth")

	row = layout.row()
	row.operator('bsmax.reserved', text="Retriangulate")
	row.operator('mesh.edge_rotate', text="Turn")


def get_mesh_edit_face_mode(layout, ctx):
	layout.operator('bsmax.reserved', text="Insert Vertex")

	row = layout.row()
	row1 = row.row(align=True)
	row1.operator(
		'mesh.tool_set_by_id', text="Extrude"
	).name="builtin.extrude_region"
	row1.operator(
		'wm.call_menu', text='', icon='TOPBAR'
	).name = "MESH_MT_extrude_tools"
	
	row.operator('bsmax.reserved', text="Outline")

	row = layout.row()
	row.operator('mesh.tool_set_by_id', text="Bevel").name="builtin.bevel"
	row.operator(
		'mesh.tool_set_by_id', text="Inset"
	).name="builtin.inset_faces"

	row = layout.row()
	row.operator('mesh.bridge_edge_loops', text="Bridge")
	row.operator('mesh.flip_normals', text="Flip")

	layout.operator('bsmax.reserved', text="Hinge Frome Edge")
	layout.operator('bsmax.reserved', text="Extrude Along Spline")


def get_mesh_edit(cls, layout, ctx):
	vert, edge, face = ctx.tool_settings.mesh_select_mode
	box = layout.box()
	if vert:
		cls.bl_label = "Edit Vertex"
		get_mesh_edit_vertex_mode(box, ctx)
	
	if edge:
		cls.bl_label = "Edit Edge"
		get_mesh_edit_edge_mode(box, ctx)
	
	if face:
		cls.bl_label = "Edit Face"
		get_mesh_edit_face_mode(box, ctx)


def get_mesh_edit_geometry(layout, ctx):
	layout.operator('screen.repeat_last', text='Repeat last')

	layout.prop(
		ctx.scene.tool_settings, 'use_transform_correct_face_attributes',
		text='Preserve UVs'
	)

	row = layout.row()
	row.operator('bsmax.reserved', text='Create')
	row.operator('bsmax.reserved', text='Collapse')
	# bpy.ops.mesh.edge_collapse()

	row = layout.row()
	row1 = row.row(align=True)
	row1.operator('mesh.attach', text='Attach')
	row1.operator('bsmax.reserved', text='', icon='TOPBAR')
	row.operator('mesh.detach', text='Detach')

	box = layout.box()
	box.operator('bsmax.reserved', text='Slice Plane')
	row = box.row()
	row.operator('bsmax.reserved', text='Slice')
	row.operator('bsmax.reserved', text='Reset Plane')
	row = box.row()
	row.operator('mesh.bisect', text='QuickSlice')
	row.operator('mesh.knife_tool', text='Cut')

	row = box.row()
	row.operator('mesh.loopcut_slide', text='Loop Cut')
	
	row = layout.row()
	row.operator('mesh.subdivide', text='MSmooth')
	row.operator('mesh.unsubdivide', text='Un-Subdivide')

	row = box.row()
	row.operator('bsmax.reserved', text='Make Planer')
	row = row.row(align=True)
	row.operator('bsmax.reserved', text='', icon="EVENT_X")
	row.operator('bsmax.reserved', text='', icon="EVENT_Y")
	row.operator('bsmax.reserved', text='', icon="EVENT_Z")
	row = box.row()
	row.operator('bsmax.reserved', text='View Align')
	row.operator('bsmax.reserved', text='Grid Align')

	layout.operator('bsmax.reserved', text='Relax')

	row = layout.row()
	row.operator('mesh.quads_convert_to_tris', text='Tesselate')
	# (quad_method='BEAUTY', ngon_method='BEAUTY')
	row.operator('mesh.tris_convert_to_quads', text='Tri to Quad')

	row = layout.row(align=True)
	row.operator('bsmax.reserved', text='Relax')
	row.operator('bsmax.reserved', text='', icon='TOPBAR')

	row = layout.row()
	row.operator('bsmax.reserved', text='Hide Selection')
	row.operator('bsmax.reserved', text='Unhide All')
	layout.operator('bsmax.reserved', text='Hide Unselected')

	row = layout.row()
	row.operator('bsmax.reserved', text='Copy')
	row.operator('bsmax.reserved', text='Paste')


def get_mesh_edit_UV(layout, ctx):
	box = layout.box()
	row = box.row()
	row.operator('uv.unwrap')
	row.operator("uv.reset", text="Reset")

	box = layout.box()
	row = box.row()
	row.operator('mesh.mark_seam', text="Mark Seam").clear=False
	row.operator('mesh.mark_seam', text="Clear Seam").clear=True

	box = layout.box()
	row = box.row()
	row.operator("uv.cube_project", text="", icon="MESH_CUBE")
	row.operator("uv.cylinder_project", text="", icon="MESH_CYLINDER")
	row.operator("uv.sphere_project", text="", icon="MESH_UVSPHERE")

	box.operator(
		"uv.project_from_view", text="Project From View"
	).scale_to_bounds=False

	box.operator(
		"uv.project_from_view", text="Project From View (Bounds)",
	).scale_to_bounds=True

	box = layout.box()
	box.operator("uv.smart_project", text="Smart Project")
	box.operator("uv.lightmap_pack", text="Light Pack")
	box.operator("uv.follow_active_quads", text="Follow Active Quads")


def get_mesh_properties(layout, ctx):
	pass


def get_mesh_material_id(layout, ctx):
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


def get_mesh_subdivision_surface(layout, ctx):
	pass


def get_mesh_subdivision_displacment(layout, ctx):
	pass


def get_mesh_paint_deform(layout, ctx):
	pass


class BsMax_PT_CP_EditMesh_Selection(Panel):
	bl_idname = 'BSMAX_PT_cp_editMesh_selection'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Selection'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_selection(layout, ctx)


class BsMax_PT_CP_EditMesh_Soft_Selection(Panel):
	bl_idname = 'BSMAX_PT_cp_editMesh_soft_selection'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Soft Selection'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_soft_selection(layout, ctx)


# Verteices, Edge, Border, Polygon
class BsMax_PT_CP_EditMesh_Edit(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_edit'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Edit'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_edit(self, layout, ctx)


class BsMax_PT_CP_EditMesh_Edit_Geometry(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_edit_geometry'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Edit Geometry'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_edit_geometry(layout, ctx)


class BsMax_PT_CP_EditMesh_Vertex_Properties(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_vertex_properties'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Properties'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_properties(layout, ctx)


class BsMax_PT_CP_EditMesh_Material_IDs(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_material_ids'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Material IDs'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_material_id(layout, ctx)


class BsMax_PT_CP_EditMesh_UV(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_uv'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'UV'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_edit_UV(layout, ctx)


class BsMax_PT_CP_EditMesh_Vertex_Colors(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_vertex_colors'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Vertex Color'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_properties(layout, ctx)


class BsMax_PT_CP_EditMesh_Subdivision_Surface(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_subdivision_surface'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Subdivision Surface'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_subdivision_surface(layout, ctx)


class BsMax_PT_CP_EditMesh_Subdivision_Displacment(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_subdivision_displacment'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Subdivision Displacment'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_subdivision_displacment(layout, ctx)


class BsMax_PT_CP_EditMesh_Paint_Deform(Panel):
	bl_idname = 'BSMAX_PT_cp_editmesh_paint_deform'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Paint Deform'
	bl_category = 'BsMax'

	@classmethod
	def poll(self, ctx):
		return is_edit_mesh(ctx)
	
	def draw(self, ctx):
		layout = self.layout
		get_mesh_paint_deform(layout, ctx)


class MESH_MT_Extrude_Tools(Menu):
	bl_idname = "MESH_MT_extrude_tools"
	bl_label = "Extrud"

	def draw(self, ctx):
		layout = self.layout
		layout.operator(
			'mesh.tool_set_by_id', text="Region"
		).name="builtin.extrude_region"

		layout.operator(
			'mesh.tool_set_by_id', text="Manifold"
		).name="builtin.extrude_manifold"

		layout.operator(
			'mesh.tool_set_by_id', text="Along Normals"
		).name="builtin.extrude_along_normals"

		layout.operator(
			'mesh.tool_set_by_id', text="Invidual"
		).name="builtin.extrude_individual"

		layout.operator(
			'mesh.tool_set_by_id', text="To Cursor"
		).name="builtin.extrude_to_cursor"


classes = (
	BsMax_PT_CP_EditMesh_Selection,
	BsMax_PT_CP_EditMesh_Soft_Selection,
	BsMax_PT_CP_EditMesh_Edit,
	BsMax_PT_CP_EditMesh_Edit_Geometry,
	# BsMax_PT_CP_EditMesh_Vertex_Properties,
	BsMax_PT_CP_EditMesh_Material_IDs,
	BsMax_PT_CP_EditMesh_UV,
	# BsMax_PT_CP_EditMesh_Vertex_Colors,
	# BsMax_PT_CP_EditMesh_Subdivision_Surface,
	# BsMax_PT_CP_EditMesh_Subdivision_Displacment,
	# BsMax_PT_CP_EditMesh_Paint_Deform,

	MESH_MT_Extrude_Tools
)


def register_edit_mesh():
	for c in classes:
		register_class(c)


def unregister_edit_mesh():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_edit_mesh()