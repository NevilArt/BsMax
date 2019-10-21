from .q_refrence import QuadMenuRef
from .q_graphic import get_rectangle
from .q_items import ItemShape

class QuadSeprator:
	def __init__(self, x, y, width, y_offset, mirror):
		self.x = x
		self.y = y
		self.y_offset = y_offset
		self.width = width
		self.height = 1
		self.my_x = x
		self.my_y = y - y_offset
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
		if self.mirror[0]:
			self.my_x = self.x - self.width
		if self.mirror[1]:
			self.my_y = (self.y + self.y_offset) - self.height
		brd_x = self.my_x
		brd_y = self.my_y
		brd_width  = self.width
		brd_height = self.height
		brd_color = self.color
		brd_v, brd_i = get_rectangle(brd_width, brd_height, brd_x, brd_y)
		border = ItemShape(brd_v, brd_i, brd_color)
		self.controllers.append(border)

	def apply(self):
		pass

	def mousehover(self, x, y, clicked):
		return False

__all__ = ["QuadSeprator"]