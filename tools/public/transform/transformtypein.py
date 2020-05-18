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

import bpy, math
from bpy.props import FloatProperty,BoolProperty
from math import radians,degrees
from mathutils import Vector

class BsMax_OT_TransformTypeIn(bpy.types.Operator):
	bl_idname = "bsmax.transformtypein"
	bl_label = "Transform Type-in"
	pos_abs_x: FloatProperty(name="X")
	pos_abs_y: FloatProperty(name="Y")
	pos_abs_z: FloatProperty(name="Z")
	pos_off_x: FloatProperty(name="X")
	pos_off_y: FloatProperty(name="Y")
	pos_off_z: FloatProperty(name="Z")
	rot_abs_x: FloatProperty(name="X")
	rot_abs_y: FloatProperty(name="Y")
	rot_abs_z: FloatProperty(name="Z")
	rot_off_x: FloatProperty(name="X")
	rot_off_y: FloatProperty(name="Y")
	rot_off_z: FloatProperty(name="Z")
	scl_abs_x: FloatProperty(name="X")
	scl_abs_y: FloatProperty(name="Y")
	scl_abs_z: FloatProperty(name="Z")
	scl_off_x: FloatProperty(name="X",default=100)
	scl_off_y: FloatProperty(name="Y",default=100)
	scl_off_z: FloatProperty(name="Z",default=100)
	percent: FloatProperty(name="%",default=100)

	squash: BoolProperty(name="Squash")
	pos,rot,scl = [],[],[]
	objects,abss,offs = [],[],[]
	tool = None

	def draw(self, ctx):
		self.tool = ctx.workspace.tools.from_space_view3d_mode(ctx.mode,create=False).idname
		label = "" #ctx.scene.type
		layout = self.layout
		row = layout.row()
		box = row.box()
		col = box.column(align=True)
		col.label(text="Absolute:"+label)
		if len(self.objects) == 1:
			if self.tool == 'builtin.move':
				col.prop(self,"pos_abs_x")
				col.prop(self,"pos_abs_y")
				col.prop(self,"pos_abs_z")
			elif self.tool == 'builtin.rotate':
				col.prop(self,"rot_abs_x")
				col.prop(self,"rot_abs_y")
				col.prop(self,"rot_abs_z")
			elif self.tool == 'builtin.scale':
				col.prop(self,"scl_abs_x")
				col.prop(self,"scl_abs_y")
				col.prop(self,"scl_abs_z")
		if self.tool == 'builtin.scale':
			box.prop(self,"squash")
		box = row.box()
		col = box.column(align=True)
		col.label(text="Offset:"+label)
		if self.tool == 'builtin.move':
			col.prop(self,"pos_off_x")
			col.prop(self,"pos_off_y")
			col.prop(self,"pos_off_z")
		elif self.tool == 'builtin.rotate':
			col.prop(self,"rot_off_x")
			col.prop(self,"rot_off_y")
			col.prop(self,"rot_off_z")
		elif self.tool == 'builtin.scale':
			col.prop(self,"scl_off_x")
			col.prop(self,"scl_off_y")
			col.prop(self,"scl_off_z")
			col.prop(self,"percent")

		self.getdata(ctx)
		self.pos_off_x,self.pos_off_y,self.pos_off_z = 0,0,0
		self.rot_off_x,self.rot_off_y,self.rot_off_z = 0,0,0
		self.scl_off_x,self.scl_off_y,self.scl_off_z = 100,100,100
		self.percent = 100

	def update_abs(self):
		if self.tool == 'builtin.move':
			location = self.objects[0].location
			location[0] = self.pos_abs_x
			location[1] = self.pos_abs_y
			location[2] = self.pos_abs_z
		elif self.tool == 'builtin.rotate':
			rotation = self.objects[0].rotation_euler
			rotation[0] = radians(self.rot_abs_x)
			rotation[1] = radians(self.rot_abs_y)
			rotation[2] = radians(self.rot_abs_z)
		elif self.tool == 'builtin.scale':
			scale = self.objects[0].scale
			scale[0] = self.scl_abs_x / 100.0
			scale[1] = self.scl_abs_y / 100.0
			scale[2] = self.scl_abs_z / 100.0

	def update_off(self):
		for i in range(len(self.objects)):
			obj = self.objects[i]
			if self.tool == 'builtin.move':
				obj.location[0] = self.pos[i].x+self.pos_off_x
				obj.location[1] = self.pos[i].y+self.pos_off_y
				obj.location[2] = self.pos[i].z+self.pos_off_z
				
			elif self.tool == 'builtin.rotate':
				obj.rotation_euler[0] = self.rot[i].x+radians(self.rot_off_x)
				obj.rotation_euler[1] = self.rot[i].y+radians(self.rot_off_y)
				obj.rotation_euler[2] = self.rot[i].z+radians(self.rot_off_z)

			elif self.tool == 'builtin.scale':
				obj.scale[0] = self.scl[i].x*self.scl_off_x/100
				obj.scale[1] = self.scl[i].y*self.scl_off_y/100
				obj.scale[2] = self.scl[i].z*self.scl_off_z/100

				obj.scale[0] *= self.percent/100
				obj.scale[1] *= self.percent/100
				obj.scale[2] *= self.percent/100

	def check(self, ctx):
		mode = self.get_ui()
		if mode == 'abs':
			self.update_abs()
		elif mode == 'off':
			self.update_off()
		return True

	def getdata(self, ctx):
		selection = ctx.selected_objects
		if len(selection) == 1:
			location = selection[0].location
			self.pos_abs_x = location.x
			self.pos_abs_y = location.y
			self.pos_abs_z = location.z
			sre = selection[0].rotation_euler
			self.rot_abs_x = degrees(sre.x)
			self.rot_abs_y = degrees(sre.y)
			self.rot_abs_z = degrees(sre.z)
			scale = selection[0].scale
			self.scl_abs_x = scale.x * 100
			self.scl_abs_y = scale.y * 100
			self.scl_abs_z = scale.z * 100
			self.percent = 100

		self.pos,self.rot,self.scl = [],[],[]

		for obj in selection:
			self.pos.append(obj.location)
			self.rot.append(obj.rotation_euler)
			self.scl.append(obj.scale)

	def execute(self, ctx):
		return {'FINISHED'}

	def cancel(self, ctx):
		return None # {'CANCELED'}

	def get_ui(self):
		ret = "None"
		# read ui values
		abss = [self.pos_abs_x, self.pos_abs_y, self.pos_abs_z,
				self.rot_abs_x, self.rot_abs_y, self.rot_abs_z,
				self.scl_abs_x, self.scl_abs_y, self.scl_abs_z]
		offs = abss.copy() + [self.percent]

		# compar values with olders
		if len(abss) == len(self.abss):
			for i in range(len(abss)):
				if abss[i] != self.abss[i]:
					ret = "abs"
					break
		if len(offs) == len(self.offs):
			for i in range(len(offs)):
				if offs[i] != self.offs[i]:
					ret = "off"
					break

		# update values
		self.abss = abss.copy()
		self.offs = offs.copy()
		return ret
	   
	def invoke(self, ctx, event):
		self.objects = ctx.selected_objects
		self.getdata(ctx)
		self.get_ui()
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)

def register_transformtypein():
	bpy.utils.register_class(BsMax_OT_TransformTypeIn)

def unregister_transformtypein():
	bpy.utils.unregister_class(BsMax_OT_TransformTypeIn)