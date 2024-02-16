import pandas as pd 

from Helpers.positions import calculate_speed_in_km_per_h
from Helpers.positions import calculate_middle_point

from Data_reading.modifying_dfs import Aliases as als

from Data_reading.reading import give_modified_lines_stops_df
from Data_reading.reading import give_modified_bus_stops_df
from Data_reading.reading import give_modified_curr_positions_df
from Data_reading.reading import give_modified_time_tables_df

SPEED_STR = 'speed'
SPEED_LIMIT = 50
MAX_MEASURED_SPEED = 100 

def sort_by_time(dataframe):
    df_sorted = dataframe.sort_values(by = als.TIME.value)
    return df_sorted

def divide_on_dataframes_by_given_column_name(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def divide_on_dataframes_by_line(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, als.LINE.value)

def divide_on_dataframes_by_vehicle_num(dataframe):
    return divide_on_dataframes_by_given_column_name(dataframe, als.VEHICLE_NUMBER.value)


def give_dataframe_of_coords_with_line_and_speed(dataframe):
    dataframes_for_vehicles = divide_on_dataframes_by_vehicle_num(dataframe)
    
    rows_to_df_of_coords = []
    for vehicle_num, df_with_positions_of_vehicle in dataframes_for_vehicles.items():
        df_with_positions_of_vehicle = sort_by_time(df_with_positions_of_vehicle)
        
        num_of_rows = df_with_positions_of_vehicle.shape[0]
        for i in range(0, num_of_rows - 1):
            curr_row = df_with_positions_of_vehicle.iloc[i]
            next_row = df_with_positions_of_vehicle.iloc[i + 1]
            
            line = curr_row[als.LINE.value]
            time_start = curr_row[als.TIME.value]
            time_finish = next_row[als.TIME.value] 
            position_start = (curr_row[als.LAT.value], curr_row[als.LON.value])
            position_finish = (next_row[als.LAT.value], next_row[als.LON.value])
            
            mid_position = calculate_middle_point(position_start, position_finish)
            
            speed = calculate_speed_in_km_per_h(position_start, position_finish, time_start, time_finish)
            if speed == None:
                continue
            
            new_row = [line, mid_position[0], mid_position[1], speed]
            
            rows_to_df_of_coords.append(new_row)
            
    columns_names = [als.LINE.value, als.LAT.value, als.LON.value, als.SPEED.value]
    coords_dataframe = pd.DataFrame(rows_to_df_of_coords, columns = columns_names)
    
    return coords_dataframe
            
def give_list_of_overspeed_coords(dataframe_with_speed_col):
    overspeed = f"{SPEED_LIMIT} < {SPEED_STR} < {MAX_MEASURED_SPEED}"
    return dataframe_with_speed_col.query(overspeed)

def give_list_of_allowed_speed_coords(dataframe_with_speed_col):
    allowed_speed = f"{SPEED_STR} < {SPEED_LIMIT}"
    return dataframe_with_speed_col.query(allowed_speed)


def give_lines_with_most_frequent_overspeed(dataframe, minimal_num_of_vehicles = 3, how_many = 3):
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
    
    return result_for_each_line[length - how_many: ]

def give_data_with_allowed_and_not_allowed_speed(positions_df):
    with_speed_df = give_dataframe_of_coords_with_line_and_speed(positions_df)
    
    allowed = give_list_of_allowed_speed_coords(with_speed_df)
    over = give_list_of_overspeed_coords(with_speed_df)
    
    points_and_values = [(r[als.LAT.value], r[als.LON.value], 0.5) for index, r in allowed.iterrows()]
    points_and_values += [(r[als.LAT.value], r[als.LON.value], 1) for index, r in over.iterrows()]
    
    return points_and_values
    

if __name__ == '__main__':
    positions_df = give_modified_curr_positions_df()
    
    data = give_data_with_allowed_and_not_allowed_speed(positions_df)
    
    from Helpers.visualization import plot_points_on_map
    
    plot_points_on_map(data, 15, 12)
    


        
    
    
    