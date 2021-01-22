############################################################################
#	BsMax, 3D apps inteface simulator and tools pack for Blender
#	Copyright (C) 2020  Naser Merati (Nevil)
#
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

# Idea from "Kursad Karatas"
# https://blender.stackexchange.com/questions/15172/turn-weight-paintvertex-groups-into-vertex-paint

import bpy
from mathutils import Color
from bpy.props import BoolProperty
from bpy.types import Operator

class Object_OT_Weight_to_Vertex_Color(Operator):
	bl_idname = "object.weight_to_vertex_color"
	bl_label = "Weight to Vertex Color"
	bl_space_type = "VIEW_3D"
	bl_options = {'REGISTER', 'UNDO'}
	
	colored: BoolProperty(name="Color / BW", default=False)

	@classmethod
	def poll(cls, ctx):
		return ctx.active_object is not None

	def transfer_weight_to_vertex_color(self, obj):
		col = Color()
		col.r, col.g, col.b = 1, 1, 1
		col.h, col.s, col.v = 0, 1, 1
		
		for poly in obj.data.polygons:
			for loop in poly.loop_indices:
				weight = 0
				vertindex = obj.data.loops[loop].vertex_index		
				try:
					weight = obj.vertex_groups.active.weight(vertindex)
					if self.colored:
						col.h, col.s, col.v = 0.6666 * weight, 1, 1
					else:
						col.r = col.g = col.b = weight
				except:
					if self.colored:
						col.r, col.g, col.b = 1, 1, 1
						col.h, col.s, col.v = 0.666, 1, 1
					else:
						col.h, col.s, col.v = 0, 1, 1
						col.r, col.g, col.b = 0, 0, 0
				
				obj.data.vertex_colors.active.data[loop].color = (col.b, col.g, col.r, 1)

	def check_for_active_chanels(self, obj):
		if obj.vertex_groups.active_index == -1:
			return False
		if obj.data.vertex_colors.active_index == -1:
			obj.data.vertex_colors.new(name=obj.vertex_groups.active.name)
		return True

	def draw(self, ctx):
		layout = self.layout
		icon = 'COLORSET_13_VEC' if self.colored else 'COLORSET_02_VEC'
		layout.prop(self, 'colored', icon=icon)
	
	def check(self, ctx):
		self.transfer_weight_to_vertex_color(ctx.active_object)
		ctx.active_object.data.update()
	
	def execute(self, ctx):
		if self.check_for_active_chanels(ctx.active_object):
			self.transfer_weight_to_vertex_color(ctx.active_object)
			ctx.active_object.data.update()
		# self.report({'OPERATOR'},'bpy.ops.object.weight_to_vertex_color()')
		return {'FINISHED'}


def paint_menu(self,ctx):
	self.layout.separator()
	self.layout.operator("object.weight_to_vertex_color")

def register_paint():
	bpy.utils.register_class(Object_OT_Weight_to_Vertex_Color)
	bpy.types.VIEW3D_MT_paint_vertex.append(paint_menu)

def unregister_paint():
	bpy.types.VIEW3D_MT_paint_vertex.remove(paint_menu)
	bpy.utils.unregister_class(Object_OT_Weight_to_Vertex_Color)

if __name__ == "__main__":
	register_paint()