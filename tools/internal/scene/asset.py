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
#2026/09/25 Created

import bpy
from bpy.types import Operator

class BSMAX_OT_object_to_own_collection(Operator):
	"""Create a collection named after each selected object and move it there"""
	bl_idname = "bsmax.object_to_own_collection"
	bl_label = "Object To Own Collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return len(context.selected_objects) > 0

	def execute(self, context):
		for obj in list(context.selected_objects):
			# reuse existing collection with same name, or create one
			coll = bpy.data.collections.get(obj.name)
			if coll is None:
				coll = bpy.data.collections.new(obj.name)
				context.scene.collection.children.link(coll)

			# unlink from all current collections
			for c in list(obj.users_collection):
				c.objects.unlink(obj)

			# link to the new/target collection
			coll.objects.link(obj)

		return {'FINISHED'}


def register_asset():
	bpy.utils.register_class(BSMAX_OT_object_to_own_collection)


def unregister_asset():
	bpy.utils.unregister_class(BSMAX_OT_object_to_own_collection)


if __name__ == "__main__":
	register_asset()
