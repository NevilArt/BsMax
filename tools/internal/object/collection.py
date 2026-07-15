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
# 2024/06/28
# 2026/08/02 Sort Selected Collection added

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


def clear_collections(obj):
	for collection in obj.users_collection:
		collection.objects.unlink(obj)


def sorted_children_order(children, selected_set):
	selected = [c for c in children if c in selected_set]
	if not selected:
		return list(children)

	first_selected_index = next(i for i, c in enumerate(children) if c in selected_set)
	unselected = [c for c in children if c not in selected_set]
	selected_sorted = sorted(selected, key=lambda c: c.name.lower())

	before = [c for c in children[:first_selected_index] if c not in selected_set]
	after = [c for c in unselected if c not in before]

	return before + selected_sorted + after


def get_collection_parent_map(root):
	parent_map = {}

	def recurse(coll):
		for child in coll.children:
			parent_map[child] = coll
			recurse(child)

	recurse(root)
	return parent_map


def sort_selected_collections(context):
	selected = get_selected_collections(context)
	if not selected:
		return

	parent_map = get_collection_parent_map(context.scene.collection)

	groups = {}
	for c in selected:
		parent = parent_map.get(c)
		if parent is None:
			continue  # scene root collection itself has no parent, skip it
		groups.setdefault(parent, []).append(c)

	for parent, sel_children in groups.items():
		children = list(parent.children)
		selected_set = set(sel_children)
		new_order = sorted_children_order(children, selected_set)

		if new_order == children:
			continue  # already in order, avoid needless unlink/relink

		for c in children:
			parent.children.unlink(c)
		for c in new_order:
			parent.children.link(c)


def get_selected_collections(context):
	"""
	Returns the list of selected Collection objects from the Outliner.
	Must be called with outliner context (e.g. via context override,
	or from an operator invoked while hovering the Outliner).
	"""
	return [item for item in context.selected_ids if isinstance(item, bpy.types.Collection)]


#TODO move selected collecion to active collection too
# need to get list of selected collection API
class Collection_OT_Move_To_Active(Operator):
	bl_idname = 'collection.move_to_active'
	bl_label = "Move to active collection"
	bl_description = "Move Selected Objects in Outliner to Active Collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			clear_collections(obj)
			ctx.collection.objects.link(obj)
		return{'FINISHED'}


#TODO make this Link to selected collections
class Collection_OT_Link_To_Active(Operator):
	bl_idname = 'collection.link_to_active'
	bl_label = "Link to active collection"
	bl_description = "Link selected objects in to active collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			if not ctx.collection in obj.users_collection:
				ctx.collection.objects.link(obj)
		return{'FINISHED'}


class Collection_OT_Remove_From_Collection(Operator):
	bl_idname = 'collection.remove_from_collection'
	bl_label = "Remove from collections"
	bl_description = "Remove objects from selected collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			if len(obj.users_collection) > 1:
				ctx.collection.objects.unlink(obj)
		return{"FINISHED"}



class Outliner_OT_Rename_Selection(Operator):
	bl_idname = 'outliner.rename_selection'
	bl_label = "Rename"
	bl_description = "Rename objects"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		#TODO put this in multi item rename operator
		count = len(ctx.selected_objects)
		if count > 1:
			bpy.ops.wm.multi_item_rename(force='OBJECT')
		elif count == 1:
			bpy.ops.outliner.item_rename('INVOKE_DEFAULT')
		return{'FINISHED'}
	

class Outliner_OT_Link_Collection_To_Scenes(Operator):
	bl_idname = 'outliner.link_to_scenes'
	bl_label = "Link To Scenes"
	bl_description = "Link Active collection to all Other Scenes"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self, ctx):
		collection = ctx.collection
		for scene in bpy.data.scenes:
			all_collection = scene.collection.children_recursive
			if collection in all_collection:
				continue

			scene.collection.children.link(collection)

		return {'FINISHED'}


class Collection_OT_Sort_Selected_Collection(Operator):
	bl_idname = 'collection.sort_selected'
	bl_label = "Sort Selected Collection"
	bl_description = "Sort Selected Collection by Name"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return bool(getattr(context, "selected_ids", None))
	
	def execute(self, context):
		sort_selected_collections(context)
		return {'FINISHED'}


def outliner_header(self, _):
	layout = self.layout
	layout.operator(
		'collection.move_to_active', text="", icon='ADD'
	)
	
	layout.operator(
		'collection.remove_from_collection', text="", icon='REMOVE'
	)

	layout.operator(
		'collection.link_to_active', text="", icon='LIBRARY_DATA_DIRECT'
	)

	layout.operator(
			'collection.sort_selected', text="", icon='SORTALPHA'
		)


def outliner_collection(self, _):
	layout = self.layout
	layout.operator('outliner.link_to_scenes', text="Link to other Scenes")
	layout.separator()


classes = {
	Collection_OT_Move_To_Active,
	Collection_OT_Link_To_Active,
	Collection_OT_Remove_From_Collection,
	Outliner_OT_Rename_Selection,
	Outliner_OT_Link_Collection_To_Scenes,
	Collection_OT_Sort_Selected_Collection
}


def register_collection():
	for cls in classes:
		register_class(cls)

	bpy.types.OUTLINER_HT_header.append(outliner_header)
	bpy.types.OUTLINER_MT_collection.prepend(outliner_collection)


def unregister_collection():
	bpy.types.OUTLINER_HT_header.remove(outliner_header)
	bpy.types.OUTLINER_MT_collection.remove(outliner_collection)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_collection()