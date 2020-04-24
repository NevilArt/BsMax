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
from mathutils import Matrix
from bsmax.actions import set_create_target, set_as_active_object, delete_objects
from bsmax.state import has_constraint

class BsMax_OT_MakeTargetLight(Operator):
	bl_idname = "bsmax.maketargetlight"
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
		return {'FINISHED'}

class BsMax_OT_MakeFreeLight(Operator):
	bl_idname = "bsmax.makefreelight"
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
		return {'FINISHED'}

classes = [BsMax_OT_MakeTargetLight,BsMax_OT_MakeFreeLight]

def register_targetlight():
	[bpy.utils.register_class(c) for c in classes]

def unregister_targetlight():
	[bpy.utils.unregister_class(c) for c in classes]