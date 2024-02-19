""" 
Functions to handle distances, time and speed and related things when
we have coordinates as our data.
"""

import geopy.distance
from datetime import datetime

SECONDS_IN_HOUR = 3600

def calculate_time_in_sec_between_dates(time_start, time_end):
    time_difference = time_end - time_start
    time_difference_seconds = time_difference.total_seconds()

    return time_difference_seconds

def distance_between_two_points_in_km(coords_1, coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).km

def calculate_speed_in_km_per_h(coords_start, coords_end, 
                                time_start, time_end):
    dist = distance_between_two_points_in_km(coords_start, coords_end)
    delta_time_sec = calculate_time_in_sec_between_dates(time_start, time_end)
    
    delta_time_hours = delta_time_sec / SECONDS_IN_HOUR
    if delta_time_hours == 0:
        return None
    
    return dist / delta_time_hours

def calculate_middle_point(coords_1, coords_2):
    lat1, lon1 = coords_1
    lat2, lon2 = coords_2

    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    
    return mid_lat, mid_lon
    

        
    