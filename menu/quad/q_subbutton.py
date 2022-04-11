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

from .q_refrence import quadmenuref
from .q_graphic import get_rectangle, get_arrow
from .q_items import ItemShape, ItemText
from .q_submenu import QuadSubMenu



class QuadSubMenuButton:
	def __init__(self, x, y, width, y_offset, text, items, mirror):
		global quadmenuref
		self.x = x
		self.y = y
		self.y_offset = y_offset
		self.width = width
		self.height = quadmenuref.size
		self.text = text
		self.color = quadmenuref.bg_color
		self.mirror = mirror
		self.items = items
		self.button = None
		self.submenue = None
		self.controllers = []
		self.my_x = x
		self.my_y = y-y_offset
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()
		if self.submenue != None:
			self.submenue.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()
		if self.submenue != None:
			self.submenue.update_lbl()

	def create(self):
		global quadmenuref
		# Draw body button
		if self.mirror[0]:
			self.my_x = self.x - self.width
		self.my_y = self.y - self.y_offset
		if self.mirror[1]:
			self.my_y = self.y + (self.y_offset - quadmenuref.size)
			
		btn_x = self.my_x
		btn_y = self.my_y
		btn_width = self.width
		btn_height = self.height
		btn_color = quadmenuref.bg_color
		btn_v, btn_i = get_rectangle(btn_width, btn_height, btn_x, btn_y)
		self.button = ItemShape(btn_v, btn_i, btn_color)
		self.controllers.append(self.button)

		# Draw Arrow mark
		arr_x = self.my_x + (self.width - self.height)
		if self.mirror[0]:
			arr_x = self.my_x
		arr_y = self.my_y
		arr_mirror = self.mirror[0]
		arr_offset = self.height * 0.15
		arr_width = self.height * 0.7
		arr_color = quadmenuref.border_color
		arr_v, arr_i = get_arrow(arr_width, arr_x + arr_offset,
								arr_y + arr_offset, arr_mirror)
		icon = ItemShape(arr_v, arr_i, arr_color)
		self.controllers.append(icon)

		txt_x = btn_x
		if self.mirror[0]:
			txt_x = btn_x - self.height
		txt_y = btn_y + 5
		txt_color = quadmenuref.text_color
		txt = ItemText(txt_x, txt_y, self.text, self.width, txt_color, self.mirror[0])
		self.controllers.append(txt)

	def apply(self):
		self.action.DoAction()

	def mousehover(self, x, y, clicked):
		global quadmenuref
		if ((self.my_x <= x <= self.my_x + self.width) and \
			 (self.my_y <= y <= self.my_y + self.height)):

			self.button.color = quadmenuref.hover_color
			self.submenue = QuadSubMenu(self.my_x, self.my_y, self.items, self)

		else:
			self.button.color = quadmenuref.bg_color

			if self.submenue != None:
				if not self.submenue.mousehover(x, y, clicked):
					self.submenue = None