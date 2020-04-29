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

# TODO extend and unselect for element select

class BsMax_OT_SelectElement(Operator):
	bl_idname = "mesh.selectelement"
	bl_label = "Select Element"
	def execute(self, ctx):
		if ctx.active_object != None:
			if ctx.mode == "EDIT_MESH":
				v,e,f = ctx.tool_settings.mesh_select_mode
				if v:
					pass
				if e:
					bpy.ops.mesh.smart_select_loop('INVOKE_DEFAULT')
				if f:
					bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT')
		return{"FINISHED"}
	
def register_select():
	bpy.utils.register_class(BsMax_OT_SelectElement)

def unregister_select():
	bpy.utils.unregister_class(BsMax_OT_SelectElement)