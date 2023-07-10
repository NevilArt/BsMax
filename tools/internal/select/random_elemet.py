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

import bpy, bmesh

from bpy.types import Operator



class Object_OT_Select_random_element(Operator):
	bl_idname = "object.select_random_element"
	bl_label = "Select Random Element"
	bl_options = {'REGISTER', 'UNDO'}

	elements = []
	selected = []
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.selected_objects) > 0:
				return ctx.mode == 'EDIT_MESH'
		return False
	
	def get_element(self, obj, index):
		bm = bmesh.from_edit_mesh(obj.data)
		bm.faces[4].select = True
	
	def execute(self, ctx):
		obj = ctx.active_object
		count = len(obj.data.polygons)
		index = 0
		while index <= count:
			obj.data.polygons[index].select
		return{"FINISHED"}



def register_random_element():
	bpy.utils.register_class(Object_OT_Select_random_element)



def unregister_random_element():
	bpy.utils.unregister_class(Object_OT_Select_random_element)



if __name__ == "__main__":
	register_random_element()