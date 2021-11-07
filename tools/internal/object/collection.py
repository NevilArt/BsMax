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
from bpy.types import Operator, Menu



def get_active_collection(ctx):
	active_layer_name = ctx.view_layer.active_layer_collection.name
	if active_layer_name == "Master Collection":
		collection = ctx.scene.collection
	else:
		collection = bpy.data.collections[active_layer_name]
	return collection

def clear_collections(ctx, obj):
	for collection in obj.users_collection:
		collection.objects.unlink(obj)



class Collection_OT_Move_To_Active(Operator):
	bl_idname = "collection.move_to_active"
	bl_label = "Move to active collection"
	bl_description = "Move selected objects in to active collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		active_collection = get_active_collection(ctx)
		active_layer = ctx.view_layer.active_layer_collection
		for obj in ctx.selected_objects:
			clear_collections(ctx, obj)
			active_collection.objects.link(obj)
		ctx.view_layer.active_layer_collection = active_layer
		return{"FINISHED"}



class Collection_OT_Link_To_Active(Operator):
	bl_idname = "collection.link_to_active"
	bl_label = "Link to active collection"
	bl_description = "Link selected objects in to active collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		active_collection = get_active_collection(ctx)
		active_layer = ctx.view_layer.active_layer_collection
		for obj in ctx.selected_objects:
			#TODO check is in coolection or not
			active_collection.objects.link(obj)
		ctx.view_layer.active_layer_collection = active_layer
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
	self.layout.operator("collection.link_to_active", text="", icon='LIBRARY_DATA_DIRECT')


classes = [Collection_OT_Move_To_Active,
	Collection_OT_Link_To_Active,
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