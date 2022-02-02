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

import blf
from .q_refrence import quadmenuref
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
		global quadmenuref
		mirror = self.parent.mirror
		# calculate the width from texts lenght
		width = 100 # minimum width is 100
		for i in self.items:
			if i.text != None:
				size = int(quadmenuref.size * 0.75)
				blf.size(0, size, 72)
				w,h = blf.dimensions(0, i.text)
				if w > width:
					width = int(w)
		
		width += int(quadmenuref.size * 2)

		y_offset = 0

		my_x = self.x + self.parent.width - 1
		if mirror[0]:
			my_x = self.x + 1
		my_y = self.y + quadmenuref.size + 1
		if mirror[1]:
			my_y = self.y - 1

		for i in range(len(self.items)):
			item = self.items[i]
			
			if item.text == None:
				y_offset += 1
			else:
				y_offset += quadmenuref.size

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