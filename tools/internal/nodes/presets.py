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
from bpy.types import Operator
from bpy.props import StringProperty



def get_root_path(version="presets"):
	# bpy.utils.user_resource('SCRIPTS') + "\\addons\\BsMax"
	dirs = path.dirname(__file__).split('\\')
			
	# Remove 3 step of sub folders to get Addon root Directory
	root_path = ''
	for i in range(len(dirs)-3):
		root_path += dirs[i] + '\\'
	
	#TODO check for file exist or not
	print(">> ", root_path + version + '.blend\\NodeTree\\')

	# Make Path
	return root_path + version + '.blend\\NodeTree\\'

presetsRootPath = get_root_path()



class Scene_OT_Import_Node_Group(Operator):
	bl_idname = "scene.import_node_groupe"
	bl_label = "Import Node Groupe Preset"
	bl_description = "Import Node Groupe Presets"
	bl_options = {'REGISTER', 'INTERNAL'}

	name: StringProperty()
	version: StringProperty()

	def execute(self, ctx):
		# Check for exist
		if not self.name in bpy.data.node_groups:
			# Append the Node Tree
			bpy.ops.wm.append(
				filename=self.name,
				directory=get_root_path(self.version)
			)
		return{"FINISHED"}



class NodeGroupe_OT_Import(Operator):
	bl_idname = "nodes.import_node_group"
	bl_label = "Import Node Group"
	bl_description = "Import Node Group"
	bl_options = {'REGISTER', 'INTERNAL'}

	name: StringProperty()

	def execute(self, ctx):
		global presetsRootPath
		# Check for exist
		if not self.name in bpy.data.node_groups:
			# Append the Node Tree
			bpy.ops.wm.append(filename=self.name, directory=presetsRootPath)

		# Add to node editor
		value = 'bpy.data.node_groups["' + self.name + '"]'

		editorType = {
			'GeometryNodeTree':'GeometryNodeGroup',
			'ShaderNodeTree':"ShaderNodeGroup"
		}

		nodeGrroupType = editorType[ctx.area.ui_type]

		bpy.ops.node.add_node(type=nodeGrroupType, use_transform=True,
			settings=[{"name":"node_tree", "value":value}])
		
		bpy.ops.node.translate_attach('INVOKE_DEFAULT')
		
		return{"FINISHED"}




classes = (
	Scene_OT_Import_Node_Group,
	NodeGroupe_OT_Import
)



def register_presets():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_presets():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_presets()