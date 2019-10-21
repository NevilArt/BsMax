from .q_refrence import QuadMenuRef
from .q_graphic import get_frame
from .q_items import ItemShape

class QuadBorderFrame:
	def __init__(self, x, y, width, height, mirror):
		self.x = x
		self.y = y - height
		self.width = width
		self.height = height
		self.color = QuadMenuRef.border_color
		self.mirror = mirror
		self.controllers = []
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()

	def create(self):
		brd_x = self.x
		if self.mirror[0]:
			brd_x = self.x - self.width
		brd_y = self.y
		if self.mirror[1]:
			brd_y = self.y + self.height
		brd_width  = self.width
		brd_height = self.height
		brd_color = self.color
		brd_v, brd_i = get_frame(brd_width, brd_height, brd_x, brd_y, 1)
		border = ItemShape(brd_v, brd_i, brd_color)
		self.controllers.append(border)

	def apply(self):
		pass

	def mousehover(self, x, y, clicked):
		return False

__all__ = ["QuadBorderFrame"]