""" 
In this module we have functions doing same thing for different data:

we download json with data and then convert it to DataFrame so we can
save it as csv file.
"""


import pandas as pd 
from time import sleep
import json

import data_download as dd

LINE_STR = 'line'
NUM_OF_STOP_STR = 'nr_przystanku'
NUM_OF_STOP_GROUP_STR = 'nr_zespolu'

VALUE_STR = 'value'
VALUES_STR = 'values'
KEY_STR = 'key'
RESULT_STR = 'result'

STOPS_ON_ROUTES_FILENAME = 'stops_of_buses.csv'
BUS_STOPS_FILENAME = 'bus_stops.csv'
CURR_POSITIONS_OF_BUSES_FILENAME = 'curr_position_of_buses.csv'
TIME_TABLES_FILENAME = 'time_tables.csv'

POSITIONS_UPDATE_TIME_SEC = 11
INTERVAL_IN_SECONDS = 16

def creat_df_lines_stops():
    bus_time_table = dd.get_public_transport_routes()
    
    bus_stops_to_df = []
    for line_num, routes_of_line in bus_time_table.items():
        for route in routes_of_line.values():
            bus_stops_on_route = route.values()
            
            for bus_stop in bus_stops_on_route:
                bus_stop[LINE_STR] = line_num
                bus_stops_to_df.append(bus_stop)    
            
    dfs = [pd.json_normalize(bus_stop) for bus_stop in bus_stops_to_df]
    df = pd.concat(dfs, ignore_index = True)
    return df
  
def creat_df_bus_stops():
    bus_stops_data = dd.get_bus_stop_informations()
    
    rows_with_bus_stop_data = []
    for bus_stop in bus_stops_data:
        bus_stop_info = [x[VALUE_STR] for x in bus_stop[VALUES_STR]]
        rows_with_bus_stop_data.append(bus_stop_info)
        
    first_bus_stop = 0
    single_bus_stop_data = bus_stops_data[first_bus_stop][VALUES_STR]
    column_names = [x[KEY_STR] for x in single_bus_stop_data]
    
    df = pd.DataFrame(rows_with_bus_stop_data, columns = column_names)
    return df


def creat_df_curr_positions_of_buses():
    buses_position_data = dd.get_curr_position_of_buses()
    
    dfs = []
    for bus_position in buses_position_data:
        try:
            df = pd.json_normalize(bus_position)
            dfs.append(df)
        except:
            print(buses_position_data)
            break
        
    result_df = pd.concat(dfs, ignore_index=True)

    return result_df

def creat_list_of_dfs_curr_positions_of_buses(interval_in_sec):
    iterations = interval_in_sec // POSITIONS_UPDATE_TIME_SEC + 1
    dfs = []
    for i in range(iterations):
        df = creat_df_curr_positions_of_buses()
        dfs.append(df)
        sleep(POSITIONS_UPDATE_TIME_SEC)
        
    concatenated_df = pd.concat(dfs, axis = 0, ignore_index = True)
    return concatenated_df

def give_all_time_tables(df_stops_on_routes):
    result = []
    for i, row in df_stops_on_routes.iterrows():
        print(i)
        if i >= 300:
            break

        line = row[LINE_STR]
        stop_num = row[NUM_OF_STOP_STR]
        group_num = row[NUM_OF_STOP_GROUP_STR]
        
        time_table = dd.get_bus_time_table(line = line, 
                                        bus_stop_nr = stop_num, 
                                        bus_stop_id = group_num)
        
        arrive_data = (line, stop_num, group_num, time_table[RESULT_STR])
        result.append(arrive_data)
        
    return result

def creat_df_time_tables(df_stops_on_routes):
    data_for_df_time_tables = []
    col_names_for_df_time_tables = [LINE_STR, NUM_OF_STOP_STR, 
                                    NUM_OF_STOP_GROUP_STR]
    colums_names_not_filled = True

    time_tables_arr = give_all_time_tables(df_stops_on_routes)
    
    for line_num, bus_stop_num, group_num, time_table in time_tables_arr:
        
        for single_arrive_data in time_table:
            row_values = [line_num, bus_stop_num, group_num]
            for list_of_params in single_arrive_data.values():
                for single_param in list_of_params:
                    row_values.append(single_param[VALUE_STR])

                data_for_df_time_tables.append(row_values)

                if colums_names_not_filled:
                    for single_param in list_of_params:
                        col_names_for_df_time_tables.append(single_param['key'])

                    colums_names_not_filled = False
        
    dataframe = pd.DataFrame(data_for_df_time_tables, 
                             columns = col_names_for_df_time_tables)
    return dataframe
         
def give_all_dataframes_and_their_titles():
    dataframes_to_save = []
    
    df_stops_on_routes = creat_df_lines_stops()
    dataframes_to_save.append((STOPS_ON_ROUTES_FILENAME, df_stops_on_routes))
    
    df_bus_stops = creat_df_bus_stops()
    dataframes_to_save.append((BUS_STOPS_FILENAME, df_bus_stops))
    
    df_curr_positions_of_buses = creat_list_of_dfs_curr_positions_of_buses(INTERVAL_IN_SECONDS)
    dataframes_to_save.append((CURR_POSITIONS_OF_BUSES_FILENAME, df_curr_positions_of_buses))
    
    df_time_tables = creat_df_time_tables(df_stops_on_routes)
    dataframes_to_save.append((TIME_TABLES_FILENAME, df_time_tables))
    
    return dataframes_to_save    

if __name__ == '__main__':  
    df = creat_df_lines_stops()
    df1 = creat_df_time_tables(df)
    print(df1)