import pandas as pd 
from time import sleep

import data_download as dd
import json


LINE = 'line'
NUM_OF_STOP = 'nr_przystanku'
NUM_OF_STOP_GROUP = 'nr_zespolu'

POSITIONS_UPDATE_TIME_SEC = 15
INTERVAL_IN_SECONDS = 16

def create_dataframe_with_stops_of_buses():
    bus_time_table = dd.get_public_transport_routes()
    
    lines_nums = bus_time_table.keys()
    
    bus_stops_to_dataframe = []
    for line in lines_nums:
        routes_of_line = bus_time_table[line].values()
        for route in routes_of_line:
            bus_stops_on_route = route.values()
            for bus_stop in bus_stops_on_route:
                bus_stop[LINE] = line
                bus_stops_to_dataframe.append(bus_stop)
    
    dfs = [pd.json_normalize(bus_stop) for bus_stop in bus_stops_to_dataframe]
    
    df = pd.concat(dfs, ignore_index = True)
    return df
            
def create_dataframe_with_bus_stops():
    bus_stops_data = dd.get_bus_stop_informations()
    
    array_of_rows_with_bus_stop_data = []
    for bus_stop in bus_stops_data:
        single_bus_stop_info = [x['value'] for x in bus_stop['values']]
        array_of_rows_with_bus_stop_data.append(single_bus_stop_info)
        
    first_bus_stop = 0
    single_bus_stop_data = bus_stops_data[first_bus_stop]['values']
    column_names = [x['key'] for x in single_bus_stop_data]
    
    df = pd.DataFrame(array_of_rows_with_bus_stop_data, columns = column_names)
    return df

def create_dataframe_with_curr_position_of_buses():
    buses_position_data = dd.get_curr_position_of_buses()
    
    dfs = [pd.json_normalize(bus_position) for bus_position in buses_position_data]

    df = pd.concat(dfs, ignore_index=True)

    return df

def create_list_of_dataframes_with_curr_position_of_buses(interval_in_seconds):
    iterations = interval_in_seconds // POSITIONS_UPDATE_TIME_SEC + 1
    dataframes = []
    for i in range(iterations):
        df = create_dataframe_with_curr_position_of_buses()
        dataframes.append(df)
        sleep(POSITIONS_UPDATE_TIME_SEC)
        
    concatenated_df = pd.concat(dataframes, axis = 0, ignore_index = True)
    return concatenated_df


def create_dataframe_with_time_tables(stops_of_buses):
    data_for_dataframe_with_time_tables = []
    column_names_for_dataframe_with_time_tables = [LINE]
    colums_names_not_filled = True

    for i, row in stops_of_buses.iterrows():
        print(i, len(data_for_dataframe_with_time_tables))
        if  i >= 3:  # to delete !!
            break
        line = row[LINE]
        num_of_stop = row[NUM_OF_STOP]
        num_of_stop_group = row[NUM_OF_STOP_GROUP]
        
        time_table = dd.get_bus_time_table(line = line, 
                                        bus_stop_nr = num_of_stop, 
                                        bus_stop_id = num_of_stop_group)
        
        #dd.print_readable(time_table)
        for one_arrival_data in time_table['result']:
            row_values = [line]
            for list_of_params in one_arrival_data.values():
                for single_param in list_of_params:
                    row_values.append(single_param['value'])
                    
                data_for_dataframe_with_time_tables.append(row_values)
                
                if colums_names_not_filled:
                    for single_param in list_of_params:
                        column_names_for_dataframe_with_time_tables.append(single_param['key'])
                        
                    colums_names_not_filled = False
        
    dataframe = pd.DataFrame(data_for_dataframe_with_time_tables, columns = column_names_for_dataframe_with_time_tables)
    return dataframe
         
def give_all_dataframes_and_their_titles():
    dataframes_to_save = []
    
    df_stops_of_buses = create_dataframe_with_stops_of_buses()
    dataframes_to_save.append(("stops_of_buses.csv", df_stops_of_buses))
    
    df_bus_stops = create_dataframe_with_bus_stops()
    dataframes_to_save.append(("bus_stops.csv", df_bus_stops))
    
    df_curr_position_of_buses = create_list_of_dataframes_with_curr_position_of_buses(INTERVAL_IN_SECONDS)
    dataframes_to_save.append(("curr_position_of_buses.csv", df_curr_position_of_buses))
    
    df_time_tables = create_dataframe_with_time_tables(df_stops_of_buses)
    dataframes_to_save.append(("time_tables.csv", df_time_tables)) # we need it, just for case of test
    
    return dataframes_to_save    
    
           
# stops_of_buses = create_dataframe_with_stops_of_buses()
#df = create_dataframe_with_time_tables(stops_of_buses)
# print(df.size)
        