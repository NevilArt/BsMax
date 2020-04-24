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

import bpy, mathutils
from bpy.types import Menu, Operator

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

class BsMax_OT_ModifyPivot(Operator):
	bl_idname = "object.modifypivotpoint"
	bl_label = "Modify Pivot Point"

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
	
class BsMax_OT_PivotToFirstPoint(Operator):
	bl_idname = "pivot.tofirstpoint"
	bl_label = "Pivot to First point"

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
					new_origin = obj.data.splines[0].bezier_points[0].co.copy()
					obj.data.transform(mathutils.Matrix.Translation(-new_origin))
					obj.matrix_world.translation += new_origin
		return {"FINISHED"}
				

class BsMax_MT_SetPivotPoint(Menu):
	bl_idname = "BSMAX_MT_SetPivotPoint"
	bl_label = "Set Pivot Point"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("object.origin_set",text="Object to Pivot").type='GEOMETRY_ORIGIN'
		layout.operator("object.origin_set",text="Pivot to Object").type='ORIGIN_GEOMETRY'
		layout.operator("object.origin_set",text="Pivot to 3D Cursor").type='ORIGIN_CURSOR'
		layout.operator("object.origin_set",text="Pivot to Center").type='ORIGIN_CENTER_OF_VOLUME'
		layout.operator("object.origin_set",text="Pivot to Geometry").type='ORIGIN_CENTER_OF_MASS'
		layout.operator("pivot.tofirstpoint",text="Pivot to First BezierPoint")

def snap_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("pivot.tofirstpoint")

classes = [BsMax_OT_PivotToFirstPoint,BsMax_MT_SetPivotPoint,BsMax_OT_ModifyPivot]

def register_pivotpoint():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_snap.append(snap_menu)

def unregister_pivotpoint():
	bpy.types.VIEW3D_MT_snap.remove(snap_menu)
	[bpy.utils.unregister_class(c) for c in classes]