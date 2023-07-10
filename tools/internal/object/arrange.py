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

from mathutils import Vector
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty

from bsmax.math import get_distance, point_on_curve, get_bias
from bsmax.bsmatrix import matrix_from_elements
from bsmax.operator import PickOperator


#TODO object on same point detection issue nedd to fix

class ObjectData:
	def __init__(self, obj):
		self.owner = obj
		self.matrix_world = obj.matrix_world.copy()
	
	def set_transform(self, matrix):
		self.owner.matrix_world = matrix

	def reset(self):
		self.owner.matrix_world = self.matrix_world



def get_farest_objects(objs):
	""" return two farest object in given list """
	first, last, max_distance = objs[1], objs[2], 0
	for i in range(len(objs)):
		for j in range(i, len(objs)):
			# Get location in world coordinate
			location_i = objs[i].matrix_world.to_translation()
			location_j = objs[j].matrix_world.to_translation()
			current_distance = get_distance(location_i, location_j)
			# Get longest distance
			if current_distance > max_distance:
				max_distance = current_distance
				first, last = objs[i], objs[j]
	return 	first, last



def collect_distances(first, objs):
	""" Collect and sort all objects distance from the first one """
	distances = []
	location_first = first.matrix_world.to_translation()
	for obj in objs:
		location_current = obj.matrix_world.to_translation()
		distances.append(get_distance(location_first, location_current))
	distances.sort()
	return distances



def sort_object_by_distance_order(first, distances, objs):
	""" Sort objects by distance order to keep the Original order """
	sorted_objs = []
	location_first = first.matrix_world.to_translation()
	for distance in distances:
		for obj in objs:
			location_current = obj.matrix_world.to_translation()
			if get_distance(location_first, location_current) == distance:
				sorted_objs.append(obj)
	return sorted_objs



class Object_OT_Arrange_by_Distance(Operator):
	""" Get two farest object and arrange other objects between them """
	bl_idname = "object.arrange_by_distance"
	bl_label = "Arrange By Distance"
	bl_description = "Arrange Selected object in a line"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 2
		return False

	def execute(self, ctx):
		# Collect basic infos
		objs = ctx.selected_objects
		first, last = get_farest_objects(objs)
		distances = collect_distances(first, objs)
		objs = sort_object_by_distance_order(first, distances, objs)

		# Get Location step
		location_first = first.matrix_world.to_translation()
		location_last = last.matrix_world.to_translation()
		location_step = (location_last - location_first) / (len(objs) - 1)

		# get Rotation Steps
		sx, sy, sz = first.matrix_world.to_euler()
		ex, ey, ez = last.matrix_world.to_euler()
		step_x = (ex - sx) / (len(objs) - 1)
		step_y = (ey - sy) / (len(objs) - 1)
		step_z = (ez - sz) / (len(objs) - 1)

		# Get Scale Step
		scale_first = first.matrix_world.to_scale()
		scale_last = last.matrix_world.to_scale()
		scale_step = (scale_last - scale_first) / (len(objs) - 1)

		# Set Transform for each object
		for i, obj in enumerate(objs[1:-1], start=1):

			location = location_first + (location_step * i)

			x = sx + step_x*i
			y = sy + step_y*i
			z = sz + step_z*i
			euler_rotation = Vector((x, y, z))

			scale = scale_first + (scale_step * i)

			obj.matrix_world = matrix_from_elements(location, euler_rotation, scale)

		return{"FINISHED"}



class Object_OT_Arrange_On_Path(Operator):
	bl_idname = "object.arrange_on_path"
	bl_label = "Path Sort Apply"
	bl_options = {'REGISTER', 'INTERNAL','UNDO'}
	
	objs, path = [], None
	start: FloatProperty(name="Start:",
		min=0, max=1, step=0.01, precision=3, default=0.0)
	bias: FloatProperty(name="Bias:",
		min=-1, max=1, step=0.01, precision=3, default=0)
	end: FloatProperty(name="End:",
		min=0, max=1, step=0.01, precision=3, default=1.0)

	align: EnumProperty(name="align", options = {"ENUM_FLAG"},
		items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')])

	def draw(self, ctx):
		layout = self.layout
		row = layout.row(align=True)
		row.prop(self, "start")
		row.prop(self, "bias")
		row.prop(self, "end")
		#TODO ther is a miss calculation on rotaion need to fix befo enable is
		# row = layout.row(align=True)
		# row.prop(self, "align")
	
	def set_transform(self, obj, path, time):
		location, rotation, _ = point_on_curve(path, 0, time)
		location.x *= path.scale.x ** 2
		location.y *= path.scale.y ** 2
		location.z *= path.scale.z ** 2
		location = location @ path.matrix_world.inverted() + path.location
		euler_rotation = obj.matrix_world.to_euler()
		if 'X' in self.align:
			euler_rotation.x = rotation.x
		if 'Y' in self.align:
			euler_rotation.y = rotation.y
		if 'Z' in self.align:
			euler_rotation.z = rotation.z
		scale = obj.matrix_world.to_scale()
		obj.set_transform(matrix_from_elements(location, euler_rotation, scale))
		
	def check(self, ctx):
		# Collect basic info
		close = self.path.data.splines[0].use_cyclic_u
		count = len(self.objs)
		length = self.end - self.start

		# sort by distance to keep original order
		first, _ = get_farest_objects(self.objs)
		distances = collect_distances(first, self.objs)
		self.objs = sort_object_by_distance_order(first, distances, self.objs)

		for i in range(count):
			t = i/count if close else i / (count - 1) if count > 1 else 0
			t = get_bias(self.bias, t)
			time = self.start + t * length
			self.set_transform(self.objs[i], self.path, time)

	def execute(self,ctx):

		return {'FINISHED'}
	
	def cancel(self, ctx):
		for obj in self.objs:
			obj.reset()

	def invoke(self, ctx, event):
		self.objs.clear()
		for obj in ctx.selected_objects:
			if obj != ctx.active_object:
				self.objs.append(ObjectData(obj))
		self.path = ctx.active_object
		self.check(ctx)
		return ctx.window_manager.invoke_props_dialog(self)



class Object_OT_Arrange_Path_picker(PickOperator):
	bl_idname = "object.arrange_path_picker"
	bl_label = "Arrange on Curve"
	bl_description = "Sort Selected object on a Curve"
	
	filters = ['CURVE']
	def picked(self, ctx, source, subsource, target, subtarget):
		ctx.view_layer.objects.active = target
		bpy.ops.object.arrange_on_path('INVOKE_DEFAULT')



def object_sort_menu(self, ctx):
	layout = self.layout
	layout.operator("object.align_selected_to_target", text='Align Objects (BsMax)')
	layout.separator()
	layout.operator("object.arrange_by_distance", text="Arrange By Distance")
	layout.operator("object.arrange_path_picker", text="Arrange on Curve")



classes = (
	Object_OT_Arrange_by_Distance,
	Object_OT_Arrange_On_Path,
	Object_OT_Arrange_Path_picker
)



def register_arrange():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_transform_object.append(object_sort_menu)



def unregister_arrange():
	bpy.types.VIEW3D_MT_transform_object.remove(object_sort_menu)
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_arrange()