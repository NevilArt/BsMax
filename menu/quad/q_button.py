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
from .q_graphic import get_rectangle, get_setting_button, get_checkmark
from .q_items import ItemShape, ItemText



class QuadButton:
	def __init__(self, x, y, width, y_offset, text, action, mirror):
		global quadmenuref
		
		self.x = x
		self.y = y
		self.y_offset = y_offset
		self.width = width
		self.height = quadmenuref.size
		self.text = text
		self.color = quadmenuref.bg_color
		self.mirror = mirror
		self.action = action
		self.button = None
		self.setting = None
		self.controllers = []
		self.x1 = x
		self.x2 = x+quadmenuref.size
		self.x3 = x+(width-quadmenuref.size)
		self.x4 = x+width
		self.y1 = y-y_offset
		self.y2 = (y+quadmenuref.size)-y_offset
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()

	def create(self):
		global quadmenuref

		if self.mirror[0]:
			self.x1 = self.x - self.width
			self.x2 = self.x1 + quadmenuref.size
			self.x3 = self.x1 + (self.width - quadmenuref.size)
			self.x4 = self.x
		if self.mirror[1]:
			self.y1 = (self.y + self.y_offset) - self.height
			self.y2 = (self.y + self.y_offset)

		# Draw setting button
		the_width = self.width
		if self.action.setting != None:
			stg_x = self.x3
			if self.mirror[0]:
				stg_x = self.x1
			stg_y = self.y1
			stg_width = self.height
			stg_height = self.height
			stg_offset = self.height * 0.15
			stg_color = quadmenuref.bg_color
			stg_icon_color = quadmenuref.border_color
			stg_v, stg_i = get_rectangle(stg_width, stg_height, stg_x, stg_y)
			self.setting = ItemShape(stg_v, stg_i, stg_color)
			self.controllers.append(self.setting)
			stg_v, stg_i = get_setting_button(stg_width * 0.7, stg_x + stg_offset, stg_y + stg_offset)
			icon = ItemShape(stg_v, stg_i, stg_icon_color)
			self.controllers.append(icon)
			the_width = self.width - self.height

		# Draw body button
		btn_x = self.x1
		if self.mirror[0]:
			if self.action.setting == None:
				btn_x = self.x1
			else:
				btn_x = self.x2
		btn_y = self.y1
		btn_width = the_width
		btn_height = self.height
		btn_color = quadmenuref.bg_color
		btn_v, btn_i = get_rectangle(btn_width, btn_height, btn_x, btn_y)
		self.button = ItemShape(btn_v, btn_i, btn_color)
		self.controllers.append(self.button)

		# Draw Check mark
		if self.action.check:
			chk_x = self.x1
			if self.mirror[0]:
				chk_x = self.x3
			chk_y = self.y1
			chk_offset = self.height * 0.15
			chk_width = self.height * 0.7
			chk_color = quadmenuref.border_color
			chk_v, chk_i = get_checkmark(chk_width,chk_x+chk_offset,chk_y+chk_offset)
			check = ItemShape(chk_v, chk_i, chk_color)
			self.controllers.append(check)

		txt_x = btn_x
		if self.mirror[0] and self.action.setting != None:
			txt_x = btn_x - self.height
		txt_y = btn_y + 5
		txt_color = quadmenuref.text_color
		if not self.action.enabled:
			txt_color = quadmenuref.text_disable
		txt = ItemText(txt_x,txt_y,self.text,self.width,txt_color,self.mirror[0])
		self.controllers.append(txt)

	def mousehover(self, x, y, clicked):
		ssx = self.x3
		sex = self.x4
		bsx = self.x1
		bex = self.x3
		if self.mirror[0]:
			ssx = self.x1
			sex = self.x2
			bsx = self.x2
			bex = self.x4
		# No setting button
		if self.setting == None:
			if ((self.x1 <= x <= self.x4) and (self.y1 <= y <= self.y2)):
				self.button.color = quadmenuref.hover_color
				if clicked and self.action.enabled:
					self.action.DoAction()
				return True
			else:
				self.button.color = quadmenuref.bg_color
			return False
		# has seting button
		else:
			if ((bsx <= x <= bex) and (self.y1 <= y <= self.y2)): 
				self.button.color = quadmenuref.hover_color
				if clicked and self.action.enabled:
					self.action.DoAction()
			else:
				self.button.color = quadmenuref.bg_color
			if ((ssx  < x <= sex) and (self.y1 <= y <= self.y2)):
				self.setting.color = quadmenuref.hover_color
				if clicked and self.action.enabled:
					self.action.OpenSetting()
			else:
				self.setting.color = quadmenuref.bg_color