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

import bpy,sys

class QuadMenuRef:
	action = None
	finish = False
	size = 15
	header_color  = (0.23, 0.23, 0.23, 1.0) 
	bg_color      = (0.27, 0.27, 0.27, 1.0)
	hover_color   = ( 0.0,  0.5,  1.0, 1.0)
	text_color    = ( 0.9,  0.9,  0.9, 1.0)
	text_hover    = ( 0.1,  0.1,  0.1, 1.0)
	text_disable  = ( 0.5,  0.5,  0.5, 1.0)
	border_color  = ( 0.0,  0.0,  0.0, 1.0)

	def execute():
		QuadMenuRef.finish = True
		if QuadMenuRef.action != None:
			action = QuadMenuRef.action
			QuadMenuRef.action = None
			try:
				exec(action)
			except:
				print("An exception occurred with " + action)