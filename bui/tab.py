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
from .master.bui import BUI
from .master.graphic import Rectangle
from .master.caption import Caption
from .checkbutton import CheckButton
from .box import Box

class Tab(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)
		self.pos.auto = True
		self.size.auto = True

		""" special variables """
		self._selected = 0
		self.default = 0
		self.setup()
		owner.append(self)

	def add(self,text=""):
		""" get radio size """
		caption = Caption(None,text=text,font_size=self.caption.font_size)
		w,h = caption.size.x, caption.size.y
		index = len(self.buttons.controllers)

		button = CheckButton(self.buttons,text=text,size=[w+20,25],row=2,column=index)
		button.onclick = self.picked
		button.background.fillet.bottom_left = 0
		button.background.fillet.bottom_right = 0
		button.size.auto = False
		button.checked = len(self.buttons.controllers)-1 == self.default

		page = Box(self.pages,background=True,row=1,column=index)
		page.background.color.set((0.1,0.1,0.1,1),(0.1,0.1,0.1,1),(0.1,0.1,0.1,1))
		page.table.gap.set(2,2)
		page.border.set(3,3,3,3)
		page.enabled = button.checked

		return page
		
	def setup(self):
		self.buttons = Box(self,row=2,column=1)
		self.buttons.table.gap.set(1,0)
		self.pages = Box(self,row=1,column=1)
		self.pages.table.gap.set(2,2)

	def picked(self):
		for index,cbtn in enumerate(self.buttons.controllers):
			cbtn.checked = (cbtn == self.active)
			if cbtn.checked:
				self._selected = index
		for index,page in enumerate(self.pages.controllers):
			page.enabled = (index == self._selected)

	def click(self):
		self.owner.focus_on(self)
		if self.onclick != None:
			self.onclick()

	@property
	def selected(self):
		return self._selected
	@selected.setter
	def selected(self, selected):
		if selected != self._selected:
			if 0 < selected < len(self.buttons.controllers):
				for cbtn in self.buttons.controllers:
					cbtn.checked = False
				self.buttons.controllers[selected].checked = True
				self._selected = selected

__all__ = ["Tab"]