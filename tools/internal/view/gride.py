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

from bsmax.mouse import get_view_orientation
from bsmax.gride import Local_Gride



local_gride = Local_Gride()
local_gride.set(2, 20, None)
local_gride.cross_on = True
local_gride.genarate_gride_lines()



class View3D_OT_Show_Hide_Gride(bpy.types.Operator):
	bl_idname = "view3d.show_hide_gride"
	bl_label = "Show Hide Gride"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def blender_gride(self, ctx, state):
		overlay = ctx.space_data.overlay
		overlay.show_floor = state
		overlay.show_ortho_grid = state
		overlay.show_axis_x = state
		overlay.show_axis_y = state
		overlay.show_axis_z = False
	
	def max_gride(self, ctx, stata):
		global local_gride
		if stata:
			local_gride.register(ctx)
		else:
			local_gride.unregister()

	def execute(self, ctx):
		bg = ctx.space_data.overlay.show_floor
		mg = local_gride.handler != None

		view_orientation, _ = get_view_orientation(ctx)
		if view_orientation == 'USER':
			# Prespactive/Camera
			if bg and not mg:
				self.blender_gride(ctx, False)
				self.max_gride(ctx, True)

			elif not bg and mg:
				self.blender_gride(ctx, False)
				self.max_gride(ctx, False)

			else:
				self.blender_gride(ctx, True)
				self.max_gride(ctx, False)
		
		else:
			# Flat views
			self.max_gride(ctx, False)
			self.blender_gride(ctx, not bg)

		return{"FINISHED"}



def register_gride():
	bpy.utils.register_class(View3D_OT_Show_Hide_Gride)



def unregister_gride():
	bpy.utils.unregister_class(View3D_OT_Show_Hide_Gride)



if __name__ == "__main__":
	register_gride()