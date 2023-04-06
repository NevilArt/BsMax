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

from bpy.types import Operator, Menu



class Material_OT_Assign_To_Selection(Operator):
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
		elif ctx.mode == 'EDIT_MESH':
			bpy.ops.object.material_slot_assign()
		return{"FINISHED"}



class BsMax_MT_material_presets(Menu):
	bl_idname = "BSMAX_MT_material_import"
	bl_label = "BsMax Presets"

	def draw(self, ctx):
		layout=self.layout
		# Effects
		layout.operator("nodes.import_node_groupe",
						text="Blure").name='Blure'

		layout.operator("nodes.import_node_groupe",
						text="Falloff").name='Falloff'

		# Map
		layout.separator()
		layout.operator("nodes.import_node_groupe",
						text="Ocean Caustic").name='Ocean Caustic'

		# Parallax (coordinate)
		layout.separator()
		layout.operator("nodes.import_node_groupe",
						text="Parallax Box").name='Parallax Box X4'

		layout.operator("nodes.import_node_groupe",
						text="Parallax Layer").name='Parallax Layer X4'

		layout.operator("nodes.import_node_groupe",
						text="Parallax Ice").name='Parallax Ice'

		# Sprite Sheet (Coordinate)
		layout.separator()
		layout.operator("nodes.import_node_groupe",
						text="Sprite Sheet").name='Sprite Sheet'

		layout.operator("nodes.import_node_groupe",
						text="Sprite Play Loop").name='Sprite Play Loop'

		layout.operator("nodes.import_node_groupe",
						text="Sprite Play Range").name='Sprite Play Range'

		# Coordinate
		layout.separator()
		layout.operator("nodes.import_node_groupe",
						text="Untile").name='Untile'




class BsMax_MT_Materia_Collection(Menu):
	bl_idname = "BSMAX_MT_material_collection"
	bl_label = "Material/Collection"

	def draw(self, ctx):
		layout=self.layout
		material_editor = layout.operator("editor.float", text="Material Editor", icon='MATERIAL')
		material_editor.ui_type='ShaderNodeTree'
		material_editor.shader_type='OBJECT'
		material_editor.multiple=False
		layout.operator("object.move_to_collection",
			text="Move To Collection", icon='OUTLINER_COLLECTION')



def bsmax_matt_menu(self, ctx):
	layout = self.layout
	layout.separator()
	self.layout.menu("BSMAX_MT_material_import")



classes = (Material_OT_Assign_To_Selection,
	BsMax_MT_material_presets,
	BsMax_MT_Materia_Collection
)

def register_matt():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_matt():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_matt()