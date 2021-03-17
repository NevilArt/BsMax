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



class KeyData:
	def __init__(self):
		self.Key_All = False
		self.Key_Available = True
		self.Key_Position = True
		self.Key_Rotation = True
		self.Key_Scale = True
		# self.Key_IKParams = False
		# self.Key_ObjParams = False
		# self.Key_CusAttributes = False
		# self.Key_Modifiers = False
		# self.Key_Materials = False
		# self.Key_Other = False
kd = KeyData()



class Anim_OT_Set_Key_Filters(Operator):
	bl_idname="anim.set_key_filters"
	bl_label="Set Key Filters"
	bl_description="Set Key Filter"

	Key_All: BoolProperty(name="All")
	Key_Available: BoolProperty(name="Available",default=True)
	Key_Position: BoolProperty(name="Position",default=True)
	Key_Rotation: BoolProperty(name="Rotation",default=True)
	Key_Scale: BoolProperty(name="Scale",default=True)
	# Key_IKParams: BoolProperty(name="IK Parameters")
	# Key_ObjParams: BoolProperty(name="Object Parameters")
	# Key_CusAttributes: BoolProperty(name="CUstom Attributes")
	# Key_Modifiers: BoolProperty(name="Modifiers")
	# Key_Materials: BoolProperty(name="Materials")
	# Key_Other: BoolProperty(name="Other")

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.prop(self, "Key_All")
		row.prop(self, "Key_Available")
		row.prop(self, "Key_Position")
		row.prop(self, "Key_Rotation")
		row.prop(self, "Key_Scale")
		# row.prop(self, "Key_ObjParams")
		# row.prop(self, "Key_CusAttributes")
		# row.prop(self, "Key_Modifiers")
		# row.prop(self, "Key_Materials")
		# row.prop(self, "Key_Other")
		
	def execute(self, ctx):
		kd.Key_All = self.Key_All
		kd.Key_Available = self.Key_Available
		kd.Key_Position = self.Key_Position
		kd.Key_Rotation = self.Key_Rotation
		kd.Key_Scale = self.Key_Scale
		# kd.Key_ObjParams = self.Key_ObjParams
		# kd.Key_CusAttributes = self.Key_CusAttributes
		# kd.Key_Modifiers = self.Key_Modifiers
		# kd.Key_Materials = self.Key_Materials
		# kd.Key_Other = self.Key_Other
		return {'FINISHED'}

	def invoke(self, ctx, event):
		self.Key_All = kd.Key_All
		self.Key_Available = kd.Key_Available
		self.Key_Position = kd.Key_Position
		self.Key_Rotation = kd.Key_Rotation
		self.Key_Scale = kd.Key_Scale
		# self.Key_ObjParams = kd.Key_ObjParams
		# self.Key_CusAttributes = kd.Key_CusAttributes
		# self.Key_Modifiers = kd.Key_Modifiers
		# self.Key_Materials = kd.Key_Materials
		# self.Key_Other = kd.Key_Other
		self.Cast = True
		return ctx.window_manager.invoke_props_dialog(self,width=140)

#obj.modifiers[0].keyframe_insert(data_path="thickness")



class Anim_OT_Auto_Key_Toggle(Operator):
	bl_idname = "anim.auto_key_toggle"
	bl_label = "Auto Key Toggle"

	def execute(self, ctx):
		state = ctx.scene.tool_settings.use_keyframe_insert_auto
		ctx.scene.tool_settings.use_keyframe_insert_auto = not state
		""" change dopesheet header color """
		dopesheet_space = ctx.preferences.themes[0].dopesheet_editor.space
		if state:
			dopesheet_space.header = (0.2588, 0.2588, 0.2588, 1.0)
		else:
			dopesheet_space.header = (0.5, 0.0, 0.0, 1.0)
		return{"FINISHED"}



# def set_key(objs, key):
# 	for obj in objs:
# 		obj.keyframe_insert(data_path=key)

class Anim_OT_Set_Key(Operator):
	bl_idname = "anim.set_key"
	bl_label = "Set Keys"

	# @classmethod
	# def poll(self, ctx):
	# 	return len(ctx.selected_objects) > 0

	def execute(self, ctx):
		if ctx.mode in ['OBJECT', 'POSE']:
			#objs=ctx.selected_objects
			if kd.Key_All:
				bpy.ops.anim.keyframe_insert_menu(type='Location')
				bpy.ops.anim.keyframe_insert_menu(type='Rotation')
				bpy.ops.anim.keyframe_insert_menu(type='Scaling')
			else:
				if kd.Key_Available:
					try:
						bpy.ops.anim.keyframe_insert_menu(type='Available')
					except:
						pass
				if kd.Key_Position:
					bpy.ops.anim.keyframe_insert_menu(type='Location')
				if kd.Key_Rotation:
					bpy.ops.anim.keyframe_insert_menu(type='Rotation')
				if kd.Key_Scale:
					bpy.ops.anim.keyframe_insert_menu(type='Scaling')
		self.report({'OPERATOR'},"bpy.ops.anim.set_key()")
		return{"FINISHED"}



# Delete selected objects animation
class Anim_OT_Delete_Selected_Animation(Operator):
	bl_idname = "anim.delete_selected_animation"
	bl_label = "Delete Selected Animation"
	bl_options={'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.animation_data_clear()
		self.report({'OPERATOR'},"bpy.ops.anim.delete_selected_animation()")
		return{"FINISHED"}



class Anim_OT_Frame_Set(Operator):
	bl_idname = "anim.frame_set"
	bl_label = "Set Frame"
	frame: EnumProperty(name='Frame', default='Next',
		items =[('Next','Next',''),('Previous','Previous',''),
				('First','First',''),('Last','Last','')])
	
	def execute(self, ctx):
		scene = ctx.scene
		frame, first, last = scene.frame_current, scene.frame_start, scene.frame_end
		if self.frame == 'Next':
			frame += 1
			frame = first if frame > last else frame
		elif self.frame == 'Previous':
			frame -= 1
			frame = last if frame < first else frame
		elif self.frame == 'First':
			frame = first
		else:
			frame = last
		ctx.scene.frame_current = frame
		return{"FINISHED"}



class Dopesheet_OT_Zoom_Extended(Operator):
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
	bl_idname = 'anim.delete_key'
	bl_label = 'Delete Key'
	bl_options={'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type in {'DOPESHEET_EDITOR','GRAPH_EDITOR'}

	def execute(self, ctx):
		if ctx.area.type == 'DOPESHEET_EDITOR':
			bpy.ops.action.delete()
		elif ctx.area.type == 'GRAPH_EDITOR':
			bpy.ops.graph.delete()
		return{'FINISHED'}

# class Graph_Editor_OT_Hide(Operator):
# 		graph.select_linked


classes = [Anim_OT_Set_Key_Filters,
			Anim_OT_Auto_Key_Toggle,
			Anim_OT_Set_Key,
			Anim_OT_Delete_Selected_Animation,
			Anim_OT_Frame_Set,
			Dopesheet_OT_Zoom_Extended,
			Anim_OT_Delete_Key]

def register_animation_key():
	[bpy.utils.register_class(c) for c in classes]

def unregister_animation_key():
	[bpy.utils.unregister_class(c) for c in classes]