import bpy
from bpy.props import EnumProperty, BoolProperty
from mathutils import Vector, Matrix
from bpy.types import Panel, Menu, UIList, Operator, PropertyGroup

# Original Code by Ozzkar
# Edit by Nevil

def GetPosData(obj):
	cld = []
	msh = obj.data
	if obj.type == 'MESH' and len(msh.vertices) > 0:
		# for vert in msh.vertices:
		# 	cld.append(obj.matrix_world @ vert.co)
		cld = [obj.matrix_world @ vert.co for vert in msh.vertices]
	elif obj.type == 'CURVE' and len(msh.splines) > 0:
		for spn in msh.splines:
			for pts in spn.bezier_points:
				cld.append(obj.matrix_world @ pts.co)
	elif obj.type == 'SURFACE' and len(msh.splines) > 0:
		for spn in msh.splines:
			for pts in spn.points:
				cld.append(obj.matrix_world @ pts.co)
	elif obj.type == 'FONT' and len(msh.splines) > 0:
		for s in msh.splines:
			for pts in s.bezier_points:
				cld.append(obj.matrix_world @ pts.co)
	# get min/max/center/pivot data
	if len(cld) == 0 or obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT'}:
		return obj.location.copy(), obj.location.copy(), obj.location.copy(), obj.location.copy()
	p_min = cld[0].copy()
	p_max = cld[0].copy()
	for v in cld:
		if p_min.x > v.x:
			p_min.x = v.x
		if p_min.y > v.y:
			p_min.y = v.y
		if p_min.z > v.z:
			p_min.z = v.z
		if p_max.x < v.x:
			p_max.x = v.x
		if p_max.y < v.y:
			p_max.y = v.y
		if p_max.z < v.z:
			p_max.z = v.z
	return p_min, (p_min+p_max)/2, obj.location.copy(), p_max

def StoreFormData(self, ctx):
	self.pos_curs = ctx.scene.cursor.location.copy()
	self.rot_curs = ctx.scene.cursor.rotation_euler.copy()

	for obj in ctx.selected_objects:
		p_min,p_mid,p_piv,p_max = GetPosData(obj)
		self.pos_list.append([p_min,p_mid,p_piv,p_max])
		self.rot_list.append(obj.rotation_euler.copy())
		self.scl_list.append(obj.scale.copy())

def AlignObject_Execute(self, ctx):
	a_box = GetPosData(ctx.active_object)
	a_rot = ctx.active_object.rotation_euler
	a_scl = ctx.active_object.scale

	# set modes
	c_id, t_id = 0, 0
	if self.c_mode == 'MID':
		c_id = 1
	if self.c_mode == 'PIV':
		c_id = 2
	if self.c_mode == 'MAX':
		c_id = 3
	if self.t_mode == 'MID':
		t_id = 1
	if self.t_mode == 'PIV':
		t_id = 2
	if self.t_mode == 'MAX':
		t_id = 3

	# check cursor to cursor
	if self.c_mode == '3DC' and self.t_mode == '3DC':
		return

	# check active object agains itself
	if len(ctx.selected_objects) == 1 and self.c_mode != '3DC' and self.t_mode != '3DC':
		return

	# set 3D cursor
	if self.c_mode == '3DC':
		# Position
		cursor = ctx.scene.cursor
		if self.pos_x:
			cursor.location[0] = a_box[t_id].x
		if self.pos_y:
			cursor.location[1] = a_box[t_id].y
		if self.pos_z:
			cursor.location[2] = a_box[t_id].z
		# rotation
		if self.rot_x:
			cursor.rotation_euler.x = a_rot.x
		if self.rot_y:
			cursor.rotation_euler.y = a_rot.y
		if self.rot_z:
			cursor.rotation_euler.z = a_rot.z
		return

	if self.t_mode == '3DC':
		scp = ctx.scene.cursor.location.copy()
		for i, obj in enumerate(ctx.selected_objects):
			# Position
			pos_list = self.pos_list
			if self.pos_x:
				obj.location.x = scp.x+(pos_list[i][2].x-pos_list[i][c_id].x)
			if self.pos_y:
				obj.location.y = scp.y+(pos_list[i][2].y-pos_list[i][c_id].y)
			if self.pos_z:
				obj.location.z = scp.z+(pos_list[i][2].z-pos_list[i][c_id].z)
			# Rotation
			if self.rot_x:
				obj.rotation_euler.x = self.rot_curs[0]
			if self.rot_y:
				obj.rotation_euler.y = self.rot_curs[1]
			if self.rot_z:
				obj.rotation_euler.z = self.rot_curs[2]
		return

	# set selection
	for i, obj in enumerate(ctx.selected_objects):
		if obj != ctx.active_object:
			# position
			pos_list = self.pos_list
			if self.pos_x:
				obj.location.x = a_box[t_id].x+(pos_list[i][2].x-pos_list[i][c_id].x)
			if self.pos_y:
				obj.location.y = a_box[t_id].y+(pos_list[i][2].y-pos_list[i][c_id].y)
			if self.pos_z:
				obj.location.z = a_box[t_id].z+(pos_list[i][2].z-pos_list[i][c_id].z)
			# rotation
			if self.rot_x:
				obj.rotation_euler.x = a_rot.x
			if self.rot_y:
				obj.rotation_euler.y = a_rot.y
			if self.rot_z:
				obj.rotation_euler.z = a_rot.z
			# scale
			if self.scl_x:
				obj.scale.x = a_scl.x
			if self.scl_y:
				obj.scale.y = a_scl.y
			if self.scl_z:
				obj.scale.z = a_scl.z

