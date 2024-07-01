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
# 2024/06/06

import bpy

import math

from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty, FloatProperty
from bpy.utils import register_class, unregister_class


def copy_to_clipboard(ctx, text):
	ctx.window_manager.clipboard = text


def keys_to_array_string(keys, mode, decimal=0, scale=1):
	if mode == '3DSMAX':
		script = "#("
		for index, key in enumerate(keys):
			frame = key[0]
			value = key[1]*scale

			script += "#("
			script += str(int(frame))
			script += ","
			script += str(value) if decimal == 0 else str(round(value, decimal))
			script += ")"
			script += "," if index < len(keys)-1 else ""

		script += ")"
		return script

	if mode == 'PYTHON':
		script = "[]"
		return script

	if mode == 'MEL':
		script = "{}"
		return script

	return ""


def for_loop_script_for_chanel(chanel, mode):
	if mode == '3DSMAX':
		script = "for key in keys do at time key[1] "
		script += "cam." + chanel +" = key[2]"
		return script
	return ""


def chanel_to_maxscript_field(chanel, target, decimal=0, scale=1):
	script = " keys = "
	script += keys_to_array_string(chanel, '3DSMAX', decimal, scale) + "\n"
	script += " " + for_loop_script_for_chanel(target, '3DSMAX') + "\n"
	script += "\n"
	return script


def data_to_maxscript(cls, data):
	""" cls : Camera_OT_Copy \n
		animation_data : CameraAnimationData
	"""
	script = "-- Camera paste Script Start from here --\n" 
	if cls.create:
		script += "cam = Freecamera isSelected:on\n"
		script += "cam.name = \"" + data.owner.name + "\"\n"
	else:
		script += "cam = $\n"
	
	"if classof cam != Camera do return"
	
	if cls.clip:
		script += "cam.clipManually = True \n"

	script += "on animate on (\n"

	if cls.transform:
		script += chanel_to_maxscript_field(
			data.location_x_keys, "position.x", 0, cls.scale
		)
		script += chanel_to_maxscript_field(
			data.location_y_keys, "position.y", 0, cls.scale
		)
		script += chanel_to_maxscript_field(
			data.location_z_keys, "position.z", 0, cls.scale
		)

		script += chanel_to_maxscript_field(
			data.rotation_euler_x_keys, "rotation.x"
		)
		script += chanel_to_maxscript_field(
			data.rotation_euler_y_keys, "rotation.y"
		)
		script += chanel_to_maxscript_field(
			data.rotation_euler_z_keys, "rotation.z"
		)

		script += chanel_to_maxscript_field(data.scale_x_keys, "scale.x")
		script += chanel_to_maxscript_field(data.scale_y_keys, "scale.y")
		script += chanel_to_maxscript_field(data.scale_z_keys, "scale.z")

	if cls.fov:
		script += chanel_to_maxscript_field(data.lens_keys, "fov", 3)

	if cls.clip:
		script += chanel_to_maxscript_field(
			data.clip_start_keys, "nearclip", 3, cls.scale
		)
		
		script += chanel_to_maxscript_field(
			data.clip_end_keys, "farclip", 3, cls.scale
		)

	script += ")\n" #end of animate on
	script += "-- Camera paste Script end here --\n" 
	return script


#TODO check is camera selected
def data_to_script(cls, data, target):
	script = ""
	if target == '3DSMAX':
		return data_to_maxscript(cls, data)

	return script


def get_datapath(action, chanel):
	for fcurve in action.fcurves:
		if fcurve.data_path == chanel:
			return fcurve
	return None


def get_sensor_width_value(camera, fcurve, frame):
	if fcurve:
		return fcurve.evaluate(frame)
	return camera.data.sensor_width


def get_fcurve_keys(fcurve):
	keys = []
	if fcurve:
		for keyframe in fcurve.keyframe_points:
			frame, value = keyframe.co
			keys.append((frame, value))
	return keys


