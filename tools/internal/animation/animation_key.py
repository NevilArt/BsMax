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

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import BoolProperty, EnumProperty, IntProperty, PointerProperty


class KeyData:
	def __init__(self):
		self.available = True
		self.location = True
		self.rotation = True
		self.scale = False
		self.visual_location = False
		self.visual_rotation = False
		self.visual_scale = False
		self.bbone_shape = False
		self.whole_character = False
		self.whole_character_selected = False

key_data = KeyData()



class Anim_State:
	def __init__(self):
		self.lock_on_panel = False

anim_state = Anim_State()



class Anim_OT_Set_Key_Filters(Operator):
	bl_idname = 'anim.set_key_filters'
	bl_label = 'Set Key Filters'
	bl_description = 'Set Key Filter'

	available: BoolProperty(name='Avalable')
	location: BoolProperty(name='Location')
	rotation: BoolProperty(name='Rotation')
	scale: BoolProperty(name='Scale')
	visual_location: BoolProperty(name='Visual Location')
	visual_rotation: BoolProperty(name='Visual Rotation')
	visual_scale: BoolProperty(name='Viasual Scale')
	bbone_shape: BoolProperty(name='BBone Shape')
	whole_character: BoolProperty(name='Whole Character')
	whole_character_selected: BoolProperty(name='Whole Character (Selected only)')

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		box.prop(self, 'available')
		box.prop(self, 'location')
		box.prop(self, 'rotation')
		box.prop(self, 'scale')
		box = layout.box()
		box.prop(self, 'visual_location')
		box.prop(self, 'visual_rotation')
		box.prop(self, 'visual_scale')
		box = layout.box()
		box.prop(self, 'bbone_shape')
		box.prop(self, 'whole_character')
		box.prop(self, 'whole_character_selected')
		
	def set(self):
		global key_data
		key_data.available = self.available
		key_data.location = self.location
		key_data.rotation = self.rotation
		key_data.scale = self.scale
		key_data.visual_location = self.visual_location
		key_data.visual_rotation = self.visual_rotation
		key_data.visual_scale = self.visual_scale
		key_data.bbone_shape = self.bbone_shape
		key_data.whole_character = self.whole_character
		key_data.whole_character_selected = self.whole_character_selected
	
	def execute(self, ctx):
		self.set()
		return {'FINISHED'}
	
	def cancel(self, ctx):
		self.set()

	def invoke(self, ctx, event):
		global key_data
		self.available = key_data.available
		self.location = key_data.location
		self.rotation = key_data.rotation
		self.scale = key_data.scale
		self.visual_location = key_data.visual_location
		self.visual_rotation = key_data.visual_rotation
		self.visual_scale = key_data.visual_scale
		self.bbone_shape = key_data.bbone_shape
		self.whole_character = key_data.whole_character
		self.whole_character_selected = key_data.whole_character
		return ctx.window_manager.invoke_props_dialog(self,width=200)



class Anim_OT_Set_Key(Operator):
	""" Set keyframe on selected objects specific chanels """
	bl_idname = "anim.set_key"
	bl_label = "Set Keys"

	@classmethod
	def poll(self, ctx):
		return ctx.mode in ['OBJECT', 'POSE']

	def execute(self, ctx):
		global key_data

		if ctx.mode == 'POSE' and len(ctx.selected_pose_bones) == 0:
			return{'FINISHED'}

		if ctx.mode == 'OBJECT' and len(ctx.selected_objects) == 0:
			return{'FINISHED'}
		
		anim = bpy.ops.anim

		if key_data.available:
			try:
				anim.keyframe_insert_menu(type='Available')
			except:
				pass
		
		if key_data.location:
			anim.keyframe_insert_menu(type='Location')
		if key_data.rotation:
			anim.keyframe_insert_menu(type='Rotation')
		if key_data.scale:
			anim.keyframe_insert_menu(type='Scaling')
		
		if key_data.visual_location:
			anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLoc')
		if key_data.visual_rotation:
			anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualRot')
		if key_data.visual_scale:
			anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualScaling')

		if key_data.bbone_shape:
			anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualScaling')
		if key_data.whole_character:
			anim.keyframe_insert_menu(type='WholeCharacter')
		if key_data.whole_character_selected:
			anim.keyframe_insert_menu(type='WholeCharacterSelected')

		return{'FINISHED'}



