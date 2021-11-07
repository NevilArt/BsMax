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
from bpy.props import BoolProperty

class Object_OT_Snap_Setting(Operator):
	bl_idname = "object.snap_setting"
	bl_label = "Snap Setting"
	snap = ""

	def execute(self, ctx):
		t = ctx.scene.tool_settings
		# snap To (Poly)
		if self.snap == "Grid Points":
			t.snap_elements = {'INCREMENT'}
		elif self.snap == "Vertex":
			t.snap_elements = {'VERTEX'}
		elif self.snap == "Edge/Segment":
			t.snap_elements = {'EDGE'}
		elif self.snap == "Face":
			t.snap_elements = {'FACE'}
		elif self.snap == "Volume":
			t.snap_elements = {'VOLUME'}

		# snap To (UV)
		elif self.snap == "Vertex UV":
			t.snap_uv_element = 'VERTEX'
		elif self.snap == "Grid Points UV":
			t.snap_uv_element = 'INCREMENT'

		# snap The
		elif self.snap == "Active":
			t.snap_target = 'ACTIVE'
		elif self.snap == "Mediom":
			t.snap_target = 'MEDIAN'
		elif self.snap == "Center":
			t.snap_target = 'CENTER'
		elif self.snap == "Closest":
			t.snap_target = 'CLOSEST'

		# snap Setting
		elif self.snap == "Rotation":
			t.use_snap_align_rotation = not t.use_snap_align_rotation
		elif self.snap == "Peelobject":
			t.use_snap_peel_object = not t.use_snap_peel_object
		#update toolbar command neded
		return{"FINISHED"}

class Snap:
	def __init__(self,snap_elements,use_snap_translate,
					use_snap_rotate,use_snap_scale):
		self.snap_elements = snap_elements
		self.use_snap_translate = use_snap_translate
		self.use_snap_rotate = use_snap_rotate
		self.use_snap_scale = use_snap_scale
	def store(self,ctx):
		self.snap_elements = ctx.scene.tool_settings.snap_elements
	def restore(self,ctx):
		t = ctx.scene.tool_settings
		t.snap_elements = self.snap_elements
		t.use_snap_translate = self.use_snap_translate
		t.use_snap_rotate = self.use_snap_rotate
		t.use_snap_scale = self.use_snap_scale

class snap_setting:
	move = Snap({'INCREMENT'},True,False,False)
	rotate = Snap({'INCREMENT'},False,True,False)
	#scale = Snap(t.snap_elements,False,False,True)

class Object_OT_Snap_Toggle(Operator):
	bl_idname = "object.snap_toggle"
	bl_label = "Snap Toggle"
	auto: BoolProperty(default=False)
	def execute(self, ctx):
		t = ctx.scene.tool_settings
		if self.auto:
			if t.use_snap and t.use_snap_rotate:
				snap_setting.rotate.store(ctx)
				snap_setting.move.restore(ctx)
				t.use_snap_translate = True
				t.use_snap_rotate = False
		else:
			if t.use_snap_translate and t.use_snap:
				snap_setting.move.store(ctx)
				t.use_snap = False
				t.use_snap_translate = False
			else:
				t.use_snap = True
				snap_setting.move.restore(ctx)
				t.use_snap_translate = t.use_snap
		return{"FINISHED"}

class Object_OT_Angel_Snap(Operator):
	bl_idname = "object.angel_snap"
	bl_label = "Angel Snap"
	
	auto: BoolProperty(default=False)
	
	def execute(self, ctx):
		t = ctx.scene.tool_settings
		if self.auto:
			if t.use_snap:
				snap_setting.move.store(ctx)
				snap_setting.rotate.restore(ctx)
				t.use_snap_translate = False
				t.use_snap_rotate = True
		else:
			if t.use_snap_translate and t.use_snap:
				snap_setting.move.store(ctx)
				t.use_snap_translate = False

			if t.use_snap_rotate and t.use_snap:
				t.use_snap = False
				t.use_snap_rotate = False
			else:
				t.use_snap = True
				snap_setting.rotate.restore(ctx)
				t.use_snap_rotate = True
		return{"FINISHED"}

class Object_OT_Placment(Operator):
	bl_idname = "object.placment"
	bl_label = "placment"
	
	def execute(self, ctx):
		ctx.scene.tool_settings.use_snap = True
		ctx.scene.tool_settings.snap_elements = {'FACE'}
		ctx.scene.tool_settings.use_snap_align_rotation = True
		ctx.scene.tool_settings.use_snap_translate = True
		ctx.scene.tool_settings.use_snap_project = True
		bpy.ops.wm.tool_set_by_id(name='builtin.move')
		self.report({'OPERATOR'},'bpy.ops.object.placment()')
		return{"FINISHED"}

classes = [Object_OT_Snap_Setting,
	Object_OT_Snap_Toggle,
	Object_OT_Angel_Snap,
	Object_OT_Placment]

def register_snap():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_snap():
	for c in classes:
		bpy.utils.unregister_class(c)