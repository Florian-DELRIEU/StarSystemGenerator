from Class.Satellite import *
from Class.Planet import *
from Functions.Tables import *
from Functions.Functions import *
import random as rd
import numpy as np
from MyPack.Utilities import truncSignificatif

class Orbit:
    """
    Objet de Type Orbite
    -   self.Parent: Nom de l'étoile parente
    -   self.IsRogue: l'orbite est Rogue si :True:
    -   self.OrbitDistance: Rayon de l'orbite
    -   self.Zone: Zone habitable ou non selon le rayon et la catégorie de l'étoile
    -   self.Contain: Type de planète que doit contient l'orbite utilisé par l'objet :Planet:
    -   self.AsteroidBeltType: si pas :None: alors determine le type de la ceinture d'astéroide
    -   self.AsteroidComposition: Composition de la ceinture
    -   self.nbSatellites: Nombre de satellites
    -   self.dicoSatellites: Regroupe le nombre de satellites par type
    -   self.Satellites: Listes de satellites issue de :self.dicoSatellites:
    """
    def __init__(self,Auto=True,itsStar=None,IsRogue=False):
        """
        :param itsStar: Objet :Star: parente
        :param IsRogue: si :True: creer une orbite rogue
        :param Auto: si generation auto ou non
        """
        if itsStar is not None:
            self.MaxRange = itsStar.MaxRange
            self.Parent = itsStar.FullClassName
        else:
            self.MaxRange = 13
            self.Parent = "G3V"  # Valeur par défaut (a modifier)
        self.IsRogue = IsRogue
        self.OrbitDistance = float()
        self.Zone = str()
        self.Contain = str()
        self.nbSatellites = 0
        self.Satellites_list = list()
        self.AsteroidBeltType = None
        self.AsteroidComposition = None
        self.dicoSatellites = dict()
        if Auto: self.Autogen()

    def __repr__(self):
        txt = "{} ({} orbit) at {} Orbit-Distance".format(self.Contain, self.Zone, self.OrbitDistance)
        if self.IsRogue: txt = "Rogue " + txt
        return txt

    def __del__(self):
        print("{} deleted".format(self))

    def Autogen(self):
        self.OrbitDistance = truncSignificatif(rd.uniform(0,self.MaxRange),2)  # Distance de l'orbite
        self.Zone = DetermineZone(self.Parent,self.OrbitDistance)  # Determine la zone où se situe l'orbite
        if   self.Zone == "Inner":      self.Contain = choice(InnerZone)
        elif self.Zone == "Habitable":  self.Contain = choice(HabitableZone)
        elif self.Zone == "Outer":      self.Contain = choice(OuterZone)
        else:                           self.Contain = None
        self.rollSatellites()

    def GenerateAsteroidBeltType(self):
        """
        Genere la composition de la ceinture d'asteroid si elle existe
        :return:
        """
        if self.Contain == "Asteroid Belt":  # Verifie si c'est une ceinture d'asteroid
        # Choisis le type en fonction de sa zone
            if   self.Zone == "Inner":      self.AsteroidBeltType = choice(dico=InnerAsteroidBelt)
            elif self.Zone == "Habitable":  self.AsteroidBeltType = choice(dico=HabitableAsteroidBelt)
            elif self.Zone == "Outer":      self.AsteroidBeltType = choice(dico=OuterAsteroidBelt)
        # Ajoute les détails de sa composition en fonction de son type
            if   self.AsteroidBeltType == "aM": self.AsteroidComposition = ["Nickel","Iron"," Others Heavy Metals"]
            elif self.AsteroidBeltType == "aS": self.AsteroidComposition = ["Stone and Rock"]
            elif self.AsteroidBeltType == "aC": self.AsteroidComposition = ["Carbon","Hydrated Materials","Hydrocarbons"]
            elif self.AsteroidBeltType == "aI": self.AsteroidComposition = ["Ice","Frozen Methane",
                                                                        "Frozen gases and liquid","(Comets Nursery)"]
            self.AsteroidBeltType += " Asteroid Belt"  # Juste pour renommage
        else:
            print("This is not Asteroid Belt !")

    def rollSatellites(self):
        """
        Genere le nombre de chaque types de satéllites voir :SystemRepository:
        :return: Dictionnaire contenant le nombre de chaque Type de satellites
        """
        if self.Contain in ["Small Terrestrial","Reducing","Mesoplanet"]:
            self.dicoSatellites = rolldico(SmallPlanetSat)
        elif self.Contain in ["Small Gas Giant","Gas Giant"]:
            self.dicoSatellites = rolldico(SmallGiantSat)
        elif self.Contain in ["Gas SuperGiant","Gas UltraGiant"]:
            self.dicoSatellites = rolldico(BigGiantSat)
        elif self.Contain not in ["Asteroid Belt","Empty","None"] :  # Tout le reste sauf asteroid belt
            self.dicoSatellites = rolldico(TerrestrialPlanetSat)
    #  Compte le nombre total de satellites
        for k in self.dicoSatellites.keys(): self.nbSatellites += self.dicoSatellites[k]

    def createPlanet(self):
        setattr(self,"Planet", Planet(itsOrbit=self))

    def createSatellites(self):
        """
        Cree les objets satellites dans l'attribut self.Satellites en fonction de :dicoSatellite:
        """
        cacheContain = self.Contain  # stocke :self.Contain: avant modification
        for currentSatellitesType in self.dicoSatellites.keys():  # Chaque Type de satellites
            for _ in np.arange(self.dicoSatellites[currentSatellitesType]):  # autant de fois qu'il y en a
                if currentSatellitesType in ["HugeMoon","LargeMoon","MediumMoon"]:  # selon la taille
                    PlanetMoonType = MoonAsPlanet(currentSatellitesType,self.Zone)    # Creation en tant que :Planet:
                    self.Contain = PlanetMoonType  # Pour utiliser la meme methode de creation que les planete
                    self.Satellites_list.append(Planet(itsOrbit=self, MoonType=currentSatellitesType))
                else:
                    self.Satellites_list.append(Satellite(currentSatellitesType))  # Creer l'objet :satellite: de Type :k:
        self.Contain = cacheContain  # recupere la veritable valeur