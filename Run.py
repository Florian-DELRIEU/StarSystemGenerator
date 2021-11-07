from Class.System import *
from Class.Planet import *
from Functions.Functions import *
import numpy as np

"""
Fonctions utilisant :SystemGen: pour la génération de systemes
"""
#from Class import System,Planet
#from Functions.Functions import *
#import numpy as np

def SpeedTest():
	import time as t
	n = 0
	Number_loop = 100
	begin = t.time()
	print("Generating... ")
	while n <= Number_loop - 1:
		n += 1
		Planet
	duration = t.time() - begin
	print(duration)
	speed = Number_loop/duration
	print("Le programme génère ", speed, " planètes/secondes")


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
		for starindic in S.Star_list:
			curstar = getattr(S,starindic)
			if len(curstar.OrbitList) is not curstar.NbOrbit:
				print("Error")
				break
	n += 1

def TestDetermineDistance(howmany=10):
	error = 0
	for _ in np.arange(howmany):
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
	S = System()
	S.createPlanet()
	S.createSatellites()
	S.Show()

def BasicGeneration():
	S = System()
	S.createPlanet()
	S.createSatellites()
	S.Show(3)

def CreateSpecialPlanet(PlaneteType,PlaneteZone):
	P = Planet()
	while P.Type != PlaneteType or P.Zone != PlaneteZone:
		P = Planet()
	P.Show()
	return P

def CreateSpecialSystem(NbOrbit):
	S = System()
	while S.nbOrbit != NbOrbit:
		S = System()
	S.Show()
	return S


########################################################################################################

#P = CreateSpecialPlanet("Small Terrestrial","Inner")
S = System()
S1 = S.__copy__()
#S.Show()
#S.OrderingPlanets()
#S.Show()