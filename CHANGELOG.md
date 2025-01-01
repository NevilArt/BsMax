# 0, 1, 3, 20241226
* Marker Copy/Paste added.
* Render preset tool updated.

# 0, 1, 3, 202408234
* Topo Symmetrize tool that keep UV data (under the EditMesh/Mesh menu)
* Camera target select search from last constraint and ignore disable ones this makes better result.
* Alingt Target to camera matchs the target to camera direction (Camera/Target/Align).
* Command panel Instancer warning issue fixed.
* Batch Rename for VSE issue fixed.
* Place for Farsi arabic type corrector.

# 0, 1, 3, 20240714
* Multi object Connector for geometry node (select objects in viewport in node editor active node that has object input sokets and run Auto object picker).
* Farsi and Arabic typing tool (only apears in seach menu "Farsi & Arabic Corrector") (type text press OK and paste your text any where you need).
* Auto rename shifted markers to frame number (timeline marker/auto rename).
* "Delete Animation" operator shapekey bug fixed.
* Codes for older than Blender 3.6 removed.
* blender_manifest.toml file removed from github version and became a normal addon again. 

# 0, 1, 3, 20240701
* BsMax on Blender 4.2 is not shown as legesy any more.
* Render preset Save/Load update, bugfix and adapted for new EEVEE.
* Add object Validate to Cleanup tools list too and bug fixed.
* In outliner rightclick menu link collection to other scene Operator added.
* Qaudmenu Delete Animation operator improved and can clear all animation data rather than only key frames of Object itself and ignor all subchanels.
* New Delete Animation operator (View3D/Object/Animation/Delete Animation).
* All Curve edit tools Has written again (Some not complete yet).
* Curve Select by Length, Count and Close has Set, Extend and Substract mode.
* Divide plus, Refine, Breake, Make first are ready but there is some issues on Merg by distance and Boolean yet and trying fo fix.

# 0, 1, 2, 20240605
* Kemap issues from last update fixed.
* GraphEditor select chanels auto hide unselected chanels (3DsMax Mode).
* Copy Camera animation to other softwares (Alpha version yet).
* Export Camera via Alembic do not transfer FOV animation. this tool helps to port fov and other animations to 3DsMax scene (Maya option is on the way too).

# 0, 1, 2, 20240603
* Join plus issue with None mesh object fixed.
* Mouse Weel up/down in edit mode select more and less (3DsMax & Blender adapted).
* Bone Hierarchy selection tool error on None Armatour selected in pose mode fixed.
* Link/Append/Import added to Add menu for speed up work flow (Shift+A).
* Cylinder pirimitive issue with bevel modifier when slice is on fixed.
* Code cleaning and some other minor bug fixed.

# 0, 1, 2, 20240527
* Backburner submiter has some updates
* 1. custom Repository directory option.
* 2. Incremental number to repository file rather than random number.
* 3. Use jobname as repository file name optional.
* 4. Automaticaly add scene and viewlayer name to jobname if was more then one.
* Geometry data clean stuff add that work on multiple object rather then only active object.(View3D/Object/Clean Up/ ...)
* "Freeze on" repeat calculation issue fixed. (Tools/Animation/...)

# 0, 1, 2, 20240523
* Create Primitive naming issue fixed.
* Smart loop bug fixed.
* Batch rename issue fixed.
* Instancer bug fixed.

# 0, 1, 2, 20240520
* Align Object issues from last update fixed.
* Mesh to hair guid pre setup operator added 
* Some update for Blender 4.2 compatibliti.
* Menu and Operator search keymaps swaped. (X for menu, Ctrl+Shift+Alt+X for Operator)

