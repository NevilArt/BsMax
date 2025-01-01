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
import os

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from time import sleep


def delete_isolated_empties():
	object_count = len(bpy.data.objects)
	
	for obj in bpy.data.objects:
		if obj.type != 'EMPTY':
			continue

		if obj.children:
			continue

		bpy.data.objects.remove(obj)

	if object_count == len(bpy.data.objects):
		return
	
	delete_isolated_empties()


def delete_by_namekeys(keys):
	for key in keys:
		for obj in bpy.data.objects:
			if key in obj.name:
				bpy.data.objects.remove(obj)
	delete_isolated_empties()


def delete_by_hierarchy(obj):
	objs = obj.children_recursive
	objs += [obj]
	for obj in objs:
		try:
			bpy.data.objects.remove(obj)
		except:
			pass


def delete_layout(ctx):
	objs = []
	camera = None
	# collect all layout objects
	for name in ['Char_Parent', 'Env_Parent']:
		if name in bpy.data.objects:
			parent = bpy.data.objects[name]
			objs.append(parent)
			objs += parent.children_recursive

	# detect camera of layout
	for obj in objs:
		if obj.type == 'CAMERA':
			camera = obj
			break
	
	# unlink camera from parents
	if camera:
		bpy.ops.object.select_all(action='DESELECT')
		camera.select_set(True)
		ctx.view_layer.objects.active = obj
		bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

	# delete all layout objects
	for name in ['Char_Parent', 'Env_Parent']:
		if name in bpy.data.objects:
			delete_by_hierarchy(bpy.data.objects[name])

	return camera


def delete_free_cameras():
	bpy.ops.object.select_all(action='DESELECT')

	for cam in bpy.data.objects:
		if cam.type != 'CAMERA':
			continue
		
		if cam.parent:
			continue

		bpy.data.objects.remove(cam)


def delete_curves():
	for obj in bpy.data.objects:
		if obj.type == 'CURVES':
			bpy.data.objects.remove(obj)
	delete_isolated_empties()


def delete_non_geometry_branches():
	# delete empty objects witout parent and
	# name dose not countain :Geometry
	for obj in bpy.data.objects:
		if obj.type != 'EMPTY':
			continue
		
		if obj.parent:
			continue
		
		if ':Geometry' in obj.name:
			continue

		delete_by_hierarchy(obj)

	delete_isolated_empties()


def delete_mesh_geometry():
	# Delete empty objects with :MeshGeometry on name
	for obj in bpy.data.objects:
		if obj.type != 'EMPTY':
			continue
		
		if ':MeshGeometry' in obj.name:
			delete_by_hierarchy(obj)

	delete_isolated_empties()


def delete_special_sufixes(type, suffix):
	for obj in bpy.data.objects:
		if obj.type != type:
			continue

		if obj.name.lower().endswith(suffix):
			bpy.data.objects.remove(obj)

	delete_isolated_empties()


def delete_special_keys(type, suffix):
	for obj in bpy.data.objects:
		if obj.type != type:
			continue

		if suffix in obj.name.lower():
			bpy.data.objects.remove(obj)

	delete_isolated_empties()


def force_get_colection(ctx, name):
	collections = bpy.data.collections
	if name in collections:
		collection = collections[name]
		return collection

	newCollection = collections.new(name)
	ctx.scene.collection.children.link(newCollection)
	return newCollection


def link_objs_to_collection(objs, collection):
	for obj in objs:
		for layer in obj.users_collection:
			layer.objects.unlink(obj)
		collection.objects.link(obj)


def put_everything_in_new_collection(ctx):
	collection = force_get_colection(ctx, "ABC Meshes")
	objs = bpy.data.objects
	link_objs_to_collection(objs, collection)


# objects are in condition that not able to auto detect for now
# listed here and to delete by name
# TODO put this in a text file in project refrence or repository folder
# and let code stay dynamic for difrent projects
def check_black_list():
	balack_list = {
		"Ayse_Rig_Final:Ayse_Face_main1",
		"Ayse_Rig_Final:Ayse_Face_main5",
		"Ayse_Rig_Final:Ayse_Face_main7",
		"Ayse_Rig_Final:Ayse_Face_main6",
		"Cemil_Rig_Final:Cemil_Labtume_bl_shape_geo",
		"Zahra_Rig_Final:Zahra_Face1",
		"kerim_Rig_V1:Kerim_Eyebrows_Wrapped",
		"kerim_Rig_V1:Kerim_Face1",
		"kerim_Rig_V1:Kerim_Face2"
	}
	for name in balack_list:
		if name in bpy.data.objects:
			obj = bpy.data.objects[name]
			bpy.data.objects.remove(obj)
	delete_isolated_empties()


# long delays couse the blender crash
# short sleep delays solve the issue for now
def clean_abc_scene(ctx):
	delete_free_cameras()
	delete_layout(ctx)
	sleep(0.1)

	delete_curves()
	sleep(0.1)

	keys = {':skinCage', ':Group'}
	delete_by_namekeys(keys)
	sleep(0.1)

	delete_non_geometry_branches()
	sleep(0.1)

	delete_mesh_geometry()
	sleep(0.1)


	delete_special_sufixes('MESH', "_prx")
	delete_special_sufixes('MESH', "_wrap")
	delete_special_keys('MESH', "_prx")
	delete_special_keys('MESH', "_proxy")
	delete_special_keys('MESH', "base")

	check_black_list()

	put_everything_in_new_collection(ctx)


