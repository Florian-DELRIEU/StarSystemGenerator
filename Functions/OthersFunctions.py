from Class.Planet import Planet

def setGravLock(planet:Planet):
    """
    TODO
        - Ajouter des paramètres
    :param planet:
    :return:
    """
    SolarMass = planet.Parent.DicoNote["Solar Mass"] # Masse Solaire du parent
    Distance = planet.Distance
    LockTime = Distance**6 / SolarMass**2  # Formule simplifiée