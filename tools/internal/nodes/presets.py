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



def get_root_path():
	# bpy.utils.user_resource('SCRIPTS') + "\\addons\\BsMax"
	dirs = path.dirname(__file__).split('\\')
			
	# Remove 3 step of sub folders to get Addon root Directory
	root_path = ''
	for i in range(len(dirs)-3):
		root_path += dirs[i] + '\\'

	# Make Path
	return root_path + 'presets.blend\\NodeTree\\'

presetsRootPath = get_root_path()



class NodeGroupe_OT_Import(Operator):
	bl_idname = "nodes.import_node_groupe"
	bl_label = "Import Node Groupe Preset"
	bl_description = "Import Node Groupe Presets"
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

		editorType = {'GeometryNodeTree':'GeometryNodeGroup',
					'ShaderNodeTree':"ShaderNodeGroup"
		}

		nodeGrroupType = editorType[ctx.area.ui_type]

		bpy.ops.node.add_node(type=nodeGrroupType, use_transform=True,
			settings=[{"name":"node_tree", "value":value}])
		
		bpy.ops.node.translate_attach('INVOKE_DEFAULT')
		
		return{"FINISHED"}



def register_presets():
	bpy.utils.register_class(NodeGroupe_OT_Import)

def unregister_presets():
	bpy.utils.unregister_class(NodeGroupe_OT_Import)

if __name__ == "__main__":
	register_presets()