def get_transform_animation(cls):
	action = cls.owner.animation_data.action
	if not action:
		return
	
	for fcurve in action.fcurves:
		if fcurve.data_path == 'location':
			if fcurve.array_index == 0:
				cls.location_x_keys = get_fcurve_keys(fcurve)
			
			if fcurve.array_index == 1:
				cls.location_y_keys = get_fcurve_keys(fcurve)

			if fcurve.array_index == 2:
				cls.location_z_keys = get_fcurve_keys(fcurve)

		if fcurve.data_path == 'rotation_euler':
			if fcurve.array_index == 0:
				cls.rotation_euler_x_keys = get_fcurve_keys(fcurve)
			
			if fcurve.array_index == 1:
				cls.rotation_euler_y_keys = get_fcurve_keys(fcurve)

			if fcurve.array_index == 2:
				cls.rotation_euler_z_keys = get_fcurve_keys(fcurve)
		
		if fcurve.data_path == 'scale':
			if fcurve.array_index == 0:
				cls.scale_x_keys = get_fcurve_keys(fcurve)
			
			if fcurve.array_index == 1:
				cls.scale_y_keys = get_fcurve_keys(fcurve)

			if fcurve.array_index == 2:
				cls.scale_z_keys = get_fcurve_keys(fcurve)
		

def get_fov_animation(cls):
	camera_data = bpy.data.cameras[cls.data.name]
	action = camera_data.animation_data.action
	lens_fcurve = get_datapath(action, 'lens')
	sensor_width_fcurve = get_datapath(action, 'sensor_width')

	if lens_fcurve:
		for keyframe in lens_fcurve.keyframe_points:
			frame, lens = keyframe.co
			sensor_width = get_sensor_width_value(
				cls.owner, sensor_width_fcurve, frame
			)

			fov = math.degrees(2 * math.atan(sensor_width / (2 * lens)))
			cls.lens_keys.append((frame, fov))


def get_clip_animation(cls):
	camera_data = bpy.data.cameras[cls.data.name]
	action = camera_data.animation_data.action
	start_clip_fcurve = get_datapath(action, 'clip_start')
	end_clip_fcurve = get_datapath(action, 'clip_end')
	cls.clip_start_keys = get_fcurve_keys(start_clip_fcurve)
	cls.clip_end_keys = get_fcurve_keys(end_clip_fcurve)


def create_camera(cameraData):
	camera_data = bpy.data.cameras.new(name=cameraData.cameraName)
	camera_object = bpy.data.objects.new(cameraData.cameraName, camera_data)
	bpy.context.scene.collection.objects.link(camera_object)

	for transform in cameraData.transform:
		print(transform)

	return camera_object


class Key:
	def __init__(self):
		self.frame = 0
		self.value = 0
		self.type = None
	

class CameraAnimationData:
	def __init__(self, camera):
		self.owner = camera
		self.data = camera.data

		self.location_x_keys = []
		self.location_y_keys = []
		self.location_z_keys = []
		self.rotation_euler_x_keys = []
		self.rotation_euler_y_keys = []
		self.rotation_euler_z_keys = []
		self.scale_x_keys = []
		self.scale_y_keys = []
		self.scale_z_keys = []

		self.type_keys = []
		self.lens_keys = []#done
		self.lens_unit_keys = []
		self.shift_x_keys = []
		self.shift_y_keys = []
		self.clip_start_keys = []#done
		self.clip_end_keys = []#done
		self.clip_end_keys = []
		self.dof_focus_distance_keys = []
		self.dof_aperture_fstop_keys = []
		self.dof_aperture_blades_keys = []
		self.dof_aperture_rotation_keys = []
		self.dof_aperture_ratio_keys = []
		self.sensor_fit_keys = []
		self.sensor_width_keys = []
		self.show_safe_areas_keys = []
		self.show_safe_center_keys = []
		self.display_size_keys = []
		self.show_limits_keys = []
		self.show_mist_keys = []
		self.show_sensor_keys = []
		self.show_name_keys = []
		self.passepartout_alpha_keys = []
		self.show_sensor_keys = []
		self.show_composition_thirds_keys = []
		self.show_composition_center_keys = []
		self.show_composition_center_diagonal_keys = []
		self.show_composition_golden_keys = []
		self.show_composition_golden_tria_a_keys = []
		self.show_composition_golden_tria_b_keys = []
		self.show_composition_harmony_tri_a_keys = []
		self.show_composition_harmony_tri_b_keys = []


