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

function make_ik_stretchable =
(	
	local IKS = (for i in selection where classof i == IK_Chain_Object collect i)
	
    for i in IKS do (
		mode = ""
		if i.transform.controller[1] as string == "SubAnim:Swivel_Angle" do (
            mode = "HIK"
        )
		
        if i.transform.controller[1] as string == "SubAnim:Twist_Start_Angle" do(
            mode = "SPIK"
        )

        if mode == "HIK" then (
			select #(i.transform.controller.startJoint,i.transform.controller.endJoint)
			Mybone = listofbones_fn()
			XreftoXYZ_fn Mybone
			bsize = #()
            orig = 0
			
            for j = 1 to Mybone.count-1 do (
                append bsize (distance Mybone[j] Mybone[j+1])
            )
			
            for j = 1 to bsize.count do (
                orig += bsize[j]
            )
			
            for j = 2 to Mybone.count do (
				mynewcontroller = float_script()
				mynewcontroller.AddNode "start" Mybone[1]
				mynewcontroller.AddNode "end" i
				myscript = "orig = " + orig as string + "\n"
				myscript += "D = distance start.pos end.pos\n"
				myscript += "if D > orig then xpos = " + bsize[j-1] as string + " + ((D - orig)/ "+ (Mybone.count-1) as string +")\n"
				myscript += "else xpos = "  + bsize[j-1] as string
				mynewcontroller.script = myscript
				Mybone[j].transform.controller.FK_Sub_Control.controller.Position.controller.X_Position.controller = mynewcontroller
			)
		) 
		else if mode == "SPIK" then (
			select #(i.transform.controller.startJoint,i.transform.controller.endJoint)
			Mybone = listofbones_fn()
			XreftoXYZ_fn Mybone
			myspline = i.transform.controller.startJoint.position.controller.path_constraint.path
			bsize = #(); orig = curveLength myspline;
			for j = 1 to Mybone.count-1 do (
                append bsize (distance Mybone[j] Mybone[j+1])
            )

            for j = 1 to bsize.count do (
                orig += bsize[j]
            )

            for j = 2 to Mybone.count do (
				mynewcontroller = float_script()
				mynewcontroller.AddNode "start" Mybone[1]
				mynewcontroller.AddNode "end" i
				mynewcontroller.AddNode "spline" myspline
				myscript = "orig = " + (orig / 2) as string + "\n"
				myscript += "D = curveLength spline\n"
				myscript += "if D > orig then xpos = " + bsize[j-1] as string + " + ((D - orig)/ "+ (Mybone.count-1) as string +")\n"
				myscript += "else xpos = "  + bsize[j-1] as string
				mynewcontroller.script = myscript
				Mybone[j].transform.controller.FK_Sub_Control.controller.Position.controller.X_Position.controller = mynewcontroller
			)
			
            thepoint = myspline.modifiers[#Spline_IK_Control].helper_list
			addcontroller_fn i "Position_XYZ" undefined
			addcontroller_fn i "Position_Constraint" thepoint[thepoint.count]
		)
	)

    select IKS
)


function clear_transform_controllers =
(
	for obj in selection do (
		local OrigTransform = obj.transform
		try( obj.Transform.controller = prs())catch()
		
        try( obj.pos.controller = Position_XYZ())catch()
        
        try(obj.pos.controller.X_Position.controller = bezier_float ())catch()
        try(obj.pos.controller.Y_Position.controller = bezier_float ())catch()
        try(obj.pos.controller.Z_Position.controller = bezier_float ())catch()
		
        try(obj.rotation.controller = Euler_XYZ())catch()
        
        try(obj.rotation.controller.X_Rotation.controller = bezier_float ())catch()
        try(obj.rotation.controller.Y_Rotation.controller = bezier_float ())catch()
        try(obj.rotation.controller.Z_Rotation.controller = bezier_float ())catch()
		
        try(obj.scale.controller = bezier_scale())catch()
		try(obj.transform = OrigTransform)catch()
	)
)



function spline_control =
(
	-- This cool is not create by me but is a cool one --
	if isKindOf $ Shape do (
		local obj = $
		local master = obj.baseObject[#Master]
		animateVertex obj #all

		TMDef = attributes pointTM attribID:#(0x174e3aa5, 0x67203398) \
				(parameters data (pos type:#point3; invTM type:#matrix3))

		fn getMatricesAlongSplineCurve spl curve count closed: =
		(
			local lastTangent = tangentCurve3D spl curve 0
			local lastRot = arbAxis lastTangent as quat
			local step = 1d0 / (count - (if closed then 0 else 1))

			for i = 0 to count collect (
				local location = interpCurve3D spl curve (i * step) pathParam:on
				local tangent = tangentCurve3D spl curve (i * step) pathParam:on

				local axis = normalize (cross tangent lastTangent)
				local theta = acos (dot tangent lastTangent)
				local rotation = quat theta axis

				lastTangent = tangent
				lastRot *= rotation
				translate (lastRot as matrix3) location
			)
		)

		fn addCtrl subAnim obj pt =
		(
			local ctrl = Point3_Script()
			custAttributes.add ctrl TMDef

			subAnim.controller = ctrl
			ctrl.addObject #pt (NodeTransformMonitor node:pt)
			ctrl.addObject #master (NodeTransformMonitor node:obj)
			ctrl.script = "if isValidNode pt do this.pos = pt.objectTransform.pos\n" + \
				"if isValidNode master do this.invTM = inverse master.objectTransform\n" + \
				"this.pos * this.invTM"
		)

		for spl = 1 to numSplines obj do (
			local knotCount = numKnots obj spl
			local knotTMs = getMatricesAlongSplineCurve obj spl knotCount closed:(isClosed obj spl)

			for knot = 1 to knotCount do (
				local knotPos = master["Spline_" + spl as string + "___Vertex_" + knot as string]
				local knotInVec = master["Spline_" + spl as string + "___InVec_" + knot as string]
				local knotOutVec = master["Spline_" + spl as string + "___OutVec_" + knot as string]

				local posPt = in obj Point prefix:"Knot" wirecolor:green cross:on box:off transform:knotTMs[knot]
				addCtrl knotPos obj posPt

				if getKnotType obj spl knot != #corner do (
					addCtrl knotInVec obj (in posPt Point prefix:"Tangent" wirecolor:green cross:off box:off centerMarker:on pos:(knotInVec.value * obj.objectTransform))
					addCtrl knotOutVec obj (in posPt Point prefix:"Tangent" wirecolor:green cross:off box:off centerMarker:on pos:(knotOutVec.value * obj.objectTransform))
				)
			)
		)
	)
)



rollout MorpherConnectorRO "Morph Chanel Connector"
(
    local Leftlist = #(), RightList = #()

    pickbutton leftpbtn "Pic object"  width:120 height:30 align:#Left autoDisplay:true across:2
    pickbutton rightpbtn "Pic object"  width:120 height:30 align:#Right autoDisplay:true
    listbox leftlb "" width:120 height:30 align:#Left across:2
    listbox Righttlb "" width:120 height:30 align:#Right
    button CLtRbtn ">" width:25 align:#Center offset:[0, -leftlb.height ] tooltip:"Copy Left to Right"
    button CRtLbtn "<"  width:25 align:#Center tooltip:"Copy Right to Left"
    button ILtRbtn ":>"  width:25 align:#Center tooltip:"Instance left to Right"
    button IRtLbtn "<:"  width:25 align:#Center tooltip:"Instance Right to Left"

    function GetMTList Obj =
    (
        local hasmorpher = false, Targets = #()

        for i in Obj.Modifiers do (
            if IsValidMorpherMod i do (
                hasmorpher = true
                break
            )
        )

        if hasmorpher do (
            Local T = #()

            for i = 1 to 100 do (
                if WM3_MC_GetName Obj.morpher i != "- empty -" do (
                    append T #(i, (i as string + ":" + WM3_MC_GetName Obj.morpher i))
                    if T.count >= 10 do ( 
                        join Targets T
                        T = #()
                    )
                )

                if i == 100 do if T.count > 0 do join Targets T
            )
        )
        return Targets
    )
    
    function connector Obj1 Obj2 Ind1 Ind2 Mode =
    (
        if Obj1 != undefined and Obj2 != undefined and Ind1 > 0 and Ind2 > 0 do (
            case Mode of (
                "copy": Obj2.morpher[Ind2].controller = copy Obj1.morpher[Ind1].controller
                "instance": Obj2.morpher[Ind2].controller = Obj1.morpher[Ind1].controller
            )
        )
    )

    on leftpbtn picked obj do
    (
        LeftObj = leftpbtn.object
        if LeftObj != undefined do (
            Leftlist = GetMTList LeftObj
            leftlb.items = for n in Leftlist collect n[2]
        )
    )
    
    on rightpbtn picked obj do
    (
        RightObj = rightpbtn.object
        if RightObj != undefined do (
            RightList = GetMTList RightObj
            Righttlb.items = for n in RightList collect n[2]
        )
    )
    
    on CLtRbtn pressed do (
        connector leftpbtn.object rightpbtn.object leftlb.selection Righttlb.selection "copy"
    )

    on CRtLbtn pressed do (
        connector rightpbtn.object leftpbtn.object Righttlb.selection leftlb.selection "copy"
    )
    
    on ILtRbtn pressed do (
        connector leftpbtn.object rightpbtn.object leftlb.selection Righttlb.selection "instance"
    )
    
    on IRtLbtn pressed do (
        connector rightpbtn.object leftpbtn.object Righttlb.selection leftlb.selection "instance"
    )
)

function morpher_connector =
(
	Createdialog MorpherConnectorRO width:300
)



function joystick_creator =
(
	local Rects = #(), JoyMode = undefined;
	-- Analioze the object on scene and cose compatibles for create joysticks --
	function Scanfn =
	(
		Rects = #()
		TMode = undefined;
		for R in selection do (
            if classof R == Rectangle do (
                if R.children.count == 0 do (
                    if R.width == R.length then (
                        NewMode = "J"
                    )
                    else if R.width > R.Length then (
                        if R.Length > R.width / 2.0 then (
                            NewMode = "J"
                        )
                        else (
                            NewMode = "H"
                        )
                    )
                    else if R.length > R.width then (
                        if R.width > R.length / 2.0 then (
                            NewMode = "J"
                        )
                        else(
                            NewMode = "V"
                        )
                    )
                    if TMode == undefined then (
                        TMode = NewMode
                        append Rects R
                    )
                    else if NewMode == TMode do (
                        append Rects R
                        break
                    )
                )
            )
        )
		Return TMode
	)
	local TheMode = Scanfn()
	
    function JoystickCreatorDialog = 
    (
        if selection.count > 0 do (
            TheMode = Scanfn()
            if Rects.count > 0 do (
                select Rects
                R = Rects[1]
                -- Geus Mode --
                local Horizontal = false, Vertival = false
                
                if R.width == R.length then (
                    TheMode = "J"
                )
                else if R.width > R.Length then (
                    if R.Length > R.width / 2.0 then (
                        TheMode = "J"
                    )
                    else (
                        TheMode = "H"
                    )
                )
                else if R.length > R.width then (
                    if R.width > R.length / 2.0 then (
                        TheMode = "J"
                    )
                    else (
                        TheMode = "V"
                    )
                )

                -- Setup a mode selector dialog --
                rollout JoystickCreatorRo ""
                (
                    timer clock interval:30
                    button ULbt "" width:50 height:50 across:3
                    button UCbt "" width:50 height:50
                    button URbt "" width:50 height:50
                    button MLbt "" width:50 height:50 across:3
                    button MCbt "" width:50 height:50
                    button MRbt "" width:50 height:50
                    button DLbt "" width:50 height:50 across:3
                    button DCbt "" width:50 height:50
                    button DRbt "" width:50 height:50

                    on clock tick do (
                        if keyboard.escPressed do (
                            destroydialog JoystickCreatorRo
                        )
                    )
                    
                    on JoystickCreatorRo open do
                    (
                        buttons = #()
                        
                        case TheMode of (
                            "J": (Horizontal = true; Vertival = true;)
                            "H": (buttons = #(ULbt, UCbt, URbt, DLbt, DCbt, DRbt); Horizontal = true; Vertival = false;)
                            "V": (buttons = #(ULbt, MLbt, DLbt, URbt, MRbt, DRbt); Horizontal = false; Vertival = true;)
                        )
                        
                        for b in buttons do (
                            b.visible = false
                        )
                    )
                    
                    function CreateJoystickfn Left Right Up Down =
                    (
                        for Frame in Rects do (
                            --## check if another joy avalible delete older one --
                            Frame.cornerRadius = if Horizontal and Vertival then (Frame.width + Frame.length) / 15.0 else if Frame.width < Frame.length then Frame.width / 2.0 else  Frame.length / 2.0 -- Round the corners
                            
                            -- create handel and gide lines --
                            Handel = if Horizontal and Vertival then circle radius:Frame.cornerRadius else circle radius:Frame.cornerRadius--rectangle width:Frame.cornerRadius length:Frame.cornerRadius cornerRadius:(Frame.cornerRadius / 10.0)
                            Handel.transform = Frame.transform
                            Handel.parent = Frame
                            
                            -- set defoult position --
                            XL = if Left then Frame.width / 2.0 - Frame.cornerRadius else 0
                            XR = if Right then Frame.width / 2.0 - Frame.cornerRadius else 0
                            in coordsys Frame Handel.pos.x += XR - XL
                            
                            YU = if Down then Frame.Length / 2.0 - Frame.cornerRadius else 0
                            YD = if Up then Frame.Length / 2.0 - Frame.cornerRadius else 0
                            in coordsys Frame Handel.pos.Y -= YU - YD
                            
                            -- Frease Position -- 
                            Handel.pos.controller = Position_List()
                            Handel.pos.controller.Position_XYZ.controller = bezier_position ()
                            Handel.pos.controller.setname 1 "Frozen Position"
                            Handel.pos.controller.Available.controller = Position_XYZ ()
                            Handel.pos.controller.setname 2 "Zero Pos XYZ"
                            Handel.position.controller.SetActive 2
                            
                            -- Frease rotation --
                            Handel.rotation.controller = rotation_list()
                            Handel.rotation.controller.setname 1 "Frozen Rotation"
                            Handel.rotation.controller.Available.controller  = Euler_XYZ()
                            Handel.rotation.controller.setname 2 "Zero Euler XYZ"
                            
                            -- Create Limite controllers --
                            Handel.pos.controller.Zero_Pos_XYZ.controller.X_Position.controller = float_limit ()
                            upper_limit = if not Horizontal then 0 else if Left then Frame.width - Frame.cornerRadius * 2 else if Right then 0 else Frame.width / 2 - Frame.cornerRadius
                            Handel.pos.controller.Zero_Pos_XYZ.controller.X_Position.controller.upper_limit = upper_limit
                            lower_limit = if not Horizontal then 0 else -(if Right then Frame.width - Frame.cornerRadius * 2 else if Left then 0 else Frame.width / 2 - Frame.cornerRadius)
                            Handel.pos.controller.Zero_Pos_XYZ.controller.X_Position.controller.lower_limit = lower_limit
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Y_Position.controller = float_limit ()
                            upper_limit = if not Vertival then 0 else if Up then 0 else if Down then Frame.Length - Frame.cornerRadius * 2  else Frame.Length / 2 - Frame.cornerRadius
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Y_Position.controller.upper_limit = upper_limit
                            lower_limit = if not Vertival then 0 else -(if Down then 0 else if Up then Frame.Length - Frame.cornerRadius * 2 else Frame.Length / 2 - Frame.cornerRadius)
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Y_Position.controller.lower_limit = lower_limit
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Z_Position.controller = float_limit ()
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Z_Position.controller.upper_limit = 0
                            Handel.pos.controller.Zero_Pos_XYZ.controller.Z_Position.controller.lower_limit = 0
                            
                            -- Setup tools -------------------------------------------------------------------------------------------------------------------
                            AttributeHolder = (EmptyModifier ())
                            AttributeHolder.name = "Controller"
                            Ca = attributes Joystick
                            (
                                parameters params_pr rollout:params_ro
                                (
                                    Up type:#float range:[0.0,100.0,0.0] ui:Usp
                                    Down type:#float range:[0.0,100.0,0.0] ui:Dsp
                                    Left type:#float range:[0.0,100.0,0.0] ui:Lsp
                                    Rigth type:#float range:[0.0,100.0,0.0] ui:Rsp
                                )
                                
                                rollout params_ro "Params"
                                ( 
                                    Global _ME_ = undefined
                                
                                    function Connectfn Controller Target =
                                    (
                                        if _ME_ != undefined and Target != undefined do (
                                            Global _TheSpecialTargetNode_ = Target
                                            hasmorpher = false
                                            for i in Target.Modifiers do (
                                                if IsValidMorpherMod i do (
                                                    hasmorpher = true
                                                    break
                                                )
                                            )
                                            
                                            if hasmorpher then (
                                                Local T = #(), Targets = #()
                                                for i = 1 to 100 do (
                                                    if WM3_MC_GetName Target.morpher i != "- empty -" do (
                                                        append T #(i, WM3_MC_GetName Target.morpher i)

                                                        if T.count >= 10 do (
                                                            append Targets T
                                                            T = #()
                                                        )
                                                    )
                                                    if i == 100 do (
                                                        if T.count > 0 do (
                                                            append Targets T
                                                        )
                                                    )
                                                )
                                                
                                                Local BtnWidth = 100, BtnHeight = 23
                                                Local W = Targets.count * (BtnWidth + 5)
                                                
                                                fn GetPos i j BW BH =
                                                (
                                                    x = ((i - 1) * (BW + 3)) + 5
                                                    y = ((j - 1) * (BH + 3)) + 5
                                                    return [x ,y ] as string
                                                )
                                                S = "rollout Connectorro \"Connector\"\n"
                                                S += "(\n"
                                                
                                                for i = 1 to Targets.count do (
                                                    for j = 1 to Targets[i].count do (
                                                        S += "	Button Btn" + (i * 10 + j) as string + " \""+ Targets[i][j][2] + "\" width:" + BtnWidth as string + " Pos:" + GetPos i j BtnWidth BtnHeight +"\n"
                                                        S += "	on Btn" + (i * 10 + j) as string + " pressed do\n"
                                                        S += "	(\n"
                                                        --S += "		$" + Target.name + ".morpher[" + Targets[i][j][1] as string +"].controller = $" + _ME_.name + ".modifiers[#Controller]." + Controller + ".controller\n"
                                                        S += "		" + "_TheSpecialTargetNode_" + ".morpher[" + Targets[i][j][1] as string +"].controller = $'" + _ME_.name + "'.modifiers[#Controller]." + Controller + ".controller\n"
                                                        S += "		Destroydialog Connectorro\n"
                                                        S += "	)\n"
                                                    )
                                                )
                                                S += ")\n"
                                                S += "createdialog Connectorro width:" + W as string
                                                execute S
                                            )
                                            else ()
                                        )
                                    )
                                    
                                    on params_ro open do (
                                        if selection.count == 1 do(
                                            _ME_ = selection[1]
                                        )
                                    )
                                    
                                    pickbutton Cubt "Up" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
                                    spinner Usp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false
                                    on Cubt picked Targ do Connectfn "up" Targ
                                    
                                    pickbutton CDbt "Down" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
                                    spinner Dsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false
                                    on CDbt picked Targ do Connectfn "down" Targ
                                    
                                    pickbutton CLbt "Left" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
                                    spinner Lsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false
                                    on CLbt picked Targ do Connectfn "left" Targ
                                    
                                    pickbutton CRbt "Right" width:50 across:2 tooltip:"Connect To.." offset:[-15,0] 
                                    spinner Rsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false
                                    on CRbt picked Targ do Connectfn "rigth" Targ
                                )
                            )
                            custAttributes.add AttributeHolder Ca
                            -- Up --
                            AttributeHolder.Joystick.Up.controller = Float_script()
                            TheLimit = Handel.pos.controller.Zero_Pos_XYZ.Y_position.controller.Limits.Upper_Limit
                            AttributeHolder.Joystick.Up.controller.addTarget "Value" Handel.pos.controller.Zero_Pos_XYZ.Y_position.controller
                            AttributeHolder.Joystick.Up.controller.Script = "if Value > 0 then (Value / " + TheLimit as string + ") * 100 else 0"
                            -- Down --
                            AttributeHolder.Joystick.Down.controller = Float_script()
                            TheLimit = Handel.pos.controller.Zero_Pos_XYZ.Y_position.controller.Limits.Lower_Limit
                            AttributeHolder.Joystick.Down.controller.addTarget "Value" Handel.pos.controller.Zero_Pos_XYZ.Y_position.controller
                            AttributeHolder.Joystick.Down.controller.Script =  "if Value < 0 then (Value / " + TheLimit as string + ") * 100 else 0"
                            -- Left --
                            AttributeHolder.Joystick.Left.controller = Float_script()
                            TheLimit = Handel.pos.controller.Zero_Pos_XYZ.X_position.controller.Limits.Lower_Limit
                            AttributeHolder.Joystick.Left.controller.addTarget "Value" Handel.pos.controller.Zero_Pos_XYZ.X_position.controller
                            AttributeHolder.Joystick.Left.controller.Script =  "if Value < 0 then (Value / " + TheLimit as string + ") * 100 else 0"
                            --Right --
                            AttributeHolder.Joystick.Rigth.controller = Float_script()
                            TheLimit = Handel.pos.controller.Zero_Pos_XYZ.X_position.controller.Limits.Upper_Limit
                            AttributeHolder.Joystick.Rigth.controller.addTarget "Value" Handel.pos.controller.Zero_Pos_XYZ.X_position.controller
                            AttributeHolder.Joystick.Rigth.controller.Script =  "if Value > 0 then (Value / " + TheLimit as string + ") * 100 else 0"
                                
                            addModifier Handel AttributeHolder 
                            -----------------------------------------------------------------------------------------------------------------------------------
                        )
                        destroydialog JoystickCreatorRo
                    )
                    on ULbt pressed do CreateJoystickfn true false true false
                    on UCbt pressed do CreateJoystickfn false false true false
                    on URbt pressed do CreateJoystickfn false true true false
                    on MLbt pressed do CreateJoystickfn true false false false
                    on MCbt pressed do CreateJoystickfn false false false false
                    on MRbt pressed do CreateJoystickfn false true false false
                    on DLbt pressed do CreateJoystickfn true false false true
                    on DCbt pressed do CreateJoystickfn false false false true
                    on DRbt pressed do CreateJoystickfn false true false true
                )
                createdialog JoystickCreatorRo width:190 --style:#()
            )
        )
    )

    if Rects.count > 0 then (
        JoystickCreatorDialog()
    )
	else (
		rollout JoystickConnectorro "Joystick Creator"
		(
			button Convertobtn "Convert to Joystick" width:150
			on Convertobtn pressed do JoystickCreatorDialog()
			button MorphTargetPickerbtn "Morph Target Picker" width:150
			on MorphTargetPickerbtn pressed do
			(
				rollout MorphargetPicker "Morph Target Picker"
				(
					pickbutton pickmasterpbtn "Pick Master" autoDisplay:true width:150
					label Msglb ""
					button selectionorderbtn "By Selection Order" enabled:false width:150
					button Alphbetorcerbtn "By Alphabet Order" enabled:false width:150
					button DistanceOrder "By Distance Order" enabled:false width:150
					function PickMaster Obj =
					(
						if superclassof Obj.baseobject == GeometryClass then
						(
							pickmasterpbtn.object = Obj
							Msglb.caption = "Select the targets now"
							selectionorderbtn.enabled = true
							Alphbetorcerbtn.enabled = true
							DistanceOrder.enabled = true
						)
						else
						(
							pickmasterpbtn.object = undefined
							Msglb.caption = "	Pick a Geometry Object"
							selectionorderbtn.enabled = false
							Alphbetorcerbtn.enabled = false
							DistanceOrder.enabled = false
						)
					)
					on pickmasterpbtn picked obj do PickMaster Obj
					on pickmasterpbtn rightclick do if selection.count == 1 do PickMaster selection[1]
					function AddMorpher obj =
					(
						hasmorpher = false
						for i in pickmasterpbtn.object.Modifiers do if IsValidMorpherMod i do hasmorpher = true 
						if not hasmorpher do addModifier pickmasterpbtn.object (Morpher())
					)
					function NextEmptySlot Obj =
					(
						index = 1
						for i = 100 to 1 by -1 do if WM3_MC_GetTarget Obj.morpher i == undefined do ( index = i; break; )
						return index
					)
					on selectionorderbtn pressed do
					(
						AddMorpher pickmasterpbtn.object
						local Targets = #()
						for Sel in selection do append Targets Sel
						for T in Targets do ( index = NextEmptySlot pickmasterpbtn.object; WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T; )
					)
					on Alphbetorcerbtn pressed do
					(
						AddMorpher pickmasterpbtn.object
						local SelectedTargets = #(), Targets = #(), Names = #();
						for Sel in selection do ( append SelectedTargets Sel; append Names Sel.name; )
						sort Names
						for N in Names do for ST in SelectedTargets do if ST.Name == N do ( append Targets ST; break; )
						for T in Targets do ( index = NextEmptySlot pickmasterpbtn.object; WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T; )
					)
					on DistanceOrder pressed do
					(
						AddMorpher pickmasterpbtn.object
						local Targets = #()
						for Sel in selection do append Targets Sel
						for i = 1 to Targets.count do
						(
							Local Dist = Distance pickmasterpbtn.object Targets[i]
							Local index = i
							for j = i + 1 to Targets.count do if Distance pickmasterpbtn.object Targets[j] < Dist do index = j
							if index > i do ( T = Targets[index]; DeleteItem Targets index; InsertItem T Targets i )
						)
						for T in Targets do ( index = NextEmptySlot pickmasterpbtn.object; WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T; )
					)
				)
				createdialog MorphargetPicker
				destroydialog JoystickConnectorro
			)
		)
		createdialog JoystickConnectorro
	)
)



function hi_solver =
(
	function getmasterandtarget_fn =
	(
		masterbone = undefined
        targetbone = undefined
		
        if selection.count == 1 do (
            if classof selection[1] == BoneGeometry or (filterstring (selection[1] as string) "$:")[1] == "Bone" do (
			    masterbone = selection[1]
			    targetbone = masterbone.children[1]
			    while true do (
                    if targetbone.children.count == 1 then (
                        targetbone = targetbone.children[1]
                    )
                    else (
                        exit
                    )
                )
		    )
        )

        if selection.count == 2 do (
			A = selection[1]
            B = selection[2]

            while true do (
                if A.parent == undefined then (
                    exit
                )
                else if A.parent == B then (
                    targetbone = selection[1]
                    masterbone = selection[2]
                    exit
                )
                else (
                    A = A.parent
                )
            )

            while true do (
                if B.parent == undefined then (
                    exit
                )
                else if B.parent == A then (
                    targetbone = selection[2]
                    masterbone = selection[1]
                    exit
                )
                else (
                    B = B.parent
                )
            )
		)
		
        return #(masterbone,targetbone)
	)

    function listofbones_fn =
	(
		local retval = #()
		local MT = getmasterandtarget_fn()
		local masterbone = MT[1], targetbone = MT[2]
		local currentbone = masterbone
		
        if masterbone != undefined and targetbone != undefined do (
			while true do (
                if currentbone.children[1] != targetbone then (
                    append retval currentbone
                    currentbone = currentbone.children[1]
                )
                else (
                    append retval currentbone
                    append retval targetbone
                    exit
                )
            )
        )
		
        return retval
	)
	
    if selection.count != 0 do
	(
		local Mybone = listofbones_fn()
		local MT = getmasterandtarget_fn()
		local masterbone = MT[1]; targetbone = MT[2]
		if masterbone == undefined and targetbone == undefined then (
			local parents = (for i in selection where i.children.count == 1 and (filterstring (i.children[1] as string) "$:")[1] == "Bone" collect i)
			local IKS = #()
			for i in parents do (
				select i
				Mybone = listofbones_fn()
				MT = getmasterandtarget_fn()
				masterbone = MT[1]
				targetbone = MT[2]
				if masterbone != undefined and targetbone != undefined then (
					local NewIK = IKSys.ikChain masterbone targetbone "IKHISolver"
					try(NewIK.transform.controller.VHTarget = upnode_pb.object)catch()
					append IKS NewIK
				)
			)
			select IKS
		)
		else (
			NewIK = IKSys.ikChain masterbone targetbone "IKHISolver"
			try(NewIK.transform.controller.VHTarget = upnode_pb.object)catch()
			select NewIK
		)
	)-- End of if HI
)



-- macroscript TransformHolder tooltip:"Transform Holder" category:"Animation Tools"

rollout TransformHolderRO "Transform Holder"
(
    local Transforms = #(), Objs = #()
    
    button GetTransformbt "Get Selected transform" width:150
    button SetTransformbt "Set Transfrom" width:150

    on GetTransformbt pressed do
    (
        Transforms = #()
        Objs = #()
        for i in selection do (
            append Transforms i.transform
            append Objs i
        )
    )

    on SetTransformbt pressed do (
        for i = 1 to Objs.count do (
            try (
                Objs[i].transform = Transforms[i]
            )
            catch (
                -- Pass
            )
        )
    )
)

function open_transform_holder_dialog =
(
	createdialog TransformHolderRO
)