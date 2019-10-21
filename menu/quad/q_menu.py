import blf
from .q_refrence import QuadMenuRef
from .q_border import QuadBorderFrame
from .q_button import QuadButton
from .q_subbutton import QuadSubMenuButton
from .q_seprator import QuadSeprator
from .q_header import QuadHeader

class QuadMenu:
	def __init__(self, x, y, text, items, index):
		self.x = x
		self.y = y
		self.text = text
		self.items = items
		self.index = index
		self.controllers = []
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()

	def create(self):
		mirror = (False, False)
		if self.index == 2:
			mirror = (False, True)
		elif self.index == 3:
			mirror = (True, True)
		elif self.index == 4:
			mirror = (True, False)

		# calculate the width from texts lenght
		width = 100 # minimum width is 100
		for i in self.items:
			if i.text != None:
				size = int(QuadMenuRef.size * 0.75)
				blf.size(0, size, 72)
				w, h = blf.dimensions(0, i.text)
				if w > width:
					width = int(w)
		width += int(QuadMenuRef.size * 2)

		header = QuadHeader(self.x, self.y, width, self.text, mirror)
		self.controllers.append(header)

		y_offset = QuadMenuRef.size

		for i in range(len(self.items)):
			item = self.items[i]
			
			if item.text == None:
				y_offset += 1
			else:
				y_offset += QuadMenuRef.size

			if item.text == None:
				newitem = QuadSeprator(self.x, self.y, width, y_offset, mirror)
				self.controllers.append(newitem)
			elif item.action != None:
				newitem = QuadButton(self.x, self.y, width, y_offset, item.text, item, mirror)
				self.controllers.append(newitem)
			elif item.menu != None:
				newitem = QuadSubMenuButton(self.x, self.y, width, y_offset, item.text, item.menu, mirror)
				self.controllers.append(newitem)

		BorderFrame = QuadBorderFrame(self.x, self.y, width, y_offset, mirror)
		self.controllers.append(BorderFrame)

	def mousehover(self, x, y, clicked):
		for c in self.controllers:
			c.mousehover(x, y, clicked)

__all__ = ["QuadMenu"]