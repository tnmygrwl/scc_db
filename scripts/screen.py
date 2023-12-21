import numpy as np

# Constants provided
a = [0.008, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081]
b = [0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144]
k = 0.0162
C = [6.766097e-01, 2.005640e-02, 1.104259e-04, -6.969800e-07, 1.003100e-09]
B = [-6.246090e-3, -7.423444e-3, -1.048635e-2, -7.987907e-3]
C0 = -4.679983e-7


def calculate_Rt(CS_t: float, T: float) -> float:
    """
    Calculate Rt which is the ratio of specific conductance to rT.

    Parameters:
    CS_t (float): Specific Conductance
    T (float): Water temperature in degrees C

    Returns:
    float: The calculated Rt value
    """

    R = CS_t / 42.914
    rT = sum([C[i] * (T**i) for i in range(len(C))])
    return R / rT


def calculate_salinity(CS_t: float, T: float) -> float:
    """
    Calculate Salinity based on specific conductance and temperature.

    Parameters:
    CS_t (float): Specific Conductance
    T (float): Water temperature in degrees C

    Returns:
    float: The calculated salinity value
    """

    Rt = calculate_Rt(CS_t, T)
    salinity = sum([a[i] * (Rt ** (0.5 * i)) for i in range(len(a))]) + (T - 15) / (
        1 + k * (T - 15)
    ) * sum([b[i] * (Rt ** (0.5 * i)) for i in range(len(b))])
    return salinity


def calculate_TS(TC: float) -> float:
    """
    Calculate TS which is a function of temperature.
    
    Parameters:
    TC (float): Temperature in degrees C
    
    Returns:
    float: The calculated TS value
    """
    return np.log((298.15 - TC) / (273.15 + TC))


def calculate_SC(S: float, TC: float) -> float:
    """
    Calculate Salinity Correction Factor based on salinity and temperature.
    
    Parameters:
    S (float): Salinity
    TC (float): Temperature in degrees C
    
    Returns:
    float: The calculated Salinity Correction Factor
    """
    TS = calculate_TS(TC)
    ln_SC = S * sum([B[i] * (TS**i) for i in range(len(B))]) + C0 * (S**2)
    return np.exp(ln_SC)


def adjusted_DO(DO_FIELD_CAL: float, CS_t: float, T: float) -> float:):
    """
    Calculate adjusted dissolved oxygen concentration which takes into account salinity.
    
    Parameters:
    DO_FIELD_CAL (float): Field calibration of dissolved oxygen
    CS_t (float): Specific Conductance
    T (float): Water temperature in degrees C
    
    Returns:
    float: The adjusted dissolved oxygen concentration
    """
    S = calculate_salinity(CS_t, T)
    SC = calculate_SC(S, T)
    return DO_FIELD_CAL * SC
