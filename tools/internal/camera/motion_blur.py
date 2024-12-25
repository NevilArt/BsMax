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
# 2024/09/20

from typing import Any
import bpy

from bpy.types import Context, Operator
from bpy.props import IntProperty
from bpy.utils import register_class, unregister_class


def is_digits(string):
	for char in string:
		if not char in '0123456789':
			return False
	return True


def clone_camera(ctx, camera):
	camera_even = camera.copy()
	camera_odd = camera.copy()
	camera_even.name = camera.name + "_Even"
	camera_odd.name = camera.name + "_Odd"

	if camera.users_collection:
		for collection in camera.users_collection:
			collection.objects.link(camera_even)
			collection.objects.link(camera_odd)
	else:
		ctx.collection.objects.link(camera_even)
		ctx.collection.objects.link()

	if camera.animation_data:
		action = camera.animation_data.action
		camera_even.animation_data.action = action.copy()
		camera_odd.animation_data.action = action.copy()

	ctx.view_layer.update()

	return camera_even, camera_odd


def get_camera_key_times(camera):
	if not camera.animation_data or not camera.animation_data.action:
		return []
	
	channels_to_check = {'location', 'rotation_euler', 'rotation_quaternion'}
	keyframe_frames = set()

	for fcurve in camera.animation_data.action.fcurves:
		if any(channel in fcurve.data_path for channel in channels_to_check):
			keyframe_frames.update(
				[int(kf.co[0]) for kf in fcurve.keyframe_points]
			)

	return sorted(keyframe_frames)


def collect_cut_morakers(ctx, camera):
	markers = ctx.scene.timeline_markers
	markers = sorted(markers, key=lambda marker: marker.frame)
	key_times = get_camera_key_times(camera)
	return [marker for marker in markers if marker.frame in key_times]


def clone_transform_keyframe_to_time(camera, key_time, new_time):
	if camera.animation_data and camera.animation_data.action:
		action = camera.animation_data.action
		for fcurve in action.fcurves:
			# Find the keyframe at keytime
			for keyframe in fcurve.keyframe_points:
				if keyframe.co[0] == key_time:
					# Clone the keyframe to newframe
					fcurve.keyframe_points.insert(new_time, keyframe.co[1])
					fcurve.update()


def bind_camera_to_markers(camera, markers, key_offset):
	for marker in markers:
		key_time = marker.frame
		new_time = key_time + key_offset
		clone_transform_keyframe_to_time(camera, key_time, new_time)
		marker.camera = camera


class Camera_OT_Motion_Blur_Solver(Operator):
	bl_idname = 'camera.motion_blur_solver'
	bl_label = 'Motion Blure Solver'
	bl_description = "Add Marker at camera jumping frame with out Motion blur issue"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			return ctx.object.type == 'CAMERA'
		return False

	def execute(self, ctx):
		camera_even, camera_odd = clone_camera(ctx, ctx.object)
		cut_markers = collect_cut_morakers(ctx, ctx.object)
		even_markers = cut_markers[0::2]
		odd_markers = cut_markers[1::2]

		bind_camera_to_markers(camera_even, even_markers, -5)
		bind_camera_to_markers(camera_odd, odd_markers, -5)

		return{'FINISHED'}
	

class Camera_OT_Jump_Frame_Lister(Operator):
	bl_idname = 'camera.jump_frame_lister'
	bl_label = "Jump Frames Lister"
	bl_description = "Return Bitarray list for camera jumps"

	before: IntProperty(
		name="Before",
		min=0, default= 1,
		description="Number of frame most  pack befor jump marker"
	) # type: ignore
	after: IntProperty(
		name="After",
		min=0, default= 0,
		description="Number of frame most  pack After jump marker"
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			return ctx.object.type == 'CAMERA'
		return False

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.prop(self, 'before', text="Before")
		row.prop(self, 'after', text="After")

	def execute(self, ctx):
		cut_markers = collect_cut_morakers(ctx, ctx.object)
		length = self.before + self.after
		string = ""
		
		if length == 0:
			for marker in cut_markers:
				frame = marker.frame
				if frame > 0:
					string += str(frame) + ","

		elif length == 1:
			for marker in cut_markers:
				frame = marker.frame

				if frame <= 0:
					continue

				start = frame - self.before
				end = frame + self.after
				string += str(start) + "," + str(end) + ","
		
		elif length > 1:
			for marker in cut_markers:
				frame = marker.frame

				if frame <= 0:
					continue

				start = frame - self.before
				end = frame + self.after
				string += str(start) + "-" + str(end) + ","

		ctx.window_manager.clipboard = string

		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		ctx.window_manager.invoke_props_dialog(self)
		return {'RUNNING_MODAL'}
	

classes = {
	Camera_OT_Motion_Blur_Solver,
	Camera_OT_Jump_Frame_Lister
}


def motion_blur_solver_manu(self, _):
	layout = self.layout
	layout.separator()
	# layout.operator('camera.motion_blur_solver')
	layout.operator('camera.jump_frame_lister')


def register_motion_blur():
	for cls in classes:
		register_class(cls)

	bpy.types.VIEW3D_MT_view_cameras.append(motion_blur_solver_manu)


def unregister_motion_blur():
	bpy.types.VIEW3D_MT_view_cameras.remove(motion_blur_solver_manu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	# bpy.types.VIEW3D_MT_view_cameras.append(motion_blur_solver_manu)
	for cls in classes:
		register_class(cls)