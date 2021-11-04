from Class.Planet import Planet
from Class.Star import Star
from Functions.RollingFunctions import *
from Functions.Tables import *


class System:
    """
        Objet Type: Systeme Solaire
        + Par défaut (auto = True) un systeme va se générer automatiquement de manière aléatoire
                + Les étoiles
                + Les orbites dans chaque étoiles (les type de planetes sont générer mais les objets ne sont pas crées)
        + Si :auto = False: cela va générer un systeme preconfiguré (voir self.__init__)
        - self.Star : Liste regroupant les étoiles
        - self.Type : Définie le type de system selon le nombre d'étoiles (Binaire, Solitaire, ...)
        - self.nbOrbit = Nombre total d'orbite dans le systeme
        - self.nbRogueOrbit = Nombre d'orbite de planètes volées (rogue planets)
        - self._nbStar = Nombre d'étoiles déterminer par le tirage aléotoire lors de la génération du :System:
        - self.nbStar = Nombre d'étoiles determiner par la longueur de la liste :self.Star:
    """
    def __init__(self,auto=True):
        """
        Situation initiale
        :param auto: Determine la génération aléatoire ou non du systeme
        """
    # Initialisation
        self.Star_list = []  # Liste regroupant les etoiles
        self.nbRogueOrbit = 0
        self._nbStar = 1
        self.nbStar = 1
        self.nbOrbit = 0
        self.Type = str()
    # Generation
        if auto: self.Autogen()  # Lance la creation auto si :auto:=vrai

    def __repr__(self):
        """
        Determine comment afficher l'objet lorqu'il est appelé
        """
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
        for curStar in self.Star_list:
            self.nbOrbit += curStar.nbOrbit
    # self.RogueOrbit
        self.nbRogueOrbit = choice(RoguePlanet)     # Combien de Rogue Planet ?
        self.nbOrbit += self.nbRogueOrbit           # Ajoute au nombre d'orbites
        self.createRogue(self.nbRogueOrbit)

    def createRogue(self,nbRogue):
        """
        Ajoute une planète "Rogue" a l'une des étoiles du système. Ces planètes obéissent a des règles de génération
            différentes.
        :param nbRogue: Nombre de planètes à ajouter
        """
        for _ in np.arange(nbRogue):  # _ remplace la variable muette
            thisStar = rd.choice(self.Star_list)  # Choisi parmis les etoiles du systeme
            thisStar.addOrbit(IsRogue=True)       # Ajoute l'orbit Rogue a l'etoile choisis

    def determineType(self):
        """
        Fonction permettant de définir le type de systeme (Solitaire, Binaire) en fonction de :_nbStar:
        """
        if   self._nbStar == 1: self.Type = "Solitary"
        elif self._nbStar == 2: self.Type = "Binary"
        elif self._nbStar == 3: self.Type = "Ternary"
        return self.Type

    def addAllStar(self):
        """
        Ajoute :_nbStar: étoiles dans le :System: et definie l'étoile principales et ses compangons
        """
        for i in np.arange(self._nbStar):
            IsPrimary = i==0
            self.addStar(IsPrimary=IsPrimary)

    def addStar(self,Auto=True,IsPrimary=False):
        """
        Ajoute une étoile aléatoire au systeme
        :param Auto: Definie si la génération auto est activé lors de la creation de l'étoile
        :param IsPrimary: Si :True:, l'étoile est primaire
        """
        self.Star_list.append(Star(Auto=Auto, IsPrimary=IsPrimary))
        self.nbStar = len(self.Star_list)  # Mets a jour le param :nbStar:

    def delStar(self,star):
        """
        Supprime l'étoile selon son indice ou l'objet assigné
        :param star: - Si un :int(): est entré, alors détruit l'étoile avec l'indice associé
                     - Si un objet :Star: est entré, alors détruit cette étoile
        """
        if type(star) == int():
            self.Star_list.remove(self.Star_list[star])
        else:
            self.Star_list.remove(star)
            self.nbStar = len(self.Star_list)

    def refresh_nbOrbit(self):
        """
        Raffraichi le nombre d'orbite dans le système
        """
        self.nbOrbit = 0
        for thisStar in self.Star_list:
            self.nbOrbit += thisStar.nbOrbit

    def clearorbit(self):
        """
        Supprime les orbites vides ou mal places dans tout le systeme qui ne sont pas censé exister
        """
        for curStar in self.Star_list:
            for curOrbit in curStar.Orbit_list:
                if curOrbit.Zone in ["Star","TooHot","OutofRange"] or curOrbit.Contain == "Empty":
                    curStar.delOrbit(curOrbit)
        self.refresh_nbOrbit()

    def createSatellites(self):
        """
        Creer les objets satellites dans toutes les orbites du systeme (voir l'objet :Orbit:)
        Fait appel à la fonction des objets :Orbit: de :System:
        """
        for thisStar in self.Star_list:
            for thisOrbit in thisStar.Orbit_list:
                thisOrbit.createSatellites()

    def createPlanet(self):
        """
        Creer les objets planetes dans toutes les orbites du systeme
        Fait appel à la fonction des objets :Orbit: de :System:
        """
        for thisStar in self.Star_list:
            for thisOrbit in thisStar.Orbit_list:
                thisOrbit.createPlanet()

    def getPlanet(self,StarIndice,OrbitIndice):
        """
        Recupere l'objet planete dans le systeme si il existe. Moyen plus rapide que de passer dans les listes des
            étoiles et des planètes
            - getPlanet(1,3) = self.Star[1].Orbit[3].Planet
        :param StarIndice: Indice de l'étoile où se situe la planète
        :param OrbitIndice: Indice de la planète
        """
        try:
            return self.Star_list[StarIndice].Orbit[OrbitIndice].Planet
        except:
            print("This planet don't exist")

    def getOrbit(self,StarIndice,OrbitIndice):
        """
        Recupere l'objet planete dans le systeme si il existe
        :param StarIndice: Indice de l'étoile où se situe la planète
        :param OrbitIndice: Indice de la planète
        """
        try:
            return self.Star_list[StarIndice].Orbit[OrbitIndice]
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
            return self.Star_list[StarIndice].Orbit[Orbiteindice].Satellites_list[SatelliteIndice]
        except:
            print("This satellites don't exist")

    def Show(self, logLevel=2, PrintInOrder=False):
        """
        Affiche un visuel du systeme en fonction de :loglevel:
        :param logLevel:
            + si =1 affiche les étoiles et les orbites autour
            + si =2 ajoute les satellites pour chaques étoiles
        :param PrintInOrder:
            - if TRUE, run OrderingPlanets(self) to show the orbit in order of distance
        """
        if PrintInOrder:
            self.OrderingPlanets()
        print(self)
        if not 1 <= logLevel <= 3: print("Log level inconnue")
        for thisStar in self.Star_list:
            print(" *"+str(thisStar))
            for thisOrbit in thisStar.Orbit_list:
                if thisOrbit.Contain in ["Empty","None"] or thisOrbit.Zone in ["OutofRange","Star","TooHot"]:
                                                                                                        dot = "o"
                elif thisOrbit.Contain in ["Small Terrestrial","Terrestrial","Super Terrestrial",
                                         "Desert", "Oceanic", "Glaciated"]:                             dot = "H"
                else:
                                                                                                        dot = "+"
                print("   {}----- {} {}".format(thisStar.Orbit_list.index(thisOrbit)+1, dot, str(thisOrbit)))
                if logLevel >= 2:
                    for thisSatelliteType in thisOrbit.dicoSatellites.keys():
                        NumberOfSatellites = thisOrbit.dicoSatellites[thisSatelliteType]
                        if NumberOfSatellites != 0:
                            print("   |      |----- {} {}".format(
                                NumberOfSatellites,thisSatelliteType))
                        if len(thisOrbit.Satellites_list) != 0:
                            for thisSatellite in thisOrbit.Satellites_list:
                                if type(thisSatellite) is Planet and thisSatellite.MoonType is thisSatelliteType:
                                    print("   |      |        {} {}".format("+",thisSatellite))

    def OrderingPlanets(self):
        temp_list = []
        for thisStar in self.Star_list:             # for each stars
            for thisOrbit in thisStar.Orbit_list:   # for each orbit
                temp_list.append({                  # temporary list for prepare the sorting
                    "Orbit":thisOrbit,              # object to sort
                    "Distance":thisOrbit.OrbitDistance  # sorting argument
                })
            temp_list.sort(key=lambda x: x.get('Distance'))  # sorting regarding the distance
            thisStar.Orbit_list = [el["Orbit"] for el in temp_list]

