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
from .q_subbutton import QuadSubMenuButton
from .q_seprator import QuadSeprator
from .q_header import QuadHeader
from bpy.app import version



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
		global quadmenuref

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
				size = int(quadmenuref.size * 0.75)
				blf.size(0, size)
				w, _ = blf.dimensions(0, i.text)
				if w > width:
					width = int(w)
		width += int(quadmenuref.size * 2)

		header = QuadHeader(self.x, self.y, width, self.text, mirror)
		self.controllers.append(header)

		y_offset = quadmenuref.size

		for i in range(len(self.items)):
			item = self.items[i]
			
			if item.text == None:
				y_offset += 1
			else:
				y_offset += quadmenuref.size

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