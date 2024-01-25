import geopy.distance

def get_distance_between_two_points_in_km(coords_1, coords_2):
    geopy.distance.geodesic(coords_1, coords_2).km
    
def calculate_speed_in_km_per_h(coordinates_start, coordinates_end, time_start, time_end):
    distance = get_distance_between_two_points_in_km(coordinates_start, coordinates_end)
    delta_time_seconds = calculate_time_in_sec_between_to_dates_with_hours(time_start, time_end)
    
    delta_time_hours = delta_time_seconds / SECONDS_IN_HOUR
    return distance / delta_time_hours

def calculate_middle_point(coords_1, coords_2):
    half_way = 0.5
    mid_point = geopy.distance.geodesic(coords_1, coords_2).interpolate(half_way)
    return mid_point.latitude, mid_point.longitude
    

        
    