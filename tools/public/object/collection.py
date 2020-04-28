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
from bpy.types import Operator,Menu

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

class BsMax_OT_MoveToActiveCollection(Operator):
	bl_idname = "collection.movetoactivecollection"
	bl_label = "Move to active collection"
	bl_description = "Move selected objects in to active collection"

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		active_collection = get_active_collection(ctx)
		active_layer = bpy.context.view_layer.active_layer_collection
		for obj in ctx.selected_objects:
			clear_collections(ctx,obj)
			active_collection.objects.link(obj)
		ctx.view_layer.active_layer_collection = active_layer
		return{"FINISHED"}

def outliner_header(self,ctx):
	self.layout.operator("collection.movetoactivecollection", text="", icon='ADD')

def register_collection():
	bpy.utils.register_class(BsMax_OT_MoveToActiveCollection)
	bpy.types.OUTLINER_HT_header.append(outliner_header)

def unregister_collection():
	bpy.types.OUTLINER_HT_header.remove(outliner_header)
	bpy.utils.unregister_class(BsMax_OT_MoveToActiveCollection)