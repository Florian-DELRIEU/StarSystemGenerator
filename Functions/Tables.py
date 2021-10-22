"""
Regroupement de pondération pour le choix des attributs
Attribut[Valeur] = Poids
"""

# SPECTRAL
Class = dict()
Class["W"] = 0
Class["O"] = 0
Class["B"] = 0
Class["A"] = 2
Class["F"] = 4
Class["G"] = 4
Class["K"] = 5
Class["M"] = 2
DwarfClass = dict()
DwarfClass["dA"] = 0.2
DwarfClass["dF"] = 0.4
DwarfClass["dG"] = 0.4
DwarfClass["dM"] = 0.5
DwarfClass["dK"] = 0.2

StarType = dict()  # Etoile normale ou naine
StarType["Star"] = 1
StarType["Dwarf"] = 0

StarSize = dict()
StarSize["II"] = 1
StarSize["III"] = 2
StarSize["IV"] = 4
StarSize["V"] = 10
StarSize["VI"] = 2

StarDistance = dict()
StarDistance["Close"] = 2
StarDistance["Medium"] = 8
StarDistance["Far"] = 1

SystemType = dict()
SystemType["Solitary"] = 0.9
SystemType["Binary"] = 0.05
SystemType["Ternary"] = 0

InnerZone = dict()
InnerZone["Empty"] = 10
InnerZone["Asteroid Belt"] = 10
InnerZone["Mesoplanet"] = 20
InnerZone["Small Terrestrial"] = 20
InnerZone["Terrestrial"] = 20
InnerZone["Geoactive"] = 5
InnerZone["Super Terrestrial"] = 5
InnerZone["Small Gas Giant"] = 1
InnerZone["Gas Giant"] = 1
InnerZone["Reducing"] = 15
InnerZone["Gas SuperGiant"] = 1
InnerZone["Gas UltraGiant"] = 1
InnerZone["Ultra Hostile"] = 10
InnerZone["Chthonian"] = 5

HabitableZone = dict()
HabitableZone["Empty"] = 10
HabitableZone["Asteroid Belt"] = 10
HabitableZone["Mesoplanet"] = 9
HabitableZone["Small Terrestrial"] = 10
HabitableZone["Geoactive"] = 5
HabitableZone["Super Terrestrial"] = 3
HabitableZone["Desert"] = 7
HabitableZone["Gas SuperGiant"] = 1
HabitableZone["Gas Giant"] = 1
HabitableZone["Marginal"] = 5
HabitableZone["Terrestrial"] = 10
HabitableZone["Reducing"] = 5
HabitableZone["Oceanic"] = 5
HabitableZone["Glaciated"] = 5
HabitableZone["Gas UltraGiant"] = 2
HabitableZone["Ultra Hostile"] = 10

# Liste des planetes de type Habitable
HabitableList = ["Small Terrestrial", "Terrestrial", "Super Terrestrial", "Desert", "Oceanic", "Glaciated"]

OuterZone = dict()
OuterZone["Empty"] = 10
OuterZone["Asteroid Belt"] = 10
OuterZone["Mesoplanet"] = 1
OuterZone["Small Terrestrial"] = 1
OuterZone["Geo Active"] = 1
OuterZone["Super Terrestrial"] = 5
OuterZone["Gas SuperGiant"] = 10
OuterZone["Gas Giant"] = 10
OuterZone["Gas UltraGiant"] = 15
OuterZone["Ice World"] = 5
OuterZone["Dirty SnowBall"] = 5

InnerAsteroidBelt = dict()
InnerAsteroidBelt["aM"] = 3
InnerAsteroidBelt["aS"] = 3
InnerAsteroidBelt["aC"] = 1

HabitableAsteroidBelt = dict()
HabitableAsteroidBelt["aM"] = 3
HabitableAsteroidBelt["aS"] = 3
HabitableAsteroidBelt["aC"] = 1

OuterAsteroidBelt = dict()
OuterAsteroidBelt["aM"] = 1
OuterAsteroidBelt["aS"] = 3
OuterAsteroidBelt["aC"] = 2
OuterAsteroidBelt["aI"] = 4

RoguePlanet = dict()
RoguePlanet[0] = 10
RoguePlanet[1] = 2
RoguePlanet[2] = 1
RoguePlanet[3] = 0.5
RoguePlanet[4] = 0.1

ImperialClass = dict()
ImperialClass["Agri-"] = 20
ImperialClass["Civilized "] = 20
ImperialClass["Developing "] = 5
ImperialClass["Dead "] = 5
ImperialClass["Death "] = 5
ImperialClass["Feral "] = 5
ImperialClass["Feudal "] = 5
ImperialClass["Forge "] = 3
ImperialClass["Hive "] = 10
ImperialClass["Quarantined "] = 1
ImperialClass["Shrine "] = 2

"""
Les clés dictionnaires ci dessous regroupe les types de satéllites de chaque orbites et contiennent les tuples qui
définissent les nombre min et max de chaque satellites de manière aléatoire
DicoExemple["Lune"] = (valeurmin,valeurmax)

Utilisé par la fonction :rolldico:
"""
SmallPlanetSat = dict()
SmallPlanetSat["MinorRing"] = (0,0)
SmallPlanetSat["MajorRing"] = (0,0)
SmallPlanetSat["Moonlets"] = (-7,3)
SmallPlanetSat["SmallMoon"] = (-9,1)
SmallPlanetSat["MediumMoon"] = (0,0)
SmallPlanetSat["LargeMoon"] = (0,0)
SmallPlanetSat["HugeMoon"] = (0,0)

