"""
Regroupe toutes les classes d'objets et les fonctions pour le fonctionnement de :System.py:
"""
from SystemRepository import *
from SystemFunc import *
import random as rd
import MyPack.Utilities as utils
from MyPack.Convert import *

########################################################################################################################
class System:
    """
    Objet Type: Systeme Solaire
        - Par défaut un systeme va se générer automatiquement de manière aléatoire
                + Les étoiles
                + Les orbites dans chaque étoiles (les type de planetes sont générer mais les objets ne sont pas crées)
        - :self.clearOrbit: Pour nettoyer les orbites qui ne sont pas censé exister
    """
    def __init__(self,auto=True):
    # Initialisation
        self.Star = []  # Liste regroupant les etoiles
        self.nbRogueOrbit = 0
        self._nbStar = 1
        self.nbStar = 1
        self.nbOrbit = 0
        self.Type = str()
    # Generation
        if auto: self.Autogen()  # Lance la creation auto si :auto:=vrai

    def __repr__(self):
        return "{} system with {} orbits".format(
            self.Type,self.nbOrbit
        )

    def Autogen(self):
        """
        Generation auto du systeme
        :return:
        """
    # self._NbStar - Nombre d'etoile
        self.Type = choice(SystemType)
        if      self.Type == "Solitary":    self._nbStar = 1
        elif    self.Type == "Binary":      self._nbStar = 2
        elif    self.Type == "Ternary":     self._nbStar = 3
    # self.Star
        self.addAllStar()
    # self.NbOrbit
        for curStar in self.Star:
            self.nbOrbit += curStar.nbOrbit
    # self.RogueOrbit
        self.nbRogueOrbit = choice(RoguePlanet)     # Combien de Rogue Planet ?
        self.nbOrbit += self.nbRogueOrbit           # Ajoute au nombre d'orbites
        self.createRogue(self.nbRogueOrbit)

    def createRogue(self,nbRogue):
        """
        Ajoute une planète "Rogue" a l'une des étoiles du système
        :param nbRogue: Nombre de planètes à ajouter
        """
        for _ in np.arange(nbRogue):  # _ remplace la variable muette
            thisStar = rd.choice(self.Star)  # Choisi parmis les etoiles du systeme
            thisStar.addOrbit(IsRogue=True)       # Ajoute l'orbit Rogue a l'etoile choisis

    def determineType(self):
        """
        Fonction permettant de définir le type de systeme en fonction de :_nbOrbit:
        """
        if   self._nbStar == 1: self.Type = "Solitary"
        elif self._nbStar == 2: self.Type = "Binary"
        elif self._nbStar == 3: self.Type = "Ternary"
        return self.Type

    def addAllStar(self):
        """
        Ajoute toutes les :self._nbStar: étoiles dans le system
        """
        for i in np.arange(self._nbStar):
            if i==0:    IsPrimary = True  # La premiere étoiles est l'étoile principale
            else:       IsPrimary = False
            self.addStar(IsPrimary=IsPrimary)

    def addStar(self,Auto=True,IsPrimary=False):
        """
        Ajoute une étoile
        :param Auto: Definie si la génération auto est activé lors de la creation de l'étoile
        :param IsPrimary: Si :True:, l'étoile est primaire
        """
        self.Star.append(Star(Auto=Auto,IsPrimary=IsPrimary))
        self.nbStar = len(self.Star)  # Mets a jour le param :nbStar:

    def delStar(self,star):
        """
        Supprime l'étoile
        :param star: Objet étoile a supprimer. Si :Star:=int() supprime l'étoile qui a cet indice
        :return:
        """
        if type(star) == int():
            self.Star.remove(self.Star[star])
        else:
            self.Star.remove(star)
            self.nbStar = len(self.Star)

    def refresh_nbOrbit(self):
        """
        Raffraichi le nombre d'orbite dans le système
        """
        self.nbOrbit = 0
        for thisStar in self.Star:
            self.nbOrbit += thisStar.nbOrbit

    def clearorbit(self):
        """
        Supprime les orbites vides ou mal places dans tout le systeme
        """
        for curStar in self.Star:
            for curOrbit in curStar.Orbit:
                if curOrbit.Zone in ["Star","TooHot","OutofRange"] or curOrbit.Contain == "Empty":
                    curStar.delOrbit(curOrbit)
        self.refresh_nbOrbit()

    def createSatellites(self):
        """
        Creer les objets satellites dans toutes les orbites du systeme
        """
        for thisStar in self.Star:
            for thisOrbit in thisStar.Orbit:
                thisOrbit.createSatellites()

    def createPlanet(self):
        """Creer les objets planetes dans toutes les orbites du systeme"""
        for thisStar in self.Star:
            for thisOrbit in thisStar.Orbit:
                thisOrbit.createPlanet()

    def getPlanet(self,StarIndice,OrbitIndice):
        """
        Recupere l'objet planete dans le systeme si il existe
        :param StarIndice: Indice de l'étoile où se situe la planète
        :param OrbitIndice: Indice de la planète
        """
        try:
            return self.Star[StarIndice].Orbit[OrbitIndice].Planet
        except:
            print("This planet don't exist")

    def getOrbit(self,StarIndice,OrbitIndice):
        """
        Recupere l'objet planete dans le systeme si il existe
        :param StarIndice: Indice de l'étoile où se situe la planète
        :param OrbitIndice: Indice de la planète
        """
        try:
            return self.Star[StarIndice].Orbit[OrbitIndice]
        except:
            print("This orbit don't exist")

    def getSatellite(self,StarIndice,Orbiteindice,SatelliteIndice):
        """
        Recupere l'objet satellites dans le systeme si il existe
        :param StarIndice: Indice de l'étoile
        :param Orbiteindice: Indice de l'orbite
        :param SatelliteIndice: Indice du satellite
        """
        try:
            return self.Star[StarIndice].Orbit[Orbiteindice].Satellites[SatelliteIndice]
        except:
            print("This satellites don't exist")

    def Show(self, logLevel=2):
        """
        Affiche un visuel du systeme en fonction de :loglevel:
        :param logLevel:
            + si =1 affiche les étoiles et les orbites autour
            + si =2 ajoute les satellites pour chaques étoiles
        """
        print(self)
        if not 1 <= logLevel <= 3: print("Log level inconnue")
        for thisStar in self.Star:
            print(" *"+str(thisStar))
            for thisOrbit in thisStar.Orbit:
                if thisOrbit.Contain in ["Empty","None"] or thisOrbit.Zone in ["OutofRange","Star","TooHot"]:
                                                                                                        dot = "o"
                elif thisOrbit.Contain in ["Small Terrestrial","Terrestrial","Super Terrestrial",
                                         "Desert", "Oceanic", "Glaciated"]:                             dot = "H"
                else:
                                                                                                        dot = "+"
                print("   {}----- {} {}".format(thisStar.Orbit.index(thisOrbit),dot,str(thisOrbit)))
                if logLevel >= 2:
                    for thisSatelliteType in thisOrbit.dicoSatellites.keys():
                        NumberOfSatellites = thisOrbit.dicoSatellites[thisSatelliteType]
                        if NumberOfSatellites is not 0:
                            print("   |      |----- {} {}".format(
                                NumberOfSatellites,thisSatelliteType))
                        if len(thisOrbit.Satellites) is not 0:
                            for thisSatellite in thisOrbit.Satellites:
                                if type(thisSatellite) is Planet and thisSatellite.MoonType is thisSatelliteType:
                                    print("   |      |        {} {}".format("+",thisSatellite))


