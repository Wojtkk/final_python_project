import pandas as pd 

STOPS_ON_ROUTES_FILENAME = 'stops_of_buses.csv'
BUS_STOPS_FILENAME = 'bus_stops.csv'
CURR_POSITIONS_OF_BUSES_FILENAME = 'curr_position_of_buses.csv'
TIME_TABLES_FILENAME = 'time_tables.csv'

from positions import calculate_speed_in_km_per_h
from positions import calculate_middle_point

from Data_reading.modifying_dfs import *
from Data_reading.reading_data import give_modified_dataframes_from_dir

SPEED_STR = 'speed'
SPEED_LIMIT = 50
MAX_MEASURED_SPEED = 100 

def sort_by_time(dataframe):
    df_sorted = dataframe.sort_values(by = TIME_STR)
    return df_sorted

def divide_on_dataframes_by_given_column_name(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def divide_on_dataframes_by_line(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, LINE_STR)

def divide_on_dataframes_by_vehicle_num(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, VEHICLE_NUMBER_STR)


def give_dataframe_of_coords_with_line_and_speed(dataframe):
    dataframes_for_vehicles = divide_on_dataframes_by_vehicle_num(dataframe)
    
    rows_to_df_of_coords = []
    for vehicle_num, df_with_positions_of_vehicle in dataframes_for_vehicles.items():
        df_with_positions_of_vehicle = sort_by_time(df_with_positions_of_vehicle)
        
        num_of_rows = df_with_positions_of_vehicle.shape[0]
        for i in range(0, num_of_rows - 1):
            curr_row = df_with_positions_of_vehicle.iloc[i]
            next_row = df_with_positions_of_vehicle.iloc[i + 1]
            
            line = curr_row[LINE_STR]
            time_start = curr_row[TIME_STR]
            time_finish = next_row[TIME_STR] 
            position_start = (curr_row[LON_STR], curr_row[LAT_STR])
            position_finish = (next_row[LON_STR], next_row[LAT_STR])
            
            mid_position = calculate_middle_point(position_start, position_finish)
            
            speed = calculate_speed_in_km_per_h(position_start, position_finish, time_start, time_finish)
            if speed == None:
                continue
            
            new_row = [line, mid_position[0], mid_position[1], speed]
            
            rows_to_df_of_coords.append(new_row)
            
    columns_names = [LINE_STR, LON_STR, LAT_STR, SPEED_STR]
    coords_dataframe = pd.DataFrame(rows_to_df_of_coords, columns = columns_names)
    
    return coords_dataframe
            
def give_list_of_overspeed_coords(dataframe_with_speed_col):
    overspeed = f"{SPEED_LIMIT} < {SPEED_STR} < {MAX_MEASURED_SPEED}"
    return dataframe_with_speed_col.query(overspeed)

def give_list_of_allowed_speed_coords(dataframe_with_speed_col):
    allowed_speed = f"{SPEED_STR} < {SPEED_LIMIT}"
    return dataframe_with_speed_col.query(allowed_speed)


def give_lines_with_most_frequent_overspeed(dataframe, minimal_num_of_vehicles = 3):
    coords_df = give_dataframe_of_coords_with_line_and_speed(dataframe)
    
    coords_for_line_dataframes = divide_on_dataframes_by_line(coords_df)
    
    result_for_each_line = []
    for line, df in coords_for_line_dataframes.items():
        overspeed_coords_num = len(give_list_of_overspeed_coords(df))
        allowed_speed_coords = len(give_list_of_allowed_speed_coords(df))
        
        total_coords = overspeed_coords_num + allowed_speed_coords
        if total_coords < minimal_num_of_vehicles:
            continue
        
        overspeed_percentage = overspeed_coords_num / total_coords
        result_for_each_line.append((line, overspeed_percentage))
    
    result_for_each_line = sorted(result_for_each_line, key = lambda x: x[1])
    length = len(result_for_each_line)
    
    return result_for_each_line

if __name__ == '__main__':
    dataframes = give_modified_dataframes_from_dir()

    dataframes = dict(dataframes)
    positions_df = dataframes[CURR_POSITIONS_OF_BUSES_FILENAME]
    
    with_speed_df = give_dataframe_of_coords_with_line_and_speed(positions_df)
    allowed = give_list_of_allowed_speed_coords(with_speed_df)
    over = give_list_of_overspeed_coords(with_speed_df)
    
    from visualization import plot_points_on_map
    
    points_and_values = [(r[LAT_STR], r[LON_STR], 0) for index, r in allowed.iterrows()]
    points_and_values += [(r[LAT_STR], r[LON_STR], 1) for index, r in over.iterrows()]
    plot_points_on_map(points_and_values, 15, 12)
    


        
    
    
    