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
from bpy.props import IntProperty
from bsmax.actions import solve_missing_activeobject, lock_transform, modifier_add
from bsmax.state import is_objects_selected

def get_volum_dimantion(objs, selection):
	vcos = []
	for obj in objs:
		matrix = obj.matrix_world if len(objs) == 1 else obj.matrix_local
		if obj.type == 'MESH':
			if selection:
				vcos += [matrix @ v.co for v in obj.data.vertices if v.select]
			else:
				vcos += [matrix @ v.co for v in obj.data.vertices]
		elif obj.type == 'LATTICE':
			vcos += [matrix @ v.co_deform for v in obj.data.points]
		elif obj.type == 'SURFACE':
			for spline in obj.data.splines:
				vcos += [matrix @ v.co for v in spline.points]
		elif obj.type in {'FONT', 'CURVE'}:
			for spline in obj.data.splines:
				vcos += [matrix @ v.co for v in spline.bezier_points]
					
	findmin = lambda l: min(l)
	findCenter = lambda l: ( max(l) + min(l) ) / 2
	findmax = lambda l: max(l)

	x,y,z = [[v[i] for v in vcos] for i in range(3)]

	pmin = [findmin(axis) for axis in [x,y,z]]
	pcenter = [findCenter(axis) for axis in [x,y,z]]
	pmax = [findmax(axis) for axis in [x,y,z]]
	return pmin, pcenter, pmax

def get_size(pmin, pmax):
	w = pmax[0] - pmin[0]
	l = pmax[1] - pmin[1]
	h = pmax[2] - pmin[2]
	return Vector((w, l, h))

def set_transform(obj, location, rotation, dimantion):
	obj.location = location
	obj.rotation_euler = rotation
	obj.dimensions = dimantion

def set_modifier(obj, lt, selection):
	if selection:
		if obj.type == 'MESH':
			verts_index = [v.index for v in obj.data.vertices if v.select]
			# TODO check for exist if not add new one
			vg = obj.vertex_groups.new(name="FFD_modifier")
			vg.add(verts_index, 1.0, 'REPLACE')
			# setup modifier
			mod = obj.modifiers.new("Lattice", 'LATTICE')
			mod.object = lt
			mod.vertex_group = "FFD_modifier"
	else:
		mod = obj.modifiers.new("Lattice", 'LATTICE')
		mod.object = lt

def create_lattice(ctx, u, v, w):
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.add(	type='LATTICE')
	lattice = ctx.active_object
	lattice.data.points_u = u
	lattice.data.points_v = v
	lattice.data.points_w = w
	return lattice

class Lattice_OT_Set_On_Selection(Operator):
	bl_idname = "lattice.set_on_selection"
	bl_label = "Lattice (Set)"
	bl_options = {'REGISTER', 'UNDO'}
	
	res_u: IntProperty(name="Res X",min=2,max=1000,default=2)
	res_v: IntProperty(name="Res Y",min=2,max=1000,default=2)
	res_w: IntProperty(name="Res Z",min=2,max=1000,default=2)

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0

	def execute(self, ctx):
		support = ['MESH','CURVE','LATTICE','SURFACE']
		targets = [obj for obj in ctx.selected_objects if obj.type in support]
		if len(targets) > 0:
			target = targets[0]
			solve_missing_activeobject(ctx, targets) # to able to get mode
			mode = ctx.mode # store mode befor set to object mode
			lt = create_lattice(ctx, self.res_u, self.res_v, self.res_w)
			selection = "EDIT" in mode
			pmin,pcen,pmax = get_volum_dimantion(targets, selection)
			rotation = target.rotation_euler if len(targets) == 1 else [0,0,0]
			set_transform(lt, pcen, rotation, get_size(pmin, pmax))
			for target in targets:
				set_modifier(target, lt, selection)
			if len(targets) == 1:
				lt.parent = target
				lt.matrix_parent_inverse = target.matrix_world.inverted()
				lock_transform(lt,True,True,True)
		self.report({'OPERATOR'},'bpy.ops.lattice.set_on_selection()')
		return{"FINISHED"}


# Quik setup operators #
class Modifier_OT_Lattice_2x2x2_Set(Operator):
	bl_idname = "modifier.lattice_2x2x2_set"
	bl_label = "Lattice 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=2,res_v=2,res_w=2)
		self.report({'OPERATOR'},'bpy.ops.modifier.lattice_2x2x2_set()')
		return{"FINISHED"}

class Modifier_OT_Lattice_3x3x3_Set(Operator):
	bl_idname = "modifier.lattice_3x3x3_set"
	bl_label = "Lattice 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=3,res_v=3,res_w=3)
		self.report({'OPERATOR'},'bpy.ops.modifier.lattice_3x3x3_set()')
		return{"FINISHED"}

class Modifier_OT_Lattice_4x4x4_Set(Operator):
	bl_idname = "modifier.lattice_4x4x4_set"
	bl_label = "Lattice 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=4,res_v=4,res_w=4)
		self.report({'OPERATOR'},'bpy.ops.modifier.lattice_4x4x4_set()')
		return{"FINISHED"}

class Modifier_OT_FFD_2x2x2_Set(Operator):
	bl_idname = "modifier.ffd_2x2x2_set"
	bl_label = "FFD 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=2,res_v=2,res_w=2)
		self.report({'OPERATOR'},'bpy.ops.modifier.ffd_2x2x2_set()')
		return{"FINISHED"}

class Modifier_OT_FFD_3x3x3_Set(Operator):
	bl_idname = "modifier.ffd_3x3x3_set"
	bl_label = "FFD 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=3,res_v=3,res_w=3)
		self.report({'OPERATOR'},'bpy.ops.modifier.ffd_3x3x3_set()')
		return{"FINISHED"}

class Modifier_OT_FFD_4x4x4_Set(Operator):
	bl_idname = "modifier.ffd_4x4x4_set"
	bl_label = "FFD 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=4,res_v=4,res_w=4)
		self.report({'OPERATOR'},'bpy.ops.modifier.ffd_4x4x4_set()')
		return{"FINISHED"}
	
class lattice_data:
	preferences = None
	def is_3dmax(self):
		if self.preferences == None:
			return False
		print(self.preferences.viowport)
		return self.preferences.viowport == '3DsMax'
			
ld = lattice_data()

def lattice_menu(self, ctx):
	layout = self.layout
	layout.separator()
	the_name = 'FFD' if ld.is_3dmax() else 'Lattice'
	layout.operator("modifier.lattice_2x2x2_set",text=(the_name+' 2x2x2 (Set)'),icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice_3x3x3_set",text=(the_name+' 3x3x3 (Set)'),icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice_4x4x4_set",text=(the_name+' 4x4x4 (Set)'),icon="OUTLINER_OB_LATTICE")

classes = [Lattice_OT_Set_On_Selection,
	Modifier_OT_Lattice_2x2x2_Set,
	Modifier_OT_Lattice_3x3x3_Set,
	Modifier_OT_Lattice_4x4x4_Set,
	Modifier_OT_FFD_2x2x2_Set,
	Modifier_OT_FFD_3x3x3_Set,
	Modifier_OT_FFD_4x4x4_Set]

def register_lattice(preferences):
	ld.preferences = preferences
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.BSMAX_MT_lattice_create_menu.append(lattice_menu)

def unregister_lattice():
	bpy.types.BSMAX_MT_lattice_create_menu.remove(lattice_menu)
	for c in classes:
		bpy.utils.unregister_class(c)