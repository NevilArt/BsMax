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

import bpy, mathutils
from bpy.types import Operator
# from mathutils import Matrix
from bsmax.actions import set_create_target, set_as_active_object, delete_objects
from bsmax.state import has_constraint

class Light_OT_Create_Target(Operator):
	bl_idname = "light.create_target"
	bl_label = "Make Target Light"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and not has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		light = ctx.active_object
		set_create_target(light, None)
		set_as_active_object(ctx, light)
		self.report({'INFO'},'bpy.ops.light.create_target()')
		return {'FINISHED'}

class Light_OT_Clear_Target(Operator):
	bl_idname = "light.clear_target"
	bl_label = "Make Free Light"

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			if obj.type == 'LIGHT' and has_constraint(obj, 'TRACK_TO'):
				return True
		return False

	def execute(self, ctx):
		obj = ctx.active_object
		transfoem = obj.matrix_world.copy()
		targ = obj.constraints["Track To"].target
		delete_objects([targ])
		TrackToConts = [ c for c in obj.constraints if c.type == 'TRACK_TO' ]
		for c in TrackToConts:
			obj.constraints.remove(c)
		obj.matrix_world = transfoem
		self.report({'INFO'},'bpy.ops.light.clear_target()')
		return {'FINISHED'}

classes = [Light_OT_Create_Target,Light_OT_Clear_Target]

def register_targetlight():
	[bpy.utils.register_class(c) for c in classes]

def unregister_targetlight():
	[bpy.utils.unregister_class(c) for c in classes]