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

from mathutils import Vector, Matrix

from bpy.types import Menu, Operator
from bpy.props import EnumProperty

from bsmax.actions import set_origen



class BoundBox():
	def __init__(self, obj):
		self.obj = obj
		self.min = Vector((0,0,0))
		self.max = Vector((0,0,0))
		self.center = Vector((0,0,0))
		self.calculate()
	
	def calculate(self):
		b = [self.obj.matrix_world @ Vector(v) for v in self.obj.bound_box]

		self.min.x = min(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		self.max.x = max(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		self.min.y = min(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		self.max.y = max(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		self.min.z = min(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
		self.max.z = max(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
		
		self.center.x = (self.min.x + self.max.x) / 2
		self.center.y = (self.min.y + self.max.y) / 2
		self.center.z = (self.min.z + self.max.z) / 2



class Object_OT_Modify_Pivot(Operator):
	bl_idname = "object.modify_pivotpoint"
	bl_label = "Modify Pivot Point"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.active_object

	def execute(self, ctx):
		state = ctx.scene.tool_settings.use_transform_data_origin
		ctx.scene.tool_settings.use_transform_data_origin = not state
		return {"FINISHED"}




# TODO add this for mesh objects too
class Object_OT_Pivot_To_First_Point(Operator):
	bl_idname = "object.pivot_to_first_point"
	bl_label = "Pivot to First point"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if len(ctx.selected_objects) > 0:
			for obj in ctx.selected_objects:
				if obj.type != 'CURVE':
					return False
			return True
		return False

	def execute(self,ctx):
		for obj in ctx.selected_objects:
			if len(obj.data.splines)>0:
				if len(obj.data.splines[0].bezier_points)>0:
					old_origin = obj.matrix_world @ obj.data.splines[0].bezier_points[0].co
					delta_origin = obj.data.splines[0].bezier_points[0].co.copy()
					obj.data.transform(Matrix.Translation(-delta_origin))
					obj.matrix_world.translation = old_origin

		return {"FINISHED"}



def get_mass_center(obj):
	verts = [obj.matrix_world @ vert.co for vert in obj.data.vertices]

	minCo = verts[0].copy()
	maxCo = verts[0].copy()

	for co in verts:
		if minCo.x > co.x:
			minCo.x = co.x

		if minCo.y > co.y:
			minCo.y = co.y

		if minCo.z > co.z:
			minCo.z = co.z

		if maxCo.x < co.x:
			maxCo.x = co.x

		if maxCo.y < co.y:
			maxCo.y = co.y
	
	center_x = (minCo.x + maxCo.x) / 2
	center_y = (minCo.y + maxCo.y) / 2
	return Vector((center_x, center_y, minCo.z))



def get_bound_center(obj):
	bBox = BoundBox(obj)
	return Vector((bBox.center.x, bBox.center.y, bBox.min.z))



def get_touched_center(obj):
	bBox = BoundBox(obj)
	height = bBox.max.z - bBox.min.z
	level = bBox.min.z + height/100

	verts = [
		obj.matrix_world @ vert.co for vert in obj.data.vertices 
	  		if (obj.matrix_world @ vert.co).z <= level
	]

	min = verts[0].copy()
	max = verts[0].copy()

	for co in verts:
		if min.x > co.x:
			min.x = co.x

		if min.y > co.y:
			min.y = co.y

		if min.z > co.z:
			min.z = co.z

		if max.x < co.x:
			max.x = co.x

		if max.y < co.y:
			max.y = co.y
	
	center_x = (min.x + max.x) / 2
	center_y = (min.y + max.y) / 2
	return Vector((center_x, center_y, min.z))



class Object_OT_Pivot_To_Buttom_Center(Operator):
	bl_idname = "object.pivot_to_buttom_center"
	bl_label = "Pivot to object base"
	bl_options = {'REGISTER', 'UNDO'}

	center: EnumProperty(
		name="Center by:",
		default="BOUND",
		items=[
			("BOUND", "Bound Center", "Center Pivot Bouning Box"),
			("MASS", "Mass Center", "Center Pivot by vertex position avrage"),
			("TOUCH", "Touch Center", "Center by vertex on the lover part of object")
		]
	)

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0
	
	def execute(self, ctx):
		for obj in ctx.selected_objects:

			if self.center == "MASS":
				location = get_mass_center(obj)

			elif self.center == "TOUCH":
				location = get_touched_center(obj)

			else:
				location = get_bound_center(obj)

			set_origen(ctx, obj, location)

		return {"FINISHED"}



class OBJECT_MT_Set_Pivot_Object_Base(Menu):
	bl_idname = "OBJECT_MT_Set_Pivot_to_object_base"
	bl_label = "Pivot to objects Base"

	def draw(self, ctx):
		layout = self.layout
		layout.operator("object.pivot_to_buttom_center",
			text="Bound Center"
		).center="BOUND"

		layout.operator("object.pivot_to_buttom_center",
			text="Mass Center"
		).center="MASS"

		layout.operator("object.pivot_to_buttom_center",
			text="Touch Center"
		).center="TOUCH"



class OBJECT_MT_Set_Pivot_Point(Menu):
	bl_idname = "OBJECT_MT_Set_Pivot_Point"
	bl_label = "Set Pivot Point"

	def draw(self, ctx):
		layout = self.layout
		layout.operator("object.origin_set",
						text="Object to Pivot").type='GEOMETRY_ORIGIN'

		layout.operator("object.origin_set",
						text="Pivot to Object").type='ORIGIN_GEOMETRY'

		layout.operator("object.origin_set",
						text="Pivot to 3D Cursor").type='ORIGIN_CURSOR'

		layout.operator("object.origin_set",
						text="Pivot to Center").type='ORIGIN_CENTER_OF_VOLUME'

		layout.operator("object.origin_set",
						text="Pivot to Geometry").type='ORIGIN_CENTER_OF_MASS'

		layout.menu("OBJECT_MT_Set_Pivot_to_object_base")

		layout.operator("object.pivot_to_first_point",
						text="Pivot to First BezierPoint")

		layout.separator()

		layout.operator("view3d.snap_cursor_to_selected",
						text="Cursur to Selected")

		layout.operator("view3d.snap_cursor_to_center",
						text="Cursor to World Origin")

		layout.operator("view3d.snap_cursor_to_grid",
						text="Cursor to Grid")

		layout.operator("view3d.snap_cursor_to_active",
						text="Cursor to Active")

		layout.separator()

		layout.operator("view3d.snap_selected_to_grid",
						text="Selection to Gride")

		layout.operator("view3d.snap_selected_to_cursor",
						text="Selection to Cursor (keep offset)"
						).use_offset=False

		layout.operator("view3d.snap_selected_to_cursor",
						text="Selection to Cursor"
						).use_offset=True

		layout.operator("view3d.snap_selected_to_active",
						text="Selection to Active")



def snap_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.pivot_to_first_point")



classes = {
	Object_OT_Pivot_To_First_Point,
	Object_OT_Modify_Pivot,
	Object_OT_Pivot_To_Buttom_Center,
	OBJECT_MT_Set_Pivot_Object_Base,
	OBJECT_MT_Set_Pivot_Point
}



def register_pivot_point():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.VIEW3D_MT_snap.append(snap_menu)



def unregister_pivot_point():
	bpy.types.VIEW3D_MT_snap.remove(snap_menu)

	for cls in classes:
		bpy.utils.unregister_class(cls)



if __name__ == "__main__":
	register_pivot_point()