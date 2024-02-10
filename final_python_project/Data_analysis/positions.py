import geopy.distance
from datetime import datetime


SECONDS_IN_HOUR = 3600

def calculate_time_in_sec_between_to_dates_with_hours(time_start, time_end, date_format="%Y-%m-%d %H:%M:%S"):
    time_difference = time_end - time_start
    time_difference_seconds = time_difference.total_seconds()

    return time_difference_seconds

def get_distance_between_two_points_in_km(coords_1, coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).km
    
def calculate_speed_in_km_per_h(coordinates_start, coordinates_end, time_start, time_end):
    distance = get_distance_between_two_points_in_km(coordinates_start, coordinates_end)
    delta_time_seconds = calculate_time_in_sec_between_to_dates_with_hours(time_start, time_end)
    
    delta_time_hours = delta_time_seconds / SECONDS_IN_HOUR
    if delta_time_hours == 0:
        return None
    
    return distance / delta_time_hours

def calculate_middle_point(coords_1, coords_2):
    lat1, lon1 = coords_1
    lat2, lon2 = coords_2

    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    
    return mid_lat, mid_lon
    

        
    