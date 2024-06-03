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

import json
import os
import bpy

from mathutils import Vector

from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy_extras.io_utils import ImportHelper

from bsmax.actions import link_to_scene



def create_sprite_plane(ctx, name, width, height, offset):
	# offset vertexes
	#TODO need to check offset standard values
	left = -offset[0]
	right = width - offset[0]
	top = offset[1]
	bottom = -height + offset[1] 
	
	# Create vertexes
	verts = []
	verts.append(Vector((left, 0, bottom)))
	verts.append(Vector((right, 0, bottom)))
	verts.append(Vector((right, 0, top)))
	verts.append(Vector((left, 0, top)))

	# Create faces
	faces = [(0, 1, 2, 3)]
	
	# Create Object
	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata(verts, [], faces)
	obj = bpy.data.objects.new(name, mesh)
	link_to_scene(ctx, obj)

	# Create UVMap
	obj.data.uv_layers.new(name="UVMap")

	return obj



def get_name(self):
	""" set plane and mesh name as image file name
		args:
			self: class Image_Plane
		return:
			name as string
	"""
	return self.node['name'].split('.')[0]
	


def set_location(self):
	position = self.node['position']
	depth = self.node['z']
	x = position[0] * self.node['scale'][0] * self.scale
	z = -position[1] * self.node['scale'][1] * self.scale
	y = depth * self.scale
	self.owner.location = Vector((x, y, z))



def get_pivot_offset(self):
	offset = self.node['pivot_offset']
	scale = self.node['scale']
	return [offset[0]*scale[0]*self.scale, offset[1]*scale[1]*self.scale]



def get_image_size(self):
	img_size = bpy.data.images[self.node['name']].size
	w = img_size[0] * self.node['scale'][0] * self.scale
	h = img_size[1] * self.node['scale'][1] * self.scale
	return [w, h]



def get_material(self, name):
	material = bpy.data.materials.new(name)
	material.use_nodes = True
	
	if self.node['opacity'] == 1:
		material.blend_method = 'CLIP'
	else:
		material.blend_method = 'HASHED'

	node_tree = material.node_tree
	nodes = node_tree.nodes

	matt = nodes['Principled BSDF']
	matt.inputs['Subsurface IOR'].default_value = 0
	matt.inputs['Specular'].default_value = 0
	matt.inputs['Roughness'].default_value = 1
	matt.inputs['Sheen Tint'].default_value = 0
	matt.inputs['Clearcoat Roughness'].default_value = 0

	mapp = material.node_tree.nodes.new(type="ShaderNodeTexImage")
	mapp.location.x = -400
	mapp.location.y = 50

	image_file_path = self.path + '\\'
	image_file_name = os.path.normpath(self.node['resource_path'])
	mapp.image = bpy.data.images.load(image_file_path + image_file_name)

	node_tree.links.new(mapp.outputs['Color'], matt.inputs['Base Color'])
	if material.blend_method == 'CLIP':
		node_tree.links.new(mapp.outputs['Alpha'], matt.inputs['Alpha'])
	else:
		#TODO add math multili node between
		node_tree.links.new(mapp.outputs['Alpha'], matt.inputs['Alpha'])

	return material



def set_material(obj, material):
	obj.data.materials.append(material)



def shift_images(image_planes):
	if image_planes:
		bound = Bound()
		bound = image_planes[0].bound.copy()
		for image in image_planes:
			bound.combine(image.bound)
	
	w = (bound.left + bound.right) / 2
	z = bound.bottom

	for image in image_planes:
		image.owner.location.x -= w
		image.owner.location.z -= z



class Bound:
	def __init__(self):
		self.left = 0
		self.right = 0
		self.top = 0
		self.bottom = 0

	def set(self, left, right, top, bottom):
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom
	
	def from_object(self, obj):
		location = obj.location
		self.left = obj.bound_box[0][0] + location.x
		self.right = obj.bound_box[6][0] + location.x
		self.top = obj.bound_box[6][2] + location.z
		self.bottom = obj.bound_box[0][2] + location.z

	def combine(self, bound):
		self.left = min(self.left, bound.left)
		self.right = max(self.right, bound.right)
		self.top = max(self.top, bound.top)
		self.bottom = min(self.bottom, bound.bottom)
	
	def copy(self):
		bound = Bound()
		bound.left = self.left
		bound.right = self.right
		bound.top = self.top
		bound.bottom = self.bottom
		return bound



class Image_Plane:
	def __init__(self, data, path, scale):
		self.owner = None
		self.node = data
		self.path = path
		self.scale = scale

		self.bound = Bound()

	def create(self, ctx):
		name = get_name(self)
		material = get_material(self, name)
		width, height = get_image_size(self)
		pivot_offset = get_pivot_offset(self)
		self.owner = create_sprite_plane(ctx, name, width, height, pivot_offset)
		set_material(self.owner, material)
		set_location(self)
		self.bound.from_object(self.owner)




def read_json_file(filepath):
	#TODO need to safty check
	path, _ = os.path.split(filepath)
	f = open(filepath)
	data = json.load(f)
	f.close()
	return data['name'], data['nodes'], path

		

class File_TO_Sprite_JSON_Import(Operator, ImportHelper):
	"""Import json file and setup sprite sheets"""
	bl_idname = "file.sprite_json_importer"
	bl_label = "Import JSON"

	filename_ext = ".json"
	filter_glob: StringProperty(default="*.json", options={'HIDDEN'})

	# update: BoolProperty(name="update")
	
	scale: FloatProperty(name='Scale', min=0, default=0.01)
	
	format: EnumProperty(
		name="Json Source File",
		items=(
			('COA', "COA-Tools", ""),
			('SPINE', "Spine", ""),
		),
		default='COA',
	)

	unit: EnumProperty(
		name="Source Unit",
		items=(
			('INCH', "Inch", ""),
			('METR', "Metr", ""),
		),
		default='INCH',
	)

	shading: EnumProperty(
		name="shading Mode",
		items=(
			('COLOR', "Color", ""),
			('LIGHT', "Light", ""),
		),
		default='LIGHT',
	)

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'scale', text="Scale")
		layout.prop(self, 'format', text="Json Source File")
		layout.prop(self, 'unit', text="Source Unit")
		layout.prop(self, 'shading', text="Shading Mode")

	def execute(self, ctx):
		# name, nodes, path = read_json_file(self.filepath)
		_, nodes, path = read_json_file(self.filepath)

		image_planes = []
		# bones = []

		for node in nodes:
			if node['type'] == "SPRITE":
				image_planes.append(Image_Plane(node, path, self.scale))

			elif node['type'] == "BONE":
				pass

		for image in image_planes:
			image.create(ctx)

		shift_images(image_planes)

		return {'FINISHED'}



def menu_func_import(self, ctx):
	self.layout.operator(
		"file.sprite_json_importer",
		text="Sprites (*.json) [In production]"
	)



def register_sprite_json_importer():
	bpy.utils.register_class(File_TO_Sprite_JSON_Import)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)



def unregister_sprite_json_importer():
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	if File_TO_Sprite_JSON_Import.is_registered:
		bpy.utils.unregister_class(File_TO_Sprite_JSON_Import)


if __name__ == '__main__':
	register_sprite_json_importer()
