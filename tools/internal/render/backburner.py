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
# Original code for blender 2.7x from "Matt Ebb | Blaize | Anthony Hunt | Spirou4D" #
# https://blenderartists.org/t/addon-blender-to-backburner-free-autodesk-network-renderer/661539 #
# https://www.dropbox.com/s/ivschytl309jm2n/render_backburner.zip?dl=0 #
# Update and Modified for Blender 2.8x to 4.x by Nevil #

# 2026/07/15 - update for output path absolut and relative autoswitch

#TODO List
# out of range warning
# backburner frames bit array arrenge
# Frames Invert range
# Frames refine
# breake long frame strings
# Fx ir Rx or Mx fore get renge between 2 markers
# bpy.data.is_saved use this isted of is has file name or not

#ISSUE
# in frame mode can not submite a singel frame

""" This file can be instaled as an stand alone add-on too """
bl_info = {
	"name": "BsMax-Backburner",
	"description": "Backburner for Blender 3.6LTS ~ 4.5LTS",
	"author": "Matt Ebb | Blaize | Anthony Hunt | Spirou4D | Nevil",
	"version": (1, 3, 0),
	"blender": (3, 6, 0),# ~ 4.5
	"location": "Properties/ Output/ Backbrner",
	"wiki_url": "https://github.com/NevilArt/BsMax/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax/issues",
	"category": "Render"
}

from importlib.resources import path
from multiprocessing import context
from posixpath import relpath

import bpy
import os
import subprocess
import platform
import json

from bpy.props import (
	PointerProperty, StringProperty,
	BoolProperty, IntProperty, EnumProperty
)
from bpy.types import Panel, Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.app import version

last_acceptable_repository_path = ""


def backburner_path():
	os_name = platform.system()
	if os_name == 'Windows':
		return 'C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe'

	if os_name == 'Linux':
		return '/opt/Autodesk/backburner/cmdjob'

	if os_name == 'Darwin':
		return '/opt/Autodesk/backburner/cmdjob'

	return ''


def get_job_name(context):
	name = bpy.path.basename(bpy.data.filepath)
	name = (name.split('.'))[0]

	# Add scene name if there more than one scenes
	if len(bpy.data.scenes) > 1:
		name += '_' + context.scene.name

	# Add viewlayer name if there more than one view layer
	if len(context.scene.view_layers) > 1:
		name += '_' + context.window.view_layer.name
	
	return name


def string_to_integer_array(frames):
	""" Get string in BitArray format and conver to IntegerArray """
	string, ints = '', []

	""" check the string """
	for l in frames:
		if l in '0123456789,-':
			string += l

	""" convert strings to integers """
	string = string.strip()
	ranges = string.split(',')
	numstr = [r.split('-') for r in ranges]

	for n in numstr:
		if len(n) == 1:
			if n[0] != '':
				ints.append(int(n[0]))

		elif len(n) == 2:
			n1 = int(n[0])
			n2 = int(n[1])
			if n2 > n1:
				for i in range(n1, n2+1):
					ints.append(i)
	ints.sort()
	return ints


def integer_array_to_bitarray_string(ints):
	return ""


def convertable_to_integer(string):
	for digit in string:
		if not digit in '0123456789':
			return False
	return True


def get_max_file_name_digit(file_path, file_name, extention):
	files = [file for file in os.listdir(file_path)
		if file.lower().endswith(extention)
	]
	file_name_length = len(file_name)
	extention_length = len(extention)
	files = [name for name in files if name.startswith(file_name)]

	digit_parts = [name[file_name_length:-extention_length]
		   for name in files
	]

	numbers = [int(number) for number in digit_parts
		if convertable_to_integer(number)
	]
	
	return max(numbers)+1 if numbers else 0


def create_new_unigue_file_name(context):
	backburner = context.scene.backburner

	file_path = backburner.repository_path \
		if backburner.use_repository else \
			os.path.dirname(bpy.data.filepath)

	# create a file name
	file_name = backburner.job_name \
		if backburner.use_job_name else	get_job_name(context)
	
	file_name += "_BACKBURNERTEMPFILE_"
	number = get_max_file_name_digit(file_path, file_name, '.blend')
	full_name = file_path + os.sep + file_name + str(number) + '.blend'
	return full_name


def check_start_frame(_, context):
	""" Make sure start frame always smaller than end frame """
	backburner = context.scene.backburner
	if backburner.frame_start > backburner.frame_end:
		backburner.frame_end = backburner.frame_start


