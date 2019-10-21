import bpy
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy.props import IntProperty
from bsmax.actions import solve_missing_activeobject, lock_transform

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

class BsMax_OT_Lattice_Set(Operator):
	bl_idname = "bsmax.latticebox"
	bl_label = "Lattice (Set)"
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
		return{"FINISHED"}

def lattice_cls(register):
	c = BsMax_OT_Lattice_Set
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	lattice_cls(True)

__all__ = ["lattice_cls"]