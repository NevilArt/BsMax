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
# 2025/02/10

import bpy
import os

from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


def get_output_path_str(ctx):
	dirname = os.path.dirname(ctx.scene.render.filepath)

	if not dirname.endswith(('/', '\\')):
		dirname += os.sep

	if not dirname:
		dirname = os.path.expanduser('~') + os.sep

	return dirname + "output"


def get_node_by_type(ctx, type):
	node_tree = ctx.scene.node_tree
	if not node_tree:
		return None  # No node tree found

	# Check for active node first
	if node_tree.nodes.active and node_tree.nodes.active.type == type:
		return node_tree.nodes.active

	# If no active node, check for selected Render Layer nodes
	for node in node_tree.nodes:
		if node.select and node.type == type:
			return node

	return None  # No active or selected Render Layers node found


def get_render_layer_node(ctx):
	return get_node_by_type(ctx, 'R_LAYERS')


def get_outpout_node(ctx):
	return get_node_by_type(ctx, 'OUTPUT_FILE')


def set_up_output_node(ctx, node, position):
	node.label = "EXR MultiLayer"
	node.format.file_format = 'OPEN_EXR_MULTILAYER'
	node.format.exr_codec = 'DWAA'
	node.base_path = get_output_path_str(ctx)
	node.location = position
	node.width = 300


def create_node_file_output(ctx, position):
	node = ctx.scene.node_tree.nodes.new('CompositorNodeOutputFile')
	set_up_output_node(ctx, node, position)
	return node


def link_render_layers(ctx, sourceNode, targetNode, create):
	for out in sourceNode.outputs:
		# skip disabled outputs
		if (out.enabled == False):
			continue

		slot = 0
		found = False

		for src in targetNode.inputs:
			if (src.identifier == out.identifier):
				# target node already has matching input, link to it
				found = True
				ctx.scene.node_tree.links.new(out, targetNode.inputs[slot])
				break
			
			slot = slot + 1

		if not found and create:
			# target node has no matching input, create one and link to it
			targetNode.file_slots.new(out.identifier)
			ctx.scene.node_tree.links.new(out, targetNode.inputs[-1])


def auto_exr_setup(ctx, create):
	# ctx.scene.use_nodes = True

	layersNode = get_render_layer_node(ctx)
	
	if not layersNode:
		return
	
	outputNode = get_outpout_node(ctx)
	
	if not outputNode:
		outputNode = create_node_file_output(ctx, (400, 450))
	
	link_render_layers(ctx, layersNode, outputNode, create)


class Node_OT_Auto_EXR(Operator):
	bl_idname = 'node.auto_exr'
	bl_label = "Auto EXR Connector"
	bl_options = {'REGISTER', 'UNDO'}

	create: BoolProperty(
		name="Create Missing slot"
	) # type: ignore

	def draw(self, ctx):
		layout = self.layout
		
		lable = "Force to Create Missing Links" if self.create else "Link Avalible slots only"
		layout.prop(self, 'create', text=lable)
		

	def execute(self, ctx):
		auto_exr_setup(ctx, self.create)
		return {'FINISHED'}

	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self, width=400)


def composit_tool_menu(self, ctx):
	self.layout.operator('node.auto_exr')


def register_auto_exr():
	register_class(Node_OT_Auto_EXR)
	bpy.types.BSMAX_MT_compositor_tools.append(composit_tool_menu)


def unregister_auto_exr():
	bpy.types.BSMAX_MT_compositor_tools.remove(composit_tool_menu)
	unregister_class(Node_OT_Auto_EXR)


if __name__ == '__main__':
	# register_auto_exr()
	register_class(Node_OT_Auto_EXR)