def get_character_parents(ctx):
	main_parents = []
	for obj in bpy.data.objects:
		if obj.parent:
			continue

		if obj.type == 'EMPTY':
			main_parents.append(obj)
	return main_parents


def geuss_character_name(empty_name):
	parts = empty_name.split(':')
	if len(parts) == 1:
		return empty_name
	
	
	parts = parts[0].split('_')
	if len(parts) == 1:
		return parts[0]

	name = ""
	keys = {'rig', 'final'}
	for part in parts:
		if part.lower() in keys:
			break

		if name:
			name += '_'

		name += part

	return name


def geuss_charater_part_name(name):
	parts = name.split(':')
	if len(parts) == 1:
		return name
	return parts[1]


def get_mesh_objects_from_branch(root):
	mesh_objects = []
	objs = root.children_recursive
	for obj in objs:
		if obj.type == 'MESH':
			mesh_objects.append(obj)
	return mesh_objects


def get_safe_clone_node_groupe():
	if "Safe Clone" in bpy.data.node_groups:
		return bpy.data.node_groups["Safe Clone"]

	new_node_group = bpy.data.node_groups.new("Safe Clone", 'GeometryNodeTree')
	new_node_group.interface.new_socket(
		name="Geo In", in_out ="INPUT", socket_type="NodeSocketGeometry"
	)

	new_node_group.interface.new_socket(
		name="Obj In", in_out ="INPUT", socket_type="NodeSocketObject"
	)
	
	new_node_group.interface.new_socket(
		name="Geo Out", in_out ="OUTPUT", socket_type="NodeSocketGeometry"
	)

	gn_input = new_node_group.nodes.new('NodeGroupInput')
	gn_input.location = (-200, 0)

	gn_objinfo = new_node_group.nodes.new('GeometryNodeObjectInfo')
	gn_objinfo.transform_space = 'RELATIVE'

	gn_output = new_node_group.nodes.new('NodeGroupOutput')
	gn_output.location = (200, 0)

	new_node_group.links.new(
		gn_input.outputs[1], gn_objinfo.inputs[0]
	)
	
	new_node_group.links.new(
		gn_objinfo.outputs[4], gn_output.inputs[0]
	)

	return new_node_group


def create_safe_clones(ctx, mesh, collection):
	name = geuss_charater_part_name(mesh.name)
	mehs_date = bpy.data.meshes.new(name)
	new_object = bpy.data.objects.new(name, mehs_date)
	collection.objects.link(new_object)
	modifier = new_object.modifiers.new(name="Safe Clone", type='NODES')
	node_groupe = get_safe_clone_node_groupe()
	modifier.node_group = node_groupe
	modifier['Socket_1'] = mesh


def get_abc_file_name(suffix):
	file_name = bpy.data.filepath
	abc_folder = os.path.dirname(file_name) + os.sep + 'ABC'
	preffix = os.path.basename(file_name).split('.')[0]

	if not os.path.isdir(abc_folder):
		os.mkdir(abc_folder)

	return "//ABC" + os.sep + preffix + "_" + suffix + ".ABC"


def collection_export_setup(ctx, collection):
	layer_collection = ctx.view_layer.layer_collection.children[collection.name]
	ctx.view_layer.active_layer_collection = layer_collection

	if not 'Alembic' in collection.exporters:
		bpy.ops.collection.exporter_add(name="IO_FH_alembic")

	export_data = {
		'filepath': get_abc_file_name(collection.name),
		'start': ctx.scene.frame_start,
		'end': ctx.scene.frame_end,
		'evaluation_mode': 0,
		'use_instancing': False,
		'uvs': False,
		'normals': False,
		'face_sets': False,
		'orcos': False,
		'packuv': False,
		'apply_subdiv': False,
		'export_custom_properties': False,
		'export_hair': False,
		'export_particles': False,
		'curves_as_mesh': False,
		'subdiv_schema': False,
		'vcolors': False,
		'triangulate': False
	}

	export_properties = collection.exporters['Alembic'].export_properties
	for key, value in export_data.items():
		export_properties[key] = value


def create_safe_clone_of_charcters(ctx):
	chararacter_parents = get_character_parents(ctx)
	
	for character in chararacter_parents:
		name = geuss_character_name(character.name)
		collection = force_get_colection(ctx, name)
		charater_meshs = get_mesh_objects_from_branch(character)
		for mesh in charater_meshs:
			create_safe_clones(ctx, mesh, collection)
		collection_export_setup(ctx, collection)


class Nevil_OT_Maya_ABC_Cleaner(Operator):
	bl_idname = 'nevil.maya_abc_cleaner'
	bl_label = "Clear ABC from Maya v1 (Nevil)"
	bl_description = "Clear and meake redy for export abc scene from maya"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		clean_abc_scene(ctx)
		create_safe_clone_of_charcters(ctx)
		return{'FINISHED'}


classes = {
	Nevil_OT_Maya_ABC_Cleaner
}


def register_maya_abc_cleaner():
	for cls in classes:
		register_class(cls)


def unregister_maya_abc_cleaner():
	for cls in classes:
		if cls.is_registered:
			unregister_class(cls)


if __name__ == '__main__':
	register_maya_abc_cleaner()