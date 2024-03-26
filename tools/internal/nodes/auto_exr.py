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
# 2024/03/23

import bpy
import os
# import subprocess

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


# # opens the directory of the current render path
# def open_folder():
# 	path = bpy.data.scenes["Scene"].render.filepath
# 	subprocess.call("explorer " + path, shell=True)


# returns a target render path taken from the scene's render output and cleaned up as needed
def get_output_path_str(ctx):
	dirname = os.path.dirname(ctx.scene.render.filepath)

	if not dirname.endswith(('/', '\\')):
		dirname += "/"

	if not dirname:
		dirname = os.path.expanduser('~') + "/"

	return dirname + "output"

# creates a new Render Layers node at the given position
def create_node_render_layer(ctx, position):
	#TODO return if active or only one exiest else create new one
	node = ctx.scene.node_tree.nodes.new('CompositorNodeRLayers')
	node.location = position
	return node


# creates a new Output File node at the given position
def create_node_file_output(ctx, position):
	#TODO return if active or only one exiest else create new one
	ctx.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
	node = ctx.scene.node_tree.nodes.new('CompositorNodeOutputFile')
	node.label = "EXR MultiLayer"
	node.base_path = get_output_path_str(ctx)
	node.location = position
	node.width = 300
	return node


# links all outputs of the source node to inputs of the target node
def link_render_layers(ctx, sourceNode, targetNode):
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

		if not found:
			# target node has no matching input, create one and link to it
			targetNode.file_slots.new(out.identifier)
			ctx.scene.node_tree.links.new(out, targetNode.inputs[-1])


class Node_OT_Auto_EXR(Operator):
	bl_idname = "node.auto_exr"
	bl_label = "Auto EXR Connector"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, ctx):

		ctx.scene.use_nodes = True
		layersNode = create_node_render_layer(ctx, (0, 400))
		outputNode = create_node_file_output(ctx, (400, 450))
		link_render_layers(ctx, layersNode, outputNode)
		return {'FINISHED'}


def composit_tool_menu(self, ctx):
	self.layout.operator('node.auto_exr')


def register_auto_exr():
	register_class(Node_OT_Auto_EXR)
	bpy.types.BSMAX_MT_compositor_tools.append(composit_tool_menu)


def unregister_auto_exr():
	bpy.types.BSMAX_MT_compositor_tools.remove(composit_tool_menu)
	unregister_class(Node_OT_Auto_EXR)


if __name__ == "__main__":
	register_auto_exr()
