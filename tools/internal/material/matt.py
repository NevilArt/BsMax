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

class Material_OT_Assign_To_Selection(bpy.types.Operator):
	bl_idname = "material.assign_to_selection"
	bl_label = "Assign to selected objects"
	bl_description = "Assign Material to selected objects"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.space_data.type == "NODE_EDITOR":
			return ctx.space_data.shader_type == 'OBJECT'
		return False

	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			bpy.ops.object.make_links_data(type='MATERIAL')
			self.report({'OPERATOR'},'bpy.ops.object.make_links_data(type="MATERIAL")')
		elif ctx.mode == 'EDIT_MESH':
			bpy.ops.object.material_slot_assign()
			self.report({'OPERATOR'},'bpy.ops.object.material_slot_assign()')
		return{"FINISHED"}

class BsMax_MT_material_Tools(bpy.types.Menu):
	bl_idname = "BSMAX_MT_materialtools"
	bl_label = "Tools"

	def draw(self, ctx):
		layout=self.layout
		if ctx.space_data.type == "NODE_EDITOR":
			if ctx.space_data.shader_type == 'OBJECT':
				layout.operator("material.assign_to_selection",text="Assign to selected")

def matt_menu(self, ctx):
	self.layout.menu("BSMAX_MT_materialtools")

classes = [Material_OT_Assign_To_Selection,BsMax_MT_material_Tools]

def register_matt():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.NODE_MT_editor_menus.append(matt_menu)

def unregister_matt():
	bpy.types.NODE_MT_editor_menus.remove(matt_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_matt()