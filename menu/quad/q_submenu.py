import blf
from .q_refrence import QuadMenuRef
from .q_border import QuadBorderFrame
from .q_button import QuadButton
from .q_seprator import QuadSeprator
from .q_subbutton import * # QuadSubMenuButton

class QuadSubMenu:
	def __init__(self, x, y, items, parent):
		self.x = x
		self.y = y
		self.items = items
		self.parent = parent
		self.controllers = []
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()

	def create(self):
		mirror = self.parent.mirror
		# calculate the width from texts lenght
		width = 100 # minimum width is 100
		for i in self.items:
			if i.text != None:
				size = int(QuadMenuRef.size * 0.75)
				blf.size(0, size, 72)
				w,h = blf.dimensions(0, i.text)
				if w > width:
					width = int(w)
		
		width += int(QuadMenuRef.size * 2)

		y_offset = 0

		my_x = self.x + self.parent.width - 1
		if mirror[0]:
			my_x = self.x + 1
		my_y = self.y + QuadMenuRef.size + 1
		if mirror[1]:
			my_y = self.y - 1

		for i in range(len(self.items)):
			item = self.items[i]
			
			if item.text == None:
				y_offset += 1
			else:
				y_offset += QuadMenuRef.size

			#item(text, check, menu, action, setting)
			if item.text == None:
				newseprator = QuadSeprator(my_x, my_y, width, y_offset, mirror)
				self.controllers.append(newseprator)
			elif item.action != None:
				newbutton = QuadButton(my_x, my_y, width, y_offset, item.text, item, mirror)
				self.controllers.append(newbutton)
			elif item.menu != None:
				newsubmenu = QuadSubMenuButton(my_x, my_y, width, y_offset, item.menu, mirror)
				self.controllers.append(newsubmenu)

		BorderFrame = QuadBorderFrame(my_x, my_y, width, y_offset, mirror)
		self.controllers.append(BorderFrame)

	def mousehover(self, x, y, clicked):
		# return is mouse over the sub menu
		ret = False
		for c in self.controllers:
			res = c.mousehover(x, y, clicked)
			if res:
				ret = True
		return ret

__all__ = ["QuadSubMenu"]