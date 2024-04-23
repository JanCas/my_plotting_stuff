import numpy as np
from scipy.constants import value

def saturation_pressure(T):
    '''
    Calculates the saturation pressure for a given temperature.

    uses the Buck equation

    :param temperature: temperature input in kelvin units
    :return: saturation pressure of water in Pa
    '''

    T = T - 273.15

    return .61121*np.exp((18.678 - T/234.5)*(T/(257.14 + T))) * 1000

def relative_humidity(T, c):
    '''
    Calculates the relative humidity for a given temperature and concentration
    :param T: Temperature in kelvin units
    :param c: concentration of the water vapor in mol/m^3
    :return: relative humidity
    '''

    return c*value('molar gas constant')*T/saturation_pressure(T)