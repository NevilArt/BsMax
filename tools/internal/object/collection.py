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
from bpy.types import Operator



def clear_collections(obj):
	for collection in obj.users_collection:
		collection.objects.unlink(obj)


#TODO move selected collecion to active collection too
# need to get list of selected collection API
class Collection_OT_Move_To_Active(Operator):
	""" Move Selected Objects in Outliner to Active Collection """
	bl_idname = "collection.move_to_active"
	bl_label = "Move to active collection"
	bl_description = "Move selected objects in to active collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			clear_collections(obj)
			ctx.collection.objects.link(obj)
		return{"FINISHED"}



#TODO make this Link to selected collections
class Collection_OT_Link_To_Active(Operator):
	""" Add (link) Selected Objects in Outliner to Active Collection """
	bl_idname = "collection.link_to_active"
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
		return{"FINISHED"}



class Collection_OT_Remove_From_Collection(Operator):
	""" Remove (Unlink) Selected Objects in Outliner from Active Collection """
	bl_idname = "collection.remove_from_collection"
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
	bl_idname = "outliner.rename_selection"
	bl_label = "Rename"
	bl_description = "Rename objects"

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
		return{"FINISHED"}



def outliner_header(self, ctx):
	self.layout.operator("collection.move_to_active", text="", icon='ADD')
	self.layout.operator("collection.remove_from_collection", text="", icon='REMOVE')
	self.layout.operator("collection.link_to_active", text="", icon='LIBRARY_DATA_DIRECT')


classes = [Collection_OT_Move_To_Active,
	Collection_OT_Link_To_Active,
	Collection_OT_Remove_From_Collection,
	Outliner_OT_Rename_Selection]


def register_collection():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.OUTLINER_HT_header.append(outliner_header)

def unregister_collection():
	bpy.types.OUTLINER_HT_header.remove(outliner_header)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_collection()