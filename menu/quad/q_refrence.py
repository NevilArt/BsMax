import bpy, sys

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

# def getsize():
#     # | System              | Value      |
#     # |---------------------|------------|
#     # | Linux (2.x and 3.x) | linux2 (*) |
#     # | Windows             | win32      |
#     # | Windows/Cygwin      | cygwin     |
#     # | Windows/MSYS2       | msys       |
#     # | Mac OS X            | darwin     |
#     # | OS/2                | os2        |
#     # | OS/2 EMX            | os2emx     |
#     # | RiscOS              | riscos     |
#     # | AtheOS              | atheos     |
#     # | FreeBSD 7           | freebsd7   |
#     # | FreeBSD 8           | freebsd8   |
#     # | FreeBSD N           | freebsdN   |
#     # | OpenBSD 6           | openbsd6   |    

#     screensize = [1920, 1080]
#     plat = sys.platform

#     if plat == "win32":
#         import ctypes
#         user32 = ctypes.windll.user32
#         screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     elif plat == "cygwin":
#         pass
#     elif plat == "msys":
#         pass
#     elif "linux" in plat:
#         pass
#     elif plat == "darwin":
#         #import AppKit
#         #[(screen.frame().size.width, screen.frame().size.height)
#         #    for screen in AppKit.NSScreen.screens()]
#         pass
#     QuadMenuRef.size = 15

__all__ = ["QuadMenuRef"]