
# BsMax_2_80

(Works on Blender 2.80 ~ 2.90)

Recent Updates

* Some minor bug fixing.
* "Link to" operator updated (for now search the 'Link to' operator).
* Align objects draws a line to show the tool is active.
* All Operators has self report now. you can see python api of each operator in 'Info' or 'Console'.
* Time keys now working on all areas ('N' ',' '.' '/' 'Home' 'End' in Max mode)
* '[' and ']' defined to Left and Right Tool panel open/close toggle (Max Mode only).
* Keymap system has duplication check function.
* Press the 'W','E','R' again toggles between Global/Local coordinate (Max,Maya mode).
* light lister ignore the instance lights to simplify the list.
* "Clear primitive data" combined with "Convert to" command (Max Mode only)
* Hide/Undide updated but not fine yet (because of python limitation for now)
* Keep Prefrence settng when add-on has Disable/Enable or Updated.
* Align objects acts as 3DsMax now. (Select objects, press 'Alt + A' then pick Target).
* Transform type in fixed (Max mode F12)(Object mode only).
* (Ctrl + shift + C) Flet/chamfer in Curve Edit mode.
* (Ctrl + Tab) Multi Modifier Editor.
* UV projections added to UV Edit menu.
* Startup navigation key binding issue solved.
* Float modifire editor can match only selected modifier with selected objects if had same modifier.
* Snap automaticly changes on Move Rotate tool call viea short cut(act more max like).
* View undo can disable now (some times cause the viewport leg).
* Camera lister updated ('C' in Max mode).
* Animated primitives problem solved.
* Object Properties added to Quad menu (not perfect but some thing better than nothing).
* Split Edge added to quad menu.
* 'Z' for find active object in outliner (3DsMax mode).
* Zoom extended updated, works in edit mode too (3DsMax mode).
* Specific frames render replaced but not complete yet.
* 'p' for Perspective toggle removed, 'P' for Perspective and 'U' for Orthographic in 3DsMax Mode.
* Default key mode added to time line.
* keymap changes '7' view statistic, '8' open environment setting (in 3DsMax mode).
* PrimitiveData register error issue fixed.
* Info and Console key map update (More like 3DsMax).
* wireframe toggle restore the previews type (F3 in 3DsMax mode).
* Shader editor assign material to selected objects. (shader editor menu/ tools/ assign to selection).
* Move selected objects to active layer(collection) (header of outliner button with + icon).
* Pivot to first besierpoint for curve objects (View3D/Object/snap/Pivot to First Point).
* Assistance pack option removed and all tools puted under Tools menu on View3D.
* Light lister added (Render/Light lister).
* Keymap system optimized.
* Works on Blender 2.83 Beta.
* Camera lock toggle added to Quad menu.
* BUI added inside the BsMax will use for tools UI.
* Rightclick Droptool disabled when rightclick select is active.
* Automate animated link(child of). active animation assistance tool pack to see it.
* Float Primitive Panel can run in blender mode with out activing the 3DsMax tools.
* Mesh Primitives Update faster (for Blender 2.81 and above).
* New Extrud Mesh object added to Create/Mesh menu (Genarate a Mesh object) (Under Construction).
* Extrud shape object added to Create/Curve menu (Genarate a curve object).
* Convert to regular object added to contex menu and primitive parameters panel.
* Ask for close the Line if click on first point while drawing.
* ...