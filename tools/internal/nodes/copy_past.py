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
from bpy.utils import register_class, unregister_class


def get_active_node_editor_details(ctx):
	area = ctx.area
	if area.type == 'NODE_EDITOR':
		space = area.spaces.active
		space_data = ctx.space_data

		if space.tree_type == 'ShaderNodeTree':
			if space_data.shader_type in {'OBJECT', 'WORLD', 'LINESTYLE'}:
				return 'SHADER_' + space_data.shader_type
			else:
				return 'SHADER'

		elif space.tree_type == 'GeometryNodeTree':
			if space_data.geometry_nodes_type in {'MODIFIER', 'TOOL'}:
				return 'GEONODE_' + space_data.geometry_nodes_type
			else:
				return 'GEONODE'

		elif space.tree_type == 'CompositorNodeTree':
			return 'COMPOSITOR'

		elif space.tree_type == 'TextureNodeTree':
			if space_data.texture_type in {'WORLD', 'BRUSH', 'LINESTYLE'}:
				return 'TEXTURE_' + space_data.texture_type
			else:
				return 'TEXTURE'

	return None


def node_to_create_script(index, node):
	node_handler_name = "node" + str(index)

	script = "	" + node_handler_name + " = node_tree.nodes.new(type="
	script += node.bl_idname + ")\n"

	script += "	" + node_handler_name + ".location = " + str(node.location) + "\n"

	for input_socket in node.inputs:
		if input_socket.is_linked or not hasattr(input_socket, 'default_value'):
			continue
		
		input_value = str(input_socket.default_value)
		script += "	" + node_handler_name
		script += ".inputs['" + input_socket.name + "'].default_value = "
		script += input_value + "\n"

	return script


def convert_selected_nodes_to_script(node_tree):
	selected_nodes = [node for node in node_tree.nodes if node.select]
	selected_node_names = {node.name for node in selected_nodes}

	if not selected_nodes:
		return ''
	
	script = ""
	for index, node in enumerate(selected_nodes):
		script += node_to_create_script(index, node) + "\n"

	for link in node_tree.links:
		from_node = link.from_node
		to_node = link.to_node

		# if (from_node.name in selected_node_names and to_node.name not in selected_node_names) or \
		# 	(from_node.name not in selected_node_names and to_node.name in selected_node_names):

		from_node_name = from_node.name.replace(' ', '_')
		to_node_name = to_node.name.replace(' ', '_')
		from_socket = link.from_socket.name
		to_socket = link.to_socket.name

		script += "	" + "node_tree.links.new("
		script += from_node_name
		script += ".outputs['"
		script += from_socket
		script += "'], "
		script += to_node_name
		script += ".inputs['"
		script += to_socket
		script += "'])\n"

	return script


def get_script_header(current_editor):
	script = "\n----------------------------------------------\n"
	script += "import bpy\n"
	script += "editor_type = '" + current_editor + "'\n"
	script += "def recreate_nodes():\n"
	script += "	" + "node_tree = bpy.context.space_data.node_tree\n"
	return script


def get_script_footer():
	return "# Script Footer"


class Nodes_OT_Copy_To_python(Operator):
	bl_idname = 'nodes.copy_to_python'
	bl_label = "copy selected nodes"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(self, ctx):
	# 	if ctx.space_data.type == 'NODE_EDITOR':
	# 		return ctx.space_data.shader_type == 'OBJECT'
	# 	return False

	def execute(self, ctx):
		if ctx.space_data.node_tree is None:
			return
		editor = get_active_node_editor_details(ctx)
		script = get_script_header(editor)
		script += convert_selected_nodes_to_script(ctx.space_data.node_tree)
		script += get_script_footer()

		print(script)
		return{'FINISHED'}


# def def register():
# 	bpy.utils.register_module(__name__)

# def unregister():
# 	bpy.utils.unregister_module(__name__)

if __name__ == '__main__':
	register_class(Nodes_OT_Copy_To_python)
