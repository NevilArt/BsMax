class Math:
	def ComparTransform(Tr1, Tr2, Tol):
		def ComparP3(P1, P2, Tol):
			def ComparF(F1, F2, Tol):
				if F1 != F2:
					Heigher, Lower = 0,0
					if F1 >= F2:
						Heigher = F1
						Lower = F2
					else:
						Heigher = F2
						Lower = F1
					if Heigher <= Lower + Tol:
						return True 
					else:
						return False
				else:
					return True
			X = ComparF(P1.x, P2.x, Tol)
			Y = Compar(P1.y, P2.y, Tol)
			Z = ComparF(P1.z, P2.z, Tol)
			return  (X and Y and Z)
		if Tr1 != None and Tr2 != None:
			P1,P2 = Tr1.Pos, Tr2.Pos
			Q1 = quatToEuler(Tr1.rotation, order=1)
			Q2 = quatToEuler(Tr2.rotation, order=1)
			CP = P1 == P2
			CQ = ComparP3(Q1, Q2, Tol)
			return (CP and CQ)
		else:
			return False

class Sequence:
	def FillSequenceGaps(Seq, Size):
		Ret = []
		for i in range(Seq.count):
			# Fill sequence
			Ret.append(Seq[i])
			if i < Seq.count:
				# start of Gap
				if Seq[i + 1] > Seq[i] + 1:
					# accept of gap size
					if Seq[i] + Size > Seq[i + 1]:
						# Fill gap
						# for j = Seq[i] + 1 to Seq[i + 1] - 1:
						for j in range(Seq[i] + 1, Seq[i + 1] - 1):
							Ret.append(j)
		return Ret
		
	def RemoveTinys(Seq, Size):
		Ret,i = [], 1
		while i < Seq.count:
			# Check is sequence
			if Seq[i] + 1 == Seq[i + 1]:
				NewSeq = []
				# collect sequenses
				for j in range(i, Seq.count):
					if Seq[j] + 1 == Seq[j + 1]:
						NewSeq.append(Seq[j])
					else:
						NewSeq.append(Seq[j])
						break
				# ignore is to short
				if NewSeq.count > Size:
					Ret += NewSeq
				i += NewSeq.count
			else:
				Ret.append(Seq[i])
				i += 1
		if not Seq[Seq.count] in Ret:
			Ret.append(Seq[Seq.count])
		return Ret
	
	def FramesToString(Frames):
		Str = ''
		for i in rabge(Frames.count - 1):
			if Frames[i] >= 0:
				if Frames[i] + 1 == Frames[i + 1]:
					if Str[Str.count] != "-":
						if Str.count > 0 and Str[Str.count] != ",":
							Str += ","
						Str += str(Frames[i]) + "-"
				else:
					if Str.count > 0 and Str[Str.count] != "-" and Str[Str.count] != ",":
						Str += ","
					Str += str(Frames[i])
		if Str[Str.count] == "-":
			Str += str(Frames[Frames.count])
		return Str
	
	def HasRight(Frms, Index):
		Ret = False
		if Index < Frms.count:
			if Frms[index] + 1 == Frms[index + 1]:
				Ret = True
		return Ret
	
	def HasLeft(Frms, Index):
		Ret = False
		if Index > 1:
			if Frms[index] - 1 == Frms[index - 1]:
				Ret = True
		return Ret
	
	def IsRightStand(Frms, Index, Count):
		Ret = False
		if Index + 1 < Frms.count:
			if Frms[Index] + Count < Frms[Index + 1]:
				Ret = True
		return Ret
	
	def IsLeftStand(Frms, Index, Count):
		Ret = False
		if Index - 1 > 0:
			if Frms[Index - 1] + Count < Frms[Index]:
				Ret = True
		return Ret
	
	def IsRightSeq(Frms, Index, Count):
		Ret = True
		for i in range(Index,Index + count):
			if i <= Frms.count:
				Ret = (Frms[i] + 1 == Frms[i + 1])
				if not Ret:
					break
		return Ret
	
	def IsLeftSeq(Frms, Index, Count):
		Ret = True
		for i in range(Index - count, Index):
			if i > 0:
				Ret = (Frms[i] + 1 == Frms[i + 1])
				if not Ret:
					break
			else:
				Ret = False
				break
		return Ret

class CameraTools:
	def get_active_camera():
		ActiveCam = getActiveCamera()
		if ActiveCam == None:
			# Cams = for C in Cameras where superclassof C == camera collect C
			Cams = [C for C in Cameras if C.type == 'CAMERA'] # collect cameras
			if Cams.count == 1:
				ActiveCam = Cams[1]
			elif Cams.count == 0:
				print("macros.run" + "Lights and Cameras" "StandardCamera_CreateFromView") #TODO
		return ActiveCam
	
	def CollectMoveFrames(Cam):
		def ComparParams(Cam, Time1, Time2):
			Ret = True
			fov1 = at time Time1 Cam.fov #TODO :O
			fov2 = at time Time2 Cam.fov
			if fov1 == fov2 then
				Ret = True
			else
				Ret = False
			return Ret

		OldCamTransfirm, Frames = None, []
		for T in(animationRange.start, animationRange.end):
			# at time T (
			NewCamTransfirm = at time T Cam.transform
			# bpy.data.scenes[0].frame_start = 2
			# bpy.data.scenes[0].frame_end = 251
			
			Tr = not Math.Compartransfor(OldCamTransfirm, NewCamTransfirm, 0.01)
			Pa = not ComparParams(Cam, (T - 1), T)
				
			if  Tr or Pa:
				f = int(T)
				if not f in Frames:
					Frames.append(f)
				
			OldCamTransfirm = NewCamTransfirm
		# LastFrame = animationRange.end
		LastFrame = bpy.data.scenes[0].frame_end
		if not LastFrame in Frames:
			Frames.append(LastFrame)
		return Frames
	
	def CatchCameraFrames():
		Cam = getActiveCamera() 
		if Cam != None:
			""" Collect and refine frames """
			Frames = CameraTools.CollectMoveFrames(Cam)
			Frames = Sequence.FillSequenceGaps(Frames, 5)
			Frames = Sequence.RemoveTinys(Frames, 5)
			Str = Sequence.FramesToString(Frames)
			""" Apply to render setting """
			# isopen = renderSceneDialog.isOpen()
			# renderSceneDialog.close()
			# rendTimeType  = 4
			rendPickupFrames = Str
			# if isopen:
			# 	renderSceneDialog.open()
			if len(Str) > 498:
				print("Frame list is to long prees Ok to copy in clipboard")
				# setclipboardText Str
		else:
			# rendTimeType  = 1
			pass
	
	def CameraClip(State):
		ActiveCam = getActiveCamera()
		if ActiveCam != None:
			try:
				ActiveCam.clipManually = State
			except:
				pass