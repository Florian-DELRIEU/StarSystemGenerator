from Class.Orbit import *
from Functions.Functions import *
from Functions.Tables import *
import random as rd
import numpy as np

class Star:
    """
    Objet type: Etoiles
    -   self.Orbit: Liste regroupant les orbites de l'étoiles
    -   self._nbOrbit: Nombre cible d'orbite selon la génération aléatoire
    -   self.nbOrbit: Nombre courant d'orbite. Longueur de la liste :self.Orbit:
    -   self.Distance: Distance d'éloignement par rapport à l'étoile principale (0 si principale)
    -   self.IsPrimary: :True: si etoile primaire
    -   self.IsDwarf = :True: si l'étoile est Naine ou pas
    -   self.Class,self.Decimal,self.Size: Categorie d'étoile selon la classification universelle
    -   self.FullClassName: Recupere le nom selon sa category ("G3V" par exemple)
    -   self.MaxRange: Distance max d'éloignement des orbites
    -   self.Note: Notes diverse sur l'étoile en question
    """
    def __init__(self,Auto=True,IsPrimary=True):
        """
        :param Auto: Defini si la génération est auto
        :param IsPrimary: Défini si l'étoile est primaire ou pas
        """
        self.Orbit_list = []
        self._nbOrbit = 0  # Nombre cible d'orbite
        self.nbOrbit = len(self.Orbit_list)  # Nombre courant d'orbite
        self.Distance = None
        self.IsPrimary = IsPrimary  # Si etoile primaire ou companion etc...
        self.IsDwarf = False  # Si l'étoile est Naine ou pas
        self.Class,self.Decimal,self.Size = StarIs("G3V")  # Categorie d'étoile par défaut
        self.FullClassName = self.Class + str(self.Decimal) + self.Size  # Recupere le nom
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
        """
        Ajoute une orbite à l'étoile
        :param IsRogue: Ajoute une Rogue si :True:
        :return: Nouvelle orbite dans la liste
        """
    #  Distance max en fonction de l'étoile
        if self.Size == "IV":   self.MaxRange = 5
        else:                   self.MaxRange = 13
    # Creation dans la liste
        self.Orbit_list.append(Orbit(itsStar=self, IsRogue=IsRogue))
        self.nbOrbit = len(self.Orbit_list)

    def delOrbit(self,orbit,log=True):
        """
        Supprime l'orbite demandé
        Attention il faut renommer les orbites après leurs suppression car ça entraine des erreurs pour la suite
        Pour cela utilisez self.RenameOrbit()
        :param orbit: Orbite a supprimer
        :param log: si True averti l'user de la suppression de l'orbite
        """
        if orbit == int():
            try:
                self.Orbit_list[orbit]
            except:
                print("Impossible de recuperer cette orbite")
        else:
            try:
                self.Orbit_list.remove(orbit)
                if log: print("{} has been deleted".format(orbit))
            except:
                print("This orbit don't exist")
        self.nbOrbit = len(self.Orbit_list)

    def WriteNote(self):
        """
        Ecris des infos diverse complémentaire en fonction du tirage et de sa catégorie
        :return: Sous forme de dictionnaire :DicoNote:
        """
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