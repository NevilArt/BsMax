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
# Update and Modified for Blender 2.8x by Nevil #

""" This file can be instaled as an stand alone add-on too """
bl_info = {
	"name": "BsMax-Backburner",
	"description": "Backburner for Blender 2.80 ~ 2.93",
	"author": "Matt Ebb | Blaize | Anthony Hunt | Spirou4D | Nevil",
	"version": (0, 2, 0, 2),
	"blender": (2, 80, 0),# to 3.0
	"location": "Properties/ Output/ Backbrner",
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	"category": "Render"
}

import bpy, os, subprocess, random
from bpy.props import PointerProperty, StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Panel, Operator, PropertyGroup

default_path_backburner = '"C:\\Program Files (x86)\\Autodesk\\Backburner\\cmdjob.exe"'
default_path_blender = bpy.app.binary_path


def string_to_integer_array(frames):
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

def check_start_frame(self, ctx):
	csbb = ctx.scene.backburner
	if csbb.frame_start > csbb.frame_end:
		csbb.frame_end = csbb.frame_start

def check_end_frame(self, ctx):
	csbb = ctx.scene.backburner
	if csbb.frame_end < csbb.frame_start:
		csbb.frame_start = csbb.frame_end

def filter_frames_bitarray(self, ctx):
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
	
	job_details: StringProperty(name='Description', maxlen=400, default='Description',
		description='Add aditional information to render task')
	
	frames_per_task: IntProperty(name='Frames per Task', 
		min=1, max=1000, soft_min=1, soft_max=64, default=1,
		description='Number of frames to give each render node')

	timeout: IntProperty(name='Timeout', description='Timeout per task',
		default=120, min=1, max=1000, soft_min=1, soft_max=64)

	priority: IntProperty(name='Priority', description='Priority of this job',
		min=1, max=1000, soft_min=1, soft_max=64, default=50)

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

	path_backburner: StringProperty(name='Backburner Path', description='Path to Backburner cmdjob.exe', 
		maxlen=400, subtype='FILE_PATH', default=default_path_backburner)

	path_blender: StringProperty(name='Blender Path', description='Path to blender.exe',
		maxlen=400, subtype='FILE_PATH', default=default_path_blender)
	
	options: BoolProperty (name='More Options', default=False)

	background_render: BoolProperty (name='Render in Background', default=True)
	
	submit_file: BoolProperty (name='Submit file to Manager', default=False)
	
	servers: StringProperty(name='Servers', maxlen=400, default='',
		description='Render this job only with the servers specified (semi-colon separated list - ignored if group is used)')

def task_fild(start, end):
	field = 'Frame_' + str(start)
	if start != end:
		field += '-' + str(end)
	field += '\t' + str(start) + '\t' + str(end) + '\n'
	return field

def create_task_list_file(scene, filename):
	backburner = scene.backburner
	mode = backburner.override_frame_range

	""" Create Task data """
	task, frames = '', []
	step = backburner.frames_per_task

	""" Create Frame list """
	if mode == 'FRAMES':
		frames = string_to_integer_array(backburner.frames_bitarray)
	else:
		start_frame = backburner.frame_start if mode == 'RANGE' else scene.frame_start
		end_frame = backburner.frame_end if mode == 'RANGE' else scene.frame_end
		for frame in range(start_frame, end_frame):
			frames.append(frame)
		
	if step == 1:
		""" Single frame per task """
		for frame in frames:
			task += task_fild(frame, frame)
	else:
		""" Multi frame per task """
		start = end = -1
		for frame in frames:
			if start == -1:
				start = end = frame
				continue

			if frame == end + 1:
				end = frame
			else:
				task += task_fild(start, end)
				start = end = frame

			if end - start >= step:
				task += task_fild(start, end)
				start = end = -1

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



class Render_OT_Submit_To_Backburner(Operator):
	'''Submit the render to backburner'''
	bl_idname = "render.submit_to_backburner"
	bl_label = "Submit to Backburner"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(cls, ctx):
		return ctx.scene != None

	def create_new_file_name(self, scene, file_name):
		random_id = random.randint(1000000,9999999)
		append_text = '_BACKBURNERTEMPFILE_' + str(random_id)
		return os.path.splitext(file_name)[0] + append_text + '.blend'
	
	def submit(self, scene):
		self.report({'OPERATOR'},'Submitting...')
		
		cbb = scene.backburner
		
		file_name = self.create_new_file_name(scene, bpy.data.filepath)
		bpy.ops.wm.save_as_mainfile(filepath=file_name, copy=True)
		task_list_file = create_task_list_file(scene, file_name)
	

		# cmdjob.exe -jobname "testJob" 
		# -description "job de test" 
		# -timeout 6000 
		# -manager "192.168.73.91" 
		# -port "3234" 
		# -logPath "Q:/PAUL/testMax2016" 
		# -tasklist "Q:/PAUL/testMax2016/taskFileScript.txt" 
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
		if cbb.job_details != '':
			cmd += ' -description:"' + cbb.job_details + '"'
		cmd += ' -priority:' + str(cbb.priority)
		cmd += ' -timeout:' + str(cbb.timeout)
		if cbb.suspended:
			cmd += ' -suspended'
		cmd += ' -taskList:"' + task_list_file + '"'
		cmd += ' -taskName: 1'
		cmd += ' "' + cbb.path_blender + '"'
		# cmd += ' -submit: "'+ bpy.data.filepath + '"'
		if cbb.background_render:
			cmd += ' --background'
		cmd += ' "' + file_name + '"'
		cmd += ' --frame-start %tp2'
		cmd += ' --frame-end %tp3'
		cmd += ' --render-anim'

		try:
			""" Try to Submit job to backburner """
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
			if csbb.path_blender == '':
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



class RENDER_PT_Backburner(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'output'
	bl_label = 'Backburner'
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, ctx):
		csbb = ctx.scene.backburner

		layout = self.layout
		layout.operator('render.submit_to_backburner', icon='RENDER_ANIMATION')
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
		layout.prop(csbb, 'options')
		if csbb.options:
			box = layout.box()
			col = box.column()
			col.prop(csbb, 'background_render')
			col = box.column()
			col.enabled = False
			col.prop(csbb, 'submit_file')
			col.separator()
			col.prop(csbb, 'servers')



classes = [Backburner_Settings, Render_OT_Submit_To_Backburner, Render_OT_Update_Job_Name, RENDER_PT_Backburner]

def register_backburner():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.Scene.backburner = PointerProperty(type=Backburner_Settings, name='Backburner Submission')

def unregister_backburner():
	[bpy.utils.unregister_class(c) for c in classes]



""" This part will call if use as stand alone add-on """
def register():
	register_backburner()

def unregister():
	unregister_backburner()

if __name__ == "__main__":
	register_backburner()