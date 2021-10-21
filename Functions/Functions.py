import random as rd
import numpy as np
from MyPack.Convert import Csv2Dict
from MyPack.Utilities import getFromDict
CSV_path = "CSV/"
Function_path = "Functions/"
"""
Regroupement de fonction essentielles pour le fonctionnement de :SystemGen:
"""
#import random as rd
#from MyPack.Convert import *
#import MyPack.Utilities as utils


def choice(dico):  # Fonction pour faire un choix l'objet dico
    """
    :param dico: Dictionnaire dont les cles sont les valeurs des parametres, et les entrees sont les poids
    dico["valeur"] = poids
    :return: une valeur parmis dico.keys() pondere
    """
    KeyList = list(dico.keys())
    WeightList = list()
    for k in KeyList:
        WeightList.append(dico[k])
    output = rd.choices(KeyList,WeightList)
    return output[0]


def rolldico(dico):
    output = dict()
    for k in dico.keys():
        output[k] = roll(dico[k][0],dico[k][1])
    return output


def StarIs(Category=str()):
    """
    Recupere les infos dans le type de l'etoile
    :param Category:  Categorie de l'etoile (ex: "G3V")
    :return:  (exemple :Class:="G", :Decimal:=3, :Size:="V")
    """
    Decimal = int()
    for l in Category:
        if l.isnumeric(): Decimal = int(l)
    s = Category.split(str(Decimal))
    Class = s[0]
    Size = s[1]
    return Class, Decimal, Size


def DetermineZone(StarType, OrbitDistance):
    """
    Determine la zone dans laquelle se situe la planete
    :param StarType: Type de l'étoile parente (ex: "G2V")
    :param OrbitDistance:  Distance de l'orbite par rapport à l'étoile
    :return:
    """
    Class, Decimal, Size = StarIs(StarType)
# Dans le fichier .csv :Decimal: = 0ou5 uniquement
    if Decimal in [5,6,7,8,9]: Decimal = 5
    else: Decimal = 0
    cur = Csv2Dict(CSV_path+"ZoneStarSize"+Size+".csv")  # Recupere le bon fichier .csv
    cur = cur[Class+str(Decimal)]  # Recupere la zone en fonction de la position
    curindic = int(np.floor(OrbitDistance))  # Indice dans le .csv = distance
    if curindic >= len(cur):  # Si trop eloigné
        output = "OutofRange"
    else:
        output = cur[curindic]
    return output


def DetermineDistance(Type):
    CsvFile = Csv2Dict(CSV_path+"MoonDistance.csv")
    cur = roll(1,10)
    if Type == "Small Gas Giant":
        if cur <= 7: output =                           CsvFile["Close Orbit"][roll(0,18)]
        else: output =                                  CsvFile["Medium Orbit"][roll(0,19)]
    elif Type == "Gas Giant":
        if cur <= 6: output =                           CsvFile["Close Orbit"][roll(0,18)]
        elif cur in [7,8,9]: output =                   CsvFile["Medium Orbit"][roll(0,18)]
        else: output =                                  CsvFile["Far Orbit"][roll(0,18)]
    elif Type in ["Gas SuperGiant","Gas UltraGiant"]:
        if cur <= 4: output =                           CsvFile["Close Orbit"][roll(0,18)]
        elif cur in [5,6,7,8]:output=                   CsvFile["Medium Orbit"][roll(0,18)]
        else: output =                                  CsvFile["Far Orbit"][roll(0,18)]
    elif Type in ["MinorRing","MajorRing"]:
        output =                                        CsvFile["Ring System"][roll(0,18)]
    else: output =                                      CsvFile["Close Orbit"][roll(0,18)]
    return output


def roll(RangeDown,RangeUp):
    """
    Choisis un nombre au hasard entre :RangeDown: et :RangeUp:
    :param RangeDown: :int: (peut etre négatif)
    :param RangeUp: :int:
    :return: 0 si result est inferieur a 0
    """
    result = rd.randint(RangeDown, RangeUp)
    if result <= 0: result = 0
    return result


def rollchoicedico(dico,rolltuple=tuple(),modifiers=int()):
    output = str()
    cur = roll(rolltuple[0],rolltuple[1]) + modifiers
    if cur < rolltuple[0]: cur = rolltuple[0]
    if cur > rolltuple[1]: cur = rolltuple[1]
    for k in dico.keys():
        Rangedown = dico[k][0]
        Rangeup = dico[k][1]
        if Rangedown <= cur <= Rangeup:
            output = k
    return output


def rollSize(PlanetType):
    if   PlanetType in ["Mesoplanet"]:           Size = roll(1,5)
    elif PlanetType in ["ProtoPlanet"]:          Size = roll(6,15)
    elif PlanetType in ["Small Terrestrial"]:    Size = roll(3,9)
    elif PlanetType in ["Super Terrestrial"]:    Size = roll(16,30)
    elif PlanetType in ["Chthonian"]:            Size = roll(5,40)
    elif PlanetType in ["Ice World"]:            Size = roll(4,10)
    elif PlanetType in ["Dirty SnowBall"]:       Size = roll(4,10)
    elif PlanetType in ["Ultra Hostile"]:        Size = roll(5,15)
    # Gas Giant
    elif PlanetType in ["Small Gas Giant"]:      Size = roll(5,10) * 10
    elif PlanetType in ["Gas Giant"]:            Size = roll(11,20) * 10
    elif PlanetType in ["Gas SuperGiant"]:       Size = roll(21,30) * 10
    elif PlanetType in ["Gas UltraGiant"]:       Size = roll(31,40) * 10

    elif PlanetType in ["MediumMoon"]:            Size = rd.choice(np.arange(2.2, 2.7, .1))
    elif PlanetType in ["LargeMoon"]:             Size = rd.choice(np.arange(2.7, 4.5, .1))
    elif PlanetType in ["HugeMoon"]:              Size = rd.choice(np.arange(4.5, 7.0, .1))
    # others
    else:                                           Size = roll(10,15)  # Autres terrestres
    return Size*1000  # en km


