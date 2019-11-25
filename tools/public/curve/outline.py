import bpy, numpy
from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty, IntProperty
from bsmax.curve import Curve

class BsMax_OT_OutlineCurve(Operator):
	bl_idname = "curve.outlinecurve"
	bl_label = "Outline (Curve)"

	typein: BoolProperty(name="Type In:",default=False)
	value: FloatProperty(name="Value:",unit='LENGTH')
	close: BoolProperty(name="Close:",default=True)
	count: IntProperty(name="Count:",default=1)
	mirror: BoolProperty(name="Mirror:",default=False)
	curve,obj = None,None
	start,finish = False,False
	start_y = 0

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False

	def get_data(self, ctx):
		self.obj = ctx.active_object
		self.curve = Curve(self.obj)

	def get_selection(self, curve):
		selection = []
		for i in range(len(curve.splines)):
			for j in range(len(curve.splines[i].bezier_points)):
				point = curve.splines[i].bezier_points[j]
				if point.select_control_point:
					selection.append(i)
					break
		return selection

	def outline(self):
		curve = self.curve
		curve.restore()
		if self.value != 0:
			selection = self.get_selection(curve)
			for i in selection:
				curve.splines[i].set_free()
				count = 1 if self.close else self.count
				for j in range(count):
					value = self.value * (j+1)
					newspline = curve.clone(i)
					newspline.select(False)
					newspline.offset(value)
					if self.mirror and not self.close:
						mirrorspline = curve.clone(i)
						mirrorspline.select(False)
						mirrorspline.offset(-value)
						curve.splines.append(mirrorspline)
					if not curve.splines[i].use_cyclic_u and self.close:
						newspline.reverse()
						curve.join(i,newspline)
						curve.splines[i].use_cyclic_u = True
					else:
						curve.splines.append(newspline)
		curve.update()

	def abort(self):
		self.curve.reset()

	def execute(self, ctx):
		if self.value == 0:
			self.abort()
		else:
			self.outline()
		return{"FINISHED"}

	def check(self, ctx):
		if not self.start:
			self.start = True
			self.get_data(ctx)
		self.outline()

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(self,"value")
		col.prop(self,"close")
		if not self.close:
			col.prop(self,"count")
			col.prop(self,"mirror")

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
				self.outline()
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

def outline_cls(register):
	c = BsMax_OT_OutlineCurve
	if register:
		bpy.utils.register_class(c)
	else:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	outline_cls(True)

__all__ = ["outline_cls"]