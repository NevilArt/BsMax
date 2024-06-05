
############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


class ANIM_OT_Channels_Click_Plus(Operator):
	bl_idname = "anim.channels_click_plus"
	bl_label = "Mouse Click on Channel (Auto)"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	extend: BoolProperty(default=False) # type: ignore
	extend_range: BoolProperty(default=False) # type: ignore
	children_only: BoolProperty(default=False) # type: ignore

	@classmethod
	def poll(self, ctx):
		return True
	
	def execute(self, ctx):
		bpy.ops.anim.channels_click(
			'INVOKE_DEFAULT',
			extend=self.extend,
			extend_range=self.extend_range,
			children_only=self.children_only
		)
		if bpy.ops.graph.hide.poll():
			bpy.ops.graph.hide(unselected=True)
		return{'FINISHED'}


classes = {
    ANIM_OT_Channels_Click_Plus
}


def register_selection():
	for cls in classes:
		register_class(cls)


def unregister_selection():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_selection()