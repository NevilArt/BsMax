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
# Update and Modified for Blender 2.8x to 3.x by Nevil #

""" This file can be instaled as an stand alone add-on too """
bl_info = {
	"name": "BsMax-Backburner",
	"description": "Backburner for Blender 2.80 ~ 3.0",
	"author": "Matt Ebb | Blaize | Anthony Hunt | Spirou4D | Nevil",
	"version": (0, 2, 0, 8),# 2021-10-06
	"blender": (2, 80, 0),# to 3.0
	"location": "Properties/ Output/ Backbrner",
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	"category": "Render"
}

import bpy, os, subprocess, random, platform
from bpy.props import PointerProperty, StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Panel, Operator, PropertyGroup



def backburner_path():
	os_name = platform.system()
	if os_name == 'Windows':
		return '"C:\\Program Files (x86)\\Autodesk\\Backburner\\cmdjob.exe"'
	if os_name == 'Linux':
		return '"/opt/Autodesk/backburner/cmdjob"'
	if os_name == 'Darwin':
		return '"/opt/Autodesk/backburner/cmdjob"'
	return '""'



def blender_path():
	return bpy.app.binary_path



def string_to_integer_array(frames):
	""" Get string in BitArray format and conver to IntegerArray """
	string, ints = '', []

	""" check the string """
	for l in frames:
		if l in '0123456789,-':
			string += l

	""" convert strings to integers """
	string = string.strip()
	ranges = string.split(",")
	numstr = [r.split("-") for r in ranges]

	for n in numstr:
		if len(n) == 1:
			if n[0] != '':
				ints.append(int(n[0]))
		elif len(n) == 2:
			n1,n2 = int(n[0]),int(n[1])
			if n2 > n1:
				for i in range(n1,n2+1):
					ints.append(i)
	ints.sort()
	return ints



def create_new_file_name(file_name):
	random_id = random.randint(1000000, 9999999)
	append_text = '_BACKBURNERTEMPFILE_' + str(random_id)
	return os.path.splitext(file_name)[0] + append_text + '.blend'



def check_start_frame(self, ctx):
	""" Make sure star frame allways smaller then end frame """
	csbb = ctx.scene.backburner
	if csbb.frame_start > csbb.frame_end:
		csbb.frame_end = csbb.frame_start



def check_end_frame(self, ctx):
	""" Make sure end frame allways bigger then start frame """
	csbb = ctx.scene.backburner
	if csbb.frame_end < csbb.frame_start:
		csbb.frame_start = csbb.frame_end



def filter_frames_bitarray(self, ctx):
	""" Remove illeagle character from Frames field """
	csbb = ctx.scene.backburner
	string = ''
	for l in csbb.frames_bitarray:
		if l in '0123456789,-':
			string += l
	if csbb.frames_bitarray != string:
		csbb.frames_bitarray = string



