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

class KeyData(Operator):
	Key_All = False
	Key_Available = True
	Key_Position = True
	Key_Rotation = True
	Key_Scale = True
	# Key_IKParams = False
	# Key_ObjParams = False
	# Key_CusAttributes = False
	# Key_Modifiers = False
	# Key_Materials = False
	# Key_Other = False

class BsMax_OT_SetKeyFilters(Operator):
	bl_idname="bsmax.setkeyfilters"
	bl_label="Set Key Filters"
	bl_description="Set Key Filter"
	bl_options={'REGISTER', 'UNDO'}
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
		KeyData.Key_All = self.Key_All
		KeyData.Key_Available = self.Key_Available
		KeyData.Key_Position = self.Key_Position
		KeyData.Key_Rotation = self.Key_Rotation
		KeyData.Key_Scale = self.Key_Scale
		# KeyData.Key_ObjParams = self.Key_ObjParams
		# KeyData.Key_CusAttributes = self.Key_CusAttributes
		# KeyData.Key_Modifiers = self.Key_Modifiers
		# KeyData.Key_Materials = self.Key_Materials
		# KeyData.Key_Other = self.Key_Other
		return {'FINISHED'}

	def invoke(self, ctx, event):
		self.Key_All = KeyData.Key_All
		self.Key_Available = KeyData.Key_Available
		self.Key_Position = KeyData.Key_Position
		self.Key_Rotation = KeyData.Key_Rotation
		self.Key_Scale = KeyData.Key_Scale
		# self.Key_ObjParams = KeyData.Key_ObjParams
		# self.Key_CusAttributes = KeyData.Key_CusAttributes
		# self.Key_Modifiers = KeyData.Key_Modifiers
		# self.Key_Materials = KeyData.Key_Materials
		# self.Key_Other = KeyData.Key_Other
		self.Cast = True
		return ctx.window_manager.invoke_props_dialog(self,width=140)

#obj.modifiers[0].keyframe_insert(data_path="thickness")

class BsMax_OT_AutoKeyModeToggle(Operator):
	bl_idname = "bsmax.autokeymodetoggle"
	bl_label = "Auto Key Mode Toggle"

	def execute(self, ctx):
		State = ctx.scene.tool_settings.use_keyframe_insert_auto
		ctx.scene.tool_settings.use_keyframe_insert_auto = not State
		# change dopesheet header color
		#DSSpace = ctx.preferences.themes['Default'].dopesheet_editor.space
		DSSpace = ctx.preferences.themes[0].dopesheet_editor.space
		if State:
			DSSpace.header = (0.2588, 0.2588, 0.2588, 1.0)
		else:
			DSSpace.header = (0.5, 0.0, 0.0, 1.0)
		return{"FINISHED"}

# Set key animation tool (K button)
def set_key(objs, key):
	for obj in objs:
		obj.keyframe_insert(data_path=key)

class BsMax_OT_SetKeys(Operator):
	bl_idname = "bsmax.setkeys"
	bl_label = "Set Keys"

	# @classmethod
	# def poll(self, ctx):
	# 	return len(ctx.selected_objects) > 0

	def execute(self, ctx):
		print("set key")
		print(ctx.mode)
		if ctx.mode in ['OBJECT', 'POSE']:
			#objs=ctx.selected_objects
			if KeyData.Key_All:
				bpy.ops.anim.keyframe_insert_menu(type='Location')
				bpy.ops.anim.keyframe_insert_menu(type='Rotation')
				bpy.ops.anim.keyframe_insert_menu(type='Scaling')
			else:
				if KeyData.Key_Available:
					try:
						bpy.ops.anim.keyframe_insert_menu(type='Available')
					except:
						pass
				if KeyData.Key_Position:
					bpy.ops.anim.keyframe_insert_menu(type='Location')
				if KeyData.Key_Rotation:
					bpy.ops.anim.keyframe_insert_menu(type='Rotation')
				if KeyData.Key_Scale:
					bpy.ops.anim.keyframe_insert_menu(type='Scaling')
				# if KeyData.Key_ObjParams:
				# 	print("Key object params on progress")
				# if KeyData.Key_CusAttributes:
				# 	print("Key object params on progress")
				# if KeyData.Key_Modifiers:
				# 	print("Key object params on progress")
				# if KeyData.Key_Materials:
				# 	print("Key object params on progress")
				# if KeyData.Key_Other:
				# 	print("Key object params on progress")
		#elif ctx.mode == 'POSE':
			# print("-->   pose")
			# #set_key(ctx.selected_bones,"scale")
			# #ctx.active_bone.keyframe_insert("Location")#, index=2)
			# ctx.active_bone.keyframe_insert("rotation_euler")#, index=2)
			# #(data_path, index=-1, frame=bpy.context.scene.frame_current, group="")
		return{"FINISHED"}

# Delete selected objects animation
class BsMax_OT_DeleteSelectedAnimation(Operator):
	bl_idname = "bsmax.deleteselectedanimation"
	bl_label = "Delete Selected Animation"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.animation_data_clear()
		return{"FINISHED"}

class BsMax_OT_SetFrame(Operator):
	bl_idname = "bsmax.setframe"
	bl_label = "Set Frame"
	frame: EnumProperty(name='Frame', default='Next',
		items =[('Next','Next',''),('Previous','Previous',''),
				('First','First',''),('Last','Last','')])
	@classmethod
	def poll(self, ctx):
		return ctx.area.type in {'VIEW_3D','TIMELINE','NLA_EDITOR','FCURVES'}
	def execute(self, ctx):
		scene = ctx.scene
		frame,first,last = scene.frame_current,scene.frame_start,scene.frame_end
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

class BsMax_OT_TimeLineRangeChange(Operator):
	bl_idname = "bsmax.settimelinerange"
	bl_label = "TimeLine Range Change"
	start = False
	mouse_x = 0
	mode: EnumProperty(name='Mode',default='Shift',
		items =[('Shift','Shift',''), ('First','First',''), ('End','End','')])
	def modal(self, ctx, event):
		if not self.start:
			self.start = True
			self.mouse_x = event.mouse_x
		if event.type == 'MOUSEMOVE':
			scene = ctx.scene
			frame_start = scene.frame_start
			frame_end = scene.frame_end
			frame_current = scene.frame_current
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

classes = [BsMax_OT_SetKeyFilters,
			BsMax_OT_AutoKeyModeToggle,
			BsMax_OT_SetKeys,
			BsMax_OT_DeleteSelectedAnimation,
			BsMax_OT_SetFrame,
			BsMax_OT_TimeLineRangeChange]

def register_animationkey():
	[bpy.utils.register_class(c) for c in classes]

def unregister_animationkey():
	[bpy.utils.unregister_class(c) for c in classes]