import numpy as np

"""
Refactored module to calculate hour angle and related conversions, 
supporting both scalar and vector inputs.
"""

def hourangle(LST, RA):
    """
    Calculate the hour angle of an object for either an array or a single value.

    Parameters
    ----------
    LST : float or np.array of float
        The local sidereal time in hours.
    RA : float or np.array of float
        The right ascension of the object in hours.

    Returns
    -------
    float or np.array of float
        The hour angle in hours.
    """
    # Convert inputs to arrays if not already
    LST_arr = np.atleast_1d(LST)
    RA_arr = np.atleast_1d(RA)

    # Calculate the hour angle
    HA = LST_arr - RA_arr
    # Normalize HA between -12 and 12 hours
    HA = (HA + 12) % 24 - 12

    # Return scalar if input was scalar
    if np.isscalar(LST) and np.isscalar(RA):
        return HA[0]
    return HA

def ha_to_deg(HA):
    """
    Convert an hour angle from hours to degrees for either an array or a single value.

    Parameters
    ----------
    HA : float or np.array of float
        The hour angle in hours.

    Returns
    -------
    float or np.array of float
        The hour angle in degrees.
    """
    # Convert input to array if not already
    HA_arr = np.atleast_1d(HA)

    # Convert hour angle to degrees
    HA_deg = HA_arr * 15.0

    # Return scalar if input was scalar
    if np.isscalar(HA):
        return HA_deg[0]
    return HA_deg

def deg_to_ha(HA_deg):
    """
    Convert an hour angle from degrees to hours for either an array or a single value.

    Parameters
    ----------
    HA_deg : float or np.array of float
        The hour angle in degrees.

    Returns
    -------
    float or np.array of float
        The hour angle in hours.
    """
    # Convert input to array if not already
    HA_deg_arr = np.atleast_1d(HA_deg)

    # Convert degree to hours
    HA_hours = HA_deg_arr / 15.0

    # Return scalar if input was scalar
    if np.isscalar(HA_deg):
        return HA_hours[0]
    return HA_hours
