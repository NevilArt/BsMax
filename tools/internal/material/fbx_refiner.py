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
# 2024/02/25

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class ImageData():
	def __init__(self, image):
		self.image = image
		self.fileName = ""
		self.samples = []
		self.isSkin = None
	
	def is_skin_texture(self):
		return False


class ImageList():
	def __init__(self):
		self.images = []

	def is_unique(self, image):
		for img in self.images:
			if img.fileName == image.name:
				return False
		return True

	def add_if_unique(self, image):
		if self.is_unique(image):
			self.images.append(ImageData(image))


imageList = ImageList()


def set_viewport_setting(material):
	#TODO get difuse color from material node
	material.diffuse_color = (0.5, 0.5, 0.5, 1)
	material.metallic = 0
	material.roughness = 1


def get_base_node(nodes):
	""" Get node list and return first node connected to output\n
		for now just return BSDF principled node 
		args:
			nodes: node array
		return
			node
	"""
	for node in nodes:
		if node.type == 'BSDF_PRINCIPLED':
			return node
	return None


def pixel_compare(pixel1, pixel2, tolerance):
	r = pixel2[0]-tolerance < pixel1[0] < pixel2[0]+tolerance
	g = pixel2[1]-tolerance < pixel1[1] < pixel2[1]+tolerance
	b = pixel2[2]-tolerance < pixel1[2] < pixel2[2]+tolerance
	return r and g and b


def is_skin_texture(image):
	if not image.pixels:
		return False

	width = image.size[0]
	chanelSize = image.channels
	rowCount = width*chanelSize
	sapmles = []
	
	# get 100 samples from picture
	for w in range(10):
		for l in range(10):
			index = l*rowCount + w*chanelSize
			r = image.pixels[index]
			g = image.pixels[index+1]
			b = image.pixels[index+2]
			sapmles.append((r, g, b))
	
	# Casual skin tones
	skinTones = (
		(233, 203, 167),#IVORY
		(238, 208, 184),#PORCELAIN
		(247, 221, 196),#PALE IVORY
		(247, 226, 171),#WARM IVORY
		(239, 199, 148),#SAND
		(239, 192, 136),#ROSE BEIGE
		(231, 188, 145),#LIMSTONE
		(236, 192, 131),#BEIGE
		(208, 158, 125),#SIENNA
		(203, 150, 98),#HONEY
		(171, 139, 100),#BAND
		(148, 98, 61),#ALMOND
		(136, 86, 51),#CHESTNUT
		(118, 68, 31),#BRONZE
		(187, 105, 73),#UMBER
		(128, 73, 42),#GOLDEN
		(98, 58, 23),#ESPRESSO
		(48, 30, 16)#CHOCOLATE
	)

	for skinTone in skinTones:
		inRangeCount = 0

		for sample in sapmles:
			if pixel_compare(sample, skinTone, 10):
				inRangeCount += 1
		print(">> in range count", inRangeCount)
		if inRangeCount > len(sapmles)*0.75:
			return True

	return False


def check_base_color(baseColor):
	if baseColor.is_linked:
		baseImage = baseColor.links[0].from_node
		if baseImage.type == 'TEX_IMAGE':
			image = baseImage.image
			image.file_format
			image.name
			image.colorspace_settings.name
			image.pixels
			image.filepath

			# print(">> is Skin Texture")

			# print(">>>>", is_skin_texture(image))

# matt = bpy.context.object.material_slots[0].material.node_tree.nodes['Image Texture']


def check_node_tree(material):
	nodes = material.node_tree.nodes
	baseNode = get_base_node(nodes)
	
	if not baseNode:
		return False
	
	inputs = baseNode.inputs

	baseColor = inputs['Base Color']
	check_base_color(baseColor)

	inputs['Metallic'].default_value = 0
		
	# Alpha
	# Anisotropic
	# Anisotropic Rotation
	# Clearcoat
	# Clearcoat Normal
	# Clearcoat Roughness
	# Emission
	# Emission Strength
	# IOR
	# Normal
	# Roughness
	# Sheen
	# Sheen Tint
	# Specular
	# Specular Tint
	# Subsurface
	# Subsurface Anisotropy
	# Subsurface Color
	# Subsurface IOR
	# Subsurface Radius
	# Tangent
	# Transmission
	# Transmission Roughness
	# Weight


def check_simple_material(material):
	pass


def check_materials(obj):
	for slot in obj.material_slots:
		material = slot.material
		set_viewport_setting(material)
		if material.use_nodes:
			check_node_tree(material)
		else:
			check_simple_material(material)


class Material_OT_FBX_Cleaner(Operator):
	bl_idname = "material.fbx_cleaner"
	bl_label = "FBX Cleaner"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			check_materials(obj)

		return{"FINISHED"}


classes = (
	Material_OT_FBX_Cleaner,
)


def register_fbx_refiner():
	for c in classes:
		register_class(c)


def unregister_fbx_refiner():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_fbx_refiner()