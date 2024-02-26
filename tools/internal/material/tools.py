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
# 2024/02/25

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class Object_TO_Material_Slot_Remove_Plus(Operator):
	bl_idname = 'object.material_slot_remove_plus'
	bl_label = 'Remove Material Slot'
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	bl_description = "Remove The Selected Material Slot"
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'
	
	def execute(self,ctx):
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		bpy.ops.object.material_slot_remove()
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		return{'FINISHED'}


classes = (
	Object_TO_Material_Slot_Remove_Plus,
)


def register_tools():
	for c in classes:
		register_class(c)


def unregister_tools():
	for c in classes:
		unregister_class(c)


if __name__ == '__main__':
	register_tools()