def check_end_frame(_, context):
	""" Make sure end frame always bigger than start frame """
	backburner = context.scene.backburner
	if backburner.frame_end < backburner.frame_start:
		backburner.frame_start = backburner.frame_end


def filter_frames_bitarray(_, context):
	""" Remove illeagle character from Frames field """
	backburner = context.scene.backburner
	string = ''

	for l in backburner.frames_bitarray:
		if l in '0123456789,-':
			string += l

	if backburner.frames_bitarray != string:
		backburner.frames_bitarray = string


def get_render_frames_count(context):
	scene = context.scene
	backburner = scene.backburner
	mode = backburner.override_frame_range
	
	if mode == 'FRAMES':
		return len(string_to_integer_array(backburner.frames_bitarray))
	
	start_frame = backburner.frame_start \
		if mode == 'RANGE'else scene.frame_start

	end_frame = backburner.frame_end if mode == 'RANGE' else scene.frame_end

	return end_frame - start_frame + 1


def output_path_mode_switch(context, mode):
	if mode == 'ABSOLUTE':
		context.scene.render.filepath = bpy.path.abspath(context.scene.render.filepath)
	else:
		context.scene.render.filepath = bpy.path.relpath(context.scene.render.filepath)


def task_fild(start, end):
	""" Create one field of render task for multiple Frame per task mode  """
	field = 'Frame_' + str(start)

	if start != end:
		field += '-' + str(end)

	field += '\t' + str(start) + '\t' + str(end) + '\n'

	return field


def create_task_list_file(context, filename):
	""" Combine all taskes and write in
	file for submit to Backburner manager """

	scene = context.scene
	backburner = scene.backburner
	mode = backburner.override_frame_range

	""" Create Task data """
	task, frames = '', []
	step = backburner.frames_per_task

	""" Get user given range and genarate array of frames most render """
	if mode == 'FRAMES':
		frames = string_to_integer_array(backburner.frames_bitarray)

	else:
		start_frame = backburner.frame_start \
			if mode == 'RANGE' else scene.frame_start

		end_frame = backburner.frame_end \
			if mode == 'RANGE' else scene.frame_end

		for frame in range(start_frame, end_frame+1):
			frames.append(frame)

	if step == 1:
		""" Single frame per task """
		for frame in frames:
			task += task_fild(frame, frame)

	elif len(frames) > 0:
		""" Multi frame per task """
		start = end = frames[0]
		
		for frame in frames[1:]: # skip first element
			""" check is the next frame is part of sequence """
			if frame == end + 1:
				end = frame
			else:
				task += task_fild(start, end)
				start = end = frame

			""" Split if reach to step size """
			if end - start >= step:
				task += task_fild(start, end-1)
				start = end = frame

			""" pack the end part of sequence """
			if frame == frames[-1]:
				end = frame
				task += task_fild(start, end)

	""" Write task to file """
	dir = os.path.dirname(filename)
	if os.access(dir, os.W_OK):
		task_list_file_name = os.path.join(dir, 'submit_temp_cmd')
		file = open(task_list_file_name, 'w')
		file.write(task)
		file.close()

	return task_list_file_name


def create_cmd_command(context):
	backburner = context.scene.backburner

	relpath = bpy.path.relpath(context.scene.render.filepath)
	if relpath:
		output_path_mode_switch(context, 'ABSOLUTE')

	file_name = create_new_unigue_file_name(context)
	bpy.ops.wm.save_as_mainfile(filepath=file_name, copy=True)

	if relpath:
		output_path_mode_switch(context, 'RELATIVE')

	task_list_file = create_task_list_file(context, file_name)

	# cmdjob.exe
	# -jobname "testJob"
	# -description "job de test"
	# -timeout 6000
	# -manager "192.168.73.91"
	# -port "3234"
	# -logPath "Q:/PAUL/testMax2016" 
	# -tasklist "Q:/PAUL/testMax2016/taskFileScript.txt"
	# -numTasks 10
	# -group "Blender"
	# -taskname 1 -jobParamFile "Q:/PAUL/testMax2016/jobParams.txt"
	# -priority 0
	# -servers "n091-a" "C:/Program Files/Autodesk/3ds Max 2016/3dsmax.exe"
	# -q -mip -silent -U MAXScript %tp2

	""" Create Backburner CMD Command """
	cmd = [backburner.path_backburner]
	cmd += ['-jobName:', backburner.job_name]
	cmd += ['-manager:', backburner.manager]

	if backburner.port != 3234:
		cmd += ['-port:', str(backburner.port)]

	if backburner.group != '':
		cmd += ['-group:', backburner.group]

	if backburner.job_details != '':
		cmd += ['-description:', backburner.job_details]

	cmd += ['-priority:', str(backburner.priority)]
	cmd += ['-timeout:', str(backburner.timeout)]

	if backburner.suspended:
		cmd += ['-suspended']

	cmd += ['-taskList:', task_list_file]
	cmd += ['-taskName:', '1']

	if backburner.use_custom_path:
		cmd += [backburner.blender_path]
	else:
		cmd += [bpy.app.binary_path]
	# cmd += ['-submit:', bpy.data.filepath]

	if backburner.background_render:
		cmd += ['--background']

	cmd += [file_name]
	cmd += ['--frame-start', '%tp2']
	cmd += ['--frame-end', '%tp3']
	cmd += ['--render-anim']
	
	return task_list_file, cmd


