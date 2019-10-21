import bpy
from mathutils import Matrix

def solve_missing_activeobject(ctx, objs):
	if ctx.active_object == None:
		if len(objs) > 0:
			ctx.view_layer.objects.active = objs[0]

def lock_transform(obj, move, rotate, scale):
	for i in range(3):
		obj.lock_location[i] = move
		obj.lock_rotation[i] = rotate
		obj.lock_scale[i] = scale

def set_transform(obj, coordinate, location, rotation, dimantion):
	if coordinate == 'locaL':
		pass
	elif coordinate in {'world','global'}:
		pass
	elif coordinate == 'parent':
		pass
	obj.location = location
	obj.rotation_euler = rotation
	obj.dimensions = dimantion

def duplicate_linked(ctx, obj):
	# not a god method has to fix
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(state = True)
	bpy.ops.object.duplicate(linked=True, mode='TRANSLATION')
	return ctx.view_layer.objects.active

def duplicate_copy(ctx, obj):
	# not a god method has to fix
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(state = True)
	bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
	return ctx.view_layer.objects.active

def modifier_add(ctx, objs, modifier):
	activeobject = ctx.active_object
	for obj in ctx.selected_objects:
		ctx.view_layer.objects.active = obj
		bpy.ops.object.modifier_add(type=modifier)
	ctx.view_layer.objects.active = obj

def link_to_scene(ctx, obj):
	activelayername = ctx.view_layer.active_layer_collection.name
	if activelayername == "Master Collection":
		collection = ctx.scene.collection
	else:
		collection = bpy.data.collections[activelayername]
	collection.objects.link(obj)

def set_as_active_object(ctx, obj):
	if obj != None:
		bpy.ops.object.select_all(action = 'DESELECT')
		obj.select_set(state = True)
		ctx.view_layer.objects.active = obj

def delete_objects(objs):
	bpy.ops.object.delete({"selected_objects": objs})

def set_create_target(obj, targ):
	cont = obj.constraints.new('TRACK_TO')
	if targ == None:
		targ = bpy.data.objects.new("empty", None )
		targ.empty_display_type = 'CUBE'
		targ.empty_display_size = 0.25
		activelayername = bpy.context.view_layer.active_layer_collection.name
		col = bpy.data.collections[activelayername]
		col.objects.link(targ)
		targ.name = obj.name + "_target"
		targ.location = obj.location
		targ.rotation_euler = obj.rotation_euler
		targ.matrix_basis @= Matrix.Translation((0.0, 0.0, -2.0))
	cont.target = targ
	cont.track_axis = 'TRACK_NEGATIVE_Z'
	cont.up_axis = 'UP_Y'
	return targ

def get_objects_target(obj):
	return None

__all__ = ["solve_missing_activeobject",
		"lock_transform",
		"set_transform",
		"duplicate_linked",
		"duplicate_copy",
		"add_modifier",
		"link_to_scene",
		"delete_objects",
		"set_as_active_object",
		"set_create_target"]
