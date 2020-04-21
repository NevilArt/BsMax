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

from .assistant import register_assistant,unregister_assistant
from .public import public_cls
from .special import special_cls

def register_tools(pref):
	register_assistant()
	public_cls(True,pref)
	special_cls(True,pref)

def unregister_tools(pref):
	unregister_assistant()
	public_cls(False,pref)
	special_cls(False,pref)

def tools_cls(reg, pref):
	if reg:
		register_tools(pref)
	else:
		unregister_tools(pref)