# 0, 1, 2, 20240508
* A global Bound box calculator Created (for now only Align object use it).
* Align Object updated and detects more object bound rather than only Mesh and Curve (develop continue till support all types).
* "Image Crop" node group added to shader editor that lets tiling only cropped part of the image [watch Here](https://youtu.be/W9LHtzHNxWE).

# 0, 1, 2, 20240422
* Armature auto bone alignment tool (Tools/Rig/Auto Bone Alignment).
* Code cleaning and some bug fixed.

# 0, 1, 2, 20240408
* Primitive issue with new change of  blender 4.1 mostly fixed.
* Link to operator has new option to keep hierarchy (Option appears only if selection has hierarchy).
* In 3DsMax key maps in Blender 4.1+ additional key removed and uses Blender default "K" in 3D view and pose mode.
* And many code Cleaneng.

# 0, 1, 2, 20240326
* Some new tools added under Command Panel modifier list.
* Make unique tool optimized (View3D/Object/Relation/Make unigue).
* Basic Auto EXR connector added but need to more work on it 

# 0, 1, 2, 20240314
* Command Panel Modifier list updated.
* Some more compatibility with Blender 4.1Beta

# 0, 1, 2, 20240304
* Render preset save load clened up, need some more correction yet.
* Command panel Display tab updated.
* Command panel Edit Curve partly added.
* Keymapbug from last update fixed.

# 0, 1, 2, 20240226
* 3DsMax Commandpanel EditPoly/Mesh panel updated alot (CP/Modifier Tab/Edit mode).
* Edit Curve and Edit modifer panel are the next.

# 0, 1, 2, 20240212
* Create primitive updated to work with Blender 4.1 too.
* 3DsMax Command panel Create stuff updated.

# 0, 1, 2, 20240208
* Primitives can be edit under "comand panel/modifiers" similar to 3DsMax.
* Light lister issue for Blender 4.0 Fixed.
* Maya Key map has some clenup and update.
* Command panel create issue fixed.

# 0, 1, 2, 20240206
* Crowds geometry node presets add to preset menu (add menu on geo node editor)
*    Crowds walking on a path.
*    Crowds in studiom.
*    Crowds taking or working groups.
*    Animals inside a fance.
*    Note: Crowds works on Blender 4.0 and above.
* 3DsMax comand panel has some improvment but still many works has to do.
* Geomeetry node Modifiers now can be add from blendeere 3.6 too.

# 0, 1, 2, 20240129
* 3DsMax Comand panel now active from prefrenses not experimental.
* More modifiers added to 3DsMax Comand panel modifier list.
* Comand Panel modifier list add to all selected objects.
* Some Crowd Tools added to view3D tool panel (More and tutorial coming soon).
* Convert Primitive to GeoNode become optinal and off by default.

# 0, 1, 2, 20240122
Many items added to 3Ds Max Side panel and so many to still need to working on.
* Some Modifiers can be add from 3Ds Max side panel.
* GeoNode modifiers appear only on Blender 4.0 and above.

# 0, 1, 2, 20240108
* 3DsMax command panel is under Construction.
* Draw Box error for Blender 3.6 and lower is fixed.

# 0, 1, 2, 20240105
* Box primitive convert to Geometrynode after Draw. (Experimental if ok will apply to all other primitives too).
* Draw primitive issue for blender 4.1 Alpha fixed.
* Some other bug fixed.

# 0, 1, 2, 20231225
* Align objects and Target weld preview line is back for Blender 4.0.
* Draw Primitives Local preview gride is back for Blender 4.0.
* Draw Primitives Abort issue in Blender 4.0 Fixed.

# 0, 1, 2, 20231210
* Backburner submiter optimized, Same functionality with less registerd operators.
* Reset operator open new empty scene with one click. (File/Reset)
* Note: You still able to add and delete defult cube from New. (File/New/General)
* Join plus rename UVs chanels if chanels count is same in surce and target objects. (Optinal)
* Quadmenu Convert to issues fixed. (3DsMax mode)
* After effect exporter is part of BsMax now (Original authors Bartek Skorupa & Damien Picard)

# 0, 1, 2, 20231127
* Backburner timeout limit issue fixed.
* Backburner submiter shows numbeer of frames are going to render, helps to avoid submit thousands of frame by mistake.
* Unfinished stuff put on experimental mode and hide by default.

# 0, 1, 2, 20230831
* Some bug fix and code cleaning done.
* Working on a new selection set for armature.

# 0, 1, 2, 20230724
* Select Children/Parent work on selected armature rather than only active one.
* Paste Pose works on selected armature rather than only active one (if all bone selected).
* Armature Selection set hold shift for add selection, hold alt for remove from selection.
* Some more future for selection I'm working on and will update soon.

# 0, 1, 2, 20230710
* Stuff and codes for older then Blender 3.3 droped.
* Daz3d to Blender armature auto renamer tool.
* Some code cleaning.

# 0, 1, 1, 20230630
* Blender 3.6 and later Parent coordinate added to quadmenu (Alt+RMB 3DsMax Mode).
* Red timeline at starup issue fixed.
* Issue with Enable/Disable addon in Blender 3.6 fixed.
* Theme changes (Camera, Empty, Light) color reset on addon disable or remove.

# 0, 1, 1, 20230628
* Just some bug fixed and new stuff that not completed yet.

# 0, 1, 1, 20230619
* Set pivot to bottom center tool replaced with Set Pivot to Base with more option.
* BsMax works on Blender 4.0 Alpha too.

# 0, 1, 1, 20230613
* Multyshapekey Tool has aditive mode if use '+' rather than '_' (need a better sorting yet).
* e.g. key+25, key+50, ... ,key+100.

# 0, 1, 1, 20230523
* Autokey Red bar issue with difrent themes fixed.
* More maxscript fixes still not completed yet.

# 0, 1, 1, 20230522
* Theme change can be disable from addon prefrence option.
* Multi Target ShapeKey tool can be inistaled as stand alone addon (requested).
* Maxscript pack inistalation issue and many of bugs fixed (need to work on it yet).
* Character to ABC maxscript tool added.
* Auto Facial GUI maxscript added (need to update and bugfix yet).

# 0, 1, 1, 20230515
* Maxscript Pack updated
Some of the tools I wrote in 2 decade working with 3DsMax collected in Bsmax/Maxscript folder I`ll add all other tools too.
The reason I put maxscript stuff inside the Blender Addon is some of tools are working directly with paralel one in Blender and has to update together.
* e.g. Copy object Transform in 3DsMax and paste on an object inside the Blender.
* e.g. Copy camera with animation inside 3DsMax or Blender and paste inside other 3DsMax, Blender or Unreal engine.
* How to use :
Drag and drop inistall.ms file in to 3DsMax viewport.
* There is no tutorial at the time but I`ll make a refrence page soon as posible.
* Almost 50 Tool update and added but need to check and more cleanup yet and some of them may not work properly yet.
* Similar Tool package for Unreal engine is on the way too.

# 0, 1, 1, 20230406
* Shader and GNode preset menu moved to end of add menu.
* 3DsMax to Blender Maxscript updated now support link constraint cameras too.

# 0, 1, 1, 20230313
* Scale parapeter added for Bolt primitive.
* GN 'Probability' node group added to GN/Tools/Append GNode Trees.
* Note: Control Colection info item propablity on 'Instance on points'.
* Connect nodegroup output to 'Instance on points' Selection.

# 0, 1, 1, 20230220
* New Bolt primitive added.
* Note: This Bolt mesh generated by internal Bolt Factory addons itself. the only additional abelty is that culd change and update parameters any time you want, not only at creating.

# 0, 1, 1, 20230214
* New QuadSphere premitive added.

# 0, 1, 1, 20230206
* New Torusknot Curve primitive added.
* Circle Curve primitive now has segment count parameter too.
* Helix primitive now has Bezier and Segment mode.

# 0, 1, 1, 20221227
* Pick DOF target depth works for Active Camera rather then Selected one.
* Parametric Primitive Object could be add from add menu too.

# 0, 1, 1, 20221212
* Camera DOF depth picker, while a camera with DOF target selected got to "View/Cameras/Pick DOF Depth" and then click on any surface to put DOF targen on it.
* [Multi shape key](https://www.youtube.com/watch?v=De3fiWcQnpA) Driver issue fixed.

# 0, 1, 1, 20221110
* Some code cleaning and bug fixing.
* 'Ctrl + Shift + W' UV editor Merg by distance.

# 0, 1, 1, 20220919
* Fillet/Chamfer mouse release issue fixed for now (this tool need to rewrite completely).
* Curve tools get_segment issue fixed (Teapot, Refine, divide and many other tools fixed).

# 0, 1, 1, 20220905
* Draw Lattice, Light prop ... height Z correction issue fix.
* Draw primitive below the grid issue fixed for now but better solution will replace soon.

# 0, 1, 1, 20220822
* 'Select Keyed Bones' (Pose Mode: Select> Select Keyed Bones).
* Set lattice in mesh edit mode added to 'Edit mode: View3d> Add' menu too.
* 'Ctrl + shift + D' Detach in Mesh Edit mode (3DsMax mode).

# 0, 1, 1, 20220815
* 'Make Unique' seprate groupe of linked/instance objects keep linked with each other (View3d> Object> relation> Make unique).
* New 'Delete' Operator keeps Children world transform when parent delete (3DsMax and Blender adaptive mode 'Delete')
* New 'Select All' operator that select all pose bones as same time (Select> All + Bones).
* Clean up the curve tools code (make ready for future updates).

# 0, 1, 1, 20220801
* 'Snapshot' operator added (View3D> object> Snapshot).
* 'Shapekey sort' Reorder shapekeys by name.
* Freeze/Unfreeze operator on quadmenu works on bone edit and pose mode too.
* Select More/Less 'Ctrl + PUp/PDown' repeat the action on hod key (3DsMax Mode).

# 0, 1, 1, 20220725
* 'View3D> Tools' menu issue in blender 3.x fixed.
* 'Bendy Bone Controller' creator tools added 'View3d> Tools> Rigg> Add BBone Control'.
* Render preset save load works for cycle x too (Render properties> Preset).

# 0, 1, 1, 20220704
* All stuff for Older Blender than the 2.93 removed.
* 'Ctrl + RMB Double click' add selected only the picked objects children (3DsMax).
* 'Ctrl + Shift + P' Link to. (3DsMax, Blender Adaptive).
* Selection Keys fixed for Weight Paint mode (3DsMax).
* Camera FOV target create location on rigged cameras fixed.

# 0, 1, 0, 20220621
* Joystick Creator store 'Display Meshes' in a collection rather than delete them.
* Joystick Creator share display mesh if there are same rather than new for each.
* New 'Circular Joystick' added. Create a Circle and call operator.
* Some minor bugs fixed.

# 0, 1, 0, 20220606
* Draw object Gride preview added (For now just a prototype).
* 'Create Bone' Bone roll rotation fixed and now works correctly in IK mode.
* 'Select Flipped UVs' [UV editor> select> Select Filipped UVs].
* 'Create Upnode' add parented empty object (object> parent> create upnode).

# 0, 1, 0, 20220529
* 'Lattice / FFD' set operator miss calculation fixed and performed.
* New 'Transform class' And 'Grid Display', not implement in all other tools yet.
* 'Ctrl + Inser' set Pivot menu add to pose & bone edit mode too (3DsMax mode).
* 'Random Object color' unlike the other random display, manualy editable and change every time (Object> show/hide > Random object color).

# 0, 1, 0, 20220516
* Ocean Caustic added to map presets "Shader editor/Tools/Append Node Trees".
* 'Alt + Space' Selection Lock Toggle (3DsMax mode).
* 'Light lister' ignore material with emission strength 0.
* 'Ctrl + C/V' in EDIT_MESH mode Copy/Paste single vertex location (Mirror Optinal).
* File Version Operator moved from edit menu to file menu.
* Sprite sheet node groupe order changed to Up to Down, Left to Right.
* some issue from previes update has been fiexed.

# 0, 1, 0, 20220509
* Keymaps updated to be compatable with 'Blender 3.2' too.
* 'Sprite play loop/ragge' node groupse added to shader node groups presets.
* 'Freez On' operator can be lock to right panel (Optinal).
* 'Copy/Paste Transform' to other Blender('Ctrl+C/V' 3DsMax & Blender Adaptive).
* Some Bugfixed, Cleanup and small issues fixed.

# 0, 1, 0, 20220503
* 'Parallax Ice' Node groupe for easy and fast Ice effect in EEVEE.
* 'Sprite 2D' Node groupe for display or animate sprite sheet.
* Detach operator in quadmenu keeps last setting for next oparation (3DsMax mode).
* Version operator show the Current blend file version (Menu/Edit/File Version).
* 'Shift + E' Extrude edit curve (3DsMax mode).
* 'Ctrl + Insert' as copy 'Shfit + Insert' as paste on most parts (3DsMax mode).

# 0, 1, 0, 20220425
* 'C' Camera search works on DopeSheet, timeline, CurveEditor and LNA too (3DsMax mode).
* 'camera.search' operator removed 'camera.select' do the same job ('C' in max mode).
* UV Tools panel a little bit arranged and get better but not final yet.
* Changes on previous update causes problem on older blenders (2.8x) that issue fixed.
* Some other minor Bugfix and Cleanup.

# 0, 1, 0, 20220417
* UV Tools collected on 'UV Tools' panel to faster acces (Not final).
* New UV split operator that work in sync mode too.
* 'Ctrl / Shift' Selection issue for Blender 3.x fixed.
* 'Ctrl + RMB' or 'Shift + RMB' Select more 'Alt + RMB' Deselect (3DsMax Mode).
* Collection hide bye Number in view3D disabled in 3DsMax mode.
* 'Ctrl + Left/Right' jump to Previes/Next Marker (3DsMax and Blender Adaptive).
* '[' & ']' Left/Right Panel toggle works in all areas (3DsMax mode).
* 'N' Auto key Toggle works in all areas (3DsMax mode).
* Some minor bugs fixed.

# 0, 1, 0, 20220410
* 'Hair from Curve' suport Poly curve too (Tools/Particle/..).
* 'Hair Guides To Curve' create Poly curve rather than Beziear curve (Faster and Accurate)
* ['Grab style'](https://www.youtube.com/watch?v=A2Dr8MO_aq4) operator Freeze hair dynamic style as hair brush (Tools/Particle/..).
* 'G' Hide/Show gride works on flat views too (3DsMax mode).
* Mesh Attach operator can pick Font object too.

# 0, 1, 0, 20220404
* Bugfix and code Cleaning.
* some arrangement in [BsMax Wiki](https://github.com/NevilArt/BsMax/wiki).

# 0, 1, 0, 20220326
* Change the Addon github Name From 'BsMax_2_80' to 'BsMax'.
* Quadmenu 'Freeze transform/ Transform to zero' works corectly (3DsMax mode).
* 'WERVX[]' type proplem in Edit Text Mode solved.
* Some bug caused by 3.x Api update are fixed and Code cleaning.

# 0, 1, 0, 20220321
* 'Make Library Override (Multi)' Convert selected object rather than only active object (Object/Relation/..).
* 'Distance Sort' & 'Path Sort' improved and bug fixed (Object/Transform/..).
* 'Distance Sort' & 'Path Sort' renamed to 'Arrange by Distance',  'Arrange on Curve'
* Quick setup for create pillows 'Create/Mesh/Extera/Pillow' (Basic one will be improved).

# 0, 1, 0, 20220313
* Selction issue in pose mode fixed (3DsMax mode).
* New operator select Splines by Close/Open (EditCurve/Select/Select Close).
* Hide/Unhie on Edit Mode affect only on active element(Vertex,  Edge or Face).
* Hide/Unhide menu and key maps fixed for Curve and Armature too.
* 'Quadmenu' Mesh edit NURMS Toggle actived.
* 'Quadmenu' Mesh Edit'Triangulate' placed as 'Edit Triangulation'.
* 'Quadmenu' Outline and Bevel tools are active.
* Some other minor bugs fiexed.

# 0, 1, 0, 20220307
* 'Chamfer' Operator 'Ctrl+Shift+C' and same in Quadmenu works fine (3DsMax model).
* 'Chamfer' Operator automatically switch to vertex and edge mode depends on mode.
* Object Properties is better than before but still far from perfect (3DsMax model).
* 'Weld' Operator in quadmenu now is working (3DsMax model).
* Quadmenu Select instance issue fixed (3DsMax mode).

# 0, 1, 0, 20220303
* Quadmenu 'Freeze' Operator makes object display as solid color.
* 'Hide/Unhide' Operator in Quadmenu do not affect render setting anymore.
* 'Alt+Q' works on all Modes in View3d (3DsMax mode only).

# 0, 1, 0, 20220228
* Paralax Node tree added "Shader editor/Tools/Append Node Trees/...".
* Note: Paralax map works on coordinate system and Not suport UVMap yet.
* Backburner submitter 'Frame per task' miscalculation fixed.
* Backburner submitter load preset error fixed.
* Some other minor bug fixed.

# 0, 1, 0, 20220222
* Parent Constraint stuff added to animation Quadmenu 'Alt + RMB'
* Some minor Bugs Fixed.

# 0, 1, 0, 20220221
* Image Blure,  Fallof,  Untile Node preset can be append from "Shader editor/Tools/Append Node Trees/..."

# 0, 1, 0, 20220202
* Helix primitive height miscalculation fixed.
* Primitive Icosphere issue with Blender 3.0 fixed (API update).
* All Quadmenu Items rechecked and refiend much as possible.

# 0, 1, 0, 20220124
* Create Line,  Empty and Lights issu from last update fixed.
* Primitive draw on surface and view Done.
* Hold 'Ctrl' while draw primitive opjects draws on one step.
* Better method for calculate second radius (Cone,  Helix).
* Note: Some of primitive (e.g. Arc) not working for now but will fix and update soon.

# 0, 1, 0, 20220111
* Tool menu issue from last update fixed.
* The error on Disable/Enalble of addon fixed.
* 'anim.set_key_filters' unregister issue fixed.

# 0, 1, 0, 20220109
* 'Align object' tool completely renewed based on world martix (better and faster).
* 'Align object' can align perfectly on pose bone (Rotation and Scale).
* 'Align object' do not affect selection anymore.
* 'Fix override driver' tool none mesh type error solved.
* 'Create object' set 'Object type visablity' on while create.

# 0, 1, 0, 20211210
* 'Select Camera' Operator issue fixed for scene without Camera.
* Show types toggle keys added to pose mode (Max mode).

# 0, 1, 0, 20211128
* Draw object on master collection in Blender 3.0 problem solved.
* Convert to operator issue with some modifiers fiexed.
* Code review and some clean up and arangment.

# 0, 1, 0, 20211107
* save_preferences issu fixed for Blender 3.0
* 'Shift+M' call collection Menu (Max mode) (replacment for 'M' that used for Material Editor).
* 'Path Constraint' by default set keys type as Linear.
* 'Ctrl+S' in text editor Save text if external Save blend file if internal (Max Mode).
* 'Shift+V' Preview Menu (Max Mode).

# 0, 1, 0, 20211013
* New Create Primitive operator for draw object on surface.
* Note: for now just Applyed for objects without width and length parameter.

# 0, 1, 0, 20211006
* Camera target and FOV create in same collection as the camera is.
* Backburner submitter works on Mac (thanks to CalvinAndHobbies).

# 0, 1, 0, 20210915
* Backburner submitter`s double first frame issue fixed.
* New 'Premiere' keyspap added for VSE addes (BsMax/Custom/Video sequencer)
* VSE 'Alt + Arrow' keys Move active Strip (like in premire) (Max and Premiere Mode)
* VSE 'H' Mute/Unmute toggle (Max and Premiere Mode)
* Maxscript folder added,  will contain some tools. for now trasfer Camera + Keyframes from 3DsMax to Blender.

# 0, 1, 0, 20210905
* Experimental 'Autogrid' added for Create primitive operator..

# 0, 1, 0, 20210903
* Spiderweb polished and some bugfiex (Create Bitmap not working yet disabled for now).
* Set soft limit for some of SpiderWeb creator parameters to avoid crashing.

# 0, 1, 0, 20210902
* The Abandoned SpiderWeb tool from "Maxime Herpin" updated to work with Blender 2.80+ and add as an operator to BsMax (Draw lines with anotation then Create/Mesh/Extera/SpiderWeb).
* Note: SpiderWeb tool is buggy but works for most cases. Don't worry about Bugs all will be fix soon.

# 0, 1, 0, 20210830
* Backburner submiter -1_end and miss last frame bug fixed.
* Backburner submiter can submit Server Group name too.
* Hair cache combine use cache name rather than 'combined' for combined forlder name.
* Press 'Ctrl+Z' while Create Primitive object crash bug fixed.

# 0, 1, 0, 20210808
* Backburner tool Inteface cleaned up and some bug fixed.
* Backburner submitter as float dialog added to render menu.
* 'New Editor' menu added to 'Windows' menu.

# 0, 1, 0, 20210806
* Save/Load button added for backburner setting.
* Backburner can send job for custom version (By default current Blender Version).

# 0, 1, 0, 20210726
* In Backburner submiter 'frame per task' added for 'Specific frames' mode too.

# 0, 1, 0, 20210722
* Submit to Backburner Operator now create a seprate temp file for render.
* Backburner has an option for submit as suspended or not.
* Pre/Post Render Script operator added under Render Properties/Script.
* Note: just write the name of script in text editor for Pre/Post Render script.

# 0, 1, 0, 20210715
* Multiple Hair cache combine operator added to automate the index switch.
* Add a new mode for keep Blender mode keymaps completly untoched.

# 0, 1, 0, 20210714
* 'bpy.utils.user_resource' issue fixed.

# 0, 1, 0, 20210614
* Selection set Copy/past issue fixed.
* Selection set interface simplified.
* 'Ctrl + K' Insert Keyframe menu (Max mode).
* 'Alt + K' Delete Key (Max mode).
* 'Ctrl + Shift + K' 'Set Key Filter' (max mode).
* 'Set Key Filter' added to Time slider.

# 0, 1, 0, 20210611
* Transfer tool for Rigg Selection set to other Rigg 'Pose mode: Right Panel/Tool/Selection(Pose bone)/Transform/(Copy/Past)'

# 0, 1, 0, 20210606
* Auto library override issue fixer caused to crash on heavy secens,  disabled for now.

# 0, 1, 0, 20210604
* BsMax works with Blender defult with Rightclick select mode too.
* Fix library override issue fix on render time automaticaly.

# 0, 1, 0, 20210525
* Light lister list materials with emission (Editable only if Color or Strength slot are free).

# 0, 1, 0, 20210517
* 'OpenGL Depth Picking' Autodisable is optinal (Search for 'Auto Use Select Pick Depth Toggle' off by default)

# 0, 1, 0, 20210511
* 'OpenGL Depth Picking' Automaticly disable on Pose mode to speed up bone selecting.
* 'C' Camera search fits camera frame to view too (3DsMax Mode).
* Timeline Red bar back with no crash.

# 0, 1, 0, 20210510
* Light/Camera lister Improved.
* 'Freeze On' Repeat count issue fixed.

# 0, 1, 0, 20210506
* 'Freeze On' improved ('Animation/Freeze On')

# 0, 1, 0, 20210505
* 'Freeze On' Fix an IK controller in position for wanted frame range 'Animation/Freeze On'.

# 0, 1, 0, 20210503
* 'W, E, R' auto Coordinate Toggle 'World/Local' disabled by default. 'Ctrl+W' for Active/Deactive (3DsMax mode).

# 0, 1, 0, 20210502
* 'Parent Constraint' and 'parent to world' works on pose mode too.

# 0, 1, 0, 20210429
* 'SetKey' issue when no object select fixed. (Max mode)
* 'Edit Mode' shortkey disabled for Linked,  Proxy & Libraryoveride Armature that can not be edit.

# 0, 1, 0, 20210418
* All version check codes updated to make then add-on works on Blender 3.0 and above too;

# 0, 1, 0, 20210411
* Parent constraint now works better with Armature objects.

# 0, 1, 0, 20210328
* Minor improvement and bug fixed in some of tools.
* 'K' add key frame on ui items too (3DsMax mode).
* 'S' add key frame on ui items too (Maya mode).
* 'Connect Script To Active Object' operator bind script to the object and makes link or merge with it to news scene automatically.

# 0, 1, 0, 20210319
* '6' open float geometry node editor (Replacement for PFSurce shortcut) (3DsMax mode).
* 'bpy.ops.editor.float' Updated to work in Blender 2.93 and improved ('M',  '8',  'F11' in 3DsMax mode).

# 0, 1, 0, 20210317
* 'Align Object' works for objects with Constriants.
* 'Set start/end frame' (Right Click Menu time line and Sequencer).
* 'Join plus' Ask for apply befor join 'Ctrl + j' (Blender & 3DsMax Mode).

# 0, 1, 0, 20210310
* Render preset Save/Load and Copy/Paste operator added (Render Properties/ Presets)

# 0, 1, 0, 20210221
* "Overridelibrary" Driver Issue fixer applying for the whole scene automatically (Tools/Animation/Fix Override Driver Issue)

# 0, 1, 0, 20210219
* Solve the Library override broken shapekey drivers (Tools/Animation/Fix Override Driver Issue).

# 0, 1, 0, 20210216
* Select by Length and Segment Count added to Select Menu in Curve Edit mode.
* 'W', 'E', 'R' issue with snap fixed.

# 0, 1, 0, 20210207
* Multi target shapekey (driving multiple shapekeys automatically) added under shapekey panel.
* Very simple tool for quick rename objects data name same as object name (for now search 'Data Rename' operator).

# 0, 1, 0, 20210131
* 'Align object' issue with new merged object fixed.
* Quadmenu 'Weld' option is works now (as a temprary solution).

# 0, 1, 0, 20210128
* The issue of last update ('W, E, R' and snap) fixed.

# 0, 1, 0, 20210127
* Camera Target seprated from FOV Target.
* Camera Target tools puted on 'Properties > Object Data (Camera) > Target/Tools' panel.
* 'Blender Transform Type' added to Options make 'W, E, R' Keys work like Blender 'G, R'S' Keys (Need to restart blender on change)

# 0, 1, 0, 20210124
* 'TWEAK MMB + Shift' Align view (Replacement of 'TWEAK MMB + Alt' in Blender Default for 3DsMax Mode).
* Zoom mode setting to Horizontal mode when Maya navigation active.
* Joystick connector remove old driver if exist.
* Camera target control the F-Stop of Depth of Field too.

# 0, 1, 0, 20210122
* 'Hair guides from/to curve' added to View3D:Tools/Particle Menu.
* Mesh Edit mode Skin Resize keymap changed to 'Ctrl + Shift + A' (Max mode).
* Joystic to Shape key connector added to link context menu (Ctrl + L).
* 'Weight to Vertex Color' puted in View3d/ Paint menu (Vertex paint Mode).
* 'A' copy active object material to selected objects as 3DsMax "Assign Material to Selection" (Max mode).
* 'Create' and 'Tools' Menus shows only in object mode.
* 'Shift + T' open External Data context menu replacement for 3DsMax Asset Tracking (Max mode).

# 0, 1, 0, 20210110
* New Selection Set for Armature (Pose mode only) (View3D/ Rigth Panel/ Tool/ Selection)

# 0, 1, 0, 20210106
* Backburner Tool Updated.
* "BsMax_2_80\tools\internal\render\backburner.py" Could be installed as a standalone addons too.
* The function that has changed timeline color on auto on cused to crash blender some time. disabled till find a solution.

# 0, 1, 0, 20210103
* Submit Render jobs to Backburner (Original code from "Matt Ebb | Blaize | Anthony Hunt | Spirou4D") (For Now Windows Only).
* Updated "Backburner" addon for Blender 2.8x,  2.9x.
* Add Specific Frames type ('1, 3, 5-7') to "Backburner" tool.
* 'Ctrl+Shift+A' Create primitive Menu added to blender key-maps mode.

# 0, 1, 0, 20201229
* Armature.arrach operator bug fixed
* Hair guide from curve operator compatibility issue with Blender 2.91 fix.

# 0, 1, 0, 20201227
* Delete_plus for object mode keep children transform on parent delete. ('Delete' Max mode)
* 1, 2, 3 disabled for non converted primitive objects.
* Link_to operator issue with transformed parent Re-Link to other object fixed.
* 'pose.select_hierarchy_plus' tool replased with 'pose.select_hierarchy' for defult blender mode. ('[' ']' in Blender mode).
* "DoublClick" select children in Pose mode (Blender mode)
* Additional object (Mesh, Curve, Text) can attach to bone custome shape in pose mode (works on Rest Positon mode).
* Transform/Rotation to Zero reset bone for pose mode rather than the armature position.

# 0, 1, 0, 20201221
* Additional Primitives are create from search box (Search for 'Create' then choose the type).
* Additional Primitives are create from python Script (https://github.com/NevilArt/BsMax/wiki/bpy.ops.object.create).

# 0, 1, 0, 20201216
* Create empty frame for using as joysticks border added for 'Joystic Creator'.
* 'Ctrl + RMB' Select extended in max mode works better now.

# 0, 1, 0, 20201215
* 'Attach' tool collaps target objects modifiers before join. (for now works only for Mesh objects)

# 0, 1, 0, 20201213
* Smart loop/ring tools from 'maxivz_tools' addon updated.
* 'Convert to' and 'Join Plus' tools updated to 'No Mercy' mode (Modifier apply,  Make unique,  clear primitives data).
* 'Join Plus' issue with armature objects fixed.
* New 'pose.select_hierarchy_plus' tool select child/parent in pose mode better than original one.
* 'Ctrl + L' do 'Attribute link' if object selected do 'Light toggle' if not obj selected (Max Mode)
* Node editor 'Zoom extended' error on empty node editor has fixed ('Z' in max mode).
* Joystick connector status check updated to avoid displaying error messages.
* 'Detach' command in quad menu issue fixed and now it works.

# 0, 1, 0, 20201206
* Undo issue fixed for most of the Operators.
* "DoublClick" and "Ctrl+DoubleClick" for select children in object mode (Max mode)

# 0, 1, 0, 20201126
* Accidentally created tiny primitives removing automatically.
* Undo for Create primitives remove only the last one.

# 0, 1, 0, 20201122
* Refine tool added (insert vertex on clicked point in curves) (Curve edit mode: menu: Segment/ Refine)
* In Quad Menu Move,  Rotate,  Scale Setting buttion action issue fixed.
* Align Object added to menu: Object/Transform/Align Objects(BsMax).
* Hide/Unhide issue in Quad Menu fixed.

# 0, 1, 0, 20201117
* Max like selection key map added for particle edit mode(Max mode only).
* Hair guide from curve step_key counts issue fixed.
* Node editor 3DsMax like selection short keys (Max mode only).
* Node editor 'H' and 'Ctrl + H' actions swapped for 3DsMax mode.

# 0, 1, 0, 20201111
* Weight paint to vertex paint convertor added (for now search for "Weight to Vertex Color").
* Create Curve from hair guide tool added (for now search for "Hair Guides To Curve")

# 0, 1, 0, 20201106
* Hair guide from Curve operator added (for now select mesh search "Hair Guides From Curve" and pick Curve)
* A Simple Camera lister added (Menu: Render > Camera Lister)

# 0, 1, 0, 20201101
* Character lister added (for now very simple stuff but in time other tools will be add)
* Mesh edit mode 'Ctrl + M' Subdivid/MSmooth selected faces (Max mode only)

# 0, 1, 0, 20201029
* Atach picked object in Edit mode like 3DsMax`s edit poly attach (object mode and Edit mode in Quad menu).
* Same Attach function added for Curve & Armature too.
* ObjectPicker Operator updated.
* Pivot to First Bezier point issue fixed (Ctrl + Insert in set pivot point menu).
* Bugfix.

# 0, 1, 0, 20201028
* Default auto smooth fixed for Torus,  Teapot,  Monkey primitives.
* Bugfix.

# 0, 1, 0, 20201026 and befor
* Align Objects has better UI and able to Align Objects to Bone of Armature too.
* Primitive Geometries create and update with Shade Smooth active.
* Join (ctrl+J) clear primitive data now.
* Object display setiing assined to 'Alt+X'.
* Path Sort Operator updated (Select objects call the operator then pick path)
* PickOperator bug fixed.
* Linkto Operator now can link Object directly to a bone.
* PickOperator updated,  now can return source,  subsource,  target and subtarget.
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
* Select Element enabled for 3DsMax mode ('5' Toggle On/Off,  'Ctrl + 5' Open Setting Dialog)
* Open the keymaps list in github wiki via addon preferences (In production).
* Preferences UI changed,  more optional and easy to understand.
* Quad menu can scale from addon preferences.
* lots of code cleaning and Simplification to make future improvment easy.
* Align Objects has percentage option now and can put in halfway or increase distance by entering negative value.
* Some New Items added to Quad menu.
* "Link to" operator (Avalible in Quadmenu).
* Align objects draws a line to show the tool is active.
* All Operators has self report now. you can see python api of each operator in 'Info' or 'Console'.
* Time keys now working on all areas ('N' ', ' '.' '/' 'Home' 'End' in Max mode)
* '[' and ']' defined to Left and Right Tool panel open/close toggle (Max Mode only).
* Keymap system has duplication check function.
* Press the 'W', 'E', 'R' again toggles between Global/Local coordinate (Max, Maya mode).
* light lister ignore the instance lights to simplify the list.
* "Clear primitive data" combined with "Convert to" command (Max Mode only)
* Hide/Undide updated but not fine yet (because of python limitation for now)
* Keep Prefrence settng when add-on has Disable/Enable or Updated.
* Align objects acts as 3DsMax now. (Select objects,  press 'Alt + A' then pick Target).
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