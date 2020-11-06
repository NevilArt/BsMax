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
from mathutils import Vector, Matrix
from bsmax.math import point_on_curve
from bsmax.actions import set_origen
from bsmax.operator import PickOperator

class Particle_OT_Hair_Guides_From_Curve(PickOperator):
	bl_idname = 'particle.hair_guides_from_curve'
	bl_label = 'Hair Guides From Curve'
	bl_options = {'REGISTER', 'UNDO'}
	filters = ['CURVE']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode == 'OBJECT':
				if len(ctx.selected_objects) == 1:
					return ctx.object.type == 'MESH'
		return False
	
	def check_modifier(self, obj):
		has_particle = False
		for m in obj.modifiers:
			has_particle = m.type == 'PARTICLE_SYSTEM'
			if has_particle:
				break
		if has_particle:
			obj.particle_systems.active.particles.data.settings.type = 'HAIR'
		else:
			m = obj.modifiers.new(name='ParticleSettings', type='PARTICLE_SYSTEM')
			m.particle_system.particles.data.settings.type = 'HAIR'
	
	def get_max_lenght(self, obj):
		return max([spline.calc_length() for spline in obj.data.splines])
	
	def comb_the_hair(self, hair, curve, index):
		count = len(hair.hair_keys)
		for i in range(0, count):
			percent = i / (count - 1)
			#TODO_01 this coordinate has to fixed by difrent of two objects cordinate
			coord = point_on_curve(curve, index, percent)
			hair.hair_keys[i].co = coord

	def picked(self, ctx, source, subsource, target, subtarget):
		obj = source[0]
		
		""" Set Curve pivot same as Object """
		#TODO temprary solution for fix this read the #TODO_01
		set_origen(ctx, target, source[0].location)
		bpy.ops.object.select_all(action='DESELECT')
		source[0].select_set(state = True)
		ctx.view_layer.objects.active = source[0]

		""" Make ready for working on """
		self.check_modifier(obj)
		bpy.ops.particle.edited_clear()
		
		""" Collect data """
		hair = obj.particle_systems.active.particles.data.settings
		hair.count = len(target.data.splines)
		hair.hair_length = self.get_max_lenght(target)
		#TODO need to desin a UI for get some info from user
		hair.hair_step = 12 # optinal / pass for now

		""" Make the Brush ready """
		bpy.ops.object.mode_set(mode='PARTICLE_EDIT', toggle=False)
		bpy.ops.wm.tool_set_by_id(name='builtin_brush.Comb')

		bpy.ops.particle.brush_edit(stroke=[{'name':'', 'location':(0,0,0), 'mouse':(0,0),
			'pressure':0, 'size':0,	'pen_flip':False, 'time':0, 'is_start':True}])
		
		bpy.ops.particle.disconnect_hair()
		depsgraph = ctx.evaluated_depsgraph_get()
		obj = obj.evaluated_get(depsgraph)

		""" Comb The Hair """
		for i in range(0, hair.count):
			self.comb_the_hair(obj.particle_systems.active.particles[i], target, i)
		
		""" Commit Brush """
		bpy.ops.particle.connect_hair()
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def register_hair_guide():
	bpy.utils.register_class(Particle_OT_Hair_Guides_From_Curve)

def unregister_hair_guide():
	bpy.utils.unregister_class(Particle_OT_Hair_Guides_From_Curve)

if __name__ == "__main__":
	register_hair_guide()