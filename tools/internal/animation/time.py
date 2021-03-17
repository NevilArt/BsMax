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
from bpy.props import BoolProperty, EnumProperty



class Anim_OT_Set_TimeLine_Range(Operator):
	bl_idname = 'anim.set_timeline_range'
	bl_label = 'Set TimeLine Range'
	
	start = False
	mouse_x = 0
	mode: EnumProperty(name='Mode', default='Shift',
		items =[('Shift','Shift',''), ('First','First',''), ('End','End','')])
	
	def modal(self, ctx, event):
		if not self.start:
			self.start = True
			self.mouse_x = event.mouse_x
		if event.type == 'MOUSEMOVE':
			scene = ctx.scene
			frame_start,frame_end = scene.frame_start, scene.frame_end
			if self.start:
				scale = (frame_end - frame_start) / 100
				scale = 1 if scale < 1 else scale
				step = (event.mouse_x - self.mouse_x) / 10.0 * scale
				if self.mode == 'First':
					scene.frame_start -= step
					if frame_start == frame_end:
						scene.frame_start = frame_end - 1
				elif self.mode == 'End':
					scene.frame_end -= step
					if frame_end == frame_start:
						scene.frame_end = frame_start + 1
				else:
					step = 0 if frame_start - step < 0 else step
					scene.frame_start -= step
					scene.frame_end -= step
				if scene.frame_current < scene.frame_start:
					scene.frame_current = scene.frame_start
				if scene.frame_current > scene.frame_end:
					scene.frame_current = scene.frame_end
				self.mouse_x = event.mouse_x
				bpy.ops.action.view_all()
		if self.start and event.value == 'RELEASE':
			self.start = False
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}



class Anim_OT_Set_Current_time_as(Operator):
	bl_idname = 'anim.set_current_time_as'
	bl_label = 'Set Current time As'
	bl_options = {'REGISTER', 'INTERNAL'}

	set_as: EnumProperty(name='As', default='START', items =[('START','START Frame',''), ('END','End Frame','')])

	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.area.type in {'VIEW_3D'}

	def execute(self, ctx):
		scene = ctx.scene
		if self.set_as == 'START':
			scene.frame_start = scene.frame_current
		else:
			scene.frame_end = scene.frame_current
		return{"FINISHED"}



def time_context_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("anim.set_current_time_as",text="Set Current time As Start").set_as = 'START'
	layout.operator("anim.set_current_time_as",text="Set Current time As End").set_as = 'END'



classes = [Anim_OT_Set_TimeLine_Range,
	Anim_OT_Set_Current_time_as]

def register_time():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.DOPESHEET_MT_context_menu.append(time_context_menu)
	bpy.types.SEQUENCER_MT_context_menu.append(time_context_menu)

def unregister_time():
	bpy.types.DOPESHEET_MT_context_menu.remove(time_context_menu)
	bpy.types.SEQUENCER_MT_context_menu.remove(time_context_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_time()