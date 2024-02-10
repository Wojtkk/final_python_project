import pandas as pd
from pathlib import Path

STOPS_ON_ROUTES_FILENAME = 'stops_of_buses.csv'
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

def give_dfs_with_filenames():
    path_to_dir = give_dfs_directory()
    dataframes = []
    
    path = Path(path_to_dir)
    for file in path.iterdir():
        if file.suffix == f'.{CSV}':
            df = give_df_from_csv_files(file)
            dataframes.append((file.name, df))
    
    return dataframes

def give_modified_dataframes_from_dir():
    dfs_and_filenames = give_dfs_with_filenames()
    
    new_dfs_and_filenames = []
    for filename, df in dfs_and_filenames:
        mod_func = [(STOPS_ON_ROUTES_FILENAME, modify_stops_on_routes_df),
                    (BUS_STOPS_FILENAME, modify_bus_stops_df),
                    (CURR_POSITIONS_OF_BUSES_FILENAME, modify_curr_positions_of_buses_df),
                    (TIME_TABLES_FILENAME, modify_time_tables_df)]
        
        for name, function in mod_func:
            if (filename == name):
                function(df)
                new_dfs_and_filenames.append((name, df))
                break 
            
    return new_dfs_and_filenames
                
                
if __name__ == '__main__':
    dfs = give_modified_dataframes_from_dir()
    for filename, df in dfs:
        print(f"DataFrame from file: {filename}")
        print(df.head())




