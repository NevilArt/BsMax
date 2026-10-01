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
# 2026/09/16 Created for Blender 4.5+ (Python 3.12)
# TODO hi/low auto detect, separate all action to functions
# TODO Edit the UI

import bpy
import os

from bpy.types import Operator, Panel
from bpy.props import IntProperty, BoolProperty


def get_hipoly_lowpoly(context):
	"""Active selected mesh = lowpoly (target). Other selected mesh = hipoly (source)."""
	sel = [o for o in context.selected_objects if o.type == 'MESH']
	if len(sel) != 2:
		return None, None, "Select exactly 2 mesh objects (hipoly source + lowpoly target)."

	active = context.view_layer.objects.active
	if active not in sel:
		# Fallback: just take the two, warn nothing, pick first as lowpoly.
		lowpoly = sel[0]
		hipoly = sel[1]
	else:
		lowpoly = active
		hipoly = sel[0] if sel[1] is lowpoly else sel[1]

	if lowpoly.data.uv_layers is None or len(lowpoly.data.uv_layers) == 0:
		return None, None, f"Lowpoly object '{lowpoly.name}' has no UV map. Unwrap it first."

	return hipoly, lowpoly, None


def ensure_texture_dir():
	blend_path = bpy.data.filepath
	if not blend_path:
		return None, "Save the .blend file first (textures are saved next to it)."
	folder = os.path.join(os.path.dirname(blend_path), "texture")
	os.makedirs(folder, exist_ok=True)
	return folder, None


def get_or_create_principled(mat):
	mat.use_nodes = True
	tree = mat.node_tree
	for node in tree.nodes:
		if node.type == 'BSDF_PRINCIPLED':
			return node
	node = tree.nodes.new('ShaderNodeBsdfPrincipled')
	return node


def get_output_node(mat):
	tree = mat.node_tree
	for node in tree.nodes:
		if node.type == 'OUTPUT_MATERIAL':
			return node
	node = tree.nodes.new('ShaderNodeOutputMaterial')
	return node


def make_bake_image(name, res, colorspace):
	img = bpy.data.images.new(name=name, width=res, height=res, alpha=False)
	img.colorspace_settings.name = colorspace
	img.generated_color = (0.0, 0.0, 0.0, 1.0)
	return img


def add_image_node(mat, image, location):
	node = mat.node_tree.nodes.new('ShaderNodeTexImage')
	node.image = image
	node.location = location
	return node


def set_only_active_bake_node(mat, node):
	for n in mat.node_tree.nodes:
		n.select = False
	node.select = True
	mat.node_tree.nodes.active = node


def select_for_bake(context, hipoly, lowpoly):
	bpy.ops.object.select_all(action='DESELECT')
	hipoly.select_set(True)
	lowpoly.select_set(True)
	context.view_layer.objects.active = lowpoly


def save_image(image, folder, obj_name, suffix):
	filename = f"{obj_name}_{suffix}.png"
	path = os.path.join(folder, filename)
	image.filepath_raw = path
	image.file_format = 'PNG'
	image.save()
	return path


# --- Metallic bake workaround (no native "Metallic" bake pass in Blender) ---

def rig_metallic_emit(hipoly):
	"""For every material on hipoly, reroute Metallic input into an Emission
	shader plugged into the output, so it can be baked with type='EMIT'.
	Returns a list of restore-info dicts."""
	restore_info = []
	for slot in hipoly.material_slots:
		mat = slot.material
		if mat is None or not mat.use_nodes:
			continue
		tree = mat.node_tree
		principled = None
		for node in tree.nodes:
			if node.type == 'BSDF_PRINCIPLED':
				principled = node
				break
		if principled is None or 'Metallic' not in principled.inputs:
			continue

		output = get_output_node(mat)
		surface_input = output.inputs.get('Surface')
		orig_from_socket = None
		if surface_input and surface_input.is_linked:
			orig_from_socket = surface_input.links[0].from_socket

		emission = tree.nodes.new('ShaderNodeEmission')
		emission.location = (principled.location.x, principled.location.y - 300)

		metallic_input = principled.inputs['Metallic']
		if metallic_input.is_linked:
			src_socket = metallic_input.links[0].from_socket
			tree.links.new(src_socket, emission.inputs['Color'])
		else:
			v = metallic_input.default_value
			emission.inputs['Color'].default_value = (v, v, v, 1.0)

		if surface_input:
			tree.links.new(emission.outputs['Emission'], surface_input)

		restore_info.append({
			'mat': mat,
			'emission_node': emission,
			'output': output,
			'orig_from_socket': orig_from_socket,
		})
	return restore_info


def unrig_metallic_emit(restore_info):
	for info in restore_info:
		mat = info['mat']
		tree = mat.node_tree
		output = info['output']
		surface_input = output.inputs.get('Surface')
		if surface_input:
			for link in list(surface_input.links):
				tree.links.remove(link)
			if info['orig_from_socket'] is not None:
				tree.links.new(info['orig_from_socket'], surface_input)
		tree.nodes.remove(info['emission_node'])


# ----------------------------------------------------------------------
# Operator
# ----------------------------------------------------------------------

