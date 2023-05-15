/*##########################################################################
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
##########################################################################*/

if classof GUIRO == RolloutClass do destroydialog GUIRO
Global FacialUIs = #()
function CreateFGUI obj =
(
	if classof obj.baseobject ==  Rectangle do
	(
		Global PosManager, Talkerro
		Global SFrame = 1, Handel = 2, Hlimit = 3, Vlimit = 4, Freezed = 5, Upper = 1, Lower = 2
		Global Size = 800
		Global MainFrame = obj
		Global SubFrame = #(), Caption = #(), OrPos = #(), OrSize = #()
		Global SelectedJoys = #(), TalkFilter = #()
		function AddToCaption Tobj = append Caption #(Tobj.baseobject.text, [in coordsys MainFrame Tobj.pos.x, in coordsys MainFrame Tobj.pos.y])

		-- Collect All joysticks --
		for SF in MainFrame.children do (
			if classof SF.baseobject == text do
				AddToCaption SF -- collect caption in frame root

			for H in SF.children do (
				if classof H.baseobject == text do
					AddToCaption H -- collect caption in sub root

				if classof SF.baseobject == Rectangle do (
					--###########################################################################################################################
					-- collect handels with freezed transform --
					if H.position.controller as string == "Controller:Position_List" do
						if H.position.controller[1] as string == "SubAnim:Frozen_Position" and H.position.controller[2] as string == "SubAnim:Zero_Pos_XYZ" do (
							IsJoy = false
							local Hlim = #(), VLim = #()
							-- X_Position Controller --
							if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do (
								--if H.position.controller.Zero_Pos_XYZ[1].controller == "Controller:Float_Limit" do (
								ULimit = H.transform.controller[1][2][1][2][1].value
								--ULimit = H.pos.controller.Zero_Pos_XYZ[1].controller[2][1].value
								LLimit = H.transform.controller[1][2][1][2][2].value
								--LLimit = H.pos.controller.Zero_Pos_XYZ[1].controller[2][1].value
								Hlim = #(ULimit, LLimit)
								IsJoy = true
							)

							-- Y_Position Controller --
							if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do (
								--if H.position.controller.Zero_Pos_XYZ[2].controller == "Controller:Float_Limit" do (
								ULimit = H.transform.controller[1][2][2][2][1].value

								--ULimit = H.pos.controller.Zero_Pos_XYZ[2].controller[2][1].value
								LLimit = H.transform.controller[1][2][2][2][2].value

								--LLimit = H.pos.controller.Zero_Pos_XYZ[2].controller[2][2].value
								VLim = #(ULimit, LLimit)
								IsJoy = true
							)
							if IsJoy do Append SubFrame #(SF, H, Hlim, Vlim, true)
					)
					-- collect handels with Non freezed transform --
					if H.transform.controller[1] as string == "XXXX" do (
						IsJoy = false
						Hlim = #()
						VLim = #()

						-- X_Position Controller --
						if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do (
							ULimit = 0
							LLimit = 0
							Hlim = #(ULimit, LLimit)
							IsJoy = true
						)

						-- Y_Position Controller --
						if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do (
							ULimit = 0
							LLimit = 0
							VLim = #(ULimit, LLimit)
							IsJoy = true
						)

						if IsJoy do
							Append SubFrame #(SF, H, Hlim, Vlim, false)
					)
					--###########################################################################################################################
				)
			)-- End of or H in SF.children do
		)
		if SubFrame.count > 0 do (
			function Pixelof num = Size * ( num / MainFrame.width)
			function Valueof pix = MainFrame.width * (pix as float  / Size as float)
			Global FrameWidth = Size
			Global FrameHeight = Pixelof MainFrame.length
			--======================================================================================================================================================================--
			rollout GUIRO (filterstring MainFrame.name "_")[1]
			(
				function Pixelof num = Size * ( num / MainFrame.width)
				function Valueof pix = MainFrame.width * (pix as float  / Size as float)--## unable to convert [5.5,5.5] to type float 
				Global JoyStick = #(), Frame = #(), Nodes = #(), DifPos = #()
				Global Index = 0
				Global MXM = 0, MYM = 0, MOPX = 0, MOPY = 0
				Global HoldingFrame = 0, L1 = false
				--Global U = 0, D = 0, L = 0, R = 0
				Global OldTime = slidertime
				dotNetControl GUI_DN "System.Windows.Forms.Label" pos:[0,0] width:GUIRO.width height:(GUIRO.height - 30)
				timer Clocktm interval:10
				button Helpbt "Help" width:70 across:4
				button Aboutbt "About" width:70
				checkbutton _____ "" width:70 enabled:false
				checkbutton Posercbt "Poser" width:70
				
				function GetJoyStick X Y =
				(
					Ret = 0
					for i = 1 to Frame.count do (
						H = Frame[i]
						if X > H.Location.x and
							X < H.Location.x + H.Size.width and
							Y > H.Location.y and
							Y < H.Location.y + H.Size.Height do (
								Ret = i
								exit
							)
					)
					try(
						if Ret == 0 then
							select MainFrame
						else
							select Nodes[Ret]
						)
					catch() --## dont work after change file 
					--## do this 
					-- try if catch scan again --
					return  Ret
				)
				
				function ReposHandels =
				(
					try (
						for i = 1 to SubFrame.count do (
							HPos = in coordsys MainFrame SubFrame[i][Handel].pos
							JPos = in coordsys MainFrame SubFrame[i][SFrame].pos
							OPos = SubFrame[i][Handel].transform.controller[1][1].value -- Get Freezed position
							JoyStick[i].Location.x = DifPos[i].x + pixelof (HPos.x - JPos.x - OPos.x)
							JoyStick[i].Location.y = DifPos[i].y - pixelof (HPos.y - JPos.y - OPos.y)
						)
					)
					catch
						destroydialog GUIRO
				)
				
				function MoveJoyHandel X Y = if index > 0 do 
				(
					--###########################################################################################################################
					--stopAnimation()
					--## limitation not work on some joysticks --
					-- Apply movement to joystick
					JoyStick[index].Location.x += X
					JoyStick[index].Location.y += Y
					-- Limit tje joystick 
					if SubFrame[index][3][2] == 0 then
						if JoyStick[index].Location.x < DifPos[index].x do
							JoyStick[index].Location.x = DifPos[index].x

					else if JoyStick[index].Location.x < 0 do
						JoyStick[index].Location.x = 0
						
					if SubFrame[index][4][2] == 0 then
						if JoyStick[index].Location.y < DifPos[index].y do
							JoyStick[index].Location.y = DifPos[index].x

					else if JoyStick[index].Location.y < 0 do
						JoyStick[index].Location.y = 0
						
					if SubFrame[index][3][1] == 0 then
						if JoyStick[index].Location.x > DifPos[index].x do
							JoyStick[index].Location.x = DifPos[index].x

					else if JoyStick[index].Location.x + JoyStick[index].size.width > Frame[index].size.width do
						JoyStick[index].Location.x = Frame[index].size.width - JoyStick[index].size.width
					
					if SubFrame[index][4][1] == 0 then
						if JoyStick[index].Location.y > DifPos[index].y do
							JoyStick[index].Location.y = DifPos[index].y
					else if JoyStick[index].Location.y + JoyStick[index].size.height > Frame[index].size.height do
						JoyStick[index].Location.y = Frame[index].size.height - JoyStick[index].size.height

					-- Apply movement to handel 
					in coordsys MainFrame move SubFrame[index][Handel] [Valueof X, Valueof -Y, 0]
					--###########################################################################################################################
				)
				
				function ResetJoystick Sindex = if Sindex > 0 do undo on
				(
					-- reset the Joy position --
					JoyStick[Sindex].Location.x = DifPos[Sindex].x
					JoyStick[Sindex].Location.y = Difpos[Sindex].y

					-- reset the freezed transform and limeted controller
					try(
						SubFrame[Sindex][2].transform.controller[1][2][1].value = 0
					)
					catch()
					
					try(
						SubFrame[Sindex][2].transform.controller[1][2][2].value = 0
					)
					catch()
				)
				
				/*on Clocktm tick do
				(
					try(tt = MainFrame)catch(destroydialog GUIRO)--## do not work
					if OldTime != slidertime do ReposHandels()
					OldTime = slidertime
				)*/
				
				on GUIRO open do
				(
					-- retrive the last position ------------------------------------------------------------------------------------------------------------
					try(
						SetDialogPos GUIRO (execute(getINISetting (getMAXIniFile()) "AutoFacialGUI" "pos"))
					)
					catch()
					--------------------------------------------------------------------------------------------------------------------------------------------
					FR = MainFrame.wirecolor.R
					FG = MainFrame.wirecolor.G
					FB = MainFrame.wirecolor.B
					-- Setup the main form --
					GUI_DN.BackColor = (dotNetClass "System.Drawing.Color").FromARGB FR FG FB
					-- Set up the sticks --
					for i = 1 to SubFrame.count do (
						SF = SubFrame[i]
						-- Collect info from max objects -------------------------------------------------
						-- Global SFrame = 1, Handel = 2, Hlimit = 3, Vlimit = 4, Freezed = 5
						SFrameW = Pixelof (SF[SFrame].width * (SF[SFrame].scale.x / MainFrame.scale.x))
						SFrameH = Pixelof (SF[SFrame].length * (SF[SFrame].scale.y / MainFrame.scale.y))
						SR = SF[SFrame].wirecolor.R
						SG = SF[SFrame].wirecolor.G
						SB = SF[SFrame].wirecolor.B
						FPosX = Pixelof (in coordsys  SF[SFrame].parent SF[SFrame].pos.x) + GUI_DN.width / 2 - SFrameW / 2
						FPosY = GUI_DN.height - (Pixelof (in coordsys SF[SFrame].parent SF[SFrame].pos.y ) + GUI_DN.height / 2 + SFrameH / 2)
						-- calculation of Joy size --------------------------------------------------
						local HSizeW = 0, HSizeH = 0;
						if SF[Hlimit].count == 2 then (
							if SF[Hlimit][1] == 0 and SF[Hlimit][2] == 0 then
								HSizeW = SFrameW
							else
								HSizeW = Pixelof (((in coordsys MainFrame SF[Handel].max.x) - (in coordsys MainFrame SF[Handel].min.x)))

							if HSizeW < SFrameW / 5 do
								HSizeW = SFrameW / 5
						) -- end of if SF[3].count == 2 then

						else
							HSizeW = SFrameW

						if SF[Vlimit].count == 2 then (
							if SF[Vlimit][1] == 0 and SF[Vlimit][2] == 0 then
								HSizeH = SFrameH
							else
								HSizeH = Pixelof (((in coordsys MainFrame SF[Handel].max.y) - (in coordsys MainFrame SF[Handel].min.y)))

							if HSizeH < SFrameH / 5 do
								HSizeH = SFrameH / 5
						) -- end of if SF[4].count == 2 then

						else
							HSizeH = SFrameH

						HR = SF[Handel].wirecolor.R
						HG = SF[Handel].wirecolor.G
						HB = SF[Handel].wirecolor.B
						-- Calculation of Joy position -----------------------------------
						Offset_X =  Pixelof ((SF[3][1] + SF[3][2]) / 2)
						Offset_Y =  -Pixelof ((SF[4][1] + SF[4][2]) / 2)
						HPosX = SFrameW / 2 - HSizeW / 2 - Offset_X
						HPosY = SFrameH / 2 - HSizeH / 2 - Offset_Y
						append DifPos [HPosX, HPosY]
						----------------------------------------------------------------------
						-- create similar controllers on dot net ---
						FrameDN = dotNetObject "System.Windows.Forms.Label"
						FrameDN.Enabled = false
						--FrameDN.Name =  CName
						GUI_DN.ForeColor = (dotNetClass "System.Drawing.Color").FromARGB 200 200 200
						FrameDN.BackColor = (dotNetClass "System.Drawing.Color").FromARGB SR SG SB
						FrameDN.BorderStyle = (dotNetClass "System.Windows.Forms.BorderStyle").FixedSingle
						FrameDN.Location = dotNetObject "System.Drawing.Point" FPosX FPosY
						FrameDN.Size = dotNetObject "System.Drawing.Size" SFrameW SFrameH
						GUI_DN.Controls.Add FrameDN
						-- create hndel --
						JoyDN = dotNetObject "System.Windows.Forms.Label"
						--JoyDN.Name = HName
						JoyDN.Enabled = false
						JoyDN.Size = dotNetObject "System.Drawing.Size" HSizeW HSizeH
						JoyDN.Location = dotNetObject "System.Drawing.Point" HPosX HPosY
						JoyDN.ForeColor = (dotNetClass "System.Drawing.Color").FromARGB 255 255 255
						JoyDN.BackColor = (dotNetClass "System.Drawing.Color").FromARGB HR HG HB
						FrameDN.Controls.Add JoyDN
						-- Collect Joys --
						execute ("Append JoyStick F" + i as string)
						JoyStick[JoyStick.count] = JoyDN
						execute ("Append Frame H" + i as string)
						Frame[Frame.count] = FrameDN
						Append Nodes SF[2]					
					) -- end of for
					for C in Caption do (
						CDN = dotNetObject "System.Windows.Forms.Label"
						CDN.Enabled = false
						CDN.Text = C[1]
						CDN.TextAlign = (dotNetClass "System.Drawing.ContentAlignment").MiddleCenter
						CDN.Size = dotNetObject "System.Drawing.Size" (C[1].count * 6 + 8) 15
						CPosX = Pixelof C[2].x + GUI_DN.width / 2 - CDN.Size.width / 2
						CPosY = GUI_DN.height - (Pixelof C[2].y + GUI_DN.height / 2) - CDN.Size.height / 2
						CDN.Location = dotNetObject "System.Drawing.Point" CPosX CPosY
						GUI_DN.Controls.Add CDN
					)-- end of for C in Caption do
					ReposHandels()
				)-- end of on open
				
				on GUIRO close do 
				(
					setINISetting (getMAXIniFile()) "AutoFacialGUI" "pos" ((GetDialogPos GUIRO) as string) -- Save last position on close
					if PosManager != undefined do destroydialog PosManager -- close the posser if open
				)
				
				function DisplayActiveFrame index =
				(
					for i = 1 to Frame.count do (
						if i == index then (
							JoyStick[i].BackColor = (dotNetClass "System.Drawing.Color").FromARGB 255 255 255
							Frame[i].BorderStyle = (dotNetClass "System.Windows.Forms.BorderStyle").Fixed3D
						)
						else (
							HR = SubFrame[i][Handel].wirecolor.R
							HG = SubFrame[i][Handel].wirecolor.G
							HB = SubFrame[i][Handel].wirecolor.B
							JoyStick[i].BackColor = (dotNetClass "System.Drawing.Color").FromARGB HR HG HB
							Frame[i].BorderStyle = (dotNetClass "System.Windows.Forms.BorderStyle").FixedSingle
						)
					)
				)
				
				function Joy_MouseDown s e =
				(
					index = GetJoyStick e.x e.y
					if (dotNet.CompareEnums e.Button e.Button.Left) then (
						if index == 0 and keyboard.controlPressed do (
							Joys = #()
							for SF in SubFrame do
								append Joys SF[2]
							select Joys
						)

						if index > 0 do
							if keyboard.controlPressed then
								append SelectedJoys SubFrame[index][Handel]
							else
								SelectedJoys = #(SubFrame[index][Handel])

							DisplayActiveFrame index
					)

					if (dotNet.CompareEnums e.Button e.Button.Right) then (
						if index > 0 then
							ResetJoystick index -- Reset selected
						else if keyboard.controlPressed do
							for i = 1 to SubFrame.count do
								ResetJoystick i -- reset all joysticks

							DisplayActiveFrame index
					)

					if (dotNet.CompareEnums e.Button e.Button.middle) do (
						destroydialog GUIRO
						macros.run "Animation Tools" "FacialGUI"
					)
				) -- end of function Joy_MouseDown s e =
				
				function Joy_MouseMove s e = 
				(
					-- Get mouse movment ---
					MXM = e.x - MOPX -- Mouse X Movment
					MYM = e.y - MOPY -- Mouse Y Movement
					MOPX = e.x
					MOPY = e.y
					-- Isolate axis----------------------------------------------------------------------------
					if keyboard.altPressed do
						MXM = 0 -- only vertical move 
					if keyboard.shiftPressed do
						MYM = 0 -- only Horizontal move
					-------------------------------------------------------------------------------------------
					if (dotNet.CompareEnums e.Button e.Button.Left and index > 0) do
						if MXM != 0 or MYM != 0 do
							MoveJoyHandel MXM MYM
				)-- end of function Joy_MouseMove s e = 
				
				function Joy_MouseUp s e = if (dotNet.CompareEnums e.Button e.Button.Left) do if keyboard.controlPressed do if index != 0 do select SelectedJoys
				
				on GUI_DN MouseDown s e do Joy_MouseDown s e
				on GUI_DN MouseMove s e do Joy_MouseMove s e
				on GUI_DN MouseUp s e do Joy_MouseUp s e
					
				on GUIRO resized NewSize do
				(
					/*
					-- get scale percent --
					P = GUIRO.width as float / Size as float
					-- resize the main GUI --			
					H = GUI_DN.height as float / GUI_DN.width as float
					GUIRO.height = (GUIRO.width * H * P) + 30
					GUI_DN.width = GUI_DN.width * P
					GUI_DN.height = GUI_DN.height * P
					Size = GUIRO.width
					print P
					*/
				)
				
				on GUIRO moved pos do 
				(
					if PosManager != undefined do SetDialogPos PosManager (GetDialogPos  GUIRO + [FrameWidth + 10, 1])
				)
				
				on Helpbt pressed do 
				(
					rollout helpro "Auto GUI Help"
					(
						edittext Helpbt "" fieldWidth:350 height:300 readOnly:true
						on helpro open do
						(
							Helpbt.text = "Auto GUI V01.0.0\n\n"
							Helpbt.text += "Click On Empty Space = Select The Border Shape\n\n"
							Helpbt.text += "Ctrl + Click On Empty Space = Select All Joystick Handels\n\n"
							Helpbt.text += "Click On Joystick = Select The Handel\n\n"
							Helpbt.text += "Right Click On Joystich = Reset The Handel Pos\n\n"
							Helpbt.text += "Right Click On Empty Space = Reset All Handels Pos\n\n"
							Helpbt.text += "Middle Mouse Button = Open Selector\n\n"
							Helpbt.text += "Hold Alt = Vertical Move Only\n\n"
							Helpbt.text += "Hold Shift = Horisontal Move Only\n\n"
						)
					)
					createdialog helpro width:380 modal:true
				)
				
				on Aboutbt pressed do
				(
					rollout Aboutro "About"
					(
						label lb1 "Auto Gui V01.0.0"
						label lb2 "August 2016"
						label lb3 "Created By Nevil (Naser Merati)"
						--hyperlink lnk1 "www.firfira.com" address:"www.firfira.com"
						hyperlink lnk2 "Nevilart.blogspot.com" address:"nevilart.blogspot.com"
					)
					createdialog Aboutro modal:true
				)
				
				on Posercbt changed arg do
				(
					if arg then
					(
						rollout PosManager "Pos Manager"
						(
							Global PoserKeyCode = "SLKJASHFeOIFOeFIRFIRAbFPOKASFBOPJEIhNEVILfASfVAUIDADQWHASHdMNABDWUIDGAV1"
							Global Presets = #(), PosFile
							listbox Poslb "" width:152 height:((PosManager.height - 65) / 13) offset:[-14,-6]
							slider Applysl "" width:150 pos:[6,PosManager.height - 60] type:#float range:[0.0, 1.0, 0.0] tooltip:"slide: swich pos\nCtrl + Slide: Combine Pos"
							edittext nameet width:150 offset:[-15,0]
							function UpdateListBox =
							(
								items = #()
								for P in Presets do append items P[1]
								Poslb.items = items
							)
							function SavePresetsTofile =
							(
								str = PoserKeyCode + "\n"
								for P in Presets do (
									s = "#(\"" + P[1] + "\", ";
									for i = 2 to P.count do (
										s += P[i] as string
										if i < P.count do s += ","
									)
									s += ")\n"
									str += s
								)
								openedfile = openfile PosFile mode:"w"
								format Str to:openedfile
								close openedfile
							)
							on PosManager open do
							(
								PosFile = (getFilenamePath (getSourceFileName()) + "AutoFacialGUI\\" + GUIRO.title +".AGP")
								if doesFileExist PosFile then (
									openedfile = openfile PosFile mode:"r"
									if not eof openedfile do
										if readLine openedfile == PoserKeyCode do (
											Presets = #()
											while not eof openedfile do (
												s = readLine openedfile
												append Presets (execute s)
											)
											UpdateListBox()
										)
									close openedfile
								)
								else if makeDir (getFilenamePath PosFile) do (
									-- create a new preset file --
									openedfile = openfile PosFile mode:"w"
									format PoserKeyCode to:openedfile
									close openedfile
								)

								Poslb.selection = 0
							)
							on Poslb selected arg do
							(
								if Poslb.selected != undefined then
									nameet.text = Poslb.selected
								else
									nameet.text = ""

								if Poslb.selection > 0 and keyboard.altPressed do (
									deleteItem Presets Poslb.selection
									UpdateListBox()
									SavePresetsTofile()
									Poslb.selection = 0
									nameet.text = ""
								)
							)
							--##############################################
							on Poslb doubleClicked arg do
							(
								local val = 1.0
								local localCurntVal = #()
								local localPrestVal = #()
								for Su in SubFrame do (
									X = Su[Handel].transform.controller[1][2][1].value
									Y = Su[Handel].transform.controller[1][2][2].value
									Z = Su[Handel].transform.controller[1][2][3].value
									append localCurntVal [X, Y, Z]
									for i = 2 to Presets[Poslb.selection].count do (
										if Presets[Poslb.selection][i][1] == Su[Handel].name do (										
											append localPrestVal Presets[Poslb.selection][i][2]
											break
										)
									)
								)

								CombineMode = if Poslb.selected[1] == "+" then true else false

								for i = 1 to SubFrame.count do (
									 -- Combine mode
									if keyboard.controlPressed or CombineMode then (
										if localPrestVal[i] == [0,0,0] then
											P = (localCurntVal[i])

										else
											p = (localCurntVal[i]) * (1 - val) + ( localPrestVal[i] * Val)
									)

									else if keyboard.altPressed then (
										if localPrestVal[i] == [0,0,0] then
											P = (localCurntVal[i])
										else
											p = (localCurntVal[i]) * (1 - val) - ( localPrestVal[i] * Val)
									)

									else
										p = (localCurntVal[i]) * (1 - val) + ( localPrestVal[i] * Val) -- switch Mode

									SubFrame[i][Handel].transform.controller[1][2][1].value = p.x
									SubFrame[i][Handel].transform.controller[1][2][2].value = p.y
									SubFrame[i][Handel].transform.controller[1][2][3].value = p.z
								)
								Applysl.value = 0
								GUIRO.ReposHandels() -- update the joysticks
							)
							--########################################
							on nameet entered newname do if nameet.text != "" do
							(
								if keyboard.controlPressed then (
									if Poslb.selection > 0 do
										Presets[Poslb.selection][1] = newname -- rename selected pos
								)
								else (
									-- Create a preset ---
									newpreset = #(newname)
									for Su in SubFrame do (
										X = Su[Handel].transform.controller[1][2][1].value
										Y = Su[Handel].transform.controller[1][2][2].value
										Z = Su[Handel].transform.controller[1][2][3].value
										local newpos = #(Su[Handel].name, [X, Y, Z])
										append newpreset newpos
									)

									-- lock in avalible presets --
									IsNew = true
									for i = 1 to Presets.count do
										if newname == Presets[i][1] do (
											Presets[i] = newpreset -- replace if avalible
											IsNew = false
											break 
										)

									-- add new pos
									if IsNew do
										append Presets newpreset
								)

								-- Sort --
								local Tarray = #()
								for P in Presets do
									append Tarray P[1]
								sort Tarray
								local TParray = #()
								for T in Tarray do
									for P in Presets do
										if T == P[1] do (
											append TParray P
											break
										)
								Presets = deepcopy TParray
								-- Update other parts --
								UpdateListBox()
								SavePresetsTofile()
								nameet.text = ""
							)
							global CurntVal = #()
							global PrestVal = #()
							on Applysl buttondown do if Poslb.selection > 0 do
							(
								for Su in SubFrame do (
									X = Su[Handel].transform.controller[1][2][1].value
									Y = Su[Handel].transform.controller[1][2][2].value
									Z = Su[Handel].transform.controller[1][2][3].value
									append CurntVal [X, Y, Z]
									for i = 2 to Presets[Poslb.selection].count do (
										if Presets[Poslb.selection][i][1] == Su[Handel].name do (										
											append PrestVal Presets[Poslb.selection][i][2]
											break
										)
									)
								)
							)
							on Applysl changed Val do if Poslb.selection > 0 do
							(
								CombineMode = if Poslb.selected[1] == "+" then true else false
								for i = 1 to SubFrame.count do (
									 -- Combine mode
									if keyboard.controlPressed or CombineMode then (
										if PrestVal[i] == [0,0,0] then
											P = (CurntVal[i])
										else
											p = (CurntVal[i]) * (1 - val) + ( PrestVal[i] * Val)
									)
									else if keyboard.altPressed then (
										if PrestVal[i] == [0,0,0] then
											P = (CurntVal[i])
										else
											p = (CurntVal[i]) * (1 - val) - ( PrestVal[i] * Val)
									)

									else p = (CurntVal[i]) * (1 - val) + ( PrestVal[i] * Val) -- switch Mode

									SubFrame[i][Handel].transform.controller[1][2][1].value = p.x
									SubFrame[i][Handel].transform.controller[1][2][2].value = p.y
									SubFrame[i][Handel].transform.controller[1][2][3].value = p.z
								)
								-- GUIRO.ReposHandels() -- realtime update
							)
							on Applysl buttonup do 
							(
								CurntVal = #()
								PrestVal = #()
								Applysl.value = 0
								GUIRO.ReposHandels() -- update the joysticks
							)
							on Applysl rightClick do () -- saden load --##
						)-- end of posmanager roout
						createdialog PosManager width:150 height:(FrameHeight + 61) pos:(GetDialogPos  GUIRO + [FrameWidth + 10, 1]) style:#()
					)
					else if PosManager != undefined do destroydialog PosManager
				)
			)-- end of roolout
			createdialog GUIRO width:FrameWidth height:(FrameHeight + 30) style:#(#style_titlebar, #style_border, #style_sysmenu, #style_minimizebox)--, #style_resizing) 
			--======================================================================================================================================================================--
		) -- end of SubFrame count
	)-- end of if selection count
) -- End of function
-- Scan the scene for Facial UIs --
for R in Shapes do
(
	if classof R.baseobject == Rectangle do
	(
		ISFUI = false
		for SR in R.children do for H in SR.children do
		(
			if classof SR.baseobject == Rectangle do
			(
				try (
					if H.transform.controller[1] as string == "SubAnim:Position" do
						if H.transform.controller[1][1] as string == "SubAnim:Frozen_Position" do
							if H.transform.controller[1][2] as string == "SubAnim:Zero_Pos_XYZ" do (
								IsJoy = false

								-- check in X_Position Controller --
							if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do
								ISFUI = true
	
							-- check in Y_Position Controller --
							if H.transform.controller[1][2][1][1] as string == "SubAnim:Limited_Controller__Bezier_Float" do
								ISFUI = true

							if ISFUI do
								exit
						)
				)
				catch(
					ISFUI = false
				)
			)
		)
		if ISFUI do append FacialUIs R
	)
)-- End of scan
-- check the scan result --
if FacialUIs.count == 1 then CreateFGUI FacialUIs[1]
else if FacialUIs.count > 0 do
(
	-- Create Character Selector --
	local S = "rollout SelectCharacter \"Select Character\"\n"
	S += "(\n"
	S += "	on SelectCharacter open do try(SetDialogPos SelectCharacter (execute(getINISetting (getMAXIniFile()) \"AutoFacialGUI\" \"pos\")))catch()\n"
	for i = 1 to FacialUIs.count do
	(
		S += "		button BT" + i as string + " \"" + (filterstring FacialUIs[i].name "_")[1] + "\" width:150\n"
		S += "		on BT" + i as string + " pressed do\n"
		S += "		(\n"
		S += " 			Select $'" + FacialUIs[i].name  + "'\n"
		S += "			CreateFGUI FacialUIs[" + i as string + "]\n"
		S += "			destroydialog SelectCharacter\n"
		S += "		)\n"
	)
	S += "	button Cancel_bt \"Cancel\" width:150\n"
	S += "		on Cancel_bt pressed do destroydialog SelectCharacter\n"
	S += ")\n"
	S += "createdialog SelectCharacter"
	execute S
)
-- Update runner macro Macro --
-- execute ("macroScript FacialGUI tooltip:\"Facial GUI\" category:\"Animation Tools\" ( try(filein \"" + getSourceFileName() +"\")catch() )")