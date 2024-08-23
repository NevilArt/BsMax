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
# 2024/07/24

import bpy

from mathutils import Matrix
from bpy.types import Operator, Panel

from bsmax.actions import set_create_target, set_as_active_object
from bsmax.mouse import ray_cast


def get_constraint(object, constraint_type, reverse=False):
	constraints = \
			[constraint for constraint in reversed(object.constraints)] \
		if reverse else \
			[constraint for constraint in object.constraints]

	for constraint in constraints:
		if constraint.type == constraint_type:
			if constraint.enabled and constraint.influence > 0:
				return constraint

	return None


def is_target_camera(obj):
	if not obj:
		return False

	if not obj.type in {'CAMERA', 'LIGHT'}:
			return False

	return get_constraint(obj, 'TRACK_TO')


def cretae_dof_target_object(parent):
	target = bpy.data.objects.new('empty', None)
	target.empty_display_type = 'SPHERE'
	target.show_axis = True
	target.empty_display_size = parent.data.display_size
	collection = parent.users_collection[0]
	collection.objects.link(target)
	return target


def create_dof_driver(cam, target):
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


def set_keyframe_for_current_location(object, context):
	frame = context.scene.frame_current
	object.keyframe_insert(data_path="location", frame=frame)


class Camera_OT_Create_Target(Operator):
	bl_idname = 'camera.create_target'
	bl_label = "Make Target Camera"
	bl_description = "Create a lookat target for camera"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, context):
		if context.object:
			if context.object.type == "CAMERA":
				return not is_target_camera(context.object)
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
	bl_idname = 'camera.clear_targte'
	bl_label = "Make Free Camera"
	bl_description = " Remove loock at target and keep current transform "
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, context):
		return is_target_camera(context.object)

	def execute(self, ctx):
		camera = ctx.object
		camera.data.dof.driver_remove('aperture_fstop')
		transfoem = camera.matrix_world.copy()
		constraint = get_constraint(camera, 'TRACK_TO')
		targ = constraint.target

		bpy.ops.object.select_all(action='DESELECT')
		targ.select_set(True)
		bpy.ops.object.delete(confirm=False)

		TrackToConts = [
			constraint for constraint in camera.constraints
				if constraint.type == 'TRACK_TO'
		]

		for constraint in TrackToConts:
			camera.constraints.remove(constraint)
		
		camera.matrix_world = transfoem

		return {'FINISHED'}


class Camera_OT_Select_Target(Operator):
	bl_idname = 'camera.select_target'
	bl_label = "Select Target"
	bl_description = "Select the loockat target "
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, context):
		return is_target_camera(context.object)

	def execute(self, ctx):
		constraint = get_constraint(ctx.object, 'TRACK_TO', True)
		set_as_active_object(ctx, constraint.target)
		return {'FINISHED'}


class Camera_OT_Align_Target(Operator):
	bl_idname = 'camera.align_target'
	bl_label = "Align Target"
	bl_description = "Align Target to Camera"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, context):	
		return is_target_camera(context.object)

	def execute(self, context):
		camera = context.object
		constraint = get_constraint(camera, 'TRACK_TO', True)
		state = constraint.enabled
		target = constraint.target
		size = camera.data.display_size
		distance = (0, 0, -size*3)

		constraint.enabled = False

		target.location = camera.location
		target.rotation_euler = camera.rotation_euler
		target.matrix_basis @= Matrix.Translation(distance)

		if context.scene.tool_settings.use_keyframe_insert_auto:
			set_keyframe_for_current_location(target, context)
		
		constraint.enabled = state
		return {'FINISHED'}


#TODO find some place on UI for this operator
class Camera_OT_Active_Object_To_Active_Camera(Operator):
	bl_idname = 'camera.align_active_object_to_active_camera'
	bl_label = "Align to Active Camera"
	bl_description = "Align Active Object to Active Camera"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		if not context.object:
			return False
		return context.scene.camera

	def execute(self, context):
		camera = context.scene.camera
		target = context.object
		size = camera.data.display_size
		distance = (0, 0, -size*3)
		target.location = camera.location
		target.rotation_euler = camera.rotation_euler
		target.matrix_basis @= Matrix.Translation(distance)
		return {'FINISHED'}