def submit(context):
	task_list_file, cmd = create_cmd_command(context)
	""" Try to Submit job to backburner """
	try:
		subprocess.check_output(cmd, shell=True)
		os.remove(task_list_file)
		return True

	except:
		os.remove(task_list_file)
		return False


def get_datafiles_path():
	""" return datafile path and create if not exist """
	datafiles_path = bpy.utils.user_resource("SCRIPTS", path="addons")

	datafiles_path += os.sep + 'BsMax-datafiles'

	if not os.path.isdir(datafiles_path):
		os.mkdir(datafiles_path)

	return datafiles_path


def get_preset_file_name():
	# preset_directory = bpy.utils.extension_path_user(__package__, path="", create=True)
	return get_datafiles_path() + os.sep + 'Backburner.json'


def backburner_state_as_dictionary(context):
	backburner = context.scene.backburner
	return {
		'timeout': backburner.timeout,
		'priority': backburner.priority,
		'suspended': backburner.suspended,
		'frames_per_task': backburner.frames_per_task,
		'manager': backburner.manager,
		'port': backburner.port,
		'group': backburner.group,
		'background_render:': backburner.background_render,
		'use_job_name': backburner.use_job_name,
		'use_custom_path': backburner.use_custom_path,
		'blender_path': backburner.blender_path,
		'use_repository': backburner.use_repository,
		'repository_path': backburner.repository_path
	}


def write_dictionary_to_json_file(data, file_path):
	try:
		with open(file_path, 'w', encoding='utf-8') as json_file:
			json.dump(data, json_file, ensure_ascii=False, indent=4)
		return True
	except:
		return False


