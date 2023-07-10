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

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Operator
from bsmax.state import has_constraint


def get_view3d(ctx):
	if ctx.area.spaces.active.type == 'VIEW_3D':
		return ctx.area.spaces.active

	areas = [area for area in ctx.screen.areas if area.type == 'VIEW_3D']
	spaces = [space for area in areas
					for space in area.spaces
						if space.type == 'VIEW_3D']
	#TODO try to find biggest view 3d
	if spaces:
		return spaces[0]
	return None



def get_cameras(ctx):
	if ctx.active_object:
		if ctx.active_object.type == 'CAMERA':
			if ctx.active_object.select_get():
				return [ctx.active_object]
			else:
				return [obj for obj in bpy.data.objects if obj.type == 'CAMERA']
		else:
			return [obj for obj in bpy.data.objects if obj.type == 'CAMERA']
	else:
		if ctx.selected_objects:
			return [obj for obj in ctx.selected_objects if obj.type == 'CAMERA']
		else:
			return [obj for obj in bpy.data.objects if obj.type == 'CAMERA']



def set_camera(ctx, camera, view3d):
	ctx.scene.camera = camera
	view3d.region_3d.view_perspective = 'CAMERA'
	if ctx.area.spaces.active.type == 'VIEW_3D':
		#TODO find command rather than operator
		bpy.ops.view3d.view_center_camera('INVOKE_DEFAULT')	



# create a camera from view 
class Camera_OT_Create_From_View(Operator):
	""" Create a new camera and align it to view """
	bl_idname = 'camera.create_from_view'
	bl_label = 'Create Camera From View'
	bl_description = 'Create New Camera From View'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def camera_to_view(self, ctx):
		bpy.ops.view3d.camera_to_view()
	
	def create_new_camera(self, ctx):
		bpy.ops.object.camera_add()
		ctx.scene.camera = bpy.data.objects[ctx.active_object.name]

	def execute(self, ctx):
		obj = ctx.selected_objects
		if len(obj) == 1:
			if obj[0].type == 'CAMERA':
				ctx.scene.camera = obj[0]
				self.camera_to_view(ctx)
			else:
				self.create_new_camera(ctx)
				self.camera_to_view(ctx)
		else:
			self.create_new_camera(ctx)
			self.camera_to_view(ctx)
		
		return{'FINISHED'}



class Camera_OT_Set_Active(Operator):
	bl_idname = 'camera.set_active'
	bl_label = 'Set as Active Camera'
	bl_description = 'Set Selected Camera As Active Camera'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		if ctx.active_object != None:
			if ctx.active_object.type == 'CAMERA':
				ctx.scene.camera = ctx.active_object
				""" If Autokey on, Bind Marker To Active Camera """
				if ctx.scene.tool_settings.use_keyframe_insert_auto:
					cur_frame = ctx.scene.frame_current
					name = 'F_' + str(cur_frame)
					marker = ctx.scene.timeline_markers.new(name, frame = cur_frame)
					marker.camera = ctx.active_object
		return{'FINISHED'}



class Camera_OT_Select(Operator):
	""" List camera and make active picked one """
	bl_idname = 'camera.select'
	bl_label = 'Select Camera'
	bl_property = 'search'
	bl_description = ''

	@classmethod
	def poll(self, ctx):
		return ctx.area.type in {'VIEW_3D', 'DOPESHEET_EDITOR',
								'GRAPH_EDITOR', 'NLA_EDITOR'}
	
	def scene_cameras(self, ctx):
		return [(cam.name, cam.name, '') for cam in bpy.data.objects
											if cam.type == 'CAMERA']

	search: EnumProperty(name='Select Camera', items=scene_cameras)
	
	
	def execute(self, ctx):
		camera = bpy.data.objects[self.search]
		set_camera(ctx, camera, get_view3d(ctx))		
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		cameras = get_cameras(ctx)

		if len(cameras) == 1:
			set_camera(ctx, cameras[0], get_view3d(ctx))
			return{'FINISHED'}

		if len(cameras) > 1:
			ctx.window_manager.invoke_search_popup(self)
		return{'RUNNING_MODAL'}



class Camera_OT_Lock_To_View_Toggle(Operator):
	bl_idname = 'camera.lock_to_view_toggle'
	bl_label = 'Lock Camera to view (Toggle)'
	bl_description = 'Lock Active Camera to view'

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		ctx.space_data.lock_camera = not ctx.space_data.lock_camera
		return {'FINISHED'}



class Camera_OT_Lock_Transform(Operator):
	bl_idname = 'camera.lock_transform'
	bl_label = 'Lock Camera Transform'
	bl_description = 'Lock active cameras transform'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		cam = ctx.scene.camera
		if cam != None:
			state = not cam.lock_location[0]
			cam.lock_location = [state, state, state]
			cam.lock_rotation = [state, state, state]
			cam.lock_scale = [state, state, state]
		return {'FINISHED'}



class Camera_OT_Select_Active_Camera(Operator):
	bl_idname = 'camera.select_active_camera'
	bl_label = 'Select Active Camera/Target'
	bl_description = 'Select Acitve Camera/Target'

	selcam: BoolProperty(name='Select Camera')
	seltrg: BoolProperty(name='Select Target')

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



class Camera_OT_Show_Safe_Area(Operator):
	bl_idname = 'camera.show_safe_areas'
	bl_label = 'Show Safe Area'
	bl_description = 'Show Safe Area'

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		camera = ctx.scene.camera
		if camera:
			camera.data.show_safe_areas = not camera.data.show_safe_areas
			camera.data.show_passepartout = True
			camera.data.passepartout_alpha = 1
		return {'FINISHED'}



class Camera_OT_Lock_Toggle(Operator):
	bl_idname = 'camera.lock_toggle'
	bl_label = 'Show Safe Area'
	bl_description = 'Show Safe Area'

	name: EnumProperty(name='Name', default='CAMERA',
		items=[('CAMERA', 'Camera',''), ('CURSOR', 'Cursor','')])

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		if self.name == 'CAMERA':
			ctx.space_data.lock_camera = not ctx.space_data.lock_camera
		elif self.name == 'CURSOR':
			ctx.space_data.lock_cursor = not ctx.space_data.lock_cursor
		return {'FINISHED'}



def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('camera.create_from_view')
	layout.operator('camera.select')



classes = (
	Camera_OT_Set_Active,
	Camera_OT_Create_From_View,
	Camera_OT_Select,
	Camera_OT_Lock_To_View_Toggle,
	Camera_OT_Lock_Transform,
	Camera_OT_Select_Active_Camera,
	Camera_OT_Show_Safe_Area,
	Camera_OT_Lock_Toggle
)



def register_cameras():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)



def unregister_cameras():
	bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)	
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == '__main__':
	register_cameras()