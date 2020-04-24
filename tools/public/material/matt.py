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

class BsMax_OT_AssignToSelection(Operator):
	bl_idname = "material.assigntoselection"
	bl_label = "Assign to selected objects"
	bl_description = "Assign Material to selected objects"

	# @classmethod
	# def poll(self, ctx):
	# 	return len(ctx.selected_objects) > 1

	def execute(self, ctx):
		for o in ctx.selected_objects:
			pass
		print(ctx.area.type)
		print(ctx.space_data.type)
		return{"FINISHED"}

def matt_cls(register):
	classes = [BsMax_OT_AssignToSelection]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	matt_cls(True)

__all__ = ["matt_cls"]