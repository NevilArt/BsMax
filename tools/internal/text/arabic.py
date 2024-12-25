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
# 2024/07/14

#TODO seprator like dot makes pereview character apear as Initial or Medial

import bpy

from bpy.types import Operator
from bpy.props import StringProperty


def is_arabic_char(char):
	# Unicode range for Arabic characters
	return 0x0600 <= ord(char) <= 0x06FF


def contains_arabic(text):
	for char in text:
		if is_arabic_char(char):
			return True
	return False


def separate_arabic_non_arabic(text):
	parts = []
	current_part = ""
	is_current_part_arabic = None

	for char in text:
		is_arabic = is_arabic_char(char)
		is_space = char.isspace()

		if is_space:
			current_part += char
			continue
		
		if is_current_part_arabic is None:
			is_current_part_arabic = is_arabic

		if is_arabic == is_current_part_arabic:
			current_part += char
		else:
			parts.append(current_part)
			current_part = char
			is_current_part_arabic = is_arabic

	if current_part:
		parts.append(current_part)

	return parts


# Isolated, Initial, Medial, Final
arabic_positional_forms = {
	'\u0622': ('\u0622', '\u0622', '\uFE82', '\uFE82'),  # آ
	'\u0627': ('\uFE8D', '\uFE8D', '\uFE8E', '\uFE8E'),  # ا
	'\u0628': ('\uFE8F', '\uFE91', '\uFE92', '\uFE90'),  # ب
	'\u062A': ('\uFE95', '\uFE97', '\uFE98', '\uFE96'),  # ت
	'\u067E': ('\uFB56', '\uFB58', '\uFB59', '\uFB57'),  # پ
	'\u062B': ('\uFE99', '\uFE9B', '\uFE9C', '\uFE9A'),  # ث
	'\u062C': ('\uFE9D', '\uFE9F', '\uFEA0', '\uFE9E'),  # ج
	'\u0686': ('\uFB7A', '\uFB7C', '\uFB7D', '\uFB7B'),  # چ
	'\u062D': ('\uFEA1', '\uFEA3', '\uFEA4', '\uFEA2'),  # ح
	'\u062E': ('\uFEA5', '\uFEA7', '\uFEA8', '\uFEA6'),  # خ
	'\u062F': ('\uFEA9', '\uFEA9', '\uFEAA', '\uFEAA'),  # د
	'\u0630': ('\uFEAB', '\uFEAB', '\uFEAC', '\uFEAC'),  # ذ
	'\u0631': ('\uFEAD', '\uFEAD', '\uFEAE', '\uFEAE'),  # ر
	'\u0632': ('\uFEAF', '\uFEAF', '\uFEB0', '\uFEB0'),  # ز
	'\u0698': ('\u0698', '\uFB8A', '\uFB8B', '\uFB8B'),  # ژ
	'\u0633': ('\uFEB1', '\uFEB3', '\uFEB4', '\uFEB2'),  # س
	'\u0634': ('\uFEB5', '\uFEB7', '\uFEB8', '\uFEB6'),  # ش
	'\u0635': ('\uFEB9', '\uFEBB', '\uFEBC', '\uFEBA'),  # ص
	'\u0636': ('\uFEBD', '\uFEBF', '\uFEC0', '\uFEBE'),  # ض
	'\u0637': ('\uFEC1', '\uFEC3', '\uFEC4', '\uFEC2'),  # ط
	'\u0638': ('\uFEC5', '\uFEC7', '\uFEC8', '\uFEC6'),  # ظ
	'\u0639': ('\uFEC9', '\uFECB', '\uFECC', '\uFECA'),  # ع
	'\u063A': ('\uFECD', '\uFECF', '\uFED0', '\uFECE'),  # غ
	'\u0641': ('\uFED1', '\uFED3', '\uFED4', '\uFED2'),  # ف
	'\u0642': ('\uFED5', '\uFED7', '\uFED8', '\uFED6'),  # ق
	'\u0643': ('\uFED9', '\uFEDB', '\uFEDC', '\uFEDA'),  # ك
	'\u06A9': ('\uFB8E', '\uFEDB', '\uFEDC', '\uFB8F'),  # ک
	'\u06AF': ('\uFB92', '\uFB94', '\uFB95', '\uFB93'),  # گ
	'\u0644': ('\u0644', '\uFEDF', '\uFEE0', '\uFEDE'),  # ل
	'\u0645': ('\uFEE1', '\uFEE3', '\uFEE4', '\uFEE2'),  # م
	'\u0646': ('\uFEE5', '\uFEE7', '\uFEE8', '\uFEE6'),  # ن
	'\u0647': ('\uFEE9', '\uFEEB', '\uFEEC', '\uFEEA'),  # ه
	'\u0648': ('\uFEED', '\uFEED', '\uFEEE', '\uFEEE'),  # و
	'\u06CC': ('\u06CC', '\uFBFE', '\uFBFF', '\uFBFD'),  # ی
	'\u064A': ('\uFEF1', '\uFEF3', '\uFEF4', '\uFEF2'),  # ي
	'\u0626': ('\u0626', '\uFE8C', '\uFE8C', '\uFE8A'),  # ئ
}