def determineClimate(Cryosphere,Hydrosphere,Humidity):
    Climate = dict()
    if   Cryosphere <= 30:  Cryosphere = "Low"
    elif Cryosphere >= 70:  Cryosphere = "High"
    else:                   Cryosphere = "Medium"
    if   Hydrosphere <= 30: Hydrosphere = "Low"
    elif Hydrosphere >= 70: Hydrosphere = "High"
    else:                   Hydrosphere = "Medium"
    if   Humidity <= 30:    Humidity = "Low"
    elif Humidity >= 70:    Humidity = "High"
    else:                   Humidity = "Medium"

    Climate["Hot Desertic"] =       ("Low","Low","Low")
    Climate["Savannah"] =           ("Low","Medium","Medium")
    Climate["Jungle"] =             ("Low","High","High")
    Climate["Tropical"] =           ("Medium","Medium","Medium")
    Climate["Cool RainForest"] =    ("Medium","High","High")
    Climate["Cold Desertic"] =      ("High","Low","Low")
    Climate["Artic"] =              ("High","Medium","Medium")

    output = "Undetermined Climate"  # Climat par defaut
    for currentClimate in Climate.keys():
        # Recupere un nouveau climat si le tuple correspond
        if (Cryosphere,Hydrosphere,Humidity) == Climate[currentClimate]:
            output = currentClimate

    return output


def determineMineralSurvey(PlanetaryType):
    Mineral = dict()
    for currentMineral in ["Minerals","Common Metals","Rare Metals","Industrial Crystals",
                     "Gemstones","Radioactives"]:
        Amount = roll(1,10)
        if currentMineral == "Minerals":
            Amount += 3
            if PlanetaryType == "Ice World": Amount -= 4
        if currentMineral == "Common Metals":
            Amount += 1
            if PlanetaryType == "Ice World": Amount -= 6
            if PlanetaryType == "Dirty SnowBall": Amount -= 4
        if currentMineral == "Rare Metals":
            Amount += -2
            if PlanetaryType == "Ice World": Amount -= 8
            if PlanetaryType == "Dirty SnowBall": Amount -= 6
        if currentMineral == "Industrial Crystals":
            Amount += 0
            if PlanetaryType == "Ice World": Amount -= 5
            if PlanetaryType == "Dirty SnowBall": Amount -= 3
        if currentMineral == "Gemstones":
            Amount += -4
            if PlanetaryType == "Ice World": Amount -= 4
            if PlanetaryType == "Dirty Snowball": Amount -= 2
        if currentMineral == "Radioactive":
            Amount += -4
            if PlanetaryType == "Ice World": Amount -= 3

        if Amount <= 0:  Amount = 0
        if Amount >= 10: Amount = 10
        Mineral[currentMineral] = Amount
    return Mineral


def MoonAsPlanet(MoonType,Zone):
    from Tables import InnerZone,HabitableZone,OuterZone
    Type = str()
    if MoonType in ["HugeMoon"]:
        # Liste des type de planete que peut devenir la lune
        AvailableList = ["Terrestrial", "Geoactive", "Ultra Hostile", "Desert", "Oceanic", "Glaciated", "Exotic",
                         "Protoplanet","Ice World"]
        # Choix prédéfinie
        if Zone in ["Inner"]:      Type = choice(getFromDict(Function_path+InnerZone, AvailableList))
        if Zone in ["Habitable"]:  Type = choice(getFromDict(Function_path+HabitableZone, AvailableList))
        if Zone in ["Outer"]:      Type = choice(getFromDict(Function_path+OuterZone, AvailableList))
    if MoonType in ["LargeMoon"]:
        AvailableList = ["Small Terrestrial", "Geoactive", "Ultra Hostile", "Dirty SnowBall", "Ice World"
            , "Exotic", "Protoplanet"]
        if Zone in ["Inner"]:      Type = choice(getFromDict(Function_path+InnerZone, AvailableList))
        if Zone in ["Habitable"]:  Type = choice(getFromDict(Function_path+HabitableZone, AvailableList))
        if Zone in ["Outer"]:      Type = choice(getFromDict(Function_path+OuterZone, AvailableList))
    if MoonType in ["MediumMoon"]:
        AvailableList = ["Mesoplanet", "Protoplanet"]
        if Zone in ["Inner"]:      Type = choice(getFromDict(Function_path+InnerZone, AvailableList))
        if Zone in ["Habitable"]:  Type = choice(getFromDict(Function_path+HabitableZone, AvailableList))
        if Zone in ["Outer"]:      Type = choice(getFromDict(Function_path+OuterZone, AvailableList))

    return Type
