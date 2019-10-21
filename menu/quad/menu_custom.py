from .q_items import QuadItem

# Indexes #
# [3] [2] #
#    +    #
# [4] [1] #
###########
t, f, n = True, False, None

def seprator():
	return QuadItem(n, f, f, n, n, n)

def get_custom_submenu(ctx):
	items = []
				#  text,  check,  enabled, menu, action, setting
	action = "bpy.ops.mesh.primitive_cube_add()"
	items.append(QuadItem("Custom", f, f, n, action, n))
	return items

def get_custom_menu():
	items = []
				#  text,  check,  enabled, menu, action, setting
	items.append(QuadItem("Custom", f, f, n, "", n))
	items.append(seprator())
	submenu = get_custom_submenu(ctx)
	items.append(QuadItem("Sub Menu", f, f, submenu, n, n)) # seprator
	return items

__all__ = ["get_custom_menu" ]