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


class Console_OT_Cut(Operator):
	bl_idname = "console.cut"
	bl_label = "Cut"
	def execute(self, ctx):
		bpy.ops.console.copy('INVOKE_DEFAULT')
		bpy.ops.console.delete('INVOKE_DEFAULT')
		return {'FINISHED'}


def register_console():
	bpy.utils.register_class(Console_OT_Cut)


def unregister_console():
	bpy.utils.unregister_class(Console_OT_Cut)