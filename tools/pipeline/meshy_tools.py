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
# 2026/08/02 Meshy AI Auto Cleaner added
# 2026/08/05 Multi-Object support added
# TODO make it poplic operator and add to menu

import bpy
import os

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


def get_principled_bsdf(mat):
	"""Return the Principled BSDF node connected to Material Output, or None"""
	if mat is None or mat.node_tree is None:
		return None

	output_node = None
	for node in mat.node_tree.nodes:
		if node.type == 'OUTPUT_MATERIAL' and node.is_active_output:
			output_node = node
			break

	if output_node is None:
		return None

	surface_input = output_node.inputs.get("Surface")
	if not surface_input or not surface_input.is_linked:
		return None

	linked_node = surface_input.links[0].from_node
	if linked_node.type != 'BSDF_PRINCIPLED':
		return None

	return linked_node


def get_image_source_for_input(bsdf, input_name):
	"""
	Trace a BSDF input back to its source image.
	Returns (img_node, is_shared) where:
	  - img_node: the Image Texture node feeding it (directly or via Separate Color)
	  - is_shared: True if it's coming through a Separate Color/RGB node
				   (meaning the texture is packed/shared across channels)
	Returns (None, False) if nothing usable is found.
	"""
	socket = bsdf.inputs.get(input_name)
	if not socket or not socket.is_linked:
		return None, False

	node = socket.links[0].from_node

	# Direct connection: Image Texture -> BSDF input
	if node.type == 'TEX_IMAGE' and node.image is not None:
		return node, False

	# Indirect: Image Texture -> Separate Color/RGB -> BSDF input
	if node.type in ('SEPARATE_COLOR', 'SEPRGB'):
		color_input = node.inputs.get('Color') or node.inputs.get('Image')
		if color_input and color_input.is_linked:
			src_node = color_input.links[0].from_node
			if src_node.type == 'TEX_IMAGE' and src_node.image is not None:
				return src_node, True

	return None, False


def rename_data_to_match_object(obj):
	"""Rename obj.data (and its materials) to match the object's name"""
	if obj.data is None:
		return

	# Rename the data block (mesh, curve, light, camera, etc.)
	obj.data.name = obj.name

	# If it has material slots, rename each material too
	if hasattr(obj.data, "materials"):
		for slot in obj.material_slots:
			mat = slot.material
			if mat is not None:
				# If multiple slots share the same object name, suffix them
				if len(obj.material_slots) > 1:
					idx = list(obj.material_slots).index(slot)
					mat.name = f"{obj.name}_{idx:02d}"
				else:
					mat.name = obj.name


def clear_extra_attributes(obj):
	"""Remove all mesh attributes except position and UV maps"""
	mesh = obj.data

	# Collect names of UV map attributes (they live in mesh.uv_layers,
	# but are also exposed through mesh.attributes)
	uv_names = {uv.name for uv in mesh.uv_layers}

	attrs_to_remove = []
	for attr in mesh.attributes:
		if attr.name == "position":
			continue
		if attr.name in uv_names:
			continue
		if attr.is_required:
			# Some attributes are internal/required and can't be removed
			continue
		attrs_to_remove.append(attr.name)

	for name in attrs_to_remove:
		mesh.attributes.remove(mesh.attributes[name])

	return len(attrs_to_remove)

def get_connected_image_node(bsdf, input_name):
	"""Return the Image Texture node connected to a given BSDF input, or None"""
	socket = bsdf.inputs.get(input_name)
	if not socket or not socket.is_linked:
		return None

	node = socket.links[0].from_node
	if node.type != 'TEX_IMAGE' or node.image is None:
		return None

	return node

def rename_image(img_node, new_name):
	"""
	Rename an Image Texture node's image (datablock + file on disk)
	to new_name, preserving the original file extension.
	Returns True on success, False if it bailed for any reason.
	"""
	if img_node is None or img_node.type != 'TEX_IMAGE' or img_node.image is None:
		return False

	image = img_node.image

	if image.packed_file is not None:
		return False  # no file on disk to rename

	old_path = bpy.path.abspath(image.filepath)
	if not old_path or not os.path.exists(old_path):
		return False

	directory = os.path.dirname(old_path)
	_, ext = os.path.splitext(old_path)
	if not ext:
		ext = ".png"

	new_filename = f"{new_name}{ext}"
	new_path = os.path.join(directory, new_filename)

	if os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(old_path):
		return False  # don't overwrite a different existing file

	if os.path.abspath(new_path) == os.path.abspath(old_path):
		# Already correctly named, just make sure datablock name matches
		image.name = new_filename
		return True

	os.rename(old_path, new_path)
	image.filepath = new_path
	image.name = new_filename
	image.reload()

	return True