########################################################################################################################
class Star:
    """
    Objet type: Etoiles
    """
    def __init__(self,Auto=True,IsPrimary=True):
        """

        :param Auto: Defini si la génération est auto
        :param IsPrimary: Défini si l'étoile est primaire ou pas
        """
        self.Orbit = []
        self._nbOrbit = 0  # Nombre cible d'orbite
        self.nbOrbit = len(self.Orbit)  # Nombre courant d'orbite
        self.Distance = None
        self.IsPrimary = IsPrimary  # Si etoile primaire ou companion etc...
        self.IsDwarf = False  # Si l'étoile est Naine ou pas
        self.Class,self.Decimal,self.Size = StarIs("G3V")  # Categorie d'étoile par défaut
        self.FullClassName = self.Class + str(self.Decimal) + self.Size  # Recupere le nom du parent
        self.MaxRange = int()
        self.Note = dict()
        if Auto: self.Autogen(IsPrimary=IsPrimary)

    def __repr__(self):
        txt = "(Class {}{} {}) with {} orbits".format(
            self.Class, self.Decimal, self.Size, self.nbOrbit)
        if self.IsDwarf:    txt = "dwarf " + txt        # Si naine
        if self.IsPrimary:  txt = "Primary " + txt      # Si primaire
        else:               txt = "Companion " + txt    # Si compagnion
        if not self.IsPrimary:
                            txt = txt + " -- {} orbit-distance".format(self.Distance)
        return txt

    def Autogen(self, IsPrimary=True):
        """
        Generation automatique random
        :param IsPrimary: Si etoile primaire
        :return:
        """
    # self.Type
        self.IsPrimary = IsPrimary
    # self.Class
        self.Class = choice(Class)
    # self.Size
        self.Size = choice(StarSize)
    # self.Decimal -- Decimal classification
        self.Decimal = rd.randint(0,9)
        self.FullClassName = self.Class + str(self.Decimal) + self.Size  # Recupere le nom du parent
    # self.Note
        self.Note = self.WriteNote()
    # self.Distance -- Distance entre les etoiles
        RangeDistance = choice(StarDistance)
        if self.IsPrimary == "Primary":     self.Distance = None
        elif RangeDistance == "Close":      self.Distance = rd.randint(1, 2)
        elif RangeDistance == "Medium":     self.Distance = rd.randint(1, 10) + rd.randint(1, 10)
        elif RangeDistance == "Far":        self.Distance = rd.randint(1, 10) * 1000
    # self._NbOrbit  -- Nombre cible d'orbite a creer
        self._nbOrbit = rd.randint(1,10)
        if      self.Size == "II":      self._nbOrbit += 8
        elif    self.Size == "III":     self._nbOrbit += 6
        if      self.Class == "M":      self._nbOrbit -= 6
        elif    self.Class == "K":      self._nbOrbit -= 3
        if      self._nbOrbit < 0:      self._nbOrbit = 0  # mets 0 si inferieur a 0
        # self.Orbit
        for _ in np.arange(self._nbOrbit):  self.addOrbit()  # Ajoute toutes les orbites

    def addOrbit(self,IsRogue=False):
    #  Distance max en fonction de l'étoile
        if self.Size == "IV":   self.MaxRange = 5
        else:                   self.MaxRange = 13
    # Creation dans la liste
        self.Orbit.append(Orbit(itsStar=self,IsRogue=IsRogue))
        self.nbOrbit = len(self.Orbit)

    def delOrbit(self,orbit,log=True):
        """
        Supprime l'orbite demandé
        Attention il faut renommer les orbites après leurs suppression car ça entraine des erreurs pour la suite
        Pour cela utilisez self.RenameOrbit()
        :param orbit: Orbite a supprimer
        :param log: si True avertit l'user de la suppression de l'orbite
        :return:
        """
        if orbit == int():
            try:
                self.Orbit[orbit]
            except:
                print("Impossible de recuperer cette orbite")
        else:
            try:
                self.Orbit.remove(orbit)
                if log: print("{} has been deleted".format(orbit))
            except:
                print("This orbit don't exist")
        self.nbOrbit = len(self.Orbit)

    def WriteNote(self):
        DicoNote = dict()
        if   self.Class == "W":
            DicoNote["Surface Temperature"] = [30000,150000]  #in K
            DicoNote["Color"] = "Blue-Purple"
            DicoNote["Solar Mass"] = "Over 20"
        elif self.Class == "O":
            DicoNote["Surface Temperature"] = [30000,60000]  #in K
            DicoNote["Color"] = "Blue"
            DicoNote["Solar Mass"] = 60
        elif self.Class == "B":
            DicoNote["Surface Temperature"] = [10000,30000]  #in K
            DicoNote["Color"] = "Blue-White"
            DicoNote["Solar Mass"] = 18
        elif self.Class == "A":
            DicoNote["Surface Temperature"] = [7500,10000]  #in K
            DicoNote["Color"] = "White"
            DicoNote["Solar Mass"] = 3.2
        elif self.Class == "F":
            DicoNote["Surface Temperature"] = [6000,7500]  #in K
            DicoNote["Color"] = "Yellow-White"
            DicoNote["Solar Mass"] = 1.3
        elif self.Class == "G":
            DicoNote["Surface Temperature"] = [5000,6000]  #in K
            DicoNote["Color"] = "Yellow"
            DicoNote["Solar Mass"] = 1.1
        elif self.Class == "K":
            DicoNote["Surface Temperature"] = [3500,5000]  #in K
            DicoNote["Color"] = "Orange"
            DicoNote["Solar Mass"] = 0.8
        elif self.Class == "M":
            DicoNote["Surface Temperature"] = 3000  #in K
            DicoNote["Color"] = "Red"
            DicoNote["Solar Mass"] = 0.3

        return DicoNote