# TODO remove this tool on Blender 3.6LTS perios has done
# After Blender 4.2 this tool no longer needed
class Camera_OT_Create_DOF_Target(Operator):
	bl_idname = 'camera.create_dof_target'
	bl_label = "Create DOF Target"
	bl_description = "Creat and setup DOF target for easy arrange"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if not ctx.object:
			return False
		
		if not ctx.object.type == 'CAMERA':
			return False
		
		return ctx.object.data.dof.focus_object == None

	def execute(self, ctx):
		camera = ctx.object
		size = camera.data.display_size
		target = cretae_dof_target_object(camera)
		target.location = camera.matrix_world.to_translation()
		target.empty_display_size = size*2 
		target.name = camera.name + "_DOF_target"
		camera.data.dof.use_dof = True
		camera.data.dof.focus_object = target
		create_dof_driver(camera, target)
		set_as_active_object(ctx, camera)
		return {'FINISHED'}


# TODO remove this tool on Blender 3.6LTS perios has done
# After Blender 4.2 this tool no longer needed
class Camera_OT_Select_DOF_Target(Operator):
	bl_idname = 'camera.select_dof_target'
	bl_label = "Select DOF Target"
	bl_description = "Select DOF target Object"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		if not ctx.object:
			return False
		
		if not ctx.object.type == 'CAMERA':
			return False
		
		return ctx.object.data.dof.focus_object

	def execute(self, ctx):
		target = ctx.active_object.data.dof.focus_object
		set_as_active_object(ctx, target)
		return {'FINISHED'}

# TODO remove this tool on Blender 3.6LTS perios has done
# After Blender 4.2 this tool no longer needed
class Camera_OT_DOF_Depth_Picker(Operator):
	bl_idname = 'camera.dof_depth_picker'
	bl_label = "Pick DOF depth"
	bl_description = "Put DOF target on picked"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if not ctx.scene.camera:
			return False

		return ctx.scene.camera.data.dof.focus_object
	
	def modal(self, ctx, event):
		if ctx.area.type != 'VIEW_3D':
			return {'PASS_THROUGH'}

		if not event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
			return {'PASS_THROUGH'}

		if event.type == 'LEFTMOUSE':

			if event.value == 'PRESS':
				ret = ray_cast(ctx, event.mouse_region_x, event.mouse_region_y)				
				if ret[0]:
					ctx.scene.camera.data.dof.focus_object.location = ret[0]

			if event.value =='RELEASE':
				return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def execute(self, _):
		return {'FINISHED'}
	
	def invoke(self, ctx, _):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class Camera_PT_Panel(Panel):
	bl_label = "Target / Tools"
	bl_idname = 'DATA_PT_Camera'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls,ctx):
		return ctx.object.type == 'CAMERA'

	def draw(self, _):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.operator('camera.create_target', text="Create Target")
		row.operator('camera.clear_targte', text="Clear Target")
		row = box.row()
		row.operator('camera.select_target', text="Select Target")
		row.operator('camera.align_target', text="Align Target")

		box = layout.box()
		row = box.row()
		row.operator('camera.create_dof_target', text="Create DOF Target")
		row.operator('camera.select_dof_target', text="Select DOF Target")


def camera_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('camera.create_target')
	layout.operator('camera.clear_targte')
	layout.operator('camera.select_target')
	layout.operator('camera.dof_depth_picker', text="Pick DOF depth")


classes = {
	Camera_PT_Panel,
	Camera_OT_Align_Target,
	Camera_OT_Active_Object_To_Active_Camera,
	Camera_OT_Clear_Target,
	Camera_OT_Create_Target,
	Camera_OT_Create_DOF_Target,
	Camera_OT_DOF_Depth_Picker,
	Camera_OT_Select_DOF_Target,
	Camera_OT_Select_Target
}


def register_terget_camera():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.VIEW3D_MT_view_cameras.append(camera_menu)


def unregister_terget_camera():
	bpy.types.VIEW3D_MT_view_cameras.remove(camera_menu)

	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == '__main__':
	register_terget_camera()