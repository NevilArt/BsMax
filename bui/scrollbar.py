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
from .button import Button

class ScrollBar(BUI):
	def __init__(self,owner,pos=[0,0],size=[20,20],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None,
				# special argoments #	
				vertical=True,buttons=False):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				background=True,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)
		self.pos.auto = True
		self.vertical = vertical
		self.buttons = buttons
		self.background.color.set((0.3,0.3,0.3,1),(0.3,0.3,0.3,1),(0.3,0.3,0.3,1))
		self.setup()
		owner.append(self)
	
	def set_size(self):
		if self.vertical:
			r = w = self.size.x
			h = self.owner.size.y - r*2 if self.buttons else self.owner.size.y
		else:
			r = h = self.size.y
			w = self.owner.size.x - r*2 if self.buttons else self.owner.size.x
		self.box.size.set(w,h)

	def setup(self):
		if self.vertical:
			c1,c2,c3, r1,r2,r3 = 1,1,1, 3,2,1 
			l1,l2 = '^','v'
			r = self.size.x
		else:
			c1,c2,c3, r1,r2,r3 = 1,2,3, 1,1,1
			l1,l2 = '<','>'
			r = self.size.y

		if self.buttons:
			Button(self, size=[r,r], text=l1, column=c1, row=r1, onclick=self.start_btn_clicked)		
			Button(self, size=[r,r], text=l2, column=c3, row=r3, onclick=self.end_btn_clicked)

		self.box = Box(self, size=[1,1], column=c2, row=r2, background=True)
		self.set_size()
		self.slider_btn = Button(self.box, size=[r,r], ondrag=self.slider_btn_draged)
		self.slider_btn.pos.auto = False
		self.slider_btn.moveable = True
	
	def start_btn_clicked(self):
		self.owner.slide(-1)
	def slider_btn_draged(self,x,y):
		pass
	def end_btn_clicked(self):
		self.owner.slide(1)

	def local_update(self):
		self.set_size()
		if self.vertical:
			len = self.owner.size
			l = self.size

__all__ = ["ScrollBar"]