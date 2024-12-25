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
# 2024/09/10

from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


# Coordinate
class Object_OT_Coord_System(Operator):
	bl_idname = 'object.coordinate_system'
	bl_label = "Coordinate System"
	coordsys: StringProperty(default = 'GLOBAL') # type: ignore

	def execute(self, ctx):
		# NORMAL, GIMBAL, LOCAL, VIEW, GLOBAL, CURSOR
		ctx.window.scene.transform_orientation_slots[0].type = self.coordsys
		return{'FINISHED'}


class Object_OT_Set_Local_Coord_in_Pose_Mode(Operator):
	bl_idname = 'object.set_local_coord_in_pose_mode'
	bl_label = "Local (Pose)"

	def execute(self, ctx):
		ctx.window.scene.transform_orientation_slots[0].type = 'LOCAL'
		ctx.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
		return{'FINISHED'}


classes = {
	Object_OT_Coord_System,
	Object_OT_Set_Local_Coord_in_Pose_Mode
}


def register_coordinate():
	for cls in classes:
		register_class(cls)


def unregister_coordinate():
	for cls in classes:
		unregister_class(cls)