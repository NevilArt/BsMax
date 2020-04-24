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

from .blender import register_blenderdefault,unregister_blenderdefault
from .quad import register_quad,unregister_quad
# from .marking.init import *

class RegisterData:
	def __init__(self):
		self.pack = ''
reg = RegisterData()

def register_menu(preferences):
	unregister_menu()

	floatmenus = preferences.floatmenus
	if floatmenus == "QuadMenu_st_nokey":
		register_quad(preferences)
	elif floatmenus == "QuadMenu_st_andkey":
		register_quad(preferences)
	elif floatmenus == "Marking_Menu":
		pass
	
	reg.pack = floatmenus

def unregister_menu():
	if reg.pack == "QuadMenu_st_andkey" or reg.pack == "QuadMenu_st_nokey":
		unregister_quad()
	reg.pack = ''