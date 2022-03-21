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
from .classes import Vector2,Border,Edge

def get_area(self):
	if self.owner != None:
		lenght,size,border = self.owner.size,self.size,self.owner.border
		sx = border.left
		sy = border.bottom
		lx = lenght.x-(border.left+border.right+size.x)
		ly = lenght.y-(border.bottom+border.top+size.y)
	else:
		sx,sy = 0,0
		lx,ly = 7680,4320
	""" return start, end, lenght """
	return Vector2(sx,sy),Vector2(sx+lx,sy+ly),Vector2(lx,ly)

class Cell:
	def __init__(self):
		self.controllers = []
		self.size = Vector2(0,0)
		self.pos = Vector2(0,0)
	def get_max_size(self):
		x,y = 0,0
		for c in self.controllers:
			if c.enabled:
				x,y = max(c.size.x,x),max(c.size.y,y)
		return Vector2(x,y)
	def set_owner_pos(self):
		for c in self.controllers:
			if c.enabled:
				s,e,l = get_area(c)
				if c.pos.auto:
					if c.align.any():
						p = c.align.get_location(c,c.owner)
						c.pos.set(p.x,p.y)
					else:
						c.pos.set(self.pos.x,self.pos.y)
				else:
					if c.owner != None and not c.table.ignore:
						c.pos.min.set(s.x,s.y)	
						c.pos.max.set(e.x,e.y)

class Table:
	def __init__(self, owner):
		self.owner = owner
		self.auto = owner.size.auto
		self.controllers = owner.controllers
		self.cells = [] # 2D rows X columns
		self._size = Vector2(0,0)
		self.gap = Vector2(0,0)
		self.border = Border(0,0,0,0)
		self.ignore = False

	def create(self):
		self._size.set(0,0)
		""" get biget number in each direction """
		rows = [c.row for c in self.controllers]
		lastrow = max(rows) if len(rows) > 0 else 0
		cols = [c.column for c in self.controllers]
		lastcol = max(cols) if len(cols) > 0 else 0

		""" create a 2d variable sheet """
		self.cells = [[Cell() for x in range(lastcol+1)] for y in range(lastrow+1)]
		
		""" put controllers inside the sheet """
		for c in self.controllers:
			self.cells[c.row][c.column].controllers.append(c)

	def get_column(self,index):
		column = []
		if len(self.cells) > 0:
			if index < len(self.cells[0]):
				for row in self.cells:
					column.append(row[index])
		return column

	def get_row(self,index):
		row = []
		if index < len(self.cells):
			for r in self.cells[index]:
				row.append(r)
		return row

	def get_cell(self,column,row):
		if row < len(self.cells) > 0:
			if column < len(self.cells[0]) > 0:
				return self.cells[row][column]
		return Cell()

	def get_table_dimension(self):
		rows = len(self.cells)
		columns = len(self.cells[0]) if rows > 0 else 0
		return columns,rows

	def arrange_sizes(self):
		cols,rows = self.get_table_dimension()
		for i in range(cols):
			maxwidth,column = 0,self.get_column(i)
			for cell in column:
				maxwidth = max(maxwidth,cell.get_max_size().x)
			for cell in column:
				cell.size.x = maxwidth
		for i in range(rows):
			maxheight,row = 0,self.get_row(i)
			for cell in row:
				maxheight = max(maxheight,cell.get_max_size().y)
			for cell in row:
				cell.size.y = maxheight

	def fit_owner(self):
		if len(self.cells) > 0:
			if self.owner.size.auto:
				self.owner.size.set(self._size.x,self._size.y)

	def fit_children(self):
		for row in self.cells:
			for cell in row:
				cell.set_owner_pos()

	def update(self):
		""" update sub cells first """
		for row in self.cells:
			for cell in row:
				for c in cell.controllers:
					c.table.update()

		self.arrange_sizes()
		cols,rows = self.get_table_dimension()
		x,y = 0,0

		border = Edge(0,0,0,0) if self.owner.border.ignore else self.border

		for i in range(cols):
			y = border.bottom #+self.gap.y
			for cell in self.get_column(i):
				cell.pos.y = y
				y += cell.size.y+self.gap.y
			y += border.top
		self._size.y = y

		for i in range(rows):
			x = border.left #+self.gap.x
			for cell in self.get_row(i):
				cell.pos.x = x
				x += cell.size.x+self.gap.x
			x += border.right
		self._size.x = x

		self.fit_owner()
		self.fit_children()

	@property
	def size(self):
		if self.auto:
			self.update()
		return self._size

	@size.setter
	def size(self, newsize):
		self._size.set(newsize.x,newsize.y)

	def set(self,x,y):
		self._size.x.set(x,y)

__all__ = ["Table"]