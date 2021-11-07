/*##########################################################################
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
##########################################################################*/

/*########################################################################
# Transfer Camera with keyframes from 3dsMax to Blender
# 1.select camera in 3DsMax
# 2.execute this script
# 	some data will copy to windows clipboard
# 3.in blender script editor
# 4.past the python script text from clipboard
# 5.run the script
#	same camera with same key frames will recreate in blender
#
# Note: for now key types do not transfer.
########################################################################*/
function as_frame t = ((t as string) as integer) as string

function python_public =
(
	str = "import bpy\n"

	return str
)



struct transform_key
(
	key_time,
	
	pos_x,
	pos_y,
	pos_z,
	
	rot_x,
	rot_y,
	rot_z,

	scl_x,
	scl_y,
	scl_z
)

function append_transform_key &transform_keys key_time key_channel key_value =
(
	active_key = undefined
	
	-- try to detect key if avalibla
	for key in transform_keys do (
		if key.key_time == key_time do (
			active_key = key
			exit
		)
	)
	
	-- if not detected create new one --
	if active_key == undefined do (
		active_key = transform_key()
		append transform_keys active_key
	)
	
	-- put given data in key class --
	active_key.key_time = key_time
	
	if key_channel == "pos_x" do
		active_key.pos_x = key_value
	if key_channel == "pos_y" do
		active_key.pos_y = key_value
	if key_channel == "pos_z" do
		active_key.pos_z = key_value
	
	if key_channel == "rot_x" do
		active_key.rot_x = key_value
	if key_channel == "rot_y" do
		active_key.rot_y = key_value
	if key_channel == "rot_z" do
		active_key.rot_z = key_value
	
	if key_channel == "scl_x" do
		active_key.scl_x = key_value
	if key_channel == "scl_y" do
		active_key.scl_y = key_value
	if key_channel == "scl_z" do
		active_key.scl_z = key_value
)

function free_camera_to_blender_python cam =
(
	transform_keys = #()

	-- Collect the Position kesy --
	for key in cam.pos.controller.x_position.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "pos_x" (key.value/100)
	for key in cam.pos.controller.y_position.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "pos_y" (key.value/100)
	for key in cam.pos.controller.z_position.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "pos_z" (key.value/100)

	-- collect the rotation keys --
	for key in cam.rotation.controller.x_rotation.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "rot_x" (degtorad key.value)
	for key in cam.rotation.controller.y_rotation.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "rot_y" (degtorad key.value)
	for key in cam.rotation.controller.z_rotation.keys do
		append_transform_key &transform_keys (as_frame(key.time)) "rot_z" (degtorad key.value)
	

	-- convert dato to blender python script --
	str = "cam = create_camera('" + cam.name +  "', (0, 0, 0), (0, 0, 0))\n"
	for tk in transform_keys do (
		
		str += "set_positon_key(cam, "
		str += tk.key_time as string + ","
		str += tk.pos_x as string + ", " + tk.pos_y as string + ", " + tk.pos_z as string + ", "
		str += ")\n"
	
		str += "set_rotation_eular_key(cam, "
		str += tk.key_time as string + ","
		str += tk.rot_x as string + ", " + tk.rot_y as string + ", " + tk.rot_z as string
		str += ")\n"
		
		str += "\n"
	)

	str += "cam.data.lens_unit = 'FOV'\n"
	str += "\n"

	for key in cam.fov.keys do (
		frame = as_frame(key.time)
		str += "cam.data.angle = " + (DegToRad key.value) as string + "\n"
		str += "cam.data.keyframe_insert(data_path='lens', index=-1, frame=" + frame + ")\n"
		str += "\n"
	)
	str += "\n"
	str += "cam.data.lens_unit = 'MILLIMETERS'\n"
	
	return str
)

function target_camera_to_blender_python cam =
(
	camera_transform_keys = #()
	target_transform_keys = #()

	-- Collect the camera Position kesy --
	for key in cam.pos.controller.x_position.keys do
		append_transform_key &camera_transform_keys (as_frame(key.time)) "pos_x" (key.value/100)
	for key in cam.pos.controller.y_position.keys do
		append_transform_key &camera_transform_keys (as_frame(key.time)) "pos_y" (key.value/100)
	for key in cam.pos.controller.z_position.keys do
		append_transform_key &camera_transform_keys (as_frame(key.time)) "pos_z" (key.value/100)
	
	
	-- Collect the target Position kesy --
	for key in cam.target.pos.controller.x_position.keys do
		append_transform_key &target_transform_keys (as_frame(key.time)) "pos_x" (key.value/100)
	for key in cam.target.pos.controller.y_position.keys do
		append_transform_key &target_transform_keys (as_frame(key.time)) "pos_y" (key.value/100)
	for key in cam.target.pos.controller.z_position.keys do
		append_transform_key &target_transform_keys (as_frame(key.time)) "pos_z" (key.value/100)

	-- convert dato to blender python script --
	str = "cam = create_camera('" + cam.name +  "', (0, 0, 0), (0, 0, 0))\n"
	str += "target = create_target(cam)\n"
	for tk in camera_transform_keys do (
		
		str += "set_positon_key(cam, "
		str += tk.key_time as string + ","
		str += tk.pos_x as string + ", " + tk.pos_y as string + ", " + tk.pos_z as string + ", "
		str += ")\n"
	)

	for tk in target_transform_keys do (
		
		str += "set_positon_key(target, "
		str += tk.key_time as string + ","
		str += tk.pos_x as string + ", " + tk.pos_y as string + ", " + tk.pos_z as string + ", "
		str += ")\n"
	)

	str += "cam.data.lens_unit = 'FOV'\n"
	str += "\n"

	if classof cam.fov.controller != UndefinedClass do
		for key in cam.fov.keys do (
			frame = as_frame(key.time)
			str += "cam.data.angle = " + (DegToRad key.value) as string + "\n"
			str += "cam.data.keyframe_insert(data_path='lens', index=-1, frame=" + frame + ")\n"
			str += "\n"
		)
	str += "\n"
	str += "cam.data.lens_unit = 'MILLIMETERS'\n"
	
	return str
)


function creat_python_script_and_copy_to_clipboard =
(
	script = "from bsmax.max_to_blender import *\n"
	for obj in selection do (
		if classof obj == Freecamera do
			script += free_camera_to_blender_python obj
		if classof obj == Targetcamera do
			script += target_camera_to_blender_python obj
	)
	setclipboardText script
)

creat_python_script_and_copy_to_clipboard()
