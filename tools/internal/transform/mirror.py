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
from bpy.props import FloatProperty, EnumProperty

# Object Mode: Mirror
# Created by Ozzkar 06-Sep-2013
# Edit by Nevil 2019

def bmaxMirror_Execute_OM(self, ctx):
	ctx.active_object.matrix_world = self.old_xfrm.copy()
	if self.c_mode == 'COPY':
		if self.obj_copy == None:
			bpy.ops.object.duplicate(linked = False, mode = 'INIT')
			self.obj_copy = ctx.active_object
	elif self.c_mode == 'INST':
		if self.obj_copy == None:
			bpy.ops.object.duplicate(linked = True, mode = 'INIT')
			self.obj_copy = ctx.active_object
	else:
		if self.obj_copy != None:
			bpy.ops.object.delete(use_global = False)
			ctx.scene.objects.active = self.obj_orig
			self.obj_orig.select = True
			self.obj_copy = None
	c_ax = (False, False, False)
	t_mode = self.t_mode
	if t_mode == 'X':
		c_ax = (True,False,False)
	elif t_mode == 'Y':
		c_ax = (False,True,False)
	elif t_mode == 'Z':
		c_ax = (False,False,True)
	elif t_mode == 'XY':
		c_ax = (True,True,False)
	elif t_mode == 'YZ':
		c_ax = (False,True,True)
	elif t_mode == 'ZX':
		c_ax = (True,False,True)
	if t_mode != 'N':
		# mirror
		bpy.ops.transform.mirror(constraint_axis = c_ax,
			constraint_orientation = self.dlg_csys.transform_orientation,
			proportional = 'DISABLED', proportional_edit_falloff = 'SMOOTH',
			proportional_size = 1)#, release_confirm = False)
		#offset
		bpy.ops.transform.translate(
			value = (self.v_offs,self.v_offs,self.v_offs),
			constraint_axis = c_ax,
			constraint_orientation = self.dlg_csys.transform_orientation,
			mirror = False,
			proportional = 'DISABLED',
			proportional_edit_falloff = 'SMOOTH',
			proportional_size = 1,
			snap = False,
			snap_target = 'CLOSEST',
			snap_point = (0,0,0),
			snap_align = False,
			snap_normal = (0,0,0),
			texture_space = False)
			# ,release_confirm = False)

class Object_OT_Mirror(bpy.types.Operator):
	bl_idname = "object.mirror"
	bl_label = "Mirror"
	bl_description = "Mirror object dialog box"
	bl_options = {'REGISTER', 'UNDO'}
	old_xfrm,obj_orig,obj_copy,dlg_csys = None,None,None,None
	v_offs: FloatProperty(default=0)
	t_mode: EnumProperty(name='Axis',description='Mirror axis',default='N',
		items = [('N','None','None'),('X','X','X'),('Y','Y','Y'),('Z','Z','Z'),
			('XY','XY','XY'),('YZ','YZ','YZ'),('ZX','ZX','ZX')])
	c_mode: EnumProperty(name='Clone Selection',description='Clone mode',default='ORIG',
		items = [('ORIG','No Clone','No Clone'),('COPY','Copy','Copy'),
				('INST','Instance','Instance')])

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) == 1 and ctx.active_object != None

	def check(self, ctx):
		bmaxMirror_Execute_OM(self, ctx)
		return True

	def cancel(self, ctx):
		if self.obj_copy != None:
			bpy.ops.object.delete(use_global = False)
			ctx.scene.objects.active = self.obj_orig
		self.obj_orig.select = True
		self.obj_orig.matrix_world = self.old_xfrm.copy()

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.prop(self.dlg_csys,"transform_orientation",text="Coord. System")
		box = layout.box()
		row = box.row()
		row.prop(self,"t_mode")
		row.prop(self,"v_offs",text="Offset")
		row = box.row()
		row.prop(self,"c_mode")

	def execute(self, ctx):
		self.report({'OPERATOR'},'bpy.ops.object.mirror()')
		return {'FINISHED'}

	def invoke(self, ctx, evt):
		self.obj_copy = None
		self.obj_orig = ctx.active_object
		self.old_xfrm = self.obj_orig.matrix_world.copy()
		self.dlg_csys = ctx.space_data
		bmaxMirror_Execute_OM(self, ctx)
		ctx.window_manager.invoke_props_dialog(self)
		return {'RUNNING_MODAL'}

def register_mirror():
	bpy.utils.register_class(Object_OT_Mirror)

def unregister_mirror():
	bpy.utils.unregister_class(Object_OT_Mirror)