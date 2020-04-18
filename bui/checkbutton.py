############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

from .master.bui import BUI
from .master.graphic import Rectangle

# custom controller -------------------------------------------
class CheckButton(BUI):
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

		self.pos.limit.set(True,True)
		self.pos.max.set(7680,4320)
		self.pos.auto = True
		self.size.limit.set(True,True)
		self.size.min.set(size[0],size[1])
		self.size.default.set(size[0],size[1])
		self.size.max.set(7680,4320)
		
		self.background.fillet.set(6,6,6,6)
		self.background.color.set((0.345,0.345,0.345,1),(0.415,0.415,0.415,1),(0.474,0.620,0.843,1))

		self.checked = False
		self.setup()
		owner.append(self)

	def click(self):
		self.checked = not self.checked
		self.owner.focus_on(self)
		if self.onclick != None:
			self.onclick()

	def local_update(self):
		if self.checked:
			self.state = 2
		else:
			self.state = 0

__all__ = ["CheckButton"]