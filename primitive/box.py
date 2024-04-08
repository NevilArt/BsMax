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
# 2024/04/03

import bpy

from bpy.app import version
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive

useGeonode = False

#############################################################################
def primitive_geonode_setup(self, idName):
	if not self.owner:
		return
	
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

class PrimitiveGeoNodes():
	def __init__(self, owner, name):
		self.owner = owner
		self.modifier = None
		self.noedGroups = None
		self.nodes = None
		self.interface = None
		self.links = None
		self.setup(name)

	def setup(self, name):
		return primitive_geonode_setup(self, name)

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

#############################################################################
		
def create_box_geonode(gnBox):
	# create nodes
	input = gnBox.get_input_node(x=-500, y=0)
	outpout = gnBox.get_out_node(x=250, y=-30)

	cube = gnBox.new_node('GeometryNodeMeshCube', -100, -25, False)
	xyz1 = gnBox.new_node('ShaderNodeCombineXYZ', -300, -25, True) # cube size
	xyz2 = gnBox.new_node('ShaderNodeCombineXYZ', -95, -200, True) # transform
	transform1 = gnBox.new_node('GeometryNodeTransform', 80, -55, True)

	math1 = gnBox.new_node('ShaderNodeMath', -300, -205, True)
	math1.operation = 'MULTIPLY'

	mathx = gnBox.new_node('ShaderNodeMath', -300, -70, True)
	mathx.inputs[1].default_value = 1

	mathy = gnBox.new_node('ShaderNodeMath', -300, -115, True)
	mathy.inputs[1].default_value = 1

	mathz = gnBox.new_node('ShaderNodeMath', -300, -160, True)
	mathz.inputs[1].default_value = 1

	# create sockets
	gnBox.new_float_socket("Width", 2, None, None)
	gnBox.new_float_socket("Length", 2, None, None)
	gnBox.new_float_socket("Height", 2, None, None)
	gnBox.new_int_socket('WSegs', 1, 1, 1000)
	gnBox.new_int_socket('LSegs', 1, 1, 1000)
	gnBox.new_int_socket('HSegs', 1, 1, 1000)

	# links
	gnBox.link(input, 'Width', xyz1, 'X')
	gnBox.link(input, 'Length', xyz1, 'Y')
	gnBox.link(input, 'Height', xyz1, 'Z')

	gnBox.link(input, 'WSegs', mathx, 'Value')
	gnBox.link(input, 'LSegs', mathy, 'Value')
	gnBox.link(input, 'HSegs', mathz, 'Value')

	gnBox.link(mathx, 'Value', cube, 'Vertices X')
	gnBox.link(mathy, 'Value', cube, 'Vertices Y')
	gnBox.link(mathz, 'Value', cube, 'Vertices Z')

	gnBox.link(xyz1, 'Vector', cube, 'Size')

	gnBox.link(cube, 'Mesh', transform1, 'Geometry')
	gnBox.link(transform1, 'Geometry', outpout, 'Geometry')

	gnBox.link(input, 'Height', math1, 'Value')
	gnBox.link(math1, 'Value', xyz2, 'Z')
	gnBox.link(xyz2, 'Vector', transform1, 'Translation')



def convert_to_geometry_node_box(obj, width, length, height, wsegs, lsegs, hsegs):
	gnBox = PrimitiveGeoNodes(obj, 'Box')

	# Setup new node tree
	if len(gnBox.nodes) < 3:
		create_box_geonode(gnBox)

	gnBox.set_soket_value(2, width)
	gnBox.set_soket_value(3, length)
	gnBox.set_soket_value(4, height)
	gnBox.set_soket_value(5, wsegs)
	gnBox.set_soket_value(6, lsegs)
	gnBox.set_soket_value(7, hsegs)


