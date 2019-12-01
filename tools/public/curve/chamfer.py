import bpy
from bpy.types import Operator
from mathutils import Vector
from bpy.props import BoolProperty, FloatProperty
from bsmax.curve import Curve, Bezier_point
from bsmax.math import get_segment_length, split_segment, get_3_points_angle_3d, point_on_line

class BsMax_OT_CurveChamfer(Operator):
	bl_idname = "curve.chamfer"
	bl_label = "Fillet/Chamfer (Curve)"
	fillet: BoolProperty(name="Fillet:",default = False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	typein: BoolProperty(name="Type In:",default = False)
	start,finish = False,False
	curve,obj = None,None
	start_y = 0

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def chamfer(self):
		curve = self.curve
		curve.restore()
		selection = []
		for i in range(len(curve.splines)):
			sel = []
			for j in range(len(curve.splines[i].bezier_points)):
				point = curve.splines[i].bezier_points[j]
				if point.select_control_point:
					sel.append(j)
			if len(sel) > 1:
				selection.append([i,sel])
		value = abs(self.value)
		tention = 0.5 if self.fillet else 0
		for i, sel in selection:
			curve.splines[i].chamfer(sel, value, tention)
		curve.update()

	def abort(self):
		self.curve.reset()

	def execute(self, ctx):
		if self.value == 0:
			self.abort()
		else:
			self.chamfer()
		return {'FINISHED'}

	def check(self, ctx):
		if not self.start:
			self.start = True
			self.get_data(ctx)
		self.chamfer()

	def draw(self, ctx):
		layout = self.layout
		icon = 'SPHERECURVE' if self.fillet else 'LINCURVE'
		text = "Fillet" if self.fillet else "Chamfer"
		col = layout.column(align=True)
		col.prop(self,"fillet",text=text, icon=icon)
		col.prop(self,"value",text="Value")
		
	def modal(self, ctx, event):
		if event.type == 'LEFTMOUSE':
			if not self.start:
				self.start = True
				self.start_y = event.mouse_y
				self.get_data(ctx)
		if event.type == 'MOUSEMOVE':
			if self.start:
				scale = (event.mouse_y - self.start_y)
				self.value = scale / 200
				self.chamfer()
			if self.start and event.value =='RELEASE':
				self.finish = True
		if self.finish:
			if self.value == 0:
				self.abort()
			return {'CANCELLED'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			self.abort()
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
		
	def invoke(self, ctx, event):
		if self.typein:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self, width=120)
		else:
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}

def chamfer_cls(register):
	c = BsMax_OT_CurveChamfer
	if register: 
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	chamfer_cls(True)

__all__ = ["chamfer_cls"]