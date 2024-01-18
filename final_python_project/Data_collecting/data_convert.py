import pandas as pd 
import data_download as dd

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
    
    array_of_rows_with_buses_position = []
    for bus_position in buses_position_data:
        single_bus_position_info = bus_position.values()