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
from bpy.props import BoolProperty, FloatProperty



class Particle_OT_Hair_Select(Operator):
	bl_idname = 'particle.hair_select'
	bl_label = 'Hair Select (L.R.)'
	bl_options = {'REGISTER', 'UNDO'}

	left: BoolProperty(name="Left +x", default=False)
	right: BoolProperty(name="Right -x", default=False)
	center: BoolProperty(name="Center", default=False)
	tolerance: FloatProperty(name="Tolerance", default=0.001, min=0)
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'PARTICLE'
		return False
	
	def draw(self,ctx):
		layout = self.layout
		row = layout.row()
		row.prop(self, 'left')
		row.prop(self, 'right')
		row = layout.row()
		row.prop(self, 'center')
		if self.center:
			row.prop(self, 'tolerance')

	def execute(self,ctx):
		particles = ctx.active_object.particle_systems.active.particles
		for particle in particles:
			print( particle.location.x )
			# need to find python API for select hair particle via script
		return{"FINISHED"}
	
	def invoke(self,ctx,event):
		return ctx.window_manager.invoke_props_dialog(self)



def register_hair_symmetry():
	bpy.utils.register_class(Particle_OT_Hair_Select)



def unregister_hair_symmetry():
	bpy.utils.unregister_class(Particle_OT_Hair_Select)



if __name__ =="__main__":
	register_hair_symmetry()