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

import bpy
from .q_refrence import quadmenuref
from .q_graphic import get_rectangle
from .q_items import ItemShape, ItemText



class QuadHeader:
	def __init__(self, x, y, width, text, mirror):
		global quadmenuref
		self.x = x
		self.y = y
		self.width = width
		self.height = quadmenuref.size
		self.text = text
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
		global quadmenuref

		btn_width = self.height
		btn_height = -self.height
		btn_color = quadmenuref.hover_color

		btn_x = self.x
		if self.mirror[0]:
			btn_x = self.x - self.height

		btn_y = self.y
		if self.mirror[1]:
			btn_y = self.y + self.height

		btn_v, btn_i = get_rectangle(btn_width, btn_height, btn_x, btn_y)
		button = ItemShape(btn_v, btn_i, btn_color)
		self.controllers.append(button)

		lbl_width = self.width - btn_width
		lbl_height = btn_height
		lbl_color = quadmenuref.header_color

		lbl_x = btn_x + btn_width
		if self.mirror[0]:
			lbl_x = btn_x - lbl_width
		lbl_y = btn_y

		lbl_v, lbl_i = get_rectangle(lbl_width, lbl_height, lbl_x, lbl_y)
		label = ItemShape(lbl_v, lbl_i, lbl_color)
		self.controllers.append(label)

		txt_x = lbl_x - 3
		txt_y = lbl_y - quadmenuref.size + 3
		txt_color = quadmenuref.text_color
		txt = ItemText(txt_x, txt_y, self.text, self.width, txt_color, self.mirror[0])
		self.controllers.append(txt)

	def apply(self):
		# TODO execute header action
		# seprate blue part and gray part action
		# blue call blender menu
		# gray call last action
		#print("header action " + self.text)
		# for now just call blender default
		bpy.ops.bsmax.blenderdefaultmenucall('INVOKE_DEFAULT')

	def mousehover(self, x, y, clicked):
		global quadmenuref

		sxs = self.x
		sxe = self.x + self.width
		if self.mirror[0]:
			sxs = self.x - self.width
			sxe = self.x

		sys = self.y
		sye = self.y + quadmenuref.size
		if self.mirror[1]:
			sys = self.y - quadmenuref.size
			sye = self.y 
			
		if ((sxs <= x <= sxe) and (sys <= y <= sye)):
			if clicked:
				self.apply()
			return True
		return False