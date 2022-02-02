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
from .q_graphic import get_frame
from .q_items import ItemShape



class QuadBorderFrame:
	def __init__(self, x, y, width, height, mirror):
		self.x = x
		self.y = y - height
		self.width = width
		self.height = height
		self.color = quadmenuref.border_color
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