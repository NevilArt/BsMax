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
##################################################################
import bpy
from bsmax.state import version

class QuadMenuRef:
	def __init__(self):
		self.action = None
		self.finish = False
		self.size = 15
		
		if version() < 310:
			# version 2.8 ~ 3.0
			self.header_color  = (0.23, 0.23, 0.23, 1.0)
			self.bg_color      = (0.27, 0.27, 0.27, 1.0)
			self.hover_color   = ( 0.0,  0.5,  1.0, 1.0)
			self.text_color    = ( 0.9,  0.9,  0.9, 1.0)
			self.text_hover    = ( 0.1,  0.1,  0.1, 1.0)
			self.text_disable  = ( 0.5,  0.5,  0.5, 1.0)
			self.border_color  = ( 0.0,  0.0,  0.0, 1.0)
		else:
			# version 3.1 ~ upper
			self.header_color  = (0.23, 0.23, 0.23, 1.0)
			self.bg_color      = (0.27, 0.27, 0.27, 1.0)
			self.hover_color   = ( 0.0,  0.5,  1.0, 1.0)
			self.text_color    = ( 0.9,  0.9,  0.9, 1.0)
			self.text_hover    = ( 0.1,  0.1,  0.1, 1.0)
			self.text_disable  = ( 0.5,  0.5,  0.5, 1.0)
			self.border_color  = ( 0.0,  0.0,  0.0, 1.0)

			# self.header_color  = (0.115, 0.115, 0.115, 1.0)
			# self.bg_color      = (0.135, 0.135, 0.135, 1.0)
			# self.hover_color   = ( 0.0,  0.25,  0.5, 1.0)
			# self.text_color    = ( 0.45,  0.45,  0.45, 1.0)
			# self.text_hover    = ( 0.05,  0.05,  0.05, 1.0)
			# self.text_disable  = ( 0.25,  0.25,  0.25, 1.0)
			# self.border_color  = ( 0.0,  0.0,  0.0, 1.0)
	
	def execute(self):
		if self.action:
			try:
				exec('bpy.ops.' + self.action)
			except:
				print("An exception occurred with: bpy.ops." + self.action)
		self.action = None
		self.finish = True

quadmenuref = QuadMenuRef()