class OBJECT_OT_pbr_bake_setup(Operator):
	bl_idname = "object.pbr_bake_setup"
	bl_label = "Bake PBR Textures (Hi -> Lo)"
	bl_description = "Bake Base Color / Roughness / Metallic / Normal from hipoly to lowpoly"
	bl_options = {'REGISTER', 'UNDO'}

	resolution: IntProperty(
		name="Resolution",
		description="Texture size in pixels (square, e.g. 1024 = 1024x1024)",
		default=1024, min=64, max=8192,
	) # type: ignore

	bake_base_color: BoolProperty(
		name="Base Color (required)", default=True,
	) # type: ignore

	bake_roughness: BoolProperty(
		name="Roughness", default=True,
	) # type: ignore

	bake_metallic: BoolProperty(
		name="Metallic", default=True,
	) # type: ignore

	bake_normal: BoolProperty(
		name="Normal", default=True,
	) # type: ignore

	def invoke(self, context, event):
		hipoly, lowpoly, err = get_hipoly_lowpoly(context)
		if err:
			self.report({'ERROR'}, err)
			return {'CANCELLED'}
		self.bake_base_color = True
		return context.window_manager.invoke_props_dialog(self, width=320)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "resolution")
		layout.separator()
		layout.label(text="Maps to bake:")
		row = layout.row()
		row.enabled = False
		row.prop(self, "bake_base_color")
		layout.prop(self, "bake_roughness")
		layout.prop(self, "bake_metallic")
		layout.prop(self, "bake_normal")

	def execute(self, context):
		scene = context.scene

		hipoly, lowpoly, err = get_hipoly_lowpoly(context)
		if err:
			self.report({'ERROR'}, err)
			return {'CANCELLED'}

		folder, err = ensure_texture_dir()
		if err:
			self.report({'ERROR'}, err)
			return {'CANCELLED'}

		obj_name = lowpoly.name
		res = self.resolution

		# --- Build fresh material on lowpoly ---
		mat = bpy.data.materials.new(name=obj_name)
		mat.use_nodes = True
		lowpoly.data.materials.clear()
		lowpoly.data.materials.append(mat)

		principled = get_or_create_principled(mat)
		output = get_output_node(mat)
		if not any(l.to_node == output for l in mat.node_tree.links) :
			pass
		mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])

		# --- Store & set up render settings for baking ---
		orig_engine = scene.render.engine
		orig_samples = scene.cycles.samples if hasattr(scene, "cycles") else None
		scene.render.engine = 'CYCLES'
		scene.cycles.samples = 32
		scene.render.bake.use_selected_to_active = True
		scene.render.bake.cage_extrusion = 0.2
		scene.render.bake.margin = 16

		saved_paths = []
		y_pos = 300

		try:
			select_for_bake(context, hipoly, lowpoly)

			# ---- Base Color (always baked) ----
			img = make_bake_image(f"{obj_name}_BaseColor", res, 'sRGB')
			node = add_image_node(mat, img, (-600, y_pos)); y_pos -= 300
			set_only_active_bake_node(mat, node)
			bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
			saved_paths.append(save_image(img, folder, obj_name, "Color"))
			mat.node_tree.links.new(node.outputs['Color'], principled.inputs['Base Color'])

			# ---- Roughness ----
			if self.bake_roughness:
				img = make_bake_image(f"{obj_name}_Roughness", res, 'Non-Color')
				node = add_image_node(mat, img, (-600, y_pos)); y_pos -= 300
				set_only_active_bake_node(mat, node)
				bpy.ops.object.bake(type='ROUGHNESS')
				saved_paths.append(save_image(img, folder, obj_name, "Roughness"))
				mat.node_tree.links.new(node.outputs['Color'], principled.inputs['Roughness'])

			# ---- Metallic (via Emission workaround) ----
			if self.bake_metallic:
				img = make_bake_image(f"{obj_name}_Metallic", res, 'Non-Color')
				node = add_image_node(mat, img, (-600, y_pos)); y_pos -= 300
				set_only_active_bake_node(mat, node)
				restore_info = rig_metallic_emit(hipoly)
				try:
					bpy.ops.object.bake(type='EMIT')
				finally:
					unrig_metallic_emit(restore_info)
				saved_paths.append(save_image(img, folder, obj_name, "Metallic"))
				mat.node_tree.links.new(node.outputs['Color'], principled.inputs['Metallic'])

			# ---- Normal ----
			if self.bake_normal:
				img = make_bake_image(f"{obj_name}_Normal", res, 'Non-Color')
				node = add_image_node(mat, img, (-600, y_pos)); y_pos -= 300
				set_only_active_bake_node(mat, node)
				bpy.ops.object.bake(type='NORMAL', normal_space='TANGENT')
				saved_paths.append(save_image(img, folder, obj_name, "Normal"))
				normal_map_node = mat.node_tree.nodes.new('ShaderNodeNormalMap')
				normal_map_node.location = (-300, y_pos + 150)
				mat.node_tree.links.new(node.outputs['Color'], normal_map_node.inputs['Color'])
				mat.node_tree.links.new(normal_map_node.outputs['Normal'], principled.inputs['Normal'])

		except RuntimeError as e:
			self.report({'ERROR'}, f"Bake failed: {e}")
			return {'CANCELLED'}
		finally:
			scene.render.engine = orig_engine
			if orig_samples is not None:
				scene.cycles.samples = orig_samples

		self.report({'INFO'}, f"Baked {len(saved_paths)} texture(s) to {folder}")
		return {'FINISHED'}


class VIEW3D_PT_pbr_bake(Panel):
	bl_label = "PBR Bake (Hi -> Lo)"
	bl_idname = "VIEW3D_PT_pbr_bake"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "PBR Bake"

	def draw(self, _):
		layout = self.layout
		layout.label(text="Select hipoly, then lowpoly")
		layout.label(text="(lowpoly must be active).")
		layout.operator("object.pbr_bake_setup", icon='RENDER_STILL')


def menu_func(self, _):
	self.layout.operator(OBJECT_OT_pbr_bake_setup.bl_idname, icon='RENDER_STILL')


classes = {
	OBJECT_OT_pbr_bake_setup,
	VIEW3D_PT_pbr_bake,
}


def register_quaick_bake():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister_quaick_bake():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	for cls in classes:
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register_quaick_bake()
