import pandas as pd
from pathlib import Path

LINE_STOPS_FILENAME = 'stops_of_buses.csv'
BUS_STOPS_FILENAME = 'bus_stops.csv'
CURR_POSITIONS_OF_BUSES_FILENAME = 'curr_position_of_buses.csv'
TIME_TABLES_FILENAME = 'time_tables.csv'

from Data_reading.modifying_dfs import modify_stops_on_routes_df
from Data_reading.modifying_dfs import modify_bus_stops_df
from Data_reading.modifying_dfs import modify_curr_positions_of_buses_df
from Data_reading.modifying_dfs import modify_time_tables_df

CSV = 'csv'

DATA_COLLECTING_MODULE = Path('Data_saving')
PATH_TO_DATA_DIR = DATA_COLLECTING_MODULE / 'for_data'

def give_df_from_csv_files(path_to_file):
    df = pd.read_csv(path_to_file)
    return df

def give_dfs_directory():
    project_directory = Path(__file__).resolve().parent.parent
    target_directory = project_directory / PATH_TO_DATA_DIR
    
    return target_directory

def give_df_with_filename(filename):
    path_to_dir = give_dfs_directory()
    dataframes = []
    
    path = Path(path_to_dir)
    for file in path.iterdir():
        if filename == file.name:
            df = give_df_from_csv_files(file)
            return df
    
    return None

def give_modified_df(filename, funct_to_modify):
    df = give_df_with_filename(filename)
    funct_to_modify(df)
    return df

def give_modified_lines_stops_df():
    return give_modified_df(LINE_STOPS_FILENAME, modify_stops_on_routes_df)

def give_modified_bus_stops_df():
    return give_modified_df(BUS_STOPS_FILENAME, modify_bus_stops_df)

def give_modified_curr_positions_df():
    return give_modified_df(CURR_POSITIONS_OF_BUSES_FILENAME, 
                            modify_curr_positions_of_buses_df)

def give_modified_time_tables_df():
    return give_modified_df(TIME_TABLES_FILENAME, modify_time_tables_df)            
                
if __name__ == '__main__':
    df = give_modified_time_tables_df()
    print(df)