class Backburner_Settings(PropertyGroup):
	job_name: StringProperty(name='Job Name', maxlen=256, default='New Job',
		description='Name of the job to be shown in Backburner')
	
	job_details: StringProperty(name='Description', maxlen=400, default='',
		description='Add aditional information to render task')
	
	frames_per_task: IntProperty(name='Frames per Task', 
		min=1, max=1000, soft_min=1, soft_max=64, default=1,
		description='Number of frames to give each render node')

	timeout: IntProperty(name='Timeout', description='Timeout per task',
		default=120, min=1, max=1000, soft_min=1, soft_max=64)

	priority: IntProperty(name='Priority', description='Priority of this job (0 is Critical)',
		min=0, max=99, soft_min=0, soft_max=99, default=50)

	suspended: BoolProperty (name='Suspended', default=True,
		description='Submit Job as Suspended')

	override_frame_range: EnumProperty(name='Frames', description='Override Render frames Range', 
		default='ACTIVE', items=[('ACTIVE','Active Time',''),('RANGE','Range',''),('FRAMES','Specific Frames','')])

	frame_start: IntProperty(name='Start Frame', description='Start frame of animation sequence to render', 
		min=1, max=50000, default=1, update=check_start_frame)

	frame_end: IntProperty(name='End Frame', description='End frame of animation sequence to render',
		min=1, max=50000, default=250, update=check_end_frame)
	
	frames_bitarray: StringProperty(name='Frames', maxlen=400, default='1,3,5-7',
		description='Custom frames', update=filter_frames_bitarray)

	manager: StringProperty(name='Manager', maxlen=400, default='localhost',
		description='Name of render manager')
	
	port: IntProperty(name='Port', description='Manager Port',
		min=0, max=999999, default=3234)
	
	group: StringProperty(name='Groups', maxlen=400, default='',
		description='Name of Render Group')

	path_backburner: StringProperty(name='Backburner Path', description='Path to Backburner cmdjob.exe', 
		maxlen=400, subtype='FILE_PATH', default=backburner_path())

	use_custom_path: BoolProperty (name='Use Custom Blender', default=False)

	blender_path: StringProperty(name='Blender Path', description='Path to blender.exe',
		maxlen=400, subtype='FILE_PATH', default=blender_path())
	
	# options: BoolProperty (name='More', default=False)

	background_render: BoolProperty (name='Render in Background', default=True)
	
	submit_file: BoolProperty (name='Submit file to Manager', default=False)
	
	servers: StringProperty(name='Servers', maxlen=400, default='',
		description='Render this job only with the servers specified (semi-colon separated list - ignored if group is used)')




def task_fild(start, end):
	""" Create one field of render task for multiple Frame per task mode  """
	field = 'Frame_' + str(start)
	if start != end:
		field += '-' + str(end)
	field += '\t' + str(start) + '\t' + str(end) + '\n'
	return field



def create_task_list_file(scene, filename):
	""" Combine all taskes and write in file for submit to Backburner manager """
	backburner = scene.backburner
	mode = backburner.override_frame_range

	""" Create Task data """
	task, frames = '', []
	step = backburner.frames_per_task

	""" Get user given range and genarate array of frames most render """
	if mode == 'FRAMES':
		frames = string_to_integer_array(backburner.frames_bitarray)
	else:
		start_frame = backburner.frame_start if mode == 'RANGE' else scene.frame_start
		end_frame = backburner.frame_end if mode == 'RANGE' else scene.frame_end
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
				task += task_fild(start, end)
				start = end = frame

			""" pack the end part of sequence """
			if frame == frames[-1]:
				end = frame
				task += task_fild(start, end)

	""" Write task to file """
	dir = os.path.dirname(filename)
	if os.access(dir, os.W_OK):
		task_list_file_name = os.path.join(dir,"submit_temp_cmd")
		file = open(task_list_file_name, 'w')
		file.write(task)
		file.close()

	return task_list_file_name



def create_cmd_command(scene):
	cbb = scene.backburner

	file_name = create_new_file_name(bpy.data.filepath)
	bpy.ops.wm.save_as_mainfile(filepath=file_name, copy=True)
	task_list_file = create_task_list_file(scene, file_name)

	# cmdjob.exe -jobname "testJob"
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

	""" Create Backburner CMD Text """
	cmd = cbb.path_backburner
	cmd += ' -jobName:"' + cbb.job_name + '"'
	cmd += ' -manager: ' + cbb.manager
	# cmd += ' -port: '+ str(cbb.port)
	# cmd += ' -netmask: ' + '255.255.0.0'
	if cbb.group != '':
		cmd += ' -group:"' + cbb.group + '"'
	if cbb.job_details != '':
		cmd += ' -description:"' + cbb.job_details + '"'
	cmd += ' -priority:' + str(cbb.priority)
	cmd += ' -timeout:' + str(cbb.timeout)
	if cbb.suspended:
		cmd += ' -suspended'
	cmd += ' -taskList:"' + task_list_file + '"'
	cmd += ' -taskName: 1'
	if cbb.use_custom_path:
		cmd += ' "' + cbb.blender_path + '"'
	else:
		cmd += ' "' + blender_path() + '"'
	# cmd += ' -submit: "'+ bpy.data.filepath + '"'
	if cbb.background_render:
		cmd += ' --background'
	cmd += ' "' + file_name + '"'
	cmd += ' --frame-start %tp2'
	cmd += ' --frame-end %tp3'
	cmd += ' --render-anim'
	
	return task_list_file, cmd



