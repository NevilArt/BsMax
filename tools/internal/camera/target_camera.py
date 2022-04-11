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
from bpy.types import Operator
from bsmax.actions import (
		set_create_target,
		set_as_active_object,
		delete_objects
	)
from bsmax.state import has_constraint



class Camera_OT_Create_Target(Operator):
	bl_idname = "camera.create_target"
	bl_label = "Make Target Camera"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			if ctx.object.type == 'CAMERA' and not has_constraint(ctx.object, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.object
		size = cam.data.display_size
		target = set_create_target(cam, None, distance=(0, 0, -size*3))
		target.empty_display_size = size / 10
		target.name = cam.name + "_target"
		set_as_active_object(ctx, cam)
		return {'FINISHED'}



class Camera_OT_Clear_Target(Operator):
	bl_idname = "camera.clear_targte"
	bl_label = "Make Free Camera"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			if ctx.object.type == 'CAMERA' and has_constraint(ctx.object, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		cam = ctx.object
		cam.data.dof.driver_remove('aperture_fstop')
		transfoem = cam.matrix_world.copy()
		targ = cam.constraints["Track To"].target
		delete_objects([targ])
		TrackToConts = [ c for c in cam.constraints if c.type == 'TRACK_TO' ]
		for c in TrackToConts:
			cam.constraints.remove(c)
		cam.matrix_world = transfoem
		return {'FINISHED'}



class Camera_OT_Select_Target(Operator):
	bl_idname = "camera.select_target"
	bl_label = "Select Target"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			if ctx.object.type in ['CAMERA', 'LIGHT'] and has_constraint(ctx.object, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		targ = ctx.object.constraints["Track To"].target
		set_as_active_object(ctx, targ)
		return {'FINISHED'}



class Camera_OT_Create_DOF_Target(Operator):
	bl_idname = "camera.create_dof_target"
	bl_label = "Create DOF Target"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			if ctx.object.type == 'CAMERA':
				return ctx.object.data.dof.focus_object == None
		return False
	
	def cretae_target_object(self, parent):
		target = bpy.data.objects.new('empty', None)
		target.empty_display_type = 'SPHERE'
		target.empty_display_size = parent.data.display_size
		collection = parent.users_collection[0]
		collection.objects.link(target)
		return target
	
	def create_driver(self, cam, target):
		cam.data.dof.driver_remove('aperture_fstop')

		driver = cam.data.dof.driver_add('aperture_fstop')
		driver.driver.type = 'SCRIPTED'

		var = driver.driver.variables.new()
		var.name = 's'
		var.type = 'SINGLE_PROP'
		var.targets[0].id = target
		var.targets[0].data_path = 'empty_display_size'

		x = driver.driver.variables.new()
		x.name = 'x'
		x.type = 'TRANSFORMS'
		x.targets[0].id = target
		x.targets[0].transform_type = 'SCALE_X'

		y = driver.driver.variables.new()
		y.name = 'y'
		y.type = 'TRANSFORMS'
		y.targets[0].id = target
		y.targets[0].transform_type = 'SCALE_Y'

		z = driver.driver.variables.new()
		z.name = 'z'
		z.type = 'TRANSFORMS'
		z.targets[0].id = target
		z.targets[0].transform_type = 'SCALE_Z'

		driver.driver.expression = 's*((x+y+z)/3)'

	def execute(self, ctx):
		cam = ctx.object
		size = cam.data.display_size
		target = self.cretae_target_object(cam)
		target.location = cam.location
		target.empty_display_size = size
		target.name = cam.name + "_FOV_target"
		cam.data.dof.use_dof = True
		cam.data.dof.focus_object = target
		self.create_driver(cam, target)
		set_as_active_object(ctx, cam)
		return {'FINISHED'}


class Camera_OT_Select_DOF_Target(Operator):
	bl_idname = "camera.select_dof_target"
	bl_label = "Select DOF Target"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			if ctx.object.type == 'CAMERA':
				return ctx.object.data.dof.focus_object != None
		return False

	def execute(self, ctx):
		target = ctx.active_object.data.dof.focus_object
		set_as_active_object(ctx, target)
		return {'FINISHED'}

def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("camera.create_target")
	layout.operator("camera.clear_targte")
	layout.operator("camera.select_target")



classes = [Camera_OT_Create_Target,
		Camera_OT_Clear_Target,
		Camera_OT_Select_Target,
		Camera_OT_Create_DOF_Target,
		Camera_OT_Select_DOF_Target]

def register_terget_camera():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)

def unregister_terget_camera():
	bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_terget_camera()