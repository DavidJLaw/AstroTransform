""" 
convert target to alt az
"""

import numpy as np
from datetime import datetime, timedelta
from AstroTransform.time import JD, lst
from AstroTransform.coords import hour_angle
from astropy.time import Time

def to_alt_az(RA, DEC, Lat, Lon, obs_time, time_zone=0):
    """
    Convert a target's RA and DEC to Altitude and Azimuth.
    
    Parameters
    ----------
    RA : float
        The right ascension of the target in hours.
    DEC : float
        The declination of the target in degrees.
    Lat : float
        The latitude of the observer in degrees.
    Lon : float
        The longitude of the observer in degrees.
    obs_time : datetime.datetime
        The local time of the observation
    
    Returns
    -------
    float
        The altitude of the target in degrees.
    float
        The azimuth of the target in degrees.
        
    """
    if isinstance(obs_time, Time):
        obs_time = obs_time.to_datetime()
    if not isinstance(RA, (int, float)):
        raise TypeError("Expected a float or int for 'RA'.")
    if not isinstance(DEC, (int, float)):
        raise TypeError("Expected a float or int for 'DEC'.")
    if not isinstance(Lat, (int, float)):
        raise TypeError("Expected a float or int for 'Lat'.")
    if not isinstance(Lon, (int, float)):
        raise TypeError("Expected a float or int for 'Lon'.")
    if not isinstance(obs_time, datetime):
        raise TypeError("Expected a datetime.datetime object for 'obs_time'.")

     # Convert inputs to arrays
    RA_arr = np.atleast_1d(RA)
    DEC_arr = np.atleast_1d(DEC)
    Lat_arr = np.atleast_1d(Lat)
    Lon_arr = np.atleast_1d(Lon)
    obs_time_arr = np.atleast_1d(obs_time)

    # Convert to radians
    RA_rad = np.deg2rad(RA_arr * 15.0)
    DEC_rad = np.deg2rad(DEC_arr)
    Lat_rad = np.deg2rad(Lat_arr)
    Lon_rad = np.deg2rad(Lon_arr)

    # Calculate LST
    LST = np.array([lst.lst(t, lon, time_zone) for t, lon in zip(obs_time_arr, Lon_arr)])

    # Calculate hour angle
    HA = hour_angle.hourangle(LST, RA_arr)
    HA_rad = np.deg2rad(HA * 15.0)
    LSTrad = np.deg2rad(LST * 15.0)

    # Calculate altitude
    sin_alt = np.sin(DEC_rad) * np.sin(Lat_rad) + np.cos(DEC_rad) * np.cos(Lat_rad) * np.cos(HA_rad)
    alt = np.arcsin(sin_alt)

    # Calculate azimuth
    tolerance = 1e-6
    cos_az = (np.sin(DEC_rad) - np.sin(alt) * np.sin(Lat_rad)) / (np.cos(alt) * np.cos(Lat_rad))
    cos_az = np.clip(cos_az, -1.0, 1.0)
    az = np.arccos(cos_az)

    az = np.where(np.sin(HA_rad) > 0, 2 * np.pi - az, az)

    # Convert to degrees
    alt = np.rad2deg(alt)
    az = np.rad2deg(az)

    # If inputs were scalar, return scalar outputs
    if np.isscalar(RA) and np.isscalar(DEC) and np.isscalar(Lat) and np.isscalar(Lon) and np.isscalar(obs_time):
        return alt[0], az[0]
    else:
        return alt, az

def max_alt(DEC, Lat):
    """
    Calculate the maximum altitude of a target.
    
    Parameters
    ----------
    DEC : float
        The declination of the target in degrees.
    Lat : float
        The latitude of the observer in degrees.    
    Returns
    -------
    float
        The maximum altitude of the target in degrees.
        
    """
    if not isinstance(DEC, (int, float)):
        raise TypeError("Expected a float or int for 'DEC'.")
    if not isinstance(Lat, (int, float)):
        raise TypeError("Expected a float or int for 'Lat'.")
    # Convert inputs to arrays
    DEC_arr = np.atleast_1d(DEC)
    Lat_arr = np.atleast_1d(Lat)

    # Convert to radians
    DEC_rad = np.deg2rad(DEC_arr)
    Lat_rad = np.deg2rad(Lat_arr)

    # Calculate hour angle (0 when target transits)
    HA_rad = 0

    # Calculate altitude
    sin_alt = np.sin(DEC_rad) * np.sin(Lat_rad) + np.cos(DEC_rad) * np.cos(Lat_rad) * np.cos(HA_rad)
    alt = np.arcsin(sin_alt)

    # Convert to degrees
    alt = np.rad2deg(alt)

    # If inputs were scalar, return scalar output
    if np.isscalar(DEC) and np.isscalar(Lat):
        return alt[0]
    else:
        return alt