class Render_OT_Submit_To_Backburner(Operator):
	'''Submit the render to backburner'''
	bl_idname = "render.submit_to_backburner"
	bl_label = "Submit to Backburner"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(cls, ctx):
		return ctx.scene != None

	def submit(self, scene):
		self.report({'OPERATOR'},'Submitting...')

		task_list_file, cmd = create_cmd_command(scene)

		""" Try to Submit job to backburner """
		try:
			subprocess.check_output(cmd, shell=True)
			self.report({'OPERATOR'},'Job Submited to backburner manager')
		except:
			self.report({'WARNING'},'Backburner manager not found. Failed to submission.')
			
		""" Delete the Task list text file """
		os.remove(task_list_file)

		return {'FINISHED'}
	
	def execute(self, ctx):
		if bpy.context.blend_data.filepath != '':
			csbb = ctx.scene.backburner
			if csbb.blender_path == '':
				self.report({'ERROR'}, "Network path to Blender hasn't been set")
				return {'CANCELLED'}

			if csbb.path_backburner == '':
				self.report({'ERROR'}, "Path to Backburner cmdjob.exe hasn't been set")
				return {'CANCELLED'}

			self.submit(ctx.scene)

		else:
			self.report({'WARNING'},'Save File Befor Submit')
		return{"FINISHED"}



class Render_OT_Update_Job_Name(Operator):
	''' Autocreat Jobe name from Filename '''
	bl_idname = "render.update_job_name"
	bl_label = "Update Jon Name"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		blend_file_name = ctx.blend_data.filepath

		if blend_file_name != "":
			file_name = bpy.path.basename(blend_file_name)
			the_name = (file_name.split('.'))[0]
		else:
			the_name = "New Job"

		ctx.scene.backburner.job_name = the_name

		return{"FINISHED"}



def get_preset_file_path():
	''' Return the pathand file name of preset file '''
	preset_path = bpy.utils.user_resource('CONFIG') + '\\BsMax\\'
	
	''' Creat preset directory if not exist '''
	if not os.path.isdir(preset_path):
		os.mkdir(preset_path)
	file_name = 'Backburner.ini'

	''' if Backburner.ini file not exist create an empty one '''
	backburner_file = preset_path + file_name
	
	if not os.path.exists(backburner_file):
		if os.access(backburner_file, os.W_OK):
			file = open(backburner_file, 'w')
			file.write('')
			file.close()
	
	return preset_path, file_name



class Render_OT_Save_BackBurner(Operator):
	""" Save curent state of Backburner setting as python file """
	bl_idname = "render.save_backburner_preset"
	bl_label = "Save Backburner Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def create_script_text(self, ctx):
		backburner = ctx.scene.backburner
		text = 'import bpy\n'
		text += 'backburner = bpy.context.scene.backburner\n'
		text += 'backburner.timeout = ' + str(backburner.timeout) + '\n'
		text += 'backburner.priority = ' + str(backburner.priority) + '\n'
		text += 'backburner.suspended = ' + str(backburner.suspended) + '\n'
		text += 'backburner.frames_per_task = ' + str(backburner.frames_per_task) + '\n'
		text += 'backburner.manager = "' + backburner.manager + '"\n'
		text += 'backburner.port = ' + str(backburner.port) + '\n'
		text += 'backburner.group = "' + backburner.group + '"\n'
		text += 'backburner.background_render = ' + str(backburner.background_render) + '\n'
		text += 'backburner.use_custom_path = ' + str(backburner.use_custom_path) + '\n'
		text += 'backburner.blender_path = r"' + backburner.blender_path +'"'
		return text

	def execute(self, ctx):
		preset_path, file_name = get_preset_file_path()
		string = self.create_script_text(ctx)
		
		if not os.path.exists(preset_path):
			if os.access(preset_path, os.W_OK):
				os.mkdir(preset_path)

		preset_file = open(preset_path + file_name, "w")
		preset_file.write(string)
		preset_file.close()

		return{"FINISHED"}



