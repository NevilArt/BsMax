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
from bpy.app import version
from bpy.types import Operator, Menu

from bsmax.math import point_on_spline
from bsmax.actions import link_to_scene, match_transform
from bsmax.operator import PickOperator
from bsmax.state import is_object_mode


class Hair_Guide:
	def __init__(self):
		self.name = "ParticleSystem"
		self.hair_keys = [] # [[Vector(x,y,z), Vector(x,y,z)], [Vector(x,y,z)]]
	
	def get_hair_particle(self, ctx):
		# Get the depsgraph
		deps_graph = ctx.evaluated_depsgraph_get()
		# Get evaluated object 
		evaluated_object = ctx.object.evaluated_get(deps_graph)
		# Get active particle
		return evaluated_object.particle_systems.active
	
	def create_hair_particle(self, ctx):
		# reset avalible hair particle
		bpy.ops.particle.edited_clear()
		bpy.ops.particle.disconnect_hair()
		# create new particle sets
		hair = ctx.object.particle_systems.active.particles.data.settings
		hair.count = len(self.hair_keys)
		hair.hair_length = 1
		# get max hair count
		max_count = 0
		for hair in self.hair_keys:
			count = len(hair)
			if count > max_count:
				max_count = count
		# hair.hair_step = max_count
	
	def get_hair_style(self, ctx):
		""" Read hair style from particle setting """
		hair_particle = self.get_hair_particle(ctx)
		self.hair_keys.clear()
		for particle in hair_particle.particles:
			self.hair_keys.append([vector.co.copy() for vector in particle.hair_keys])
		self.name = hair_particle.name	

	def set_hair_style(self, ctx):
		""" create particle data from hair_keys """
		active_particle = self.get_hair_particle(ctx)
		# apply style
		for particle, key in zip(active_particle.particles, self.hair_keys):
			for hair_key, key_co in zip(particle.hair_keys, key):
				hair_key.co = key_co
		# Update view and UI
		ctx.scene.frame_set(ctx.scene.frame_current)
	

	def to_curve(self, ctx):
		""" Create Conver object from heire style """
		parent = ctx.object
		name = parent.name + "_" + self.name
		newcurve = bpy.data.curves.new(name, type='CURVE')
		newcurve.dimensions = '3D'
		curve = bpy.data.curves[newcurve.name]
		curve.splines.clear()
		
		for keys in self.hair_keys:
			count = len(keys)
			newspline = curve.splines.new('POLY')
			newspline.points.add(count-1)

			for i, co in enumerate(keys):
				newspline.points[i].co = [co.x, co.y, co.z, 1]

		curve = bpy.data.objects.new(name, newcurve)
		link_to_scene(ctx, curve)

		curve.matrix_world = parent.matrix_world
		return curve


	def from_curve(self, curve):
		""" Read curve object as hair style date """
		self.hair_keys.clear()
		
		# get max hair count
		max_count = 0
		for spline in curve.data.splines:
			count = len(spline.bezier_points)
			if count > max_count:
				max_count = count

		# read points from bezier curve
		for spline in curve.data.splines:
			new_hair = []
			for i in range(max_count):
				time = i / (max_count - 1)
				co, _, _ = point_on_spline(spline, time)
				new_hair.append(co)
			if len(new_hair) > 1:
				self.hair_keys.append(new_hair)

		# read points from poly curves
		for spline in curve.data.splines:
			new_hair = []
			for point in spline.points:
				co = [point.co[0], point.co[1], point.co[2]]
				new_hair.append(co)
			if len(new_hair) > 1:
				self.hair_keys.append(new_hair)


	def to_text(self):
		""" Conver hair style to python code array as text """
		return ""


	def from_text(self, text):
		""" Convert python array as text to hayle style data """
		pass


	def commit(self):
		""" in particle brush mode apply a brush with no change 
			this makes blender save and keep new values.
		"""
		bpy.ops.object.mode_set(mode='PARTICLE_EDIT', toggle=False)
		bpy.ops.wm.tool_set_by_id(name='builtin_brush.Comb')
		
		if version <= (2, 90, 0):
			bpy.ops.particle.brush_edit(stroke=[{'name':'',
				'location':(0, 0, 0), 'mouse':(0, 0),
				'pressure':0, 'size':0, 'pen_flip':False,
				'time':0, 'is_start':True}])
		else:
			bpy.ops.particle.brush_edit(stroke=[{'name':'',
				'location':(0, 0, 0), 'mouse':(0, 0),
				'mouse_event':(0, 0),
				'pressure':0, 'size':0, 'pen_flip':False,
				'x_tilt':0, 'y_tilt':0,
				'time':0, 'is_start':False}])
		
		# Commit the Brush
		bpy.ops.particle.connect_hair()
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



