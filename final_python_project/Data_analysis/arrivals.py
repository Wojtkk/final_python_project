import pandas as pd
import Data_reading.modifying_dfs as aliases

def divide_on_dfs_by_given_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def group_df_by_vehicles(df_with_positions):
    return divide_on_dfs_by_given_column(df_positions, aliases.VEHICLE_NUMBER_STR)

def group_by_line(lines_stops_df):
    return divide_on_dfs_by_given_column(df_positions, aliases.LINE_STR)


def df_line_stops_with_coords(line_stops_df, bus_stops_df):
    joined_df = pd.merge(line_stops_df, bus_stops_df, on = aliases.BUS_STOP_ID_STR)
    return joined_df

def calc_arrival_times():
    # for tomorrow 

def give_df_with_arrivals(df_with_positions, lines_stops_df, bus_stops_df):
    dfs_positions_of_vehicle = group_df_by_vehicles(df_with_positions)
    
    df_of_line_stops = df_line_stops_with_coords(lines_stops_df, bus_stops_df)
    
    dict_of_bus_stops_for_lines = group_by_line(lines_stops_df)
    
    arrival_dfs = []
    for single_veh_positions in dfs_with_positions_of_vehicle.keys():
        line = single_veh_positions[aliases.LINE_STR]
        single_line_stops = dict_of_all_bus_stops_for_lines[line]
        
        arrival_dfs += calc_arrival_times(single_line_stops, single_veh_positions)
        
    concatenated_df = pd.concat(arrival_dfs, ignore_index=True)
    return concatenated_df
        
        
    
    
    