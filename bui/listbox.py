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
from .box import Box
from .scrollbar import ScrollBar

class ListBox(BUI):
	def __init__(self,owner,pos=[0,0],size=[150,150],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				background=True,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)
		self.pos.auto = True
		self.item_height = 20
		self.list_height = 0
		self._list_height = 0
		self.full_height = 0
		self.items = []
		self.first = 0
		self.size_y = 0
		self.setup()
		owner.append(self)
	
	def setup(self):
		self.get_height()
		scroll_size = 15
		x,y = self.size.x, self.size.y
		self.itembox = Box(self,size=[x-scroll_size,y],column=1,row=2)
		self.itembox.table.gap.set(0,0)
		self.scroll_v = ScrollBar(self,size=[scroll_size,y],column=2,row=2,vertical=True,buttons=True)
		self.scroll_h = ScrollBar(self,size=[x,scroll_size],column=1,row=1,vertical=False,buttons=False)
		self.update_rows()
	
	def get_height(self):
		if self.size_y != self.size.y:
			self.list_height = int(self.size.y / self.item_height)
			self.full_height = len(self.items) * self.item_height
			self.size_y = self.size.y

	def update_rows(self):
		self.get_height()
		self.scroll_v.enabled = (len(self.items) > self.list_height)
		if self.scroll_v.enabled:
			self.scroll_v.size.y = self.size.y
		self.scroll_h.enabled = False
		if self.list_height != self._list_height:
			self.itembox.controllers.clear()
			w = self.size.x if not self.scroll_v.enabled else self.size.x - 20
			h = 20
			for i in range(self.list_height):
				newbox = Box(self.itembox,background=True,size=[w,h],
						column=1,row=i,onclick=self.item_clicked)
				newbox.background.color.c = (0.5,0.5,0.9,1)
				newbox.caption.align.left = True
			self._list_height = self.list_height
		
	def local_update(self):
		self.update_rows()
		last = len(self.items)
		for i in range(self.list_height):
			index = self.first + i
			self.itembox.controllers[i].caption.text = self.items[index] if index < last else ""
	
	def slide(self,value):
		self.first += value
		if self.first < 0:
			self.first = 0
		maxval = len(self.items) - self.list_height
		if self.first > maxval:
			self.first = maxval

	def item_clicked(self):
		print(self.active.caption.text)

__all__ = ["ListBox"]