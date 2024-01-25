import pandas as pd 

from reading_data import give_dataframes_from_right_folder
from positions import calculate_speed_in_km_per_h
from positions import calculate_middle_point

POSITIONS_CSV_FILENAME = 'curr_position_of_buses.csv'
LINE = 'line'
VEHICLE_NUMBER = 'VehicleNumber'
SPEED_STR = 'speed'
DATE = 'date'
LON = 'Lon'
LAT = 'Lat'

SPEED_LIMIT = 50
MAX_MEASURED_SPEED = 100 # when speed is higher we assume data error

# chcielibysmy zrobic takie statystyki:
# 
# miec liste wszystkich zmierzonych odcinkow i dla nich stwierdzone czy predkosc przekroczona
# dobrze by bylo miec jeszcze linie autobusu do tych odcinkow
# wtedy bedziemy mogli zrobic bonus - najczesciej przekraczajace predkosc autobusy

def sort_by_time(dataframe, time_column_name):
    pass # to be written

def divide_on_dataframes_by_given_column_name(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def divide_on_dataframes_by_line(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, LINE)

def divide_on_dataframes_by_vehicle_num(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, VEHICLE_NUMBER)

def give_dataframe_of_coords(dataframe):
    dataframes_for_vehicles = divide_on_dataframes_by_vehicle_num(dataframe)
    
    rows_to_df_of_coords = []
    for vehicle_num, df_with_positions_of_vehicle in dataframes_for_vehicles.items():
        sort_by_time(df_with_positions_of_vehicle, DATE)
        
        num_of_rows = df_with_positions_of_vehicle.shape[0]
        for i in range(1, num_of_rows - 1):
            curr_row = df_with_positions_of_vehicle.loc(i)
            next_row = df_with_positions_of_vehicle.loc(i + 1)
            
            line = curr_row[LINE]
            
            time_start = curr_row[DATE]
            time_finish = next_row[DATE] 

            position_start = (curr_row[LON], curr_row[LAT])
            position_finish = (next_row[LON], next_row[LAT])
            
            mid_position = calculate_middle_point(position_start, position_finish)
            
            speed = calculate_speed_in_km_per_h(position_start, position_finish, time_start, time_finish)
            
            new_row = [line, mid_position[0], mid_position[1], speed]
            
            rows_to_df_of_coords.append(new_row)
            
    columns_names = [LINE, LON, LAT, SPEED_STR]
    coords_dataframe = pd.DataFrame(rows_to_df_of_coords, columns = columns_names)
    
    return coords_dataframe
            

def give_list_of_overspeed_coords(dataframe_with_speed_col):
    overspeed = f"{SPEED_LIMIT} < {SPEED_STR} < {MAX_MEASURED_SPEED}"
    return dataframe_with_speed_col.query(overspeed)

def give_list_of_allowed_speed_coords(dataframe_with_speed_col):
    allowed_speed = f"{SPEED_STR} < {SPEED_LIMIT}"
    return dataframe_with_speed_col.query(allowed_speed)

def give_lines_with_most_frequent_overspeed(dataframe, how_many):
    coords_df = give_dataframe_of_coords(dataframe)
    
    coords_for_line_dataframes = divide_on_dataframes_by_line(coords_df)
    
    result_for_each_line = []
    for line, df in coords_for_line_dataframes.items():
        overspeed_coords_num = len(give_list_of_overspeed_coords(df))
        allowed_speed_coords = len(give_list_of_allowed_speed_coords(df))
        
        result_for_each_line.append((line, overspeed_percentage))
    
    sorted(result_for_each_line, key = lambda x: x[1])
    length = len(result_for_each_line)
    
    return result_for_each_line[:max(length, how_many)]


dataframes = give_dataframes_from_right_folder()
print(dataframes.keys())

positions_df = dataframes[POSITIONS_CSV_FILENAME]

print(positions_df.head())

fast_lines = give_lines_with_most_frequent_overspeed(positions_df, 6)

print(fast_lines)

        
    
    
    