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

# Breke given string to lines add tab to first of any line combine and return
def tab(string, count=1):
	return string

def block(name, body, keys=[]):
	if type(body) == str:
		return '<' + name + '>' + body + '</' + name + '>\n'
	
	if type(body) == list:
		if body:
			s = '<' + name + '>'
	
			for b in body:
				s += tab(b) + '\n'
	
			s += '</' + name + '>\n'
	
			return s
		
		else:
			return '<' + name + '/>\n'
	
	return ''