from src.SSG.Functions.Functions import *
import random as rd
import numpy as np

class Satellite:
    """
    Uniquement les petits satellites sans atmosphere mais avec des caractéristiques utiles
    -   self.Composition: Composition du satellite
    -   self.Type: Type du satellite
    -   self.Size: Taille
    -   self.Distance: Distance par rapport à sa planète
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
