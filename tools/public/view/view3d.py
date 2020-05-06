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

class View3D_OT_perespectivetoggle(Operator):
	bl_idname = "view3d.perespective_toggle"
	bl_label = "Perespective Toggle"
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		r3d = ctx.area.spaces[0].region_3d
		if r3d.view_perspective == 'CAMERA':
			view_matrix = ctx.area.spaces.active.region_3d.view_matrix
			r3d.view_perspective = 'PERSP'
			ctx.area.spaces.active.region_3d.view_matrix = view_matrix
		elif r3d.view_perspective == 'PERSP':
			r3d.view_perspective = 'ORTHO'
		elif r3d.view_perspective == 'ORTHO':
			r3d.view_perspective = 'PERSP'
		return{"FINISHED"}

def register_view3d():
	bpy.utils.register_class(View3D_OT_perespectivetoggle)

def unregister_view3d():
	bpy.utils.unregister_class(View3D_OT_perespectivetoggle)