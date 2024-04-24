"""
Package for calculating Local Sidereal Time.
"""

import numpy as np
from datetime import datetime, timedelta
from AstroTransform.time import JD

def local_to_ut(local_time, time_zone):
    """
    Convert local times to Universal Time for an array or a single datetime object.

    Parameters
    ----------
    local_time : datetime.datetime or np.array of datetime.datetime
        The local times to convert to Universal Time.
    time_zone : float or np.array of float
        Time zone offsets for each datetime.

    Returns
    -------
    datetime.datetime or np.array of datetime.datetime
        The Universal Times.
    """
    # Convert inputs to arrays if not already
    local_time_arr = np.atleast_1d(local_time)
    time_zone_arr = np.atleast_1d(time_zone)

    # Calculate UT for each datetime in the array
    ut = local_time_arr - np.array([timedelta(hours=offset) for offset in time_zone_arr])

    # Return scalar if input was scalar
    if np.isscalar(local_time) and np.isscalar(time_zone):
        return ut[0]
    return ut

def ut_to_local(ut, time_zone):
    """
    Convert Universal Times to local times for an array or a single datetime object.

    Parameters
    ----------
    ut : datetime.datetime or np.array of datetime.datetime
        The Universal Times to convert to local time.
    time_zone : float or np.array of float
        Time zone offsets for each datetime.
    
    Returns
    -------
    datetime.datetime or np.array of datetime.datetime
        The local times.
    """

    # Convert inputs to arrays if not already
    ut_arr = np.atleast_1d(ut)
    time_zone_arr = np.atleast_1d(time_zone)

    # Convert to local time for each datetime in the array
    local_time = ut_arr + np.array([timedelta(hours=offset) for offset in time_zone_arr])

    # Return scalar if input was scalar
    if np.isscalar(ut) and np.isscalar(time_zone):
        return local_time[0]
    return local_time

def lst(date_time, longitude, time_zone=0):
    """
    Calculate Local Sidereal Time for an array or a single datetime object.

    Parameters
    ----------
    date_time : datetime.datetime or np.array of datetime.datetime
        The datetime objects to calculate the LST for.
    longitude : float or np.array of float
        The longitude of the observer in degrees.
    time_zone : float or np.array of float
        The time zone of the observer (default 0).
    
    Returns
    -------
    float or np.array of float
        The Local Sidereal Time in hours.
    """

    # Convert input to arrays
    date_time_arr = np.atleast_1d(date_time)
    longitude_arr = np.atleast_1d(longitude)
    time_zone_arr = np.atleast_1d(time_zone)

    # Convert to UT
    ut = local_to_ut(date_time_arr, time_zone_arr)

    # Calculate Julian Date for each UT
    jd = np.array([JD.to_jd(d) for d in ut])

    # Calculate days since J2000.0 at 12:00 UT
    D = jd - 2451545.0

    # Calculate GMST for each day
    GMST = (18.697374558 + 24.06570982441908 * D) % 24

    # Calculate LST for each datetime and longitude
    LST = GMST + (longitude_arr / 15)

    # Adjust LST to be in the range [0, 24)
    LST = LST % 24

    # Return scalar if input was scalar
    if np.isscalar(date_time) and np.isscalar(longitude) and np.isscalar(time_zone):
        return LST[0]
    return LST