class Render_OT_Load_BackBurner(Operator):
	""" Load and run Backburner.py file """
	bl_idname = "render.load_backburner_preset"
	bl_label = "Load Backburner Preset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		preset_path, file_name = get_preset_file_path()
		script = open(preset_path + file_name).read()
		exec(script)

		return{"FINISHED"}



def draw_backburner_panel(self, ctx):
	csbb = ctx.scene.backburner

	layout = self.layout
	row = layout.row()
	row.operator('render.submit_to_backburner', icon='RENDER_ANIMATION')
	row.operator('render.save_backburner_preset', text='', icon='ADD')
	row.operator('render.load_backburner_preset', text='', icon='RECOVER_LAST')
	layout.separator()
	
	row = layout.row()
	row.prop(csbb, 'job_name')
	row.operator('render.update_job_name',text='', icon='FILE_REFRESH')
	
	row = layout.row()
	row.prop(csbb, 'job_details')
	row.label(text='',icon='BLANK1')
	layout.separator()

	row = layout.row()
	row.prop(csbb, 'timeout')
	row.prop(csbb, 'priority')
	row.prop(csbb, 'suspended', text='', icon='EVENT_S')
	layout.separator()
	
	row = layout.row()
	row.prop(csbb, 'override_frame_range')
	row.prop(csbb, 'frames_per_task')
	
	row = layout.row()
	if csbb.override_frame_range == 'RANGE':
		row.prop(csbb, 'frame_start')
		row.prop(csbb, 'frame_end')
	elif csbb.override_frame_range == 'FRAMES':
		layout.prop(csbb, 'frames_bitarray', text='')
	
	layout.separator()
	row = layout.row()
	row.prop(csbb, 'manager')
	row.prop(csbb, 'port')
	row.prop(csbb, 'group')
	
	row = layout.row()
	row.prop(csbb, 'use_custom_path')
	row.prop(csbb, 'background_render')
	
	if csbb.use_custom_path:
		row = layout.row()
		row.prop(csbb, 'blender_path')



class Render_OT_Backburner(Operator):
	bl_idname = 'render.backburner'
	bl_label = 'Backburner'
	bl_options = {'REGISTER'}

	def draw(self,ctx):
		draw_backburner_panel(self, ctx)
	
	def execute(self,ctx):
		return{'FINISHED'}
	
	def invoke(self,ctx,event):
		return ctx.window_manager.invoke_props_dialog(self, width=500)



class RENDER_PT_Backburner(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'output'
	bl_label = 'Backburner'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		draw_backburner_panel(self, ctx)



def backburner_menu(self, ctx):
	self.layout.operator('render.backburner',
		text='Submit to Backburner', icon='NETWORK_DRIVE')



classes = [Backburner_Settings,
	Render_OT_Backburner,
	Render_OT_Save_BackBurner,
	Render_OT_Load_BackBurner,
	Render_OT_Submit_To_Backburner,
	Render_OT_Update_Job_Name,
	RENDER_PT_Backburner]

def register_backburner():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.Scene.backburner = PointerProperty(type=Backburner_Settings, name='Backburner Submission')
	bpy.types.TOPBAR_MT_render.prepend(backburner_menu)

def unregister_backburner():
	bpy.types.TOPBAR_MT_render.remove(backburner_menu)
	[bpy.utils.unregister_class(c) for c in classes]



""" This part will call if use as stand alone add-on """
def register():
	register_backburner()

def unregister():
	unregister_backburner()

if __name__ == "__main__":
	register_backburner()