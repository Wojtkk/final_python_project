import pandas as pd 
import data_download as dd
import json

LINE = 'line'
NUM_OF_STOP = 'nr_przystanku'
NUM_OF_STOP_GROUP = 'nr_zespolu'

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

def create_dataframe_with_time_tables(stops_of_buses):
    for i, row in stops_of_buses.iterrows():
        line = row[LINE]
        num_of_stop = row[NUM_OF_STOP]
        num_of_stop_group = row[NUM_OF_STOP_GROUP]
        
        time_table = dd.get_bus_time_table(line = line, 
                                        bus_stop_nr = num_of_stop, 
                                        bus_stop_id = num_of_stop_group)
        
        print(time_table)
        break
    
        
stops_of_buses = create_dataframe_with_stops_of_buses()
# print(stops_of_buses)
create_dataframe_with_time_tables(stops_of_buses['result'])