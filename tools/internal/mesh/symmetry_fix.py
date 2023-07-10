# pX SymmetryFix
# Denys Almaral

# Tries to fix the simmetry of Editable Poly for vertices not catched by "Symmetry Tools" using conextions instead of position.
"""
 Algorithm to implement:
 
 # Find symmetrical pairs of vertices.
 # Consider x=0 vertices as paired.
 # go for every non-paired vertices and link
 # Store all edge conextions for each non-paired vertices.
 REPEAT PASSES
 # go for each non-paired Right-Side vertice
 # Check its edge conections.
 # Find a Left-Side vertice with same connections. 
 # FOUND IF: Exist only one wieh same connections.
 # Update connections.
 UNTIL CAN'T find more new pairs   
"""

# struct TVertInfo  
# ( 
# 	RightSide, 
# 	LinkedTo, 
# 	PairedWith, 
# 	vPos 
# 	#[ RightSide:boolean, LinkedTo, PairedWith, vertPos ]
# )

import bpy
from mathutils import Vector



class TVertInfo:
	def __init__(self, RightSide, LinkedTo, PairedWith, vPos):
		self.RightSide = RightSide
		self.LinkedTo = LinkedTo
		self.PairedWith = PairedWith
		self.vPos = vPos



class Bitarray:
	def __init__(self):
		self.ints = []
	def count(self, count):
		pass # fill self.ints
	def isEmpty(self):
		return True # bool



class Polyop:
	def getNumVerts(self, mesh):
		return 1 #integer
	
	def getVert(self, mesh, index):
		return Vector(0,0,0) #vector
	
	def getEdgesUsingVert(self, mesh, index):
		return [] #array of ??
	
	def setVert(self, mesh, index, pos):
		pass

polyop = Polyop()



def distance(v1, v2):
	return v1 #
	
# Tolerance = 0.005
# MySelection = #{}
# MirrorRightToLeft  = true

Tolerance = 0.005
MySelection = []
MirrorRightToLeft = True



# function FindPairs EPolyObj  = 
def FindPairs (EPolyObj):
	N = polyop.getNumVerts(EPolyObj)
	Result = [] #Bitarray
	Result.count = N	
	Result = -Result
	
	UnPairedTag = N + 99
	
	VertsInfo = [] #() --array of TVertInfo
	VertsInfo.count = N
	
	# --initializing vertInfo
	# progressStart "Analyzing..."
	# for i=1 to N do in coordsys local (
	for i in range(1,N):
		v1 = polyop.getVert(EPolyObj, i)
		VertsInfo[i] = TVertInfo(None, None, None, v1)
		VertsInfo[i].RightSide = ( v1.x >= 0 )
		
		# --Vertices on the Symmetry AXE paired with themselves. 
		if 	abs(v1.x) <= Tolerance:
			VertsInfo[i].PairedWith = i	
			Result[i] = False
		
		# --Links
		# --FindingEdge connections with other vertices
		MyEdges = polyop.getEdgesUsingVert(EPolyObj, i)
		VertsInfo[i].Linkedto = [] #{}	Bitarray
		for k in MyEdges:
			VertsInfo[i].Linkedto  = VertsInfo[i].Linkedto  + (polyop.getVertsUsingEdge(EPolyObj, k))			

		# VertsInfo[i].Linkedto =  VertsInfo[i].Linkedto - #{i}
		VertsInfo[i].Linkedto =  VertsInfo[i].Linkedto - [i] # append to array
	
	# for i=1 to N-1 do in coordsys local (
	for i in range(1,N-1):
		v1 = polyop.getVert(EPolyObj, i)
		
		# progressUpdate (i*90/N)
		# --Finding first pairs by position	
		# for j=(i+1) to N do (
		for j in range((i+1),N):
			v2 = polyop.getVert(EPolyObj, j)
			v2.x = -v2.x
			d = distance(v1, v2)
			
			if d <= Tolerance:
				VertsInfo[i].PairedWith = j
				VertsInfo[j].PairedWith = i	
				Result[i] = False
				Result[j] = False
	
	# -- Find pairs by links -------------------------- the cool start here --------------
		
	FoundNewPairs = 0
	while FoundNewPairs != 0:
		FoundNewPairs = 0
		# for i=1 to N do in coordsys local (		
		for i in range(1,N):

			if VertsInfo[i].RightSide:
				if VertsInfo[i].PairedWith == None:
					Result[i] = True
					MyCandidate = 0
					MyCandidateNum = 0
					
					# for j=1 to N-1 do (
					for j in range(1,N-1):
						if i != j:						
							RSymLinks = [] #{} Bitarray
							RUnpairedLinks = 0
							LSymLinks = [] #{}Bitarray
							LUnpairedLinks = 0
							# --Remap the links using paired Vertice Numbers. 
							# --Right
							for k in VertsInfo[i].LinkedTo:
								if VertsInfo[k].PairedWith == None:
									RUnpairedLinks +=  1
								else:
									if VertsInfo[k].RightSide:
										RSymLinks = RSymLinks + [k] #{ k }
									else:
										# RSymLinks = RSymLinks + #{ VertsInfo[k].PairedWith }
										RSymLinks = RSymLinks + [VertsInfo[k].PairedWith] #{ VertsInfo[k].PairedWith }
							# --left
							for k in VertsInfo[j].LinkedTo:
								if VertsInfo[k].PairedWith == None:
									LUnpairedLinks += 1
								else:
									if VertsInfo[k].RightSide:
										LSymLinks = LSymLinks + [k] #{ k }
									else:
										LSymLinks = LSymLinks + [VertsInfo[k].PairedWith] #{ VertsInfo[k].PairedWith } 
							
							# -- And now the moment of "almost" truth!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
							# -- The left vert qualify for pairing???
							
							# --Empty links sets, cant prove nothing 
							if (not RSymLinks.isEmpty()):
								# -- Testing if two SETS are EQUAL:
								if (RSymLinks-LSymLinks).isEmpty and (LSymLinks-RSymLinks).IsEmpty:
									# --but wat about the Unpaired links?
									if RUnpairedLinks == LUnpairedLinks:
										# --this is a good candidate!
										# --lets see if  there not already one before...
										if MyCandidate==0:
											# --Nice this is the first (hope only)
											MyCandidate=j 
											MyCandidateNum+= 1
											print ("Candidate! " + str(MyCandidate))
										else:
											# --no need for more searching there are duplicated "ideal" conditions
											# --but instead of exiting the loops, lets just count the candidates
											MyCandidateNum += 1
					
					# --if One and only One then yeah
					if MyCandidateNum == 1:
						# --We can pair vert I with vert MyCandidate
						VertsInfo[i].PairedWith = MyCandidate
						VertsInfo[MyCandidate].PairedWith = i
						FoundNewPairs += 1 
						Result[i] = False
						Result[MyCandidate] = False
						# --Mirroring vertice
						if MirrorRightToLeft:
							newPos = VertsInfo[i].vPos 
							newPos.x = -newPos.x
							polyop.setVert(EPolyObj, [MyCandidate], newPos)
						else:
							newPos = VertsInfo[MyCandidate].vPos 
							newPos.x = -newPos.x
							polyop.setVert(EPolyObj, [i], newPos)
						print ("Pair:" + str(i) + "-" + str(MyCandidate) ) 
			
		print ("Found New Pairs: " + str(FoundNewPairs))
		
		
	# progressEnd()
	Result

obj = None



if obj.type == 'MESH':
	obj.selectedVerts = FindPairs(obj)
else:
	print("Select an Editable Poly")
