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

import bpy, os, subprocess
from subprocess import Popen, PIPE
from bpy.props import PointerProperty, StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import AddonPreferences, Panel, Operator, PropertyGroup
from bsmax.math import BitArray

default_path_backburner = '"C:\\Program Files (x86)\\Autodesk\\Backburner\\cmdjob.exe"'
default_path_blender = bpy.app.binary_path


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

	override_frame_range: EnumProperty(name='Frames', description='Override Render frames Range', 
		default='ACTIVE', items=[('ACTIVE','Active Time',''),('RANGE','Range',''),('FRAMES','Specific Frames','')])

	frame_start: IntProperty(name='Start Frame', description='Start frame of animation sequence to render', 
		min=1, max=50000, soft_min=1, soft_max=64, default=1)

	frame_end: IntProperty(name='End Frame', description='End frame of animation sequence to render',
		min=1, max=50000, soft_min=1, soft_max=64, default=250)
	
	frames_bitarray: StringProperty(name='Frames', maxlen=400, default='1,3,5-7',
		description='Custom frames')

	manager: StringProperty(name='Manager', maxlen=400, default='localhost',
		description='Name of render manager')

	servers: StringProperty(name='Servers', maxlen=400, default='',
		description='Render this job only with the servers specified (semi-colon separated list - ignored if group is used)')
		
	path_backburner: StringProperty(name='Backburner Path', description='Path to Backburner cmdjob.exe', 
		maxlen=400, subtype='FILE_PATH', default=default_path_backburner)

	path_blender: StringProperty(name='Blender Path', description='Path to blender.exe',
		maxlen=400, subtype='FILE_PATH', default=default_path_blender)



def write_tasklist(scene, filename):
	backburner = scene.backburner
	mode = backburner.override_frame_range

	""" Create Task data """
	task = ''

	if mode == 'FRAMES':
		frames = BitArray()
		frames.set(backburner.frames_bitarray)
		for f in frames.get():
			str_f = str(f)
			task += 'Frame_' + str_f
			task += '\t' + str_f
			task += '\t' + str_f + '\n'
	else:
		step = backburner.frames_per_task
		start_frame = backburner.frame_start if mode == 'RANGE' else scene.frame_start
		end_frame = backburner.frame_end if mode == 'RANGE' else scene.frame_end
		curent_frame = start_frame
		while(curent_frame <= end_frame):
			seq_start = curent_frame
			seq_end = curent_frame + (step-1)
			if seq_end > end_frame:
				seq_end = end_frame
			curent_frame = seq_end + 1

			task += 'Frame_' + str(seq_start)
			if seq_start != seq_end:
				task += ' - ' + str(seq_end)
			task += '\t' + str(seq_start)
			task += '\t' + str(seq_end) + '\n'

	""" Write task to file """
	dir = os.path.dirname(filename)
	if os.access(dir, os.W_OK):
		tasklist_path = os.path.join(dir,"submit_temp.txt")
		file = open(tasklist_path, 'w')
		file.write(task)
		file.close()
	return tasklist_path



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
		
		cbb = scene.backburner
		filename = bpy.data.filepath
		tasklist_path = write_tasklist(scene, filename)
	
		cmd = '' + cbb.path_backburner + ''
		cmd += ' -jobName:"' + cbb.job_name + '"'
		cmd += ' -manager ' + cbb.manager
		cmd += ' -description:"' + cbb.job_details + '"'
		cmd += ' -priority:' + str(cbb.priority)
		cmd += ' -timeout:' + str(cbb.timeout)
		cmd += ' -suspended'
		#cmd += ' -logPath:' + os.path.join(os.path.dirname(filename),'log')
		if cbb.servers != '':
			cmd += ' -servers:' + cbb.servers
		#cmd += ' -workPath:' + blenderdir
		cmd += ' -taskList:"' + tasklist_path + '"'
		cmd += ' -taskName: 1'
		cmd += ' "' + cbb.path_blender + '" --background '
		cmd += '"' + filename + '"'
		cmd += ' --frame-start %tp2 --frame-end %tp3 --render-anim'

		try:
			#subprocess.call(cmd)
			subprocess.check_output(cmd, shell=True)
			self.report({'OPERATOR'},'Job Submited to backburner manager')
		except:
			self.report({'WARNING'},'Backburner manager not found. Failed to submission.')
			
		os.remove(tasklist_path)
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
	bl_default_closed = True

	def draw(self, ctx):
		csbb = ctx.scene.backburner

		layout = self.layout
		layout.operator('render.submit_to_backburner', icon='RENDER_ANIMATION')
		layout.separator()
		
		row = layout.row()
		row.prop(csbb, 'job_name')
		row.operator('render.update_job_name',text='', icon='FILE_REFRESH')
		layout.prop(csbb, 'job_details')
		layout.separator()

		row = layout.row()
		row.prop(csbb, 'timeout')
		row.prop(csbb, 'priority')
		layout.separator()
		layout.prop(csbb, 'override_frame_range')
		row = layout.row()
		# row.enabled = csbb.override_frame_range
		if csbb.override_frame_range == 'RANGE':
			row.prop(csbb, 'frame_start')
			row.prop(csbb, 'frame_end')
		elif csbb.override_frame_range == 'FRAMES':
			layout.prop(csbb, 'frames_bitarray', text='')
		
		if csbb.override_frame_range != 'FRAMES':
			layout.prop(csbb, 'frames_per_task')
		layout.separator()
		layout.prop(csbb, 'manager')
		layout.prop(csbb, 'servers')



classes = [Backburner_Settings, Render_OT_Submit_To_Backburner, Render_OT_Update_Job_Name, RENDER_PT_Backburner]

def register_backburner():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.Scene.backburner = PointerProperty(type=Backburner_Settings, name='Backburner Submission')

def unregister_backburner():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_backburner()