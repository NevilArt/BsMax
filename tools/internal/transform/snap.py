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
from bpy.types import Operator, Menu
from bpy.props import BoolProperty, EnumProperty



class Object_OT_Snap_Setting(Operator):
	bl_idname = "object.snap_setting"
	bl_label = "Snap Setting"

	mode : EnumProperty(
		name='Mode', default='INCREMENT',
		items=[
			('INCREMENT', 'Grid Points',''),
			('VERTEX', 'Vertex',''),
			('VOLUME','Volume',''),
			('EDGE','Edge/Segment',''),
			('FACE','Face',''),

			('CLOSEST','Closest',''),
			('CENTER','Center',''),
			('MEDIAN','Median',''),
			('ACTIVE','Active',''),

			('MOVE','Move',''),
			('ROTATE','Rotate',''),
			('SCALE','Scale','')
		]
		)

	def execute(self, ctx):
		tool_settings = ctx.scene.tool_settings
		# Snap ON
		if self.mode in {'INCREMENT', 'VERTEX', 'VOLUME', 'EDGE', 'FACE'}:
			tool_settings.snap_elements = {self.mode}

		# Snap To
		elif self.mode in {'CLOSEST', 'CENTER', 'MEDIAN', 'ACTIVE'}:
			tool_settings.snap_target = self.mode

		# Snap Toggle
		elif self.mode == "MOVE":
			tool_settings.use_snap_translate = not tool_settings.use_snap_translate
		elif self.mode == "ROTATE":
			tool_settings.use_snap_rotate = not tool_settings.use_snap_rotate
		elif self.mode == "SCALE":
			tool_settings.use_snap_scale = not tool_settings.use_snap_scale

		# elif self.snap == "Peelobject":
		# 	t.use_snap_peel_object = not t.use_snap_peel_object
		#update toolbar command neded
		return{"FINISHED"}



class Snap:
	def __init__(self, snap_elements, use_snap_translate,
					use_snap_rotate, use_snap_scale):

		self.snap_elements = snap_elements
		self.use_snap_translate = use_snap_translate
		self.use_snap_rotate = use_snap_rotate
		self.use_snap_scale = use_snap_scale

	def store(self, ctx):
		self.snap_elements = ctx.scene.tool_settings.snap_elements

	def restore(self, ctx):
		tool_settings = ctx.scene.tool_settings
		tool_settings.snap_elements = self.snap_elements
		tool_settings.use_snap_translate = self.use_snap_translate
		tool_settings.use_snap_rotate = self.use_snap_rotate
		tool_settings.use_snap_scale = self.use_snap_scale



class Snap_Setting:
	def __init__(self):
		self.move = Snap({'INCREMENT'}, True, False, False)
		self.rotate = Snap({'INCREMENT'}, False, True, False)
		# self.scale = Snap(t.snap_elements,False,False,True)

snap_setting = Snap_Setting()



class Object_OT_Snap_Toggle(Operator):
	bl_idname = "object.snap_toggle"
	bl_label = "Snap Toggle"
	auto: BoolProperty(default=False)

	def execute(self, ctx):
		global snap_setting
		tool_settings = ctx.scene.tool_settings
		if self.auto:
			if tool_settings.use_snap and tool_settings.use_snap_rotate:
				snap_setting.rotate.store(ctx)
				snap_setting.move.restore(ctx)
				tool_settings.use_snap_translate = True
				tool_settings.use_snap_rotate = False
		else:
			if tool_settings.use_snap_translate and tool_settings.use_snap:
				snap_setting.move.store(ctx)
				tool_settings.use_snap = False
				tool_settings.use_snap_translate = False
			else:
				tool_settings.use_snap = True
				snap_setting.move.restore(ctx)
				tool_settings.use_snap_translate = tool_settings.use_snap
		return{"FINISHED"}



class Object_OT_Angel_Snap(Operator):
	bl_idname = "object.angel_snap"
	bl_label = "Angel Snap"
	
	auto: BoolProperty(default=False)
	
	def execute(self, ctx):
		global snap_setting
		tool_settings = ctx.scene.tool_settings
		if self.auto:
			if tool_settings.use_snap:
				snap_setting.move.store(ctx)
				snap_setting.rotate.restore(ctx)
				tool_settings.use_snap_translate = False
				tool_settings.use_snap_rotate = True
		else:
			if tool_settings.use_snap_translate and tool_settings.use_snap:
				snap_setting.move.store(ctx)
				tool_settings.use_snap_translate = False

			if tool_settings.use_snap_rotate and tool_settings.use_snap:
				tool_settings.use_snap = False
				tool_settings.use_snap_rotate = False
			else:
				tool_settings.use_snap = True
				snap_setting.rotate.restore(ctx)
				tool_settings.use_snap_rotate = True
		return{"FINISHED"}



class Object_OT_Placment(Operator):
	bl_idname = "object.placment"
	bl_label = "placment"
	
	def execute(self, ctx):
		tool_settings = ctx.scene.tool_settings
		tool_settings.use_snap = True
		tool_settings.snap_elements = {'FACE'}
		tool_settings.use_snap_align_rotation = True
		tool_settings.use_snap_translate = True
		tool_settings.use_snap_project = True
		bpy.ops.wm.tool_set_by_id(name='builtin.move')
		return{"FINISHED"}



class OBJECT_MT_snap_setting(Menu):
	bl_idname = "OBJECT_MT_snap_setting"
	bl_label = "Snap Setting"

	def draw(self, ctx):
		layout=self.layout
		layout.popover(panel="VIEW3D_PT_snapping")



classes = (
	Object_OT_Snap_Setting,
	Object_OT_Snap_Toggle,
	Object_OT_Angel_Snap,
	Object_OT_Placment,
	OBJECT_MT_snap_setting
)



def register_snap():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_snap():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_snap()