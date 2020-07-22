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
from bsmax.state import is_mode

# TODO extend and unselect for element select

class Mesh_OT_Select_Element(Operator):
	bl_idname = "mesh.select_element"
	bl_label = "Select Element"

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "MESH_EDIT"
	
	def execute(self, ctx):
		vert,edge,face = ctx.tool_settings.mesh_select_mode
		if edge:
			bpy.ops.mesh.smart_select_loop('INVOKE_DEFAULT')
		if face:
			bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT')
		self.report({'INFO'},'bpy.ops.mesh.select_element()')
		return{"FINISHED"}
	
def register_select():
	bpy.utils.register_class(Mesh_OT_Select_Element)

def unregister_select():
	bpy.utils.unregister_class(Mesh_OT_Select_Element)