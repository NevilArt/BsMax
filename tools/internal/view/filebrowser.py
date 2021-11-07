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



class BsMax_OT_ScaleIcons(Operator):
	bl_idname = "filebrowser.scaleicons"
	bl_label = "Scale Icons"
	up: bpy.props.BoolProperty(name="scaleup",default=True)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.ui_type == 'FILE_BROWSER'

	def execute(self, ctx):
		params = ctx.space_data.params
		ver = bpy.app.version
		old = ver[0] == 2 and ver[1] < 81
		small = 'LIST_SHORT' if old else 'LIST_VERTICAL'
		medium = 'LIST_LONG' if old else 'LIST_HORIZONTAL'
		large = 'THUMBNAIL'
		if self.up:
			if params.display_type == large:
				params.display_type = small
			elif params.display_type == medium:
				params.display_type = large
			elif params.display_type == small:
				params.display_type = medium
		else:
			if params.display_type == large:
				params.display_type = medium
			elif params.display_type == medium:
				params.display_type = small
			elif params.display_type == small:
				params.display_type = large
		return{"FINISHED"}



classes = [BsMax_OT_ScaleIcons]

def register_filebrowser():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_filebrowser():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_filebrowser()