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
# 2026/09/20 Created

import bpy
from bpy.types import Operator


def get_mirror_name(name):
	"""Return the opposite-side name for a .L/.R shape key, or None if it doesn't apply."""
	if name.endswith(".L"):
		return name[:-2] + ".R"
	elif name.endswith(".R"):
		return name[:-2] + ".L"
	return None


class OBJECT_OT_shape_key_create_mirror(Operator):
	"""Duplicate every .L/.R shape key that has no opposite yet, rename it to the opposite side and mirror it"""
	bl_idname = "object.shape_key_create_mirror"
	bl_label = "Create Mirror"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.object
		if obj is None or obj.type != 'MESH':
			return False
		if obj.data.shape_keys is None:
			return False
		key_blocks = obj.data.shape_keys.key_blocks
		return any(get_mirror_name(kb.name) for kb in key_blocks)

	def execute(self, context):
		obj = context.object
		key_blocks = obj.data.shape_keys.key_blocks

		existing_names = {kb.name for kb in key_blocks}
		# Snapshot source names up front so newly created mirrors aren't
		# processed again in the same run.
		source_names = [kb.name for kb in key_blocks if get_mirror_name(kb.name)]

		original_active_index = obj.active_shape_key_index
		created = []

		for source_name in source_names:
			mirror_name = get_mirror_name(source_name)

			if mirror_name in existing_names:
				continue  # already has a mirror, skip it

			src_index = key_blocks.find(source_name)
			if src_index == -1:
				continue  # shouldn't happen, but stay safe

			obj.active_shape_key_index = src_index

			# 1. Duplicate
			bpy.ops.object.shape_key_copy()

			# The duplicate becomes the new active shape key
			new_key = obj.active_shape_key

			# 2. Rename to the opposite side
			new_key.name = mirror_name

			# 3. Mirror it in place (X axis, topology mirror off by default)
			bpy.ops.object.shape_key_mirror(use_topology=False)

			existing_names.add(mirror_name)
			created.append(mirror_name)

		# Restore original active index if it's still valid
		if original_active_index < len(key_blocks):
			obj.active_shape_key_index = original_active_index

		if created:
			self.report({'INFO'}, f"Created {len(created)} mirrored shape key(s): {', '.join(created)}")
		else:
			self.report({'INFO'}, "No new mirrors needed - all .L/.R shape keys already have one")

		return {'FINISHED'}


def draw_menu(self, context):
	self.layout.separator()
	self.layout.operator(
		OBJECT_OT_shape_key_create_mirror.bl_idname,
		icon='MOD_MIRROR'
	)


classes = {OBJECT_OT_shape_key_create_mirror}


def register_shapekey_mirror():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.MESH_MT_shape_key_context_menu.append(draw_menu)


def unregister_shapekey_mirror():
	bpy.types.MESH_MT_shape_key_context_menu.remove(draw_menu)

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register_shapekey_mirror()