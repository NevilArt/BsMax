
# BsMax_2_80

(Works on Blender 2.80 ~ 2.91)

Recent Updates

* Align Objects has better UI and able to Align Objects to Bone of Armature too.
* Primitive Geometries create and update with Shade Smooth active.
* Join (ctrl+J) clear primitive data now.
* Object display setiing assined to 'Alt+X'.
* Path Sort Operator updated (Select objects call the operator then pick path)
* PickOperator bug fixed.
* Linkto Operator now can link Object directly to a bone.
* PickOperator updated, now can return source, subsource, target and subtarget.
* New Hotkeys added to weight paint and File Browser (Max mode only).
* Camera search any object display filter toggle Keymaps added for paint/sculp modes too.
* Timeline Red header issue fixed.
* Path Constraint setting up a "Follow Path" in two clicks and set the key frame on Object rather than the path.
* Parent Constraint in object mode can directly parent the Objects to the Bone rather than Armature.
* View3D/Tools/Animation Max like Constraints tools added.
* In Pose mode Doubleclick Select All children.
* if you dont like the infinit gride then press 'G' to have a limited one.
* Jotstick connector updated for work with new Joystick creator.
* Joystick creator made a controller from Armatur can be join with rigg
* Pose menu added to Quadmenu and some Keymap added for Pose mode.
* Select Element enabled for Curve mode too ('5' Toggle On/Off)
* Select Element enabled for 3DsMax mode ('5' Toggle On/Off, 'Ctrl + 5' Open Setting Dialog)
* Open the keymaps list in github wiki via addon preferences (In production).
* Preferences UI changed, more optional and easy to understand.
* Quad menu can scale from addon preferences.
* lots of code cleaning and Simplification to make future improvment easy.
* Align Objects has percentage option now and can put in halfway or increase distance by entering negative value.
* Some New Items added to Quad menu.
* "Link to" operator (Avalible in Quadmenu).
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
* ...