def get_box_mesh(width, length, height, wsegs, lsegs, hsegs):
	verts, edges, faces = [], [], []
	# Control the input values
	if wsegs < 1: wsegs = 1
	if lsegs < 1: lsegs = 1
	if hsegs < 1: hsegs = 1

	w = width / wsegs
	l = length / lsegs
	h = height / hsegs
	hw = width / 2
	hl = length / 2

	# Create vertexes
	for he in (0.0, height):
		for i in range(wsegs + 1):
			for j in range(lsegs + 1):
				x = w * i - hw
				y = l * j - hl
				z = he
				verts.append((x, y, z))

	for i in range(1,hsegs):
		for j in range(lsegs + 1):
			x = -hw
			y = l * j - hl
			z = h * i
			verts.append((x, y, z))

		for j in range(1, wsegs + 1):
			x = w * j - hw
			y = length - hl
			z = h * i
			verts.append((x, y, z))

		for j in range(lsegs - 1, -1, -1):
			x = width - hw
			y = l * j - hl
			z = h * i
			verts.append((x , y, z))

		for j in range(wsegs - 1, 0, -1):
			x = w * j - hw
			y = -hl 
			z = h * i
			verts.append((x, y, z))

	# Create faces
	# fill plates
	for k in range(2):
		f = k * (wsegs + 1) * (lsegs + 1)
		for i in range(wsegs):
			for j in range(lsegs):
				a = j + (lsegs + 1) * i + f
				b = a + 1
				c = b + lsegs + 1
				d = c - 1
				if k == 0:
					faces.append((a, b, c, d))
				else:
					faces.append((d, c, b, a))

	# fill center
	f = ((lsegs + 1) * 2) * (wsegs + 1)
	l = (wsegs + lsegs) * 2
	for i in range(hsegs - 2):
		for j in range(l):
			a = f + i * l + j   
			if j < l - 1:
				b = a + 1
				c = b + l
				d = c - 1
			else:
				b = f + i * l
				c = f + (i + 1) * l
				d = a + l
			faces.append((d, c, b, a))

	f2 = f + l * (hsegs - 2) # last line first vertext
	if hsegs > 1:
		# silde lowr line 1
		for i in range(lsegs):
			a = i
			b = a + 1
			c = f + i + 1
			d = f + i
			faces.append((d, c, b, a))

		# silde lowr line 2
		fl, fu = lsegs, f + lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = f + wsegs + lsegs
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu = (wsegs + 1) * (lsegs + 1) * 2 + (lsegs + 1) * 2 + (wsegs - 2)
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu + i + 1
			else:
				c = f
			d = fu + i
			faces.append((d, c, b, a))

		# silde Uper line 1
		fl = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde Uper line 2
		fl += lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i
			b = a + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))

		# silde Upper line 3
		fl += wsegs
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl += lsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl + i
			if i < wsegs - 1:
				b = a + 1
				c = fu - (i + 1) * (lsegs + 1)
			else:
				b = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))
	else:
		# silde lowr line 1
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line 2
		fl = lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))

		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu - (i + 1) * (lsegs + 1)
			else:
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))

	return verts, edges, faces



class Box(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Box"
		self.finishon = 3
		self.shading = 'FLAT'

	def create(self, ctx):
		w, l, h = 1, 1, 1
		# Create Mesh Data
		mesh = get_box_mesh(0, 0, 0, w, l, h)
		# Create object and link mesh data
		self.create_mesh(ctx, mesh, self.classname)
		# Save custom atrributes on object data
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs, pd.lsegs, pd.hsegs = w, l, h

	def update(self):
		pd = self.data.primitivedata
		mesh = get_box_mesh(
			pd.width, pd.length, pd.height,
			pd.wsegs, pd.lsegs, pd.hsegs
		)
		
		self.update_mesh(mesh)


class Create_OT_Box(Draw_Primitive):
	bl_idname = "create.box"
	bl_label = "Box"
	subclass = Box()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.width = dimension.radius
				self.params.length = dimension.radius
				self.params.height = dimension.radius
			else:
				self.params.width = abs(dimension.width)
				self.params.length = abs(dimension.length)
				self.subclass.owner.location = dimension.center

		elif clickcount == 2:
			width_length = self.params.width + self.params.length

			if self.use_single_draw or width_length == 0:
				self.jump_to_end()
				return

			self.params.height = dimension.height
	
	def finish(self):
		global useGeonode
		if version >= (4, 0, 0) and useGeonode:
			owner = self.subclass.owner
			pd = owner.data.primitivedata
			convert_to_geometry_node_box(
				owner,
				pd.width, pd.length, pd.height,
				pd.wsegs, pd.lsegs, pd.hsegs
			)


def register_box(preferences):
	global useGeonode
	useGeonode = preferences.geonode_pirimitve
	bpy.utils.register_class(Create_OT_Box)

def unregister_box():
	bpy.utils.unregister_class(Create_OT_Box)

if __name__ == '__main__':
	register_box()