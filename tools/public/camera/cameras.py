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
from bpy.props import EnumProperty, BoolProperty
from bpy.types import Operator
from bsmax.state import has_constraint

# create a camera from view 
class BsMax_OT_CreateCameraFromView(Operator):
	bl_idname = "bsmax.createcamerafromview"
	bl_label = "Create Camera From View"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		obj = ctx.selected_objects
		if len(obj) == 1:
			if obj[0].type == 'CAMERA':
				ctx.scene.camera = obj[0]
				bpy.ops.view3d.camera_to_view()
			else:
				bpy.ops.object.camera_add()
				ctx.scene.camera = bpy.data.objects[ctx.active_object.name]
				bpy.ops.view3d.camera_to_view()
		else:
			bpy.ops.object.camera_add()
			ctx.scene.camera = bpy.data.objects[ctx.active_object.name]
			bpy.ops.view3d.camera_to_view()
		return{"FINISHED"}

# Set as sctive camera
class BsMax_OT_SetAsActiveCamera(Operator):
	bl_idname = "bsmax.setasactivecamera"
	bl_label = "Set as Active Camera"
	def execute(self, ctx):
		if ctx.active_object != None:
			if ctx.active_object.type == "CAMERA":
				ctx.scene.camera = ctx.active_object
				# if auto key is on bind marker to active camera
				if ctx.scene.tool_settings.use_keyframe_insert_auto:
					cur_frame = ctx.scene.frame_current
					name = "F_" + str(cur_frame)
					marker = ctx.scene.timeline_markers.new(name, frame = cur_frame)
					marker.camera = ctx.active_object
		return{"FINISHED"}

# Select Camera
class BsMax_OT_SearchCamera(Operator):
	bl_idname = "bsmax.searchcamera"
	bl_label = "Serch Camera"
	bl_property = "SceneCameras"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def scene_cameras(self, ctx):
		CamNameList = []
		for cam in bpy.data.objects:
			if cam.type == 'CAMERA':
				CamNameList.append((cam.name, cam.name, ''))
		return CamNameList

	SceneCameras: EnumProperty(items = scene_cameras)

	def execute(self, ctx):
		SelectedCamera = bpy.data.objects[self.SceneCameras]
		ctx.scene.camera = SelectedCamera
		area = next(area for area in ctx.screen.areas if area.type == 'VIEW_3D')
		area.spaces[0].region_3d.view_perspective = 'CAMERA'
		return {'FINISHED'}
	def invoke(self, ctx, event):
		wm = ctx.window_manager
		wm.invoke_search_popup(self)
		return {'FINISHED'}

# switch viewport to camera view
class BsMax_OT_SelectCamera(Operator):
	bl_idname = "bsmax.selectcamera"
	bl_label = "Select Camera"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		CamActived = False
		# Active Object is Camera
		if ctx.active_object != None:
			if ctx.active_object.type == "CAMERA":
				ctx.scene.camera = ctx.active_object
				CamActived = True
		# one selected object is camera
		if len(ctx.selected_objects) == 1:
			if ctx.selected_objects[0].type == 'CAMERA':
				ctx.scene.camera = ctx.selected_objects[0]
				CamActived = True
		# serch in scene
		if not CamActived:
			CameraList = []
			for Obj in bpy.data.objects:
				if Obj.type == 'CAMERA':
					CameraList.append(Obj.name)
			# when only one camera on scene
			if len(CameraList) == 1:
				camname = CameraList[0]
				cam = bpy.data.objects[camname]
				ctx.scene.camera = cam
				CamActived = True
			# if many cameras on scene
			elif len(CameraList) > 0:
				bpy.ops.bsmax.searchcamera('INVOKE_DEFAULT')
		# if camera actived go to camera view 
		if CamActived:
			area = next(area for area in ctx.screen.areas if area.type == 'VIEW_3D')
			area.spaces[0].region_3d.view_perspective = 'CAMERA'
		return{"FINISHED"}

class BsMax_OT_LockCameraToViewToggle(Operator):
	bl_idname = "bsmax.lockcameratoviewtoggle"
	bl_label = "Lock Camera to view (Toggle)"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		ctx.space_data.lock_camera = not ctx.space_data.lock_camera
		return {'FINISHED'}

class BsMax_OT_SelectActiveCamera(Operator):
	bl_idname = "bsmax.selectactivecamera"
	bl_label = "Select Active Camera/Target"
	selcam: BoolProperty(name="Select Camera")
	seltrg: BoolProperty(name="Select Target")

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		cam = ctx.scene.camera
		if cam != None:
			bpy.ops.object.select_all(action='DESELECT')
			if self.selcam:
				cam.select_set(state=True)
			if self.seltrg:
				if has_constraint(cam, 'TRACK_TO'):
					targ = cam.constraints["Track To"].target
					targ.select_set(state=True)
		return {'FINISHED'}

class BsMax_OT_ShowSafeAreaToggle(Operator):
	bl_idname = "bsmax.show_safe_areas"
	bl_label = "Show Safe Area"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		cam = ctx.scene.camera
		if cam != None:
			cam.data.show_safe_areas = not cam.data.show_safe_areas
		return {'FINISHED'}

def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("bsmax.createcamerafromview")
	layout.operator("bsmax.searchcamera")

classes = [BsMax_OT_SetAsActiveCamera,
			BsMax_OT_CreateCameraFromView,
			BsMax_OT_SearchCamera,
			BsMax_OT_SelectCamera,
			BsMax_OT_LockCameraToViewToggle,
			BsMax_OT_SelectActiveCamera,
			BsMax_OT_ShowSafeAreaToggle]

def register_cameras():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)

def unregister_cameras():
	bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)	
	[bpy.utils.unregister_class(c) for c in classes]