########################################################################################################################
class Orbit:
    def __init__(self,Auto=True,itsStar=None,IsRogue=False):
        """
        Objet de Type Orbite
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
        self.Satellites = list()
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
        self.OrbitDistance = utils.truncSignificatif(rd.uniform(0,self.MaxRange),2)  # Distance de l'orbite
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
                    self.Satellites.append(Planet(itsOrbit=self,MoonType=currentSatellitesType))
                else:
                    self.Satellites.append(Satellite(currentSatellitesType))  # Creer l'objet :satellite: de Type :k:
        self.Contain = cacheContain  # recupere la veritable valeur


########################################################################################################################
class Satellite:
    """
    Uniquement les petits satellites sans atmosphere mais avec des caractéristiques utiles
    """
    def __init__(self,SatType,auto=True):
        self.Composition = list()
        self.Type = SatType
        self.Size = int()
        self.Distance = int()
        if auto: self.Autogen()

    def __repr__(self):
        txt = "{} at {} orbit radii".format(self.Type,self.Distance)
        return txt

    def Autogen(self):
    #  self.Size
        if   self.Type in ["MinorRing","MajorRing"]:    self.Size = 1
        elif self.Type in ["Moonlets"]:                 self.Size = rd.choice(np.arange(100,1500,100))
        elif self.Type in ["SmallMoon"]:                self.Size = rd.choice(np.arange(1500,2200,100))
    # self.Distance
        self.Distance = DetermineDistance(self.Type)  # Recupere distance via .csv (voir :DetermineDistance:)


########################################################################################################################
class Planet:
    def __init__(self, auto=True, itsOrbit=None, MoonType=None):
        if itsOrbit is None:
            self.haveOrbit = False
            self.Zone = rd.choice(["Inner","Habitable","Outer"])
            if self.Zone == "Inner":        self.Type = choice(InnerZone)
            elif self.Zone == "Habitable":  self.Type = choice(HabitableZone)
            elif self.Zone == "Outer":      self.Type = choice(OuterZone)
            self.Satellites = list()
            self.Distance = "Unknowed"
            self.nbSatellites = 0
        else:
            self.haveOrbit = True  # Vrai si :itsOrbit: est non nul
            self.Type = itsOrbit.Contain
            self.Zone = itsOrbit.Zone
            self.Satellites = itsOrbit.Satellites
            self.Parent = itsOrbit.Parent
            self.Distance = itsOrbit.OrbitDistance
            self.nbSatellites = itsOrbit.nbSatellites
        self.MoonType = MoonType
        self.ImperialClassification = None
        self.MineralSurvey = dict()
        self.IsHabitable = False
        self.IsGasGiant = False
        self.AtmosphereComposition = "Unknowed"
        self.Size = float()
        self.SizeInEarthRadius = float()  # Affiche la taille de la planete en fonction de celle de la Terre
        self.Surface = float()
        self.Gravity = float()
        self.AtmDensity = float()
        self.Volcanism = float()
        self.Hydroshpere = float()
        self.Cryosphere = float()
        self.TectonicActivity = float()
        self.Land = float()
        self.MeanTemp = float()
        self.Humidity = float()
        self.Climate = str()
        self.Day = int()
        self.Note = str()
        self.TotalMoonSize = float()
        if auto:    self.Autogen()

    def __repr__(self):
        txt = "(size: {} earth radius)".format(utils.truncSignificatif(self.SizeInEarthRadius,3))
        if self.IsHabitable:    txt = "{} world ".format(self.Type) + txt
        else:                   txt = "{} planet ".format(self.Type) + txt
        return txt

    def Autogen(self):
    # self.size
        if self.MoonType is None: self.Size = rollSize(self.Type)
        else:                     self.Size = rollSize(self.MoonType)
        self.SizeInEarthRadius = self.Size / 12000  # Affiche la taille de la planete en fonction de celle de la Terre
        self.Surface = 2*np.pi*self.Size**2/4
        self.Gravity = self.Size / 12000
    # self.atmosphere
        # modifiers
        modifiers = 0
        if   self.Zone == "Inner":      modifiers -= 2
        elif self.Zone == "Habitable":  modifiers += 1
        elif self.Zone == "Outer":      modifiers += 2
        if   self.Size < 5000:          modifiers -= 2
        elif self.Size > 8000:          modifiers -= 2
        # Atmosphere
        if self.Type in ["Proto Planet"]:
            self.AtmosphereComposition = rollchoicedico(ProtoPlanetAtm, (1, 10), modifiers)
        elif self.Type in ["Geo Active"]:
            self.AtmosphereComposition = rollchoicedico(GeoActiveAtm, (1, 10), modifiers)
        elif self.Type in ["Mesoplanet"]:
            self.AtmosphereComposition = rollchoicedico(MesoplanetAtm, (1, 10), modifiers)
        elif self.Type in ["Reducing","Ultra Hostile"]:
            self.AtmosphereComposition = rollchoicedico(ReducingAtm, (1, 10), modifiers)
        elif self.Type in ["Marginal"]:
            self.AtmosphereComposition = rollchoicedico(MarginalAtm, (1, 10), modifiers)
        elif self.Type in ["Chthonian"]:
            self.AtmosphereComposition = rollchoicedico(ChthonianAtm, (1, 10), modifiers)
        elif self.Type in ["Ice World","Dirty SnowBall"]:
            self.AtmosphereComposition = rollchoicedico(IceWorldAtm, (1, 10), modifiers)
        elif self.Type in ["Super Terrestrial"]:
            self.AtmosphereComposition = rollchoicedico(SuperTerrestrialAtm, (1, 10), modifiers)
        elif self.Type in ["Small Terrestrial"]:
            self.AtmosphereComposition = rollchoicedico(SmallTerrestrialAtm, (1, 10), modifiers)
        else:
            self.AtmosphereComposition = rollchoicedico(TerrestrialAtm, (1, 10), modifiers)
    # self.AtmDensity
        modifiers = 1.2*(self.Size/1000)-10  # Base sur la liste de modifs dans le .pdf
        if modifiers <= -8: modifiers = -8
        elif modifiers >= 8: modifiers = 8
    # self.IsHabitable
        if self.Type in ["Small Terrestrial", "Terrestrial", "Super Terrestrial", "Desert", "Oceanic", "Glaciated"]:
            self.IsHabitable = True
        if self.Type in ["Gas Giant","Small Gas Giant","Gas SuperGiant","Gas UltraGiant"]:
            self.IsGasGiant = True

        if self.IsHabitable:
            self.AtmDensity = rollchoicedico(HabitableDensity,(1,10),modifiers)
        else:
            self.AtmDensity = rollchoicedico(UnhabitableDensity,(1,10),modifiers)
    # self.Hydrosphere, Cryosphere, Volcanism etc ...
        if self.Type in ["Proto Planet"]:
            self.Hydroshpere = 0
            self.Cryosphere = 0
            self.Volcanism = 100
            self.TectonicActivity = 100
            self.Note = ["Surface Too Hot"]

        elif self.Type in ["Geoactive"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(1,20)*5   ,roll(1,20)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (0              ,roll(1,20)*5)
            self.Volcanism =            roll(5,8)*10
            self.TectonicActivity =     roll(5,9)*10

        elif self.Type in ["Mesoplanet"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (0              ,0)
            else:                               self.Hydroshpere, self.Cryosphere = (0              ,roll(1,20)*5)
            self.Volcanism =            roll(0,8)
            self.TectonicActivity =     0
            self.Note = ["Possible ice in Shadow"]

        elif self.Type in ["Small Terrestrial"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (0              ,roll(0,10)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (0              ,roll(1,20)*5)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Desert"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(1,4)*5    ,roll(1,4)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Glaciated"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(1,20)*5  ,roll(14,16)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Marginal"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(0,8)*5    ,roll(1,4)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Oceanic"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(14,18)*5  ,roll(0,20)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Paradise","Terrestrial"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(4,16)*5   ,roll(4,16)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,4)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Reducing"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (0              ,0)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,6)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Ultra Hostile"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (None           ,None)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (None           ,None)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,None)
            self.Volcanism =            roll(0,5)*10
            self.TectonicActivity =     roll(0,5)*10

        elif self.Type in ["Super Terrestrial"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (roll(0,20)*5   ,roll(0,20)*5)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,roll(10,20)*5)
            self.Volcanism =            roll(0,6)*10
            self.TectonicActivity =     roll(0,4)*10

        elif self.Type in ["Dirty SnowBall"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (None           ,None)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (None           ,None)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,roll(6,20)*5)
            self.Volcanism =            roll(0,3)*10
            self.TectonicActivity =     roll(0,3)*10

        elif self.Type in ["Ice World"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (None           ,None)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (None           ,None)
            else:                               self.Hydroshpere, self.Cryosphere = (None           ,roll(14,20)*5)
            self.Volcanism =            roll(0,3)*10
            self.TectonicActivity =     roll(0,2)*10

        elif self.Type in ["Chthonian"]:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (0              ,0)
            else:                               self.Hydroshpere, self.Cryosphere = (0              ,0)
            self.Volcanism =            0
            self.TectonicActivity =     0
            self.Note = ["Some Dust and Ice gravity captured"]

        else:
            if self.Zone == "Inner":            self.Hydroshpere, self.Cryosphere = (0              ,0)
            elif self.Zone == "Habitable":      self.Hydroshpere, self.Cryosphere = (0              ,0)
            else:                               self.Hydroshpere, self.Cryosphere = (0              ,0)
            self.Volcanism =            0
            self.TectonicActivity =     0

    # Fait en sorte que la somme hydro+cryo ne depasse pas 100
        if self.Hydroshpere is None: self.Hydroshpere = 0
        if self.Cryosphere is None: self.Cryosphere = 0
        if self.Hydroshpere + self.Cryosphere > 100:
            self.Hydroshpere    = ( self.Hydroshpere / (self.Hydroshpere+self.Cryosphere) )*100
            self.Cryosphere     = ( self.Cryosphere / (self.Hydroshpere+self.Cryosphere) )*100
    # self.land
        self.Land = 100 - (self.Hydroshpere + self.Cryosphere)
        if self.Land < 0 : self.Land = 0
        if self.Land > 100 : self.Land = 100
        if self.IsGasGiant: self.Land = 0
    # self.Humidity
        if self.IsHabitable:
            self.Humidity = (roll(1,10)+self.Hydroshpere)/2
        else:
            self.Humidity = 0
        if self.Humidity < 0 : self.Humidity = 0
        if self.Humidity > 100 : self.Humidity = 100
    # self.Day
        self.TotalMoonSize = 0
        for sat in self.Satellites :
            self.TotalMoonSize += sat.Size
        self.Day = roll(1,10)+roll(1,10)+roll(1,10) + self.TotalMoonSize/1000
    # self.MeanTemp
        self.MeanTemp = 40 - self.Cryosphere/2
    # self.Climate
        if self.IsHabitable:
            self.Climate = determineClimate(self.Cryosphere,self.Hydroshpere,self.Humidity)
    # self.MineralSurvey
        if self.Type not in ["Gas Giant","Gas SuperGiant","Gas UltraGiant","Small Gas Giant"]:
            self.MineralSurvey = determineMineralSurvey(self.Type)
    # self.ImperialClassification
        if self.IsHabitable:
            self.ImperialClassification = choice(ImperialClass)

    def Show(self):
        if not self.haveOrbit:      Parent = "n Unknow"
        else:                       Parent = " "+ str(self.Parent)
        txt = """+++ NO NAMED +++: {} planet around a{} star
