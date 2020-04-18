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

class ProgressBar(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None,
				# Special parameters #
				percent=0):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				background=True,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)

		self.pos.auto = True

		self.percent = percent

		self.background.color.set((0.415,0.415,0.415,1),(0.415,0.415,0.415,1),(0.415,0.415,0.415,1))
		self.background.fillet.set(3,3,3,3)

		self.bar = Rectangle(self)
		self.bar.color.set((0.0,0.0,0.5,1),(0.0,0.0,0.5,1),(0.0,0.0,0.5,1))
		self.bar.align.left = True

		owner.append(self)

	def local_update(self):
		self.percent = 0 if self.percent < 0 else 100 if self.percent > 100 else self.percent
		scale = 0 if self.percent == 0 else self.percent/100
		self.bar.width = self.size.x*scale
		self.bar.height = self.size.y
		self.caption.text = str(self.percent)

__all__ = ["ProgressBar"]