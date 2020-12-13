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
from bsmax.actions import set_origen

objAxis = None
objTarget = None
checkParams = ["BsMaxAxisPivotPoint_"]
rotAxis = None
locAxis = None

def ModifyPivotPoint(ctx):
	if ctx.active_object != None:
		ops = bpy.ops
		if not any(x in ctx.active_object.name for x in checkParams):
			# Create Povot helper
			objTarget = ctx.active_object
			ops.object.select_all(action='DESELECT')
			ops.object.select_pattern(pattern="BsMaxAxisPivotPoint_*")
			ops.object.delete()
			objTarget.select_set(True)
			ops.object.empty_add(type='ARROWS')
			objAxis = ctx.active_object
			objAxis.location = objTarget.location+objTarget.delta_location
			objAxis.show_in_front = True
			euRotationMX = objTarget.rotation_euler.to_matrix()
			euRotationDeltaMX = objTarget.delta_rotation_euler.to_matrix()
			RotationFullMX = euRotationMX @ euRotationDeltaMX
			euRotationFull = RotationFullMX.to_euler()
			objAxis.rotation_euler = euRotationFull
			objAxis.name = "BsMaxAxisPivotPoint_"+objTarget.name
			ops.object.select_all(action='DESELECT')
			objAxis.select_set(True)
			ctx.view_layer.objects.active = objAxis
			ops.wm.tool_set_by_id(name="builtin.move")
		else:
			# Commit new pivot
			objAxis = ctx.active_object
			objName = objAxis.name
			objName = objName.replace("BsMaxAxisPivotPoint_","")
			ops.object.select_all(action='DESELECT')
			ctx.view_layer.objects.active = None
			bpy.data.objects[objName].select_set(True)
			ctx.view_layer.objects.active = bpy.data.objects[objName]
			objTarget = ctx.active_object

			objTarget.location = objTarget.location+objTarget.delta_location
			objTarget.delta_location = (0,0,0)

			xRot = objTarget.rotation_euler.x
			xDRot = objTarget.delta_rotation_euler.x
			yRot = objTarget.rotation_euler.y
			yDRot = objTarget.delta_rotation_euler.y
			zRot = objTarget.rotation_euler.z
			zDRot = objTarget.delta_rotation_euler.z

			objTarget.rotation_euler.x = xRot+xDRot
			objTarget.rotation_euler.y = yRot+yDRot
			objTarget.rotation_euler.z = zRot+zDRot
			objTarget.delta_rotation_euler.x = 0
			objTarget.delta_rotation_euler.y = 0
			objTarget.delta_rotation_euler.z = 0

			newRot = objAxis.rotation_euler
			newRotMX = newRot.to_matrix()
			# newRotInvMX = newRotMX.inverted()
			newRotDupMX = newRotMX @ newRotMX
			newRotDupInvMX = newRotDupMX.inverted()

			newRotMXEu = newRotMX.to_euler()
			newRotDupInvMXEu = newRotDupInvMX.to_euler()
			ops.object.transform_apply(location=False,rotation=True,scale=False)
			
			currentCursorLocation = ctx.scene.cursor.location
			ctx.scene.cursor.location = objAxis.location
			objTarget.location = objTarget.location+objTarget.delta_location
			objTarget.delta_location = (0,0,0)
			ops.object.origin_set(type='ORIGIN_CURSOR')

			objTarget.delta_rotation_euler = newRotMXEu
			objTarget.rotation_euler = newRotDupInvMXEu
			
			ops.object.transform_apply(location=False,rotation=True,scale=False)
			objTarget.delta_location = objTarget.location
			objTarget.location = (0,0,0)
			ops.object.select_all(action='DESELECT')
			objTarget.select_set(True)
			ops.object.delete({"selected_objects": [objAxis]})
			ctx.scene.cursor.location = currentCursorLocation

class Object_OT_Modify_Pivot(Operator):
	bl_idname = "object.modify_pivotpoint"
	bl_label = "Modify Pivot Point"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None

	def execute(self, ctx):
		v = bpy.app.version[1]
		if v == 80:
			ModifyPivotPoint(ctx)
		elif v >= 81:
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
		else:
			return False
	
	def execute(self,ctx):
		for obj in ctx.selected_objects:
			if len(obj.data.splines)>0:
				if len(obj.data.splines[0].bezier_points)>0:
					old_origin = obj.matrix_world @ obj.data.splines[0].bezier_points[0].co
					delta_origin = obj.data.splines[0].bezier_points[0].co.copy()
					obj.data.transform(Matrix.Translation(-delta_origin))
					obj.matrix_world.translation = old_origin
		self.report({'OPERATOR'},'bpy.ops.object.pivot_to_first_point()')
		return {"FINISHED"}

class Object_OT_Pivot_To_Buttom_Center(Operator):
	bl_idname = "object.pivot_to_buttom_center"
	bl_label = "Pivot to Buttom Center"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0
		
	def pivot_to_buttom_center(self, ctx, obj):
		""" TODO bound_box return value in local coordinate """
		""" need a fast method to get bound box in world space """
		b = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
		min_x = min(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		max_x = max(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		min_y = min(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		max_y = max(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		min_z = min(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
		center_x = (min_x + max_x)/2
		center_y = (min_y + max_y)/2
		location = Vector((center_x, center_y, min_z))
		set_origen(ctx, obj, location)

	def execute(self,ctx):
		for obj in ctx.selected_objects:
			self.pivot_to_buttom_center(ctx, obj)
		self.report({'OPERATOR'},'bpy.ops.object.pivot_to_buttom_center()')
		return {"FINISHED"}

class OBJECT_MT_Set_Pivot_Point(Menu):
	bl_idname = "OBJECT_MT_Set_Pivot_Point"
	bl_label = "Set Pivot Point"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("object.origin_set",text="Object to Pivot").type='GEOMETRY_ORIGIN'
		layout.operator("object.origin_set",text="Pivot to Object").type='ORIGIN_GEOMETRY'
		layout.operator("object.origin_set",text="Pivot to 3D Cursor").type='ORIGIN_CURSOR'
		layout.operator("object.origin_set",text="Pivot to Center").type='ORIGIN_CENTER_OF_VOLUME'
		layout.operator("object.origin_set",text="Pivot to Geometry").type='ORIGIN_CENTER_OF_MASS'
		layout.operator("object.pivot_to_buttom_center",text="Pivot to Buttom Center")
		layout.operator("object.pivot_to_first_point",text="Pivot to First BezierPoint")

def snap_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.pivot_to_first_point")

classes = [Object_OT_Pivot_To_First_Point,
	Object_OT_Modify_Pivot,
	Object_OT_Pivot_To_Buttom_Center,
	OBJECT_MT_Set_Pivot_Point]

def register_pivot_point():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_snap.append(snap_menu)

def unregister_pivot_point():
	bpy.types.VIEW3D_MT_snap.remove(snap_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_pivot_point()