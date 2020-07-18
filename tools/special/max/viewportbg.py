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
from bpy.types import Menu,Operator
from bpy.props import IntProperty

# Original code from Ozzkar Sep 2013
# Edit by Nevil July 2019

class View3D_OT_Background(Operator):
	bl_idname = "view3d.background"
	bl_label = "3D View Color"
	bl_description = "Cycle 3D view background colors"

	index: IntProperty(default = 1)

	def execute(self, ctx):
		grad = ctx.preferences.themes[0].view_3d.space.gradients
		show_grad = False

		if self.index == 1:
			#black
			grad.high_gradient[0] = 0.0
			grad.high_gradient[1] = 0.0
			grad.high_gradient[2] = 0.0
		elif self.index == 2:
			#7f7f7f - XSI
			grad.high_gradient[0] = 0.498
			grad.high_gradient[1] = 0.498
			grad.high_gradient[2] = 0.498
		elif self.index == 3:
			#a2a2a2 - maya light
			grad.high_gradient[0] = 0.635
			grad.high_gradient[1] = 0.635
			grad.high_gradient[2] = 0.635
		elif self.index == 4:
			#697b8f - maya gradient
			show_grad = True
			grad.gradient[0] = 0.0
			grad.gradient[1] = 0.0
			grad.gradient[2] = 0.0
			grad.high_gradient[0] = 0.412
			grad.high_gradient[1] = 0.482
			grad.high_gradient[2] = 0.561
		elif self.index == 5:
			#dark blue gradient
			show_grad = True
			grad.gradient[0] = 0.251
			grad.gradient[1] = 0.251
			grad.gradient[2] = 0.251
			grad.high_gradient[0] = 0.267
			grad.high_gradient[1] = 0.302
			grad.high_gradient[2] = 0.341
		else:
			#4b4b4b
			grad.high_gradient[0] = 0.294
			grad.high_gradient[1] = 0.294
			grad.high_gradient[2] = 0.294

		if bpy.app.version[1] <= 82:
			grad.show_grad = show_grad
		else:
			grad_type = 'LINEAR' if show_grad else 'SINGLE_COLOR'
			ctx.preferences.themes['Default'].view_3d.space.gradients.background_type = grad_type

		if self.index == 5:
			self.index = 0
		else:
			self.index += 1
		return {'FINISHED'}

# selection menu
class BMAX_PickViewportBackground_MT(Menu):
	bl_label = "Viewport Background"
	bl_description = "3D viewport background color"
	
	def draw(self, ctx):
		ui = self.layout
		vbg = "view3d.background"
		ui.operator(vbg, text="Elsyiun").index = 0
		ui.operator(vbg, text="Black").index = 1
		ui.operator(vbg, text="XSI").index = 2
		ui.operator(vbg, text="Maya Light").index = 3
		ui.operator(vbg, text="Maya Gradient").index = 4
		ui.operator(vbg, text="Grey Blue Gradient").index = 5

def register_viewportbg():
	bpy.utils.register_class(View3D_OT_Background)

def unregister_viewportbg():
	bpy.utils.unregister_class(View3D_OT_Background)