def rename_metallic_roughness(mat, bsdf):
	"""
	Handles Metallic + Roughness together:
	- if either/both come through a Separate Color node from ONE shared image,
	  rename that image once to <material_name>_MR
	- if directly connected (no packing), rename each independently
	"""
	metal_node, metal_shared = get_image_source_for_input(bsdf, "Metallic")
	rough_node, rough_shared = get_image_source_for_input(bsdf, "Roughness")

	# Case 1: both point to the same shared image via Separate Color
	if metal_shared and rough_shared and metal_node is rough_node:
		rename_image(metal_node, f"{mat.name}_MR")
		return

	# Case 2: independent handling (covers direct connections,
	# or shared-but-different-image edge cases)
	if metal_node is not None:
		if metal_shared:
			rename_image(metal_node, f"{mat.name}_MR")
		else:
			rename_image(metal_node, f"{mat.name}_Metallic")
		metal_node.image.colorspace_settings.name = 'Non-Color'

	if rough_node is not None and rough_node is not metal_node:
		if rough_shared:
			rename_image(rough_node, f"{mat.name}_MR")
		else:
			rename_image(rough_node, f"{mat.name}_Roughness")
		rough_node.image.colorspace_settings.name = 'Non-Color'


def get_normal_map_image_node(bsdf):
	"""
	Trace the Normal input back through the Normal Map node to find
	the source Image Texture node. Returns the img_node, or None.
	"""
	normal_input = bsdf.inputs.get("Normal")
	if not normal_input or not normal_input.is_linked:
		return None

	normal_map_node = normal_input.links[0].from_node
	if normal_map_node.type != 'NORMAL_MAP':
		return None  # Normal isn't fed by a Normal Map node — bail per your rule

	color_input = normal_map_node.inputs.get("Color")
	if not color_input or not color_input.is_linked:
		return None

	img_node = color_input.links[0].from_node
	if img_node.type != 'TEX_IMAGE' or img_node.image is None:
		return None

	return img_node


def rename_normal_map(mat, bsdf):
	"""Rename the image feeding the Normal Map node as <material_name>_Normal"""
	img_node = get_normal_map_image_node(bsdf)
	if img_node is None:
		return False
	rename_image(img_node, f"{mat.name}_Normal")
	img_node.image.colorspace_settings.name = 'Non-Color'
	return True


def rename_textures(mat):
	bsdf = get_principled_bsdf(mat)
	if not bsdf:
		return {'CANCELLED'}
	
	base_color_node = get_connected_image_node(bsdf, "Base Color")
	rename_image(base_color_node, mat.name + "_Color")

	rename_metallic_roughness(mat, bsdf)
	rename_normal_map(mat, bsdf)


def set_color_spaces(mat):
	"""
	Set colorspace to 'Non-Color' for all image texture nodes in the material
	except the one connected to Base Color (which stays 'sRGB').
	"""
	bsdf = get_principled_bsdf(mat)
	base_color_input = bsdf.inputs.get("Base Color")
	base_color_node = None

	if base_color_input and base_color_input.is_linked:
		candidate = base_color_input.links[0].from_node
		if candidate.type == 'TEX_IMAGE' and candidate.image is not None:
			base_color_node = candidate

	for node in mat.node_tree.nodes:
		if node.type != 'TEX_IMAGE' or node.image is None:
			continue

		if node is base_color_node:
			continue

		node.image.colorspace_settings.name = 'Non-Color'


class OBJECT_OT_MeshyAI_Auto_Cleaner(Operator):
	"""Mesh AI Auto Tool"""
	bl_idname = "object.meshy_ai_auto_cleaner"
	bl_label = "Meshy AI Auto Cleaner"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		# Return True/False to control when this operator is available
		return context.active_object is not None

	def execute(self, context):
		for obj in context.selected_objects:
			if obj.type != 'MESH':
				continue

			rename_data_to_match_object(obj)
			clear_extra_attributes(obj)

			for mat in obj.data.materials:
				if mat is None:
					continue
				rename_textures(mat)
				set_color_spaces(mat)

		return {'FINISHED'}


classes = {
	OBJECT_OT_MeshyAI_Auto_Cleaner
}

def register_meshy_tools():
	for cls in classes:
		register_class(cls)

def unregister_meshy_tools():
	for cls in classes:
		if cls.is_registered:
			unregister_class(cls)

if __name__ == '__main__':
	register_meshy_tools()