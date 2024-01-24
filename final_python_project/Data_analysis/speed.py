from positions import calculate_speed_in_km_per_h
import time_functions


def buses_too_fast_during_time_interval(positions_start, positions_end):
    merged_bus_data = merge_by_vehicle_id(positions_start, positions_end)
    
    select_bueses_with_to_high_speed(merged_bus_data, SPEED_LIMIT)
    
    return merged_bus_data

def buses_too_fast_through_all_time_intervals(buses_positions_in_all_moments):
    num_of_intervals = len(buses_positions_in_all_moments) - 1
    
    result_array_of_dataframes = []
    for i in range(num_of_intervals):
        pos_start = buses_positions_in_all_moments[i]
        pos_end = buses_positions_in_all_moments[i + 1]
        
        too_fast = buses_too_fast_during_time_interval(pos_start, pos_end)
        
        result_array_of_dataframes.appedn(too_fast)
        
    return result_array_of_dataframes

def calculate_percentage_of_too_fast_buses_on_each_road():
    
        
    