non_connecting_chars = {
	'\u0627', '\u062F', '\u0630', '\u0631',
	'\u0632', '\u0648', '\u0622', '\u0698'
}


def get_positional_forms(char, index):
	if char in arabic_positional_forms:
		return arabic_positional_forms[char][index]
	return char


def convert_arabic_text_for_display(text):
	converted_text = ""
	prev_char_non_connecting = False

	for i, char in enumerate(text):
		if not is_arabic_char(char):
			converted_text += char
			prev_char_non_connecting = False
			continue
		
		if prev_char_non_connecting or i == 0 or not is_arabic_char(text[i - 1]):
			if i == len(text) - 1 or not is_arabic_char(text[i + 1]):
				form = get_positional_forms(char, 0)  # Isolated
			else:
				form = get_positional_forms(char, 1)  # Initial

		elif i == len(text) - 1 or not is_arabic_char(text[i + 1]):
			form = get_positional_forms(char, 3)  # Final

		else:
			form = get_positional_forms(char, 2)  # Medial
		
		converted_text += form
		prev_char_non_connecting = char in non_connecting_chars

	return converted_text[::-1]



def arabic_text_correction(text):
	if not contains_arabic(text):
		return text
	
	parts = separate_arabic_non_arabic(text)
	parts = [parts[i] for i in range(len(parts) - 1, -1, -1)]

	new_text = ""
	for part in parts:
		is_arabic = is_arabic_char(part[0])
		if is_arabic:
			new_text += convert_arabic_text_for_display(part)
		else:
			new_text += part

	return new_text


class Text_OT_Farsi_Arabic_Corrector(Operator):
	bl_idname = 'text.farsi_arabic_corrector'
	bl_label = "ّFarsi & Arabic Corrector"
	bl_description = "Correted text will copy to clipboard"
	
	text: StringProperty(
		name="Text",
		default="",
		description=""
	) # type: ignore

	def draw(self, _):
		layout = self.layout
		layout.label(text=arabic_text_correction(self.text))
		layout.prop(self, 'text', text="")
		layout.label(text="(Click on emtry space of this dialog to see preview)")
		layout.label(text="(Press ok then past text anywhere)")

	def execute(self, ctx):
		ctx.window_manager.clipboard = arabic_text_correction(self.text)
		return {'FINISHED'}
	
	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self, width=600)


def arabic_type_menu(self, ctx):
	self.layout.operator(
		'text.farsi_arabic_corrector', text="Farsi & Arabic Type Corrector",
		icon='OUTLINER_DATA_GP_LAYER'
	)


def register_arabic():
	bpy.utils.register_class(Text_OT_Farsi_Arabic_Corrector)
	bpy.types.DATA_PT_font.prepend(arabic_type_menu)
	bpy.types.SEQUENCER_PT_effect_text_style.prepend(arabic_type_menu)


def unregister_arabic():
	bpy.types.SEQUENCER_PT_effect_text_style.remove(arabic_type_menu)
	bpy.types.DATA_PT_font.remove(arabic_type_menu)
	bpy.utils.unregister_class(Text_OT_Farsi_Arabic_Corrector)


if __name__ == '__main__':
	register_arabic()