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
from bpy.types import Operator
from mathutils import Matrix
from bsmax.actions import set_create_target, set_as_active_object, delete_objects
from bsmax.state import has_constraint

class Camera_OT_Create_Target(Operator):
	bl_idname = "camera.create_target"
	bl_label = "Make Target Camera"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'CAMERA' and not has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.active_object
		size = cam.data.display_size
		target = set_create_target(cam, None, distance=(0,0,-size*3))
		target.empty_display_size = size / 10
		set_as_active_object(ctx, cam)
		self.report({'OPERATOR'},"bpy.ops.camera.create_target()")
		return {'FINISHED'}

class Camera_OT_Clear_Target(Operator):
	bl_idname = "camera.clear_targte"
	bl_label = "Make Free Camera"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'CAMERA' and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.active_object
		transfoem = cam.matrix_world.copy()
		targ = cam.constraints["Track To"].target
		delete_objects([targ])
		TrackToConts = [ c for c in cam.constraints if c.type == 'TRACK_TO' ]
		for c in TrackToConts:
			cam.constraints.remove(c)
		cam.matrix_world = transfoem
		self.report({'OPERATOR'},'bpy.ops.camera.clear_targte()')
		return {'FINISHED'}

class Camera_OT_Select_Target(Operator):
	bl_idname = "camera.select_target"
	bl_label = "Select Target"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type in ['CAMERA', 'LIGHT'] and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		obj = ctx.active_object
		targ = obj.constraints["Track To"].target
		set_as_active_object(ctx, targ)
		return {'FINISHED'}

def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("camera.create_target")
	layout.operator("camera.clear_targte")
	layout.operator("camera.select_target")

classes = [Camera_OT_Create_Target,
		Camera_OT_Clear_Target,
		Camera_OT_Select_Target]

def register_terget_camera():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)

def unregister_terget_camera():
	bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_terget_camera()