#TODO check does camera has action or not
def get_camera_animation_data(cls, camera_object):
	if camera_object.type != 'CAMERA':
		return []
	
	animation_data = CameraAnimationData(camera_object)

	if cls.transform: 
		get_transform_animation(animation_data)

	if cls.fov:
		get_fov_animation(animation_data)

	if cls.clip:
		get_clip_animation(animation_data)

	return animation_data


def copy_camera_draw(cls):
	layout = cls.layout
	box = layout.box()
	box.prop(cls, 'create', text="Create New Camera")
	
	if cls.has_transform_animation:
		box.prop(cls, 'transform', text="Transform")
	else:
		box.label(text="There is no transform animation.")

	if cls.has_data_animation:
		box.prop(cls, 'fov', text="F.O.V.")
		box.prop(cls, 'clip', text="Near/Far Cliping")
	else:
		box.label(text="There is no attribute animation.")

	box = layout.box()
	box.prop(cls, 'target', text="Target App")
	box.prop(cls, 'scale', text="Scale")


class Camera_OT_Copy(Operator):
	bl_idname = 'camera.copy_animation'
	bl_label = "Copy Camera Animation (Alpha Version)"
	bl_description = "Copy Camera Animation as executable Script for external softwares"
	bl_options = {'REGISTER', 'UNDO'}

	target: EnumProperty(
		name="Targte",
		items=[
			('3DSMAX', "Autodesk 3DsMax", "")
		],
		default='3DSMAX'
	) # type: ignore

	scale: FloatProperty(
		name="Unit Scale:", min=0, default=1,
		description="Scale for match the unit scale"
	) # type: ignore

	create: BoolProperty(
		name="Create New Camera", default=False,
		description="Create a new camera in target software"
	) # type: ignore
	
	transform: BoolProperty(name="Transform", default=False,
		description="Copy Camera Transform or Animation"
	) # type: ignore
	
	fov: BoolProperty(name="FOV", default=True,
		description="Copy Camrea FOV value or Animation"
	) # type: ignore

	clip: BoolProperty(name="Clip", default=True,
		description="Copy Camrea Cliping value or Animation"
	) # type: ignore

	has_transform_animation = False
	has_data_animation = False

	@classmethod
	def poll(self, ctx):
		if ctx.object:
			return ctx.object.type == 'CAMERA'
		return False
	
	def draw(self, _):
		copy_camera_draw(self)
	
	def execute(self, ctx):
		animation_data = get_camera_animation_data(self, ctx.object)
		script = data_to_script(self, animation_data, self.target)
		copy_to_clipboard(ctx, script)
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		self.has_transform_animation = hasattr(
			ctx.object.animation_data.action, 'fcurves'
		)
		
		self.has_data_animation = hasattr(
			ctx.object.data.animation_data, 'action'
		)

		ctx.window_manager.invoke_props_dialog(self)
		return {'RUNNING_MODAL'}


class Camera_OT_Paste(Operator):
	bl_idname = 'camera.paste'
	bl_label = "Paste Camera"
	bl_description = "under development for now do nothing"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "OBJECT"
	
	def execute(self, ctx):
		return{'FINISHED'}


def camera_copy_manu(self, ctx):
	layout = self.layout
	if ctx.object:
		if ctx.object.type == 'CAMERA':
			layout.operator_context = 'INVOKE_DEFAULT'
			layout.operator(
				'camera.copy_animation', text="Camera Animation",
				icon='CAMERA_DATA'
			)


classes = {
    Camera_OT_Copy,
    Camera_OT_Paste
}


def register_copy_past(developmode=False):
	for cls in classes:
		register_class(cls)

	if not developmode:
		bpy.types.BSMAX_MT_view3d_copy.append(camera_copy_manu)


def unregister_copy_past():
	bpy.types.BSMAX_MT_view3d_copy.remove(camera_copy_manu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_copy_past(developmode=True)