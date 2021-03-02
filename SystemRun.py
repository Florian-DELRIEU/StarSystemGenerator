from SystemGen import *
import numpy as np

def Test1(howmany=10):
	"""
	Test si les orbites sont consistantes
	:return:
	"""
	n = 0
	while n <= howmany:
		S = System()
		print(S)
		S.clearorbit()
		for starindic in S.Star:
			curstar = getattr(S,starindic)
			if len(curstar.OrbitList) is not curstar.NbOrbit:
				print("Error")
				break
	n += 1

def TestDetermineDistance(howmany=10):
	error = 0
	for i in np.arange(howmany):
		try:
			DetermineDistance("Terrestrial")
		except:
			error += 1
	print(str(error) + " errors")

def UserSystem():
	S = System(auto=False)
	S.addAllStar()
	S.clearorbit()
	S.Show()
	return S

def TestSatellites():
	S.createPlanet()
	S.createSatellites()
	S.Show()

def MakePlanet(PlaneteType):
	P = Planet()
	while P.Type is not PlaneteType:
		P.Autogen()
	P.Show(3)