def read_json_file_to_dictionary(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as json_file:
			data = json.load(json_file)
		return data
	except:
		return {}


def draw_backburner_panel(cls, context):
	backburner = context.scene.backburner

	layout = cls.layout
	row = layout.row()
	row.operator(
		'wm.url_open',
		icon='HELP'
	).url= "https://github.com/NevilArt/BsMax/wiki/Render-Tools"

	button_text = "Submit " + str(get_render_frames_count(context))
	button_text += " frames to Backburner"
	row.operator(
		'render.backburner_action',
		text=button_text,
		icon='RENDER_ANIMATION'
	).action='SUBMIT'

	row.operator(
		'render.backburner_action', text="", icon='FILE_TICK'
	).action='SAVE'

	row.operator(
		'render.backburner_action',
		text="",
		icon='RECOVER_LAST'
	).action='LOAD'

	layout.separator()

	row = layout.row()
	row.prop(backburner, 'job_name')
	use_name_icon = 'CHECKBOX_HLT' if backburner.use_job_name else 'CHECKBOX_DEHLT'
	row.prop(backburner, 'use_job_name', text="", icon=use_name_icon)

	row.operator(
		'render.backburner_action',
		text="",
		icon='FILE_REFRESH'
	).action='GETNAME'

	row = layout.row()
	row.prop(backburner, 'job_details')
	row.label(text="", icon='BLANK1')
	layout.separator()

	row = layout.row()
	row.prop(backburner, 'timeout')
	row.prop(backburner, 'priority')
	row.prop(backburner, 'suspended', text="", icon='EVENT_S')
	layout.separator()

	row = layout.row()
	row.prop(backburner, 'override_frame_range')
	row.prop(backburner, 'frames_per_task')

	row = layout.row()
	if backburner.override_frame_range == 'RANGE':
		row.prop(backburner, 'frame_start')
		row.prop(backburner, 'frame_end')

	elif backburner.override_frame_range == 'FRAMES':
		row = layout.row()
		row.prop(backburner, 'frames_bitarray', text="")
		# row.prop(
		# 	backburner, 'invert_bitarray', text="", icon = 'ARROW_LEFTRIGHT'
		# )

	layout.separator()
	row = layout.row()
	row.prop(backburner, 'manager')
	row.prop(backburner, 'port')
	row.prop(backburner, 'group')

	row = layout.row()
	row.prop(backburner, 'use_custom_path')
	row.prop(backburner, 'background_render')

	if backburner.use_custom_path:
		row = layout.row()
		row.prop(backburner, 'blender_path')

	row = layout.row()
	row.prop(backburner, 'use_repository')
	if backburner.use_repository:
		row = layout.row()
		row.prop(backburner, 'repository_path')


def subcation_get_name(context):
	job_name = "New Job"
	
	if bpy.data.filepath:
		job_name = get_job_name(context)

	context.scene.backburner.job_name = job_name


def subaction_save(context):
	file_name = get_preset_file_name()
	backburner_state = backburner_state_as_dictionary(context)
	write_dictionary_to_json_file(backburner_state, file_name)


def subaction_load(context):
	backburner = context.scene.backburner
	file_name = get_preset_file_name()
	backburner_state = read_json_file_to_dictionary(file_name)

	for key, value in backburner_state.items():
		if hasattr(backburner, key):
			setattr(backburner, key, value)


def subaction_refine_frames(context):
	frames = string_to_integer_array("")
	integer_array_to_bitarray_string(frames)


def subaction_riverce_frames(context):
	pass


def repository_path_check(cls, _):
	global last_acceptable_repository_path
	repository_path = cls.repository_path
	if os.access(repository_path, os.W_OK):
		if repository_path[-1] == os.sep:
			cls.repository_path = repository_path[:-1]
			last_acceptable_repository_path = cls.repository_path
	else:
		cls.repository_path = last_acceptable_repository_path


def subaction_submit(self, context):
	if context.blend_data.filepath == '':
		self.report({'WARNING'}, "Save File Before Submit")
		return{'FINISHED'}

	backburner = context.scene.backburner

	if backburner.blender_path == '':
		self.report({'ERROR'}, "Network path to Blender hasn't been set")
		return {'CANCELLED'}

	if backburner.path_backburner == '':
		self.report({'ERROR'}, "Path to Backburner cmdjob.exe hasn't been set")
		return {'CANCELLED'}

	self.report({'OPERATOR'}, "Submitting...")
	
	if submit(context):
		self.report({'OPERATOR'}, "Job Submited to backburner manager")

	else:
		self.report(
			{'WARNING'}, "Backburner manager not found. Failed to submission."
		)

	#TODO delete repository render file if fails


class Backburner_Property(PropertyGroup):
	job_name: StringProperty(
		name="Job Name",
		maxlen=256,
		default="New Job",
		description="Name of the Job to be shown in Backburner Monitor"
	) # type: ignore

	use_job_name: BoolProperty(
		name="",
		default=False,
		description="Use Job Name as Repository File Name"
	) # type: ignore
	
	job_details: StringProperty(
		name="Description",
		maxlen=400, default="",
		description="Add aditional information to render task"
	) # type: ignore
	
	frames_per_task: IntProperty(
		name="Frames per Task",
		min=1, max=9999,
		soft_min=1, soft_max=1000,
		default=1,
		description="Number of frames to give each render node"
	) # type: ignore

	timeout: IntProperty(
		name="Timeout",
		min=1, max=99999,
		soft_min=1, soft_max=1440,
		default=120,
		description="Timeout per task"
	) # type: ignore

	priority: IntProperty(
		name="Priority",
		min=0, max=99,
		soft_min=0, soft_max=99,
		default=50,
		description="Priority of this job (0 is Critical)"
	) # type: ignore

	suspended: BoolProperty(
		name="Suspended",
		default=True,
		description="Submit Job as Suspended"
	) # type: ignore

	override_frame_range: EnumProperty(
		name="Frames",
		items=[
			('ACTIVE', "Active Time", ""),
			('RANGE', "Range", ""),
			('FRAMES', "Specific Frames", "")
		],
		default='ACTIVE',
		description="Override Render frames Range"
	) # type: ignore

	frame_start: IntProperty(
		name="Start Frame",
		min=1, max=50000,
		default=1,
		update=check_start_frame,
		description="Start frame of animation sequence to render"
	) # type: ignore

	frame_end: IntProperty(
		name="End Frame",
		min=1, max=50000,
		default=250,
		update=check_end_frame,
		description="End frame of animation sequence to render"
	) # type: ignore
	
	frames_bitarray: StringProperty(
		name="Frames",
		maxlen=400,
		default="1,3,5-7",
		update=filter_frames_bitarray,
		description="Custom frames"
	) # type: ignore

	invert_bitarray: BoolProperty(
		name="", default=False,
		description="Submit invert range of frames"
	) # type: ignore

	manager: StringProperty(
		name="Manager",
		maxlen=400,
		default="localhost",
		description="Name of render manager"
	) # type: ignore
	
	port: IntProperty(
		name="Port",
		min=0, max=999999,
		default=3234,
		description="Manager Port"
	) # type: ignore
	
	group: StringProperty(
		name="Groups",
		maxlen=400,
		default="",
		description="Name of Render Group"
	) # type: ignore
	
	path_backburner: StringProperty(
		name="Backburner Path",
		maxlen=400,
		subtype='FILE_PATH',
		default=backburner_path(),
		description="Path to Backburner cmdjob.exe"
	) # type: ignore

	use_custom_path: BoolProperty(
		name="Use Custom Blender",
		default=False
	) # type: ignore

	blender_path: StringProperty(
		name="Blender Path",
		maxlen=400,
		subtype='FILE_PATH',
		default=bpy.app.binary_path,
		description="Path of blender.exe"
	) # type: ignore
	
	# options: BoolProperty (name='More', default=False)

	background_render: BoolProperty (
		name="Render in Background", default=True
	) # type: ignore
	
	submit_file: BoolProperty (
		name="Submit file to Manager", default=False
	) # type: ignore

	servers_description = "Render this job only with the servers specified "
	servers_description += "(semi-colon separated list - ignored if group is used)"
	servers: StringProperty(
		name="Servers",
		maxlen=400,
		default="",
		description=servers_description
	) # type: ignore

	use_repository: BoolProperty(
		name="Use Custom Repository",
		default=False
	) # type: ignore

	repository_path: StringProperty(
		name="Repository Path",
		subtype='DIR_PATH',
		update=repository_path_check,
		description="Custom Repository Directory"
	) # type: ignore


class Render_OT_Backburner_Action(Operator):
	""" All Backburner sub action """
	bl_idname = 'render.backburner_action'
	bl_label = "Backburner Sub action"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	action: StringProperty(name='Action') # type: ignore

	def execute(self, context):

		if self.action == 'SUBMIT':
			subaction_submit(self, context)

		elif self.action == 'GETNAME':
			subcation_get_name(context)

		elif self.action == 'SAVE':
			subaction_save(context)

		elif self.action == 'LOAD':
			subaction_load(context)

		elif self.action == 'REFINEFRAMES':
			subaction_refine_frames(context)

		elif self.action == 'REVERCEFRAMES':
			subaction_riverce_frames(context)

		return {'FINISHED'}


class Render_OT_Backburner(Operator):
	""" Submit scene to Backburner as render job. """
	bl_idname = 'render.backburner'
	bl_label = "Backburner"
	bl_options = {'REGISTER'}

	def draw(self, context):
		draw_backburner_panel(self, context)
	
	def execute(self, _):
		return{'FINISHED'}
	
	def invoke(self, context, _):
		return context.window_manager.invoke_props_dialog(self, width=500)


class RENDER_PT_Backburner(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'output'
	bl_label = "Backburner"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		draw_backburner_panel(self, context)


def backburner_menu(self, _):
	self.layout.operator(
		'render.backburner',
		text="Submit to Backburner",
		icon='NETWORK_DRIVE'
	)


classes = {
	Backburner_Property,
	Render_OT_Backburner,
	Render_OT_Backburner_Action,
	RENDER_PT_Backburner
}


def register_backburner():
	for cls in classes:
		register_class(cls)
	
	bpy.types.Scene.backburner = PointerProperty(
		type=Backburner_Property,
		name="Backburner Submission"
	)

	bpy.types.TOPBAR_MT_render.prepend(backburner_menu)


def unregister_backburner():
	bpy.types.TOPBAR_MT_render.remove(backburner_menu)
	del bpy.types.Scene.backburner

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_backburner()