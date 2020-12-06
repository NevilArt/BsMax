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
from bpy.types import Operator
from bsmax.math import point_on_curve
from bsmax.actions import set_origen, link_to_scene
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
		hair.hair_step = max([len(spline.bezier_points) for spline in target.data.splines])

		""" Make the Brush ready """
		bpy.ops.object.mode_set(mode='PARTICLE_EDIT', toggle=False)
		bpy.ops.wm.tool_set_by_id(name='builtin_brush.Comb')

		bpy.ops.particle.brush_edit(stroke=[{'name':'', 'location':(0,0,0), 'mouse':(0,0),
			'pressure':0, 'size':0,	'pen_flip':False, 'time':0, 'is_start':True}])
		
		bpy.ops.particle.disconnect_hair()
		depsgraph = ctx.evaluated_depsgraph_get()
		obj = obj.evaluated_get(depsgraph)

		""" Comb The Hair """
		for i in range(hair.count):
			self.comb_the_hair(obj.particle_systems.active.particles[i], target, i)
		
		""" Commit Brush """
		bpy.ops.particle.connect_hair()
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		self.report({'OPERATOR'},'bpy.ops.particle.hair_guides_from_curve()')

class Particle_OT_Hair_Guides_To_Curve(Operator):
	bl_idname = 'particle.hair_guides_to_curve'
	bl_label = 'Hair Guides To Curve'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode == 'OBJECT':
				if len(ctx.selected_objects) == 1:
					return ctx.object.type == 'MESH'
		return False

	def center_of(self, point_a, point_b):
		return (point_a + point_b) / 2
	
	def read_hair_guide(self, ctx, obj):
		""" collect and return hair guides coordinate points """
		depsgraph = ctx.evaluated_depsgraph_get()
		obj = obj.evaluated_get(depsgraph)
		hairs = obj.particle_systems.active.particles
		return [[key.co for key in hair.hair_keys] for hair in hairs]
	
	def create_curve(self, ctx, guides, parent):
		if len(guides) > 1:
			name = parent.name + "_Hair_Guide"
			newcurve = bpy.data.curves.new(name, type='CURVE')
			newcurve.dimensions = '3D'
			curve = bpy.data.curves[newcurve.name]
			curve.splines.clear()
			
			for guide in guides:
				count = len(guide)
				newspline = curve.splines.new('BEZIER')
				newspline.bezier_points.add(count-1)
				for i in range(count):
					first, last, co = (i == 0), (i == count-1), guide[i]
					bez = newspline.bezier_points[i]
					handle_type = 'VECTOR' if first or last else 'AUTO'
					bez.co = co
					bez.handle_left = self.center_of(co, guide[i+1]) if first else co
					bez.handle_left_type = handle_type
					bez.handle_right = co if last else self.center_of(co, guide[i-1])
					bez.handle_right_type = handle_type
			
			curve = bpy.data.objects.new(name, newcurve)
			link_to_scene(ctx, curve)

			curve.location = parent.location
			curve.rotation_euler = parent.rotation_euler
			curve.scale = parent.scale
	
	def execute(self,ctx):
		obj = ctx.active_object
		guides = self.read_hair_guide(ctx, obj)
		self.create_curve(ctx, guides, obj)
		self.report({'OPERATOR'},'bpy.ops.particle.hair_guides_to_curve()')
		return{"FINISHED"}
	

classes = [Particle_OT_Hair_Guides_From_Curve, Particle_OT_Hair_Guides_To_Curve]

def register_hair_guide():
	[bpy.utils.register_class(c) for c in classes]

def unregister_hair_guide():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_hair_guide()