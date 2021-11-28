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
from bpy.props import EnumProperty,BoolProperty

class Mesh_Subobject_Mode:
	def __init__(self):
		self.active = False
		self.normal = True
		self.material = False
		self.seam = True
		self.sharp = True
		self.uv = False

msm = Mesh_Subobject_Mode()

class Mesh_OT_Select_Element_Toggle(Operator):
	bl_idname = "mesh.select_element_toggle"
	bl_label = "Select Elemant Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.mode in {'EDIT_MESH','EDIT_CURVE', 'PARTICLE'}
	
	def execute(self, ctx):
		msm.active = not msm.active
		return{"FINISHED"}

def view3d_select(mode,x,y):
	if mode == 'SET':
		bpy.ops.view3d.select(deselect_all=True, location=(x, y))
	elif mode == 'ADD':
		bpy.ops.view3d.select(toggle=True, location=(x, y))
	elif mode == 'SUB':
		bpy.ops.view3d.select(deselect=True, location=(x, y))

def mesh_select(mode):
	delimit = set()
	if msm.normal:
		delimit.add('NORMAL')
	if msm.material:
		delimit.add('MATERIAL')
	if msm.seam:
		delimit.add('SEAM')
	if msm.sharp:
		delimit.add('SHARP')
	if msm.uv:
		delimit.add('UV')

	if mode == 'SET':
		bpy.ops.mesh.select_all(action='DESELECT')
		bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT',
			deselect=False, delimit=delimit)
	elif mode == 'ADD':
		bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT',
			deselect=False, delimit=delimit)
	elif mode == 'SUB':
		bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT',
			deselect=True, delimit=delimit)

def curve_select(mode):
	if mode == 'SET':
		bpy.ops.curve.select_all(action='DESELECT')
		bpy.ops.curve.select_linked_pick('INVOKE_DEFAULT',deselect=False)
	elif mode == 'ADD':
		bpy.ops.curve.select_linked_pick('INVOKE_DEFAULT',deselect=False)
	elif mode == 'SUB':
		bpy.ops.curve.select_linked_pick('INVOKE_DEFAULT',deselect=True)

def particle_select(mode):
	if mode == 'SET':
		bpy.ops.particle.select_all(action='DESELECT')
		bpy.ops.particle.select_linked_pick('INVOKE_DEFAULT',deselect=False)
	elif mode == 'ADD':
		bpy.ops.particle.select_linked_pick('INVOKE_DEFAULT',deselect=False)
	elif mode == 'SUB':
		bpy.ops.particle.select_linked_pick('INVOKE_DEFAULT',deselect=True)

class Mesh_OT_Select_Element_Setting(Operator):
	bl_idname = "mesh.select_element_setting"
	bl_label = "Select Elemant Setting"

	active: BoolProperty(name="Active")
	normal: BoolProperty(name="Normal")
	material: BoolProperty(name="Material")
	seam: BoolProperty(name="Seam")
	sharp: BoolProperty(name="Sharp")
	uv: BoolProperty(name="UV")

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def draw(self,ctx):
		layout =self.layout
		box =layout.box()
		box.prop(self,"active")
		if self.active:
			box =layout.box()
			box.prop(self,"normal")
			box.prop(self,"material")
			box.prop(self,"seam")
			box.prop(self,"sharp")
			box.prop(self,"uv")

	def commit(self):
		msm.active = self.active
		msm.normal = self.normal
		msm.material = self.material
		msm.seam = self.seam
		msm.sharp = self.sharp
		msm.uv = self.uv
	
	def execute(self, ctx):
		self.commit()
		return{"FINISHED"}
	
	def cancel(self,ctx):
		self.commit()
		return None

	def invoke(self,ctx,event):
		self.active = msm.active
		self.normal = msm.normal
		self.material = msm.material
		self.seam = msm.seam
		self.sharp = msm.sharp
		self.uv = msm.uv
		return ctx.window_manager.invoke_props_dialog(self)

class Mesh_OT_Select_Max(Operator):
	bl_idname = "mesh.select_max"
	bl_label = "Select (3DsMax)"
	bl_options = {'REGISTER', 'INTERNAL'}

	mode: EnumProperty(name='Mode', default='SET',
		items=[('SET','Set',''),('ADD','Add',''),('SUB','Sub','')])
	
	x,y = 0,0

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def execute(self, ctx):
		if msm.active:
			mesh_select(self.mode)
		else:
			view3d_select(self.mode, self.x, self.y)
		bpy.ops.ed.undo_push()
		self.report({'OPERATOR'},'bpy.ops.mesh.select_max()')
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		return self.execute(ctx)

class Curve_OT_Select_Max(Operator):
	bl_idname = "curve.select_max"
	bl_label = "Select (3DsMax)"
	bl_options = {'REGISTER', 'INTERNAL'}

	mode: EnumProperty(name='Mode', default='SET',
		items=[('SET','Set',''),('ADD','Add',''),('SUB','Sub','')])
	
	x,y = 0,0

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_CURVE"

	def execute(self, ctx):
		if msm.active:
			curve_select(self.mode)
		else:
			view3d_select(self.mode, self.x, self.y)
		bpy.ops.ed.undo_push()
		self.report({'OPERATOR'},'bpy.ops.curve.select_max()')
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		return self.execute(ctx)

class Particle_OT_Select_Max(Operator):
	bl_idname = "particle.select_max"
	bl_label = "Select (3DsMax)"
	bl_options = {'REGISTER', 'INTERNAL'}

	mode: EnumProperty(name='Mode', default='SET',
		items=[('SET','Set',''),('ADD','Add',''),('SUB','Sub','')])
	
	x,y = 0,0

	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_CURVE"

	def execute(self, ctx):
		if msm.active:
			particle_select(self.mode)
		else:
			view3d_select(self.mode, self.x, self.y)
		bpy.ops.ed.undo_push()
		self.report({'OPERATOR'},'bpy.ops.curve.select_max()')
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		self.x, self.y = event.mouse_region_x, event.mouse_region_y
		return self.execute(ctx)

classes = [	Mesh_OT_Select_Element_Toggle,
			Mesh_OT_Select_Element_Setting,
			Mesh_OT_Select_Max,
			Curve_OT_Select_Max,
			Particle_OT_Select_Max]

def register_select():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_select():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_select()