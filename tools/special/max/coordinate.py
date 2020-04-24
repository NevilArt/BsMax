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
from bpy.props import StringProperty

# Coordinate
class BsMax_OT_CoordSystem(Operator):
	bl_idname = "bsmax.coordinatesystem"
	bl_label = "Coordinate System"
	coordsys: bpy.props.StringProperty(default = 'GLOBAL')
	def execute(self, ctx):
		# NORMAL, GIMBAL, LOCAL, VIEW, GLOBAL, CURSOR
		ctx.window.scene.transform_orientation_slots[0].type = self.coordsys
		return{"FINISHED"}

class BsMax_OT_SetLocalCoordinPoseMode(Operator):
	bl_idname = "bsmax.setlocalcoordinposemode"
	bl_label = "Local (Pose)"
	def execute(self, ctx):
		ctx.window.scene.transform_orientation_slots[0].type = 'LOCAL'
		ctx.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
		return{"FINISHED"} 

classes = [BsMax_OT_CoordSystem, BsMax_OT_SetLocalCoordinPoseMode]

def register_coordinate():
	[bpy.utils.register_class(c) for c in classes]

def unregister_coordinate():
	[bpy.utils.unregister_class(c) for c in classes]