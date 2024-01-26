import pandas as pd 

from reading_data import give_dataframes_from_right_folder
from positions import calculate_speed_in_km_per_h
from positions import calculate_middle_point

POSITIONS_CSV_FILENAME = 'curr_position_of_buses.csv'

LINE_STR = 'line'
LINES_STR = 'Lines'
VEHICLE_NUMBER_STR = 'VehicleNumber'
SPEED_STR = 'speed'
DATE_STR = 'date'
TIME_STR = 'Time'
LON_STR = 'Lon'
LAT_STR = 'Lat'

SPEED_LIMIT = 50
MAX_MEASURED_SPEED = 100 

def sort_by_time(dataframe, time_column_name):
    dataframe[time_column_name] = pd.to_datetime(dataframe[time_column_name])
    df_sorted = dataframe.sort_values(by=time_column_name)
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
        df_with_positions_of_vehicle = sort_by_time(df_with_positions_of_vehicle, TIME_STR)
        
        num_of_rows = df_with_positions_of_vehicle.shape[0]
        for i in range(0, num_of_rows - 1):
            curr_row = df_with_positions_of_vehicle.iloc[i]
            next_row = df_with_positions_of_vehicle.iloc[i + 1]
            
            line = curr_row[LINES_STR]
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


def give_lines_with_most_frequent_overspeed(dataframe, how_many, minimal_num_of_vehicles = 3):
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
    
    return result_for_each_line[:max(length, how_many)]


dataframes = give_dataframes_from_right_folder()

positions_df = dataframes[POSITIONS_CSV_FILENAME]

fast_lines = give_lines_with_most_frequent_overspeed(positions_df, 6)
fast_lines = sorted(fast_lines, key = lambda x: x[1])

for elem in fast_lines:
    print(elem)

        
    
    
    