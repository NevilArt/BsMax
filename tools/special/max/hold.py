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

class BsMax_OT_Hold(Operator):
		bl_idname = "bsmax.hold"
		bl_label = "Hold"
		def execute(self, ctx):
			print("Hold coming soon")
			return{"FINISHED"}

class BsMax_OT_Fetch(Operator):
		bl_idname = "bsmax.fetch"
		bl_label = "Fetch"
		def execute(self, ctx):
				print("Fetch coming soon")
				return{"FINISHED"}

classes = [BsMax_OT_Hold, BsMax_OT_Fetch]

def register_hold():
	[bpy.utils.register_class(c) for c in classes]

def unregister_hold():
	[bpy.utils.unregister_class(c) for c in classes]