class Anim_OT_Frame_Set(Operator):
	""" Set time slider curent time value """
	bl_idname = 'anim.frame_set'
	bl_label = 'Set Frame'

	frame: EnumProperty(name='Frame', default='Next',
						items =[('Next', 'Next', ''),
								('Previous', 'Previous', ''),
								('First', 'First', ''),
								('Last', 'Last', '')])
	
	def execute(self, ctx):
		scene = ctx.scene
		current = scene.frame_current
		first, last = scene.frame_start, scene.frame_end

		if self.frame == 'Next':
			current += 1
			current = first if current > last else current

		elif self.frame == 'Previous':
			current -= 1
			current = last if current < first else current

		elif self.frame == 'First':
			current = first

		else:
			current = last

		scene.frame_current = current
		return{'FINISHED'}



class Dopesheet_OT_Zoom_Extended(Operator):
	""" Zoom on selected or all keys """
	bl_idname = 'action.zoom_extended'
	bl_label = 'Zoom Extended'

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'DOPESHEET_EDITOR'

	def execute(self, ctx):
		bpy.ops.action.view_selected('INVOKE_DEFAULT')
		# bpy.ops.action.view_all('INVOKE_DEFAULT')
		return{'FINISHED'}



class Anim_OT_Delete_Key(Operator):
	""" Delete key withotu permisions """
	bl_idname = 'anim.delete_key'
	bl_label = 'Delete Key'
	bl_options={'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type in {'DOPESHEET_EDITOR', 'GRAPH_EDITOR'}

	def execute(self, ctx):
		if ctx.area.type == 'DOPESHEET_EDITOR':
			bpy.ops.action.delete()

		elif ctx.area.type == 'GRAPH_EDITOR':
			bpy.ops.graph.delete()

		return{'FINISHED'}



def update_freeze_on(self, ctx):
	""" Get from calculate fields """
	self.frames = self.relase - self.push
	self.next_step = self.next_push - self.push + 1
	self.repeat = (self.end - self.push) / self.next_step

class Freeze_on_Property(PropertyGroup):
	""" Data method """
	frames: IntProperty(name='Fix', min=0, default=1,
		description='Number of frames object has to fixed')
	
	next_step: IntProperty(name='Cycle', min=0, default=1,
		description='Length of walk/run cycle')
	
	repeat: IntProperty(name='Repeat', min=1, default=1,
		description='Repeat same action for next steps')
	
	""" Key chanels """
	key_location: BoolProperty(name='Key Location', default= True,
		description='Set Key for Location')
	
	key_rotation: BoolProperty(name='Key Rotation', default= True,
		description='Set key for Rotation')
	
	key_scale: BoolProperty(name='Key Scale', default= False,
		description='Set key for Scale')
	
	""" Calculator """
	calculator: BoolProperty(name='Calculator', default= False)
	
	push: IntProperty(name='Frame that first time foot touch the floor',
		min=0, default=1, update=update_freeze_on)
	
	relase: IntProperty(name='Frame that foot untouch floor',
		min=0, default=1, update=update_freeze_on)

	next_push: IntProperty(name='Second time foot touch floor',
		min=0, default=1, update=update_freeze_on)
	
	end: IntProperty(name='End of Walk/Run cycle',
		min=0, default=1, update=update_freeze_on)

	""" Simple """
	more: BoolProperty(name='More Option', default= False)
	panel: BoolProperty(name='On Panel', default= False)

def draw_freeze_on_panel(self, ctx):
	layout = self.layout
	freeze_on = ctx.scene.freeze_on

	box = layout.box()
	box.enabled = not freeze_on.calculator # disable if calc is on
	
	row = box.row()
	row.label(text='Fix position')
	row.prop(freeze_on, 'more', icon='HAND')
	row.prop(freeze_on, 'panel', icon='NODE_SEL')
	
	row = box.row()
	row = box.row(align=True)
	row.prop(freeze_on, 'frames', icon='TEMP')

	if freeze_on.more:
		row.prop(freeze_on, 'next_step', icon='TRACKING_FORWARDS_SINGLE')
		row.prop(freeze_on, 'repeat', icon='FILE_REFRESH')

		box = layout.box()
		box.label(text='Set Key For')
		row = box.row(align=True)
		row.prop(freeze_on, 'key_location', text='Location', icon='BLANK1')
		row.prop(freeze_on, 'key_rotation', text='Rotation', icon='BLANK1')
		row.prop(freeze_on, 'key_scale', text='Scale',icon='BLANK1')

		box = layout.box()
		box.prop(freeze_on, 'calculator', icon='ALIGN_TOP')
		if freeze_on.calculator:
			box.prop(freeze_on, 'push', icon='TEMP')
			box.prop(freeze_on, 'relase', icon='TEMP')
			box.prop(freeze_on, 'next_push', icon='TEMP')
			box.prop(freeze_on, 'end', icon='TEMP')
	else:
		freeze_on.next_step = 1
		freeze_on.repeat = 1


def appy_freeze_on(ctx):
	pass


class Anim_OT_Freeze_on(Operator):
	bl_idname = 'anim.freeze_on'
	bl_label = 'Freeze On'
	bl_options={'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def draw(self, ctx):
		draw_freeze_on_panel(self, ctx)	
	
	def check(self, ctx):
		global anim_state
		anim_state.lock_on_panel = self.panel
	
	def insert_key_for_current_state(self,ctx,  chanel, frame):
		# get info from scene
		freeze_on = ctx.scene.freeze_on

		# Set key for Location and Scale always is same
		if freeze_on.key_location:
			chanel.keyframe_insert(data_path='location', frame=frame)

		if freeze_on.key_scale:
			chanel.keyframe_insert(data_path='scale', frame=frame)

		# Sey key by rotation mode
		if freeze_on.key_rotation:
			if chanel.rotation_mode == 'QUATERNION':
				chanel.keyframe_insert(data_path='rotation_quaternion', frame=frame)

			elif chanel.rotation_mode == 'AXIS_ANGLE':
				chanel.keyframe_insert(data_path='rotation_axis_angle', frame=frame)

			else:
				chanel.keyframe_insert(data_path='rotation_euler', frame=frame)

	def fix_object_in_location(self, ctx, frame_current):
		# get info from scene
		freeze_on = ctx.scene.freeze_on

		# at each frame return object to first position and set key
		for obj in ctx.selected_objects:
			worldlocation = obj.matrix_world
			for frame in range(frame_current, frame_current + freeze_on.frames):
				obj.matrix_world = worldlocation
				self.insert_key_for_current_state(ctx, obj, frame)
		
	def fix_bone_in_location(self, ctx, frame_current):
		# get info from scene
		fop = ctx.scene.freeze_on

		# at each frame return bone to first position and set key
		armature = ctx.active_object
		for bone in ctx.selected_pose_bones:
			# Conver Pose bone space to world space
			bone_matrix = armature.convert_space(pose_bone=bone,
				matrix=bone.matrix, from_space='POSE', to_space='WORLD')

			for frame in range(frame_current, frame_current + fop.frames):
				ctx.scene.frame_current = frame
				ctx.view_layer.update()
				# Convert World to pose bone space
				bone.matrix = armature.convert_space(pose_bone=bone,
					matrix=bone_matrix, from_space='WORLD', to_space='POSE')
				self.insert_key_for_current_state(bone, frame)

	def execute(self, ctx):
		# get info from scene
		fop = ctx.scene.freeze_on
		
		# Store current time
		start_time = ctx.scene.frame_current
		
		# start frame already asked from user if calculator is on
		if fop.calculator:
			ctx.scene.frame_current = fop.push
			ctx.view_layer.update()

		# Repeat for each foot step
		for _ in range(fop.repeat):
		
			if ctx.mode == 'OBJECT':
				self.fix_object_in_location(ctx, ctx.scene.frame_current)

			if ctx.mode == "POSE":
				self.fix_bone_in_location(ctx, ctx.scene.frame_current)

			# jump to frame the next foot step begon most be equal of cycle length
			ctx.scene.frame_current += fop.next_step - fop.frames
			ctx.view_layer.update()
		
		# restore to begining time
		ctx.scene.frame_current = start_time
		return{'FINISHED'}
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)



class Anim_OP_Selection_Set(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Freeze on'
	bl_idname = 'VIEW3D_PT_anim_Lock_on'
	bl_category = 'Tool'

	@classmethod
	def poll(self, ctx):
		global anim_state
		return anim_state.lock_on_panel
	
	def draw(self, ctx):
		layout = self.layout
		layout.label(text='TEST')



class Anim_OP_Freeze_on(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Freeze On'
	bl_idname = 'VIEW3D_PT_freeze_on'
	bl_category = 'Tool'

	@classmethod
	def poll(self, ctx):
		return ctx.scene.freeze_on.panel
	
	def draw(self, ctx):
		self.layout.operator_context = 'EXEC_DEFAULT'
		self.layout.operator('anim.freeze_on', text='Apply')
		draw_freeze_on_panel(self, ctx)


# class Graph_Editor_OT_Hide(Operator):
# 		graph.select_linked



classes = [ Freeze_on_Property,
			Anim_OT_Set_Key_Filters,
			Anim_OT_Set_Key,
			Anim_OT_Frame_Set,
			Anim_OT_Delete_Key,
			Anim_OT_Freeze_on,
			Anim_OP_Freeze_on,
			Anim_OP_Selection_Set,
			Dopesheet_OT_Zoom_Extended
		]

def register_animation_key():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.Scene.freeze_on = PointerProperty(type=Freeze_on_Property,
												name='Freeze On')

def unregister_animation_key():
	del bpy.types.Scene.freeze_on

	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_animation_key()