def BsMaxAlign_Reset(self, ctx):
	cursor,pos_curs,rot_curs = ctx.scene.cursor,self.pos_curs,self.rot_curs
	cursor.location = pos_curs.x,pos_curs.y,pos_curs.z
	cursor.rotation_euler = rot_curs.x,rot_curs.y,rot_curs.z

	for i, obj in enumerate(ctx.selected_objects):
		# position
		obj.location.x = self.pos_list[i][2].x
		obj.location.y = self.pos_list[i][2].y
		obj.location.z = self.pos_list[i][2].z
		# rotation
		obj.rotation_euler.x = self.rot_list[i].x
		obj.rotation_euler.y = self.rot_list[i].y
		obj.rotation_euler.z = self.rot_list[i].z
		# scale
		obj.scale.x = self.scl_list[i].x
		obj.scale.y = self.scl_list[i].y
		obj.scale.z = self.scl_list[i].z
	#ctx.scene.update()

class BsMax_OT_AlignObjects(Operator):
	bl_idname = "bsmax.alignselectedobjects"
	bl_label = "Align Selected Objects"
	bl_options = {'REGISTER','UNDO'}
	pos_curs,rot_curs = Vector((0,0,0)),Vector((0,0,0))
	pos_list,rot_list,scl_list = [],[],[]
	items = [('MIN','Minimum','Minimum'),('MID','Center','Center'),
			('PIV','Pivot','Pivot'),('MAX','Maximum','Maximum'),
			('3DC','3D Cursor','3D Cursor')]
	c_mode: EnumProperty(description='Selection alignment point',default='MIN',items=items)
	t_mode: EnumProperty(description='Target alignment point',default='MIN',items=items)
	pos_x: BoolProperty()
	pos_y: BoolProperty()
	pos_z: BoolProperty()
	rot_x: BoolProperty()
	rot_y: BoolProperty()
	rot_z: BoolProperty()
	scl_x: BoolProperty()
	scl_y: BoolProperty()
	scl_z: BoolProperty()

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0 and ctx.active_object != None

	def __init__(self):
		pass

	def check(self, ctx):
		BsMaxAlign_Reset(self,ctx)
		AlignObject_Execute(self,ctx)
		return True

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.label(text = "Align Position (World):")
		row = box.row()
		row.prop(self,"pos_x",text="X Position")
		row.prop(self,"pos_y",text="Y Position")
		row.prop(self,"pos_z",text="Z Position")
		row = box.row()
		row.label(text="Current Object:")
		row.label(text="Taget Object:")
		row = box.row()
		row.prop(self,"c_mode")
		row.prop(self,"t_mode")
		box = layout.box()
		row = box.row()
		row.label(text="Align Orientation (Local):")
		row = box.row()
		row.prop(self,"rot_x",text="X Axis")
		row.prop(self,"rot_y",text="Y Axis")
		row.prop(self,"rot_z",text="Z Axis")
		box = layout.box()
		row = box.row()
		row.label(text="Match Scale:")
		row = box.row()
		row.prop(self,"scl_x",text="X Axis")
		row.prop(self,"scl_y",text="Y Axis")
		row.prop(self,"scl_z",text="Z Axis")

	def execute(self, ctx):
		return {'FINISHED'}

	def cancel(self, ctx):
		BsMaxAlign_Reset(self, ctx)

	def invoke(self, ctx, event):
		self.pos_curs,self.rot_curs = Vector((0,0,0)),Vector((0,0,0))
		self.pos_list,self.rot_list,self.scl_list = [],[],[]
		StoreFormData(self,ctx)
		AlignObject_Execute(self,ctx)
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)

def alignobjects_cls(register):
	classes = [BsMax_OT_AlignObjects]

	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else: 
		[bpy.utils.unregister_class(c) for c in classes]
	return classes

if __name__ == '__main__':
	alignobjects_cls(True)

__all__ = ["alignobjects_cls"]