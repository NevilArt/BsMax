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

class BsMax_OT_FreezeSelected(Operator):
	bl_idname = "bsmax.freezeselectedobjects"
	bl_label = "Freeze Objects"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.hide_select = True
		return{"FINISHED"}

class BsMax_OT_UnFreezeAll(Operator):
	bl_idname = "bsmax.unfreezeallobjects"
	bl_label = "Freeze Objects"
	def execute(self, ctx):
		for obj in bpy.data.objects:
			obj.hide_select = False
		return{"FINISHED"}

classes = [BsMax_OT_FreezeSelected, BsMax_OT_UnFreezeAll]

def register_freeze():
	[bpy.utils.register_class(c) for c in classes]

def unregister_freeze():
	[bpy.utils.unregister_class(c) for c in classes]