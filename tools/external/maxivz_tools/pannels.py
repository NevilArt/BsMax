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
import bpy

class MaxivzTools_PT_Panel(bpy.types.Panel):
	bl_idname = "MaxivzTools_PT_Panel"
	bl_label = "Maxivz Interactive Tools"
	bl_category = "Maxivz Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		row0 = layout.row()
		row0.operator('mesh.quick_selection_vert' ,text="Quick Sel Vert")
		row0.operator('mesh.quick_selection_edge' ,text="Quick Sel Edge")
		row0.operator('mesh.quick_selection_face' ,text="Quick Sel Face")
		row1 = layout.row()
		row1.operator('mesh.super_smart_create' ,text="Super Smart Create")
		row1.operator('mesh.smart_delete' ,text="Smart Delete")
		row2 = layout.row()
		row2.operator('mesh.smart_select_loop' ,text="Smart Loop")
		row2.operator('mesh.smart_select_ring' ,text="Smart Ring")
		row3 = layout.row()
		row3.operator('mesh.set_cylindrical_sides' ,text="Set Cylindrical Obj Sides")
		row3.operator('mesh.radial_symmetry' ,text="Radial Symmetry")
		row4 = layout.row()
		row4.operator('mesh.quick_ffd' ,text="Quick FFD")
		row4.operator('mesh.quick_pivot' ,text="Quick Pivot")
		row4.operator('mesh.simple_edit_pivot' ,text="Edit Pivot")
		row5 = layout.row()
		row5.operator('mesh.modifier_toggle' ,text="Modifier Toggle")
		row5.operator('mesh.wire_toggle' ,text="Wireframe Toggle")
		row5.operator('mesh.wire_shaded_toggle' ,text="Wireframe Shaded Toggle")
		row6 = layout.row()
		row6.operator('mesh.target_weld_toggle' ,text="Target Weld Toggle")
		row6.operator('mesh.smart_extrude_modal' ,text="Smart Extrude")
		row6.operator('mesh.smart_translate_modal' ,text="Smart Translate")
		row7 = layout.row()
		row7.operator('mesh.context_sensitive_slide' ,text="CS Slide")
		row7.operator('mesh.cs_bevel' ,text="CS Bevel")
		row8 = layout.row()
		row8.operator('uv.rotate_90_pos' ,text="Rotate UV 90 Pos")
		row8.operator('uv.rotate_90_neg' ,text="Rotate UV 90 Neg")