Segmentum:      +++ NO ENTRY +++
Sector:         +++ NO ENTRY +++
Sub-Sector:     +++ NO ENTRY +++

Global Survey:              in {} zone ({} orbit-distance)
Diameter:                   {} km ({} Terra radium)
Surface:                    {} km²
Gravity on surface:         {}g
Satellites:                 {}

Imperial classification:    {}world
Approximate Population:     +++ NO ENTRY +++

Atmosphere:                 {} atmosphere
Main Composition:           {}
Hydrosphere:                {} %
Cryosphere:                 {} %
Land cover:                 {} %

Mean Temperature:           {}°C
Global Climate:             {}
Day Duration:               {} H

Moons:                      {} Moons
        """.format(
        self.Type,Parent,
        self.Zone,self.Distance,
        self.Size,utils.truncSignificatif(self.SizeInEarthRadius,3),
        utils.truncSignificatif(np.pi * self.Size ** 2 / 4,5),
        utils.truncSignificatif(self.Gravity,3),
        self.nbSatellites,
        self.ImperialClassification,
        self.AtmDensity,
        self.AtmosphereComposition,
        utils.truncSignificatif(self.Hydroshpere,2),
        utils.truncSignificatif(self.Cryosphere,2),
        utils.truncSignificatif(self.Land,2),
        round(self.MeanTemp),
        self.Climate,
        int(self.Day),
        self.nbSatellites
        )
        txtSat = ""
        for thisSat in self.Satellites:
            currentLine = str(thisSat)
            txtSat += "      +-- {} \n".format(currentLine)

        print(txt)
        print(txtSat)


########################################################################################################################

S = System()
S.createPlanet()
S.createSatellites()
S.Show(3)
"""
input("Test de la creation de systeme")
again = True
n = 0
while n is not 10:
    n += 1
    S = System()
    print(S)
    S.clearorbit()


input("Test suppression et creation orbit manuelle")
for i in np.arange(10):
    S = System(auto=False)
    setattr(S,"Star1",Star())
    s1 = S.Star1
    s1.delOrbit("Orbit10")
    s1.addOrbit(nom="Orbit1000")
"""
