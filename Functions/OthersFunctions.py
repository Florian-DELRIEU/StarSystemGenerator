
def setGravLock(planet):
    """
    TODO
        - Ajouter des paramètres
    :param planet:
    :return:
    """
    try:
        SolarMass = planet.Parent.DicoNote["Solar Mass"] # Masse Solaire du parent
        Distance = planet.Distance
        LockTime = Distance**6 / SolarMass**2  # Formule simplifiée
        return 1/LockTime >= 10000
    except:
        return False
