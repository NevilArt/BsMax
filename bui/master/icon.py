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
from .classes import Vector2,Colors

class Icon:
	def __init__(self,name):
		self.name = name
		self.scale = 1
		self.mirror = Vector2(False,False)
		self.offset = Vector2(0,0)
		self.color = Colors()
		self.vertices = []
		self.indices = []
		self.state = 0