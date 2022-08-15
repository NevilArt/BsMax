# BsMax TODO List


### Keymaps
- [x] Loop/ring short key in UV Editor.
- [ ] Brush Size control hot keys (for max mode).
- [ ] 'F9' If no active camera in scene create temprary one.
- [ ] 3DsMax Adapted key map for animators.
- [x] Ctrl + shfit + P link to Blender adaptive mode.
- [x] Ctrl + Double click Select children select only active object children.
- [ ] 'Shift + LM click' Armature pick short path.
- [ ] Weight paint alt drag deselect (disable gradient tool).
- [ ] Weight paint Selection keys.
  - [x] Ctrl + A,D,I.
  - [ ] Ctrl/Alt + Drag.
- [ ] M, ctrl + M Collection.
- [ ] 'Ctrl + L' select linked in Weight paint vertex mode.
- [ ] Update Maya short keys too.
- [ ] Alternative to 'Shift + G' select grouped in 3dsmax mode.
- [ ] VSE hold shift select between action and new selected.
- [ ] 'Ctrl + S' image editor save as image if not saved befor. 
- [ ] 'Shift + X' set from SRG to WER in 3dsmax mode.
- [ ] 'Shift + Q' open select similar menu.
- [ ] 'Set ffd' menu in Edit Mode.
- [ ] 'LMB Double click' Face and vertex mode select linked.
- [ ] Knife tool RMB commit (3DsMax mode).


### Menu/UI
- [ ] Quadmenu.
  - [ ] UV Editor.
    - [ ] If UV editor is open add UV stuff too.
    - [ ] Seam and UV tools.
  - [ ] Mark/Clear seam if edge mode.
  - [ ] Collection stuff ctrl+rmc quad menu.
  - [ ] Put transform pivot poins in alt+rc quadmenu.
  - [ ] Weld tool setting dialog.
- [ ] Armature edit mode Show/Hide menu.
- [ ] Copy/paste vertex coodinate in Vertex menu.
- [ ] Tools menu for difrent modes.


### Tools
- [ ] UV editor Target Weld.
- [ ] File view PageUp/ PageDown.
- [ ] Make rectangular UV.
- [x] Instancer / Make Unique a grupe of objects.
- [ ] Weld tool setting dialog.
- [ ] Topology symmetry tool.
- [ ] 3DsMax Navigation (change navigation mode without release the Alt key).
- [ ] Clone object shift drag.
- [ ] Extrude open edge with shift drag.
- [ ] Max like Slice modifire quick setup.
- [ ] Global transform offset tool for selected objects in selected range.
- [ ] Armature
	- [ ] Curve keys between first and last key.
	- [ ] Select Keyed/Non-keyed controllers.
- [ ] Better Isolate system (Alt+Q).
- [ ] More stuff for Character lister(Skin on/off, Subdivision level fo mesh,...).
- [ ] Need a PickAndDo operator (Alternative for PickOperator).
- [ ] Target weld for edge mode.
- [ ] Node to text (clip board) and reverce.
- [ ] Spline vertex Hoke to object by drag and pick.
- [ ] semi instance selector.
- [ ] Make unique keep group instanses.
- [ ] Create Curve from motion path.
- [ ] Bone to IK by picking.
- [ ] Convert to armature.
- [ ] Auto instancer.
- [ ] Scene Modifier lister and manager.
- [ ] Material lister.
- [ ] Seprate group of instanced object keep instance in grupe.
- [x] Shapekeys sort by name.
- [ ] Copy/Paste material, action, modifier.
- [ ] turn normal off for objects wit subdiv modidfier.
- [ ] light group editor.
- [x] unfreaze Bone edit/ armature mode.
- [x] Snapshot.
	

### Issue
- [ ] Edge mode delete face most desolve edges too.
- [ ] Bone to Bone link_to need to fix transform.
- [ ] Press 'S' while navigation toggle Snap rather than the scale in max mode.
- [ ]	Mirro operator not working.
- [ ]	Undo.
	- [ ] Chamfer Curve.
  - [ ] Convert to ...
- [ ] Sub object check for library overide.
- [ ] Check Timeline color ot startup.
- [ ] UV editor tweak select issue.
- [ ] Draw line tool some time makes extera vertecs on Close.
- [ ] Parent constraint to rigged character issue.
- [ ] Parent constraint to parented parent issue.
- [ ] Convert to for curve objects apply modifiers not works.
- [ ] subdive operator on quad menu undo issue.
- [ ] 'LMB double click' select element not works yet.
- [ ] align objects refresh issue (refactor).


### Update
- [ ] PickOperator Subtarget to object or another subtarget.
- [ ] Put transform type in right tool panel on/off with f12.
- [ ] Transform type in sub object and pivot helper.
- [ ] Alight too adapt for edit pivot mode.
- [ ] Light lister UI has to change.
- [ ] Camera lister UI has to change.
- [ ] Align object set key for new changes if auto key is on.
- [ ] Join plus asnd attach convert text object befor  join.
- [ ] Label for joystic creator.
- [ ] Apply multiusers.
- [x] Delete operator unparent children first.
- [x] Keymap system has to optain repate option too.
- [x] Select more/less need to repeat mode active.
- [x] fix all active viewlayer lines.
- [ ] smart loop/ring update or remove.
- [x] Select all in object mode select pose bones too.
- [ ] Conver to and join plus do not works on some cases.


### Primitives
- [ ] Draw.
  - Draw on local gride.
    - [x] Draw on surface.
    - [x] Draw on view.
    - [ ] Fix height issue.
    - [ ] Fix Draw under floor issue.
  - [ ] Snapping.
  - [ ] Crearte primitive weel for segment count.
- [ ] New Primitives.
  - [ ] Torus Knot.
  - [ ] quad sphere.
  - [ ] Helix with bezier segments with less count of knots (Bezier points).
- [ ] Float edit menu for Empty objects.
- [ ] Draw area light with rectangular option.


### BUI
- [ ] New Editable Quadmenu with short key support.


## In Progress
- [ ] Wire parameter (Easy Dirver creator).
  - [x] Prototype design.
  - [ ] Create UI.
    - [x] Transform.
    - [ ] Shapekey.

- [ ] Sprite sheet Import Export.
  - [ ] Importer.
    - [x] COA-Tools Jason import planes.
    - [ ] Spine jason import.
      - [ ] Image Plane.
      - [ ] Bones.
      - [ ] Animation.
  - [ ] Exporter.
    - [ ] Cutout rigg to Unity.
    - [ ] Cutout rigg to Spine.