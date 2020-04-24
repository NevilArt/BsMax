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
from bpy.props import BoolProperty

class BsMax_OT_ScaleIcons(Operator):
	bl_idname = "filebrowser.scaleicons"
	bl_label = "Scale Icons"
	up: BoolProperty(name="scaleup",default=True)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.ui_type == 'FILE_BROWSER'

	def execute(self, ctx):
		params = ctx.space_data.params
		if self.up:
			if params.display_type == 'THUMBNAIL':
				params.display_type = 'LIST_SHORT'
			elif params.display_type == 'LIST_LONG':
				params.display_type = 'THUMBNAIL'
			elif params.display_type == 'LIST_SHORT':
				params.display_type = 'LIST_LONG'
		else:
			if params.display_type == 'THUMBNAIL':
				params.display_type = 'LIST_LONG'
			elif params.display_type == 'LIST_LONG':
				params.display_type = 'LIST_SHORT'
			elif params.display_type == 'LIST_SHORT':
				params.display_type = 'THUMBNAIL'
		return{"FINISHED"}

def register_filebrowser():
	bpy.utils.register_class(BsMax_OT_ScaleIcons)

def unregister_filebrowser():
	bpy.utils.unregister_class(BsMax_OT_ScaleIcons)