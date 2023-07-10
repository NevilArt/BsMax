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
from bpy.props import EnumProperty

from bsmax.actions import set_create_target, set_as_active_object
from bsmax.state import has_constraint



class Light_OT_Create_Target(Operator):
	bl_idname = 'light.create_target'
	bl_label = 'Make Target Light'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.active_object:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and not has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		light = ctx.active_object
		set_create_target(light, None)
		set_as_active_object(ctx, light)
		return {'FINISHED'}



class Light_OT_Clear_Target(Operator):
	bl_idname = 'light.clear_target'
	bl_label = 'Make Free Light'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.active_object:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		obj = ctx.active_object
		transfoem = obj.matrix_world.copy()
		targ = obj.constraints['Track To'].target
		bpy.ops.object.delete({'selected_objects': [targ]})
		TrackToConts = [ c for c in obj.constraints if c.type == 'TRACK_TO' ]

		for c in TrackToConts:
			obj.constraints.remove(c)

		obj.matrix_world = transfoem
		return {'FINISHED'}



class Light_OT_Set_Type(Operator):
	bl_idname = 'light.set_type'
	bl_label = 'Set Type'
	bl_options = {'REGISTER', 'UNDO'}

	mode: EnumProperty(name='Mode', default='POINT',
		items=[('POINT', 'Point',''), ('SUN', 'Sun',''), ('SPOT','Spot',''), ('AREA','Area','')])

	@classmethod
	def poll(self, ctx):
		if ctx.active_object:
			return ctx.active_object.type == 'LIGHT'
		return False

	def execute(self, ctx):
		ctx.object.data.type = self.mode
		return {'FINISHED'}



class Light_OT_Setting(Operator):
	bl_idname = 'light.setting'
	bl_label = 'Light Setting'
	bl_options = {'REGISTER', 'UNDO'}

	name: EnumProperty(name='Name', default='SHADOW',
		items=[('SHADOW', 'Shadow','')])

	@classmethod
	def poll(self, ctx):
		if ctx.active_object:
			return ctx.active_object.type == 'LIGHT'
		return False

	def execute(self, ctx):
		if self.name == 'SHADOW':
			ctx.object.data.use_shadow = not ctx.object.data.use_shadow
		return {'FINISHED'}



classes = (
	Light_OT_Create_Target,
	Light_OT_Clear_Target,
	Light_OT_Set_Type,
	Light_OT_Setting
)



def register_target_light():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_target_light():
	for c in classes:
		bpy.utils.unregister_class(c)