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

from os import path
from bpy.types import Operator, Menu
from bpy.props import StringProperty



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



class Material_OT_Import(Operator):
	bl_idname = "nodes.import_node_groupe"
	bl_label = "Import Node Groupe Preset"
	bl_description = "Import Node Groupe Presets"
	bl_options = {'REGISTER'}

	name: StringProperty()

	# @classmethod
	# def poll(self, ctx):
	# 	if ctx.space_data.type == "NODE_EDITOR" and ctx.mode == 'OBJECT':
	# 		return ctx.space_data.shader_type == 'OBJECT'
	# 	return False

	def execute(self, ctx):
		# Check for exist
		if not self.name in bpy.data.node_groups:
			# Get current script path
			dirs = path.dirname(__file__).split('\\')
			
			# TODO change this method
			# Remove 3 step of sub folders to get Addon root Directory
			root_path = ''
			for i in range(len(dirs)-3):
				root_path += dirs[i] + '\\'

			# Make Path
			directory = root_path + 'presets.blend\\NodeTree\\'

			# Append the Node Tree
			bpy.ops.wm.append(filename=self.name, directory=directory)

		# Add to node editor
		value = 'bpy.data.node_groups["' + self.name + '"]'
		editorType = {'GeometryNodeTree':'GeometryNodeGroup',
					'ShaderNodeTree':"ShaderNodeGroup"
		}
		
		nodeGrroupType = editorType[ctx.area.ui_type]

		bpy.ops.node.add_node(type=nodeGrroupType, use_transform=True,
			settings=[{"name":"node_tree", "value":value}])
		
		bpy.ops.node.translate_attach()
		
		return{"FINISHED"}



class BsMax_MT_material_presets(Menu):
	bl_idname = "BSMAX_MT_material_import"
	bl_label = "Append Node Trees"

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



class BsMax_MT_geometrynode_presets(Menu):
	bl_idname = "BSMAX_MT_geometrynode_import"
	bl_label = "Append GNode Trees"

	def draw(self, ctx):
		layout=self.layout
		# Distribution
		layout.operator("nodes.import_node_groupe",
						text="Probability 10").name='Probability 10'
		layout.operator("nodes.import_node_groupe",
						text="Sum").name='Sum'



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



class BsMax_MT_material_Tools(Menu):
	bl_idname = "BSMAX_MT_material_tools"
	bl_label = "Tools"

	def draw(self, ctx):
		layout=self.layout
		if ctx.space_data.type == "NODE_EDITOR":

			if ctx.area.ui_type == 'GeometryNodeTree':
				layout.menu("BSMAX_MT_geometrynode_import")

			elif ctx.area.ui_type == 'CompositorNodeTree':
				pass

			elif ctx.area.ui_type == 'ShaderNodeTree':

				if ctx.space_data.shader_type == 'OBJECT':
					layout.operator("material.assign_to_selection",
		     						text="Assign to selected"
					)
					
					layout.menu("BSMAX_MT_material_import")

				elif ctx.space_data.shader_type == 'WORLD':
					pass



def matt_menu(self, ctx):
	self.layout.menu("BSMAX_MT_material_tools")



classes = [Material_OT_Assign_To_Selection,
	Material_OT_Import,
	BsMax_MT_material_presets,
	BsMax_MT_geometrynode_presets,
	BsMax_MT_Materia_Collection,
	BsMax_MT_material_Tools]

def register_matt():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.NODE_MT_editor_menus.append(matt_menu)

def unregister_matt():
	bpy.types.NODE_MT_editor_menus.remove(matt_menu)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_matt()