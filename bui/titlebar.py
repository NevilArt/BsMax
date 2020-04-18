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

class TitleBar(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,
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
		""" public values """
		self.owner = owner
		self.size.auto = False
		self.size.set(200,30)
		self.size.limit.set(True,True)
		self.size.min.set(200,30)
		self.size.max.set(7680,4320)
		self.row = 1
		self.border.ignore = True
		self.moveable = True
		self.pos.auto = True
		self.caption.align.set(True,False,False,False,True)
		self.caption.offset.set(5,0)
		""" graphics """
		self.background.color.set((0.3,0.3,0.3,1),(0.3,0.3,0.3,1),(0.32,0.32,0.34,1))
		self.background.fillet.set(6,6,0,0)
		""" special """
		self.setup()
		owner._append(self)

	def close_btn_pressed(self):
		self.owner.destroy = True

	def fit_btn_pressed(self):
		pass

	def collaps_btn_pressed(self):
		self.owner.box.enabled = not self.owner.box.enabled
		if self.owner.box.enabled:
			self.background.fillet.set(6,6,0,0)
		else:
			self.background.fillet.set(6,6,6,6)
	
	def setup(self):
		self.box = Box(self,column=4)
		self.box.table.gap.set(2,2)
		self.box.align.set(False,True,False,False,True)
		self.close_btn = Button(self.box,size=[26,26],column=3,text="X",onclick=self.close_btn_pressed)
		self.close_btn.align.set(False,True,False,False,True)
		self.fit_btn = Button(self.box,size=[26,26],column=2,text="[]",onclick=self.fit_btn_pressed)
		self.fit_btn.align.set(False,False,False,False,True)
		self.collaps_btn = Button(self.box,size=[26,26],column=1,text="_",onclick=self.collaps_btn_pressed)
		self.collaps_btn.align.set(True,False,False,False,True)

	def drag(self,x,y):
		self.owner.pos.add(x,y)

__all__ = ["TitleBar"]