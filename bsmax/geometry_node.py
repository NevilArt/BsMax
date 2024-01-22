############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy


def create_geometry_node(self, idName):
	
	self.modifier = self.owner.modifiers.new(name=idName, type='NODES')
	
	# try to find n scene
	self.nodeGroup = None
	for nodeGroup in bpy.data.node_groups:
		if nodeGroup.interface.items_tree[0].description == idName:
			self.nodeGroup = nodeGroup
			self.modifier.node_group = self.nodeGroup
	
	# Create New one
	if not self.nodeGroup:
		bpy.ops.node.new_geometry_node_group_assign()

	self.nodeGroup = self.modifier.node_group
	self.nodeGroup.name = idName
	self.nodes = self.nodeGroup.nodes
	self.interface = self.nodeGroup.interface
	self.links = self.nodeGroup.links
	self.interface.items_tree[0].description = idName

def primitive_geonode_get_input_node(self, x, y):
	for node in self.nodes:
		if node.type == 'GROUP_INPUT':
			if x: 
				node.location.x = x
			if y:
				node.location.y = y
			return node
	return None

def primitive_geonode_get_output_node(self, x, y):
	for node in self.nodes:
		if node.type == 'GROUP_OUTPUT':
			if x: 
				node.location.x = x
			if y:
				node.location.y = y
			return node
	return None

def primitive_geonode_new_float_socket(self, name, default, min, max):
	newSocket = self.interface.new_socket(
		name=name, in_out='INPUT', socket_type='NodeSocketFloat'
	)
	if default:
		newSocket.default_value = default
	if min:
		newSocket.min_value = min
	if max:
		newSocket.max_value = max

def primitive_geonode_new_int_socket(self, name, default, min, max):
	newSocket = self.interface.new_socket(
		name=name, in_out='INPUT', socket_type='NodeSocketInt'
	)
	if default:
		newSocket.default_value = default
	if min:
		newSocket.min_value = min
	if max:
		newSocket.max_value = max

def primitive_geonode_new_node(self, type, x, y, hide):
	nodes = self.nodes
	newNode = nodes.new(type)
	newNode.location.x = x
	newNode.location.y = y
	newNode.hide = hide
	return newNode

class GeometryNode():
	def __init__(self, idName):
		self.noedGroups = None
		self.nodes = None
		self.interface = None
		self.links = None
		self.setup(idName)
		
    # def get_nodegroupe

	def setup(self, idName):
		return create_geometry_node(self, idName)

	def new_node(self, type, x, y, hide):
		return primitive_geonode_new_node(self, type, x, y, hide)

	def new_float_socket(self, name, default, min, max):
		return primitive_geonode_new_float_socket(self, name, default, min, max)

	def new_int_socket(self, name, default, min, max):
		return primitive_geonode_new_int_socket(self, name, default, min, max)
	
	def get_input_node(self, x=None, y=None):
		return primitive_geonode_get_input_node(self, x, y)
	
	def get_out_node(self, x=None, y=None):
		return primitive_geonode_get_output_node(self, x, y)

	def link(self, source, sourceChanelName, target, targetChanelName):
		self.links.new( 
			source.outputs[sourceChanelName],
			target.inputs[targetChanelName]
		)
	
	def set_soket_value(self, index, value):
		self.modifier["Socket_" + str(int(index))] = value