TerrestrialPlanetSat = dict()
TerrestrialPlanetSat["MinorRing"] = (-9,1)
TerrestrialPlanetSat["MajorRing"] = (0,0)
TerrestrialPlanetSat["Moonlets"] = (-6,4)
TerrestrialPlanetSat["SmallMoon"] = (-7,3)
TerrestrialPlanetSat["MediumMoon"] = (-9,1)
TerrestrialPlanetSat["LargeMoon"] = (0,0)
TerrestrialPlanetSat["HugeMoon"] = (0,0)

SmallGiantSat = dict()
SmallGiantSat["MinorRing"] = (-5,5)
SmallGiantSat["MajorRing"] = (-8,2)
SmallGiantSat["Moonlets"] = (0,10)
SmallGiantSat["SmallMoon"] = (-1,9)
SmallGiantSat["MediumMoon"] = (-7,3)
SmallGiantSat["LargeMoon"] = (-6,4)
SmallGiantSat["HugeMoon"] = (-8,2)

BigGiantSat = dict()
BigGiantSat["MinorRing"] = (-2,8)
BigGiantSat["MajorRing"] = (-5,5)
BigGiantSat["Moonlets"] = (0,13)
BigGiantSat["SmallMoon"] = (0,11)
BigGiantSat["MediumMoon"] = (0,10)
BigGiantSat["LargeMoon"] = (-4,6)
BigGiantSat["HugeMoon"] = (-6,4)

########################################################################################################################
########################################################################################################################
"""
Les cles de ces dictionnaires sont les valeurs à recuperer en sortie et les leurs entrée sont des tuples qui définissent
quels sont les scores a atteindre (aléatoirement) pour que cette clès soit choisis
ex: Dictionnaire[:Valeur:] = (:Min:, :Max:)
Si le jet est entre :Min: et :Max: alors on recupere :Valeur:
Voir la fonction :rollchoicedico:
"""

ProtoPlanetAtm = dict()
ProtoPlanetAtm["None"] = (1,2)
ProtoPlanetAtm["Hydrogen"] = (3,4)
ProtoPlanetAtm["Hydrogen Sulfide"] = (5,5)
ProtoPlanetAtm["Carbon Dioxide"] = (6,6)
ProtoPlanetAtm["Methane"] = (7,10)

GeoActiveAtm = dict()
GeoActiveAtm["None"] = (1,1)
GeoActiveAtm["Hydrogen"] = (2,2)
GeoActiveAtm["Hydrogen Fluoride"] = (3,3)
GeoActiveAtm["Hydrogen Sulfide"] = (4,7)
GeoActiveAtm["Methane"] = (8,10)

MesoplanetAtm = dict()
MesoplanetAtm["None"] = (1,3)
MesoplanetAtm["Hydrogen"] = (4,5)
MesoplanetAtm["Helium"] = (6,8)
MesoplanetAtm["Methane"] = (9,10)

ReducingAtm = dict()
ReducingAtm["Hydrogen"] = (1,1)
ReducingAtm["Bromine"] = (2,2)
ReducingAtm["Hydrochloric Acid"] = (3,4)
ReducingAtm["Sulfuric Acid"] = (5,6)
ReducingAtm["Oxygen"] = (7,7)
ReducingAtm["Fluorine"] = (8,8)
ReducingAtm["Chlorine"] = (9,10)

MarginalAtm = dict()
MarginalAtm["Carbon Dioxyde"] = (1,5)
MarginalAtm["Methane"] = (6,10)

ChthonianAtm = dict()
ChthonianAtm["None"] = (1,5)
ChthonianAtm["Hydrogen"] = (6,7)
ChthonianAtm["Hydrochloric Acid"] = (8,10)

IceWorldAtm = dict()
IceWorldAtm["None"] = (1,1)
IceWorldAtm["Hydrogen"] = (2,2)
IceWorldAtm["Hydrochloric Acid"] = (3,10)

SuperTerrestrialAtm = dict()
SuperTerrestrialAtm["Carbon Dioxide"] = (1,5)
SuperTerrestrialAtm["Hydrogen Sulfide"] = (6,6)
SuperTerrestrialAtm["Methane"] = (7,9)
SuperTerrestrialAtm["Chlorine"] = (10,10)

SmallTerrestrialAtm = dict()
SmallTerrestrialAtm["None"] = (1,5)
SmallTerrestrialAtm["Hydrogen"] = (6,7)
SmallTerrestrialAtm["Helium"] = (8,10)

TerrestrialAtm = dict()  # Personnal addon
TerrestrialAtm["Carbon Dioxyde"] = (1,1)
TerrestrialAtm["Nitrogen"] = (2,7)
TerrestrialAtm["Oxygen"] = (8,10)

HabitableDensity = dict()
HabitableDensity["Thin"] = (1,2)
HabitableDensity["Standart"] = (3,8)
HabitableDensity["Thick"] = (9,10)

UnhabitableDensity = dict()
UnhabitableDensity["Very Tenuous"] = (1,1)
UnhabitableDensity["Tenuous"] = (2,2)
UnhabitableDensity["Very Thin"] = (3,3)
UnhabitableDensity["Thin"] = (4,5)
UnhabitableDensity["Medium"] = (6,7)
UnhabitableDensity["Thick"] = (8,8)
UnhabitableDensity["Dense"] = (9,10)
UnhabitableDensity["Very Dense"] = (10,10)