def poll_check(ctx):
	""" Return true if Hair particle Avalible and Active """
	if ctx.area.type == 'VIEW_3D':
		active_particle = ctx.object.particle_systems.active
		if active_particle:
			return active_particle.particles.data.settings.type == 'HAIR'
	return False



class Particle_OT_Hair_Guides_From_Curve(PickOperator):
	""" Conver picked Curve object to Hair particle Brush """
	bl_idname = 'particle.hair_guides_from_curve'
	bl_label = 'Hair Guides From Curve'
	bl_options = {'REGISTER', 'UNDO'}
	filters = ['CURVE']

	@classmethod
	def poll(self, ctx):
		return poll_check(ctx)

	def match_curve_transform(self, ctx, curve):
		active_object = ctx.object
		match_transform(ctx, curve, active_object)
		bpy.ops.object.select_all(action='DESELECT')
		active_object.select_set(state=True)
		ctx.view_layer.objects.active = active_object
	
	def picked(self, ctx, source, subsource, target, subtarget):
		self.match_curve_transform(ctx, target)
		hair_guide = Hair_Guide()
		hair_guide.from_curve(target)
		hair_guide.create_hair_particle(ctx)
		hair_guide.set_hair_style(ctx)
		hair_guide.commit()



class Particle_OT_Hair_Guides_To_Curve(Operator):
	bl_idname = 'particle.hair_guides_to_curve'
	bl_label = 'Hair Guides To Curve'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return poll_check(ctx)

	def execute(self, ctx):
		hair_guide = Hair_Guide()
		hair_guide.get_hair_style(ctx)
		hair_guide.to_curve(ctx)
		return{"FINISHED"}



class Particle_OT_Hair_Grap_Style(Operator):
	""" Grab current style of hair particle and apply as brush """
	bl_idname = 'particle.hair_grap_style'
	bl_label = 'Hair Grab Style'
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return poll_check(ctx)
	
	def execute(self, ctx):
		hair_guide = Hair_Guide()
		hair_guide.get_hair_style(ctx)
		ctx.object.particle_systems.active.use_hair_dynamics = False
		ctx.scene.frame_set(ctx.scene.frame_current)
		hair_guide.set_hair_style(ctx)
		hair_guide.commit()
		return{"FINISHED"}



class BsMax_MT_particle_tools(Menu):
	bl_idname = "BSMAX_MT_particletools"
	bl_label = "Particle"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("particle.hair_guides_from_curve", icon="PARTICLEMODE")
		layout.operator("particle.hair_guides_to_curve", icon="TRACKING")

		hair_icon = 'HAIR' if version < (3, 2, 0) else 'CURVES'
		layout.operator("particle.hair_grap_style", icon=hair_icon)



classes = [
	Particle_OT_Hair_Guides_From_Curve,
	Particle_OT_Hair_Guides_To_Curve,
	Particle_OT_Hair_Grap_Style,
	BsMax_MT_particle_tools
	]

def register_hair_guide():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_hair_guide():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_hair_guide()