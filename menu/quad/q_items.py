import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader
from .q_refrence import QuadMenuRef

class QuadItem:
	def __init__(self, text, check, enabled, menu, action, setting):
		self.text = text
		self.check = check
		self.enabled = enabled
		self.menu = menu
		self.action = action
		self.setting = setting

	def DoAction(self):
		QuadMenuRef.action = self.action

	def OpenSetting(self):
		QuadMenuRef.action = self.setting

class ItemShape:
	def __init__(self, vertices, indices, color):
		self.vertices = vertices
		self.indices = indices
		self.color = color
		self.shader = None
		self.batch = None
		self.create()

	def update(self):
		self.shader.bind()
		self.batch = batch_for_shader(self.shader, 'TRIS', {"pos": self.vertices}, indices = self.indices)
		self.shader.uniform_float("color", self.color)
		self.batch.draw(self.shader)

	def update_lbl(self):
		pass

	def create(self):
		self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

	def mousehover(self, x, y, clicked):
		return False

class ItemText:
	def __init__(self, x, y, text, width, color, right):
		self.x = x
		self.y = y
		self.text = text
		self.size = int(QuadMenuRef.size * 0.75)
		self.right = right
		self.width = width
		self.color = color
		self.create()

	def update(self):
		pass

	def update_lbl(self):
		blf.size(0, self.size, 72)
		w, h = blf.dimensions(0, self.text)
		x = self.x + QuadMenuRef.size
		if self.right:
			x = self.x + (self.width - w - QuadMenuRef.size)
		blf.position(0, x, self.y, 0.0)
		r = self.color[0]
		g = self.color[1]
		b = self.color[2]
		a = self.color[3]
		blf.color(0, r, g, b, a)
		blf.draw(0, self.text)

	def create(self):
		pass

__all__ = ["QuadItem", "ItemShape", "ItemText"]