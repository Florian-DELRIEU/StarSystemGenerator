import random as rd

import numpy as np
from Functions.OthersFunctions import setGravLock
from Functions.RollingFunctions import *
from Functions.Tables import *
from MyPack.Utilities import truncSignificatif


class Planet:
    """
    Objet de type planète
    -   self.haveOrbit: False si la planète est générer seule
    -   self.Zone: ["Inner","Habitable","Outer"]
    -   self.Satellites: Liste de satellites
    -   self.nbSatellites: Nombre de satellites selon les infos de son :Orbit:
    -   self.Distance: Distance par rapport au soleil

    """
    def __init__(self, auto=True, itsOrbit=None, MoonType=None):
        if itsOrbit is None:
            self.haveOrbit = False
            self.Zone = rd.choice(["Inner","Habitable","Outer"])
            if self.Zone == "Inner":        self.Type = choice(InnerZone)
            elif self.Zone == "Habitable":  self.Type = choice(HabitableZone)
            elif self.Zone == "Outer":      self.Type = choice(OuterZone)
            self.Satellites_list = []
            self.Distance = "Unknowed"
            self.nbSatellites = 0
        else:
            self.haveOrbit = True  # Vrai si :itsOrbit: est non nul
            self.Type = itsOrbit.Contain
            self.Zone = itsOrbit.Zone
            self.Satellites_list = itsOrbit.Satellites_list
            self.Parent = itsOrbit.Parent
            self.Distance = itsOrbit.OrbitDistance
            self.nbSatellites = itsOrbit.nbSatellites
        self.MoonType = MoonType
        self.ImperialClassification = None
        self.MineralSurvey = {}
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
        self.isGravLocked = False
        if auto:    self.Autogen()

    def __call__(self, *args, **kwargs): pass

    def __repr__(self):
        txt = "(size: {} earth radius)".format(truncSignificatif(self.SizeInEarthRadius,3))
        if self.IsHabitable:    txt = "{} world ".format(self.Type) + txt
        else:                   txt = "{} planet ".format(self.Type) + txt
        return txt

    def Autogen(self):
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
        elif self.Size > 8000:          modifiers += 1
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
        self.isGravLocked = setGravLock(self)
        self.TotalMoonSize = 0
        for sat in self.Satellites_list :
            self.TotalMoonSize += sat.Size
        if self.isGravLocked:
            self.Day = 0
        else:
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
        Parent = "n Unknow" if not self.haveOrbit else " "+ str(self.Parent)
        txt = f"""+++ NO NAMED +++: {self.Type} planet around a{Parent} star
Segmentum:      +++ NO ENTRY +++
Sector:         +++ NO ENTRY +++
Sub-Sector:     +++ NO ENTRY +++

Global Survey:              in {self.Zone} zone ({self.Distance} orbit-distance)
Diameter:                   {self.Size} km ({self.SizeInEarthRadius} Terra radium)
Surface:                    {self.Surface} km²
Gravity on surface:         {self.Gravity}g
Satellites:                 {self.nbSatellites}

Imperial classification:    {self.ImperialClassification} world
Approximate Population:     +++ NO ENTRY +++

Atmosphere:                 {self.AtmDensity} atmosphere
Main Composition:           {self.AtmosphereComposition}
Hydrosphere:                {truncSignificatif(self.Hydroshpere,2)} %
Cryosphere:                 {truncSignificatif(self.Cryosphere,2)} %
Land cover:                 {truncSignificatif(self.Land,2)} %
Volcanism:                  {self.Volcanism} %
Tectonic activity:          {self.TectonicActivity} %
Humidity:                   {self.Humidity} %

+++ MINERAL SURVEY +++
Minerals:                   {self.MineralSurvey["Minerals"]}
Common Metals:              {self.MineralSurvey["Common Metals"]}
Rare Metals:                {self.MineralSurvey["Rare Metals"]}
Industrial Crystals:        {self.MineralSurvey["Industrial Crystals"]}
Gemstones:                  {self.MineralSurvey["Gemstones"]}
Radioactive:                {self.MineralSurvey["Radioactives"]}

Mean Temperature:           {self.MeanTemp}°C
Global Climate:             {self.Climate}
Day Duration:               {self.Day} H
Gravitation Lock:           {self.isGravLocked}

Moons:                      {self.nbSatellites} Moons
Global Notes:               {self.Note}
        """
        txtSat = ""
        for thisSat in self.Satellites_list:
            currentLine = str(thisSat)
            txtSat += "      +-- {} \n".format(currentLine)

        print(txt)
        print(txtSat)
