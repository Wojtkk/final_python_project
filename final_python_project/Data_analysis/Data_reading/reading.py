import pandas as pd
from pathlib import Path

LINE_STOPS_FILENAME = 'stops_of_buses.csv'
BUS_STOPS_FILENAME = 'bus_stops.csv'
CURR_POSITIONS_OF_BUSES_FILENAME = 'curr_position_of_buses.csv'
TIME_TABLES_FILENAME = 'time_tables.csv'

CSV = 'csv'

DATA_COLLECTING_MODULE = Path('Data_saving')

# to be for_early_data
PATH_TO_DATA_DIR_EARLY = DATA_COLLECTING_MODULE / 'for_data_early' 
PATH_TO_DATA_DIR_EARLY = DATA_COLLECTING_MODULE / 'for_data' # to remove !!!

# to be for_late_data
PATH_TO_DATA_DIR_LATE = DATA_COLLECTING_MODULE / 'for_data_late' 
PATH_TO_DATA_DIR_LATE = DATA_COLLECTING_MODULE / 'for_data' # to remove !!!


# so we can make function which reads and modify
from Data_reading.modifying_dfs import modify_line_stops_df
from Data_reading.modifying_dfs import modify_bus_stops_df
from Data_reading.modifying_dfs import modify_curr_positions_of_buses_df
from Data_reading.modifying_dfs import modify_time_tables_df

def give_df_from_csv_files(path_to_file):
    df = pd.read_csv(path_to_file)
    return df

def give_dfs_directory(late_hours):
    project_directory = Path(__file__).resolve().parent.parent
    if late_hours:
        target_directory = project_directory / PATH_TO_DATA_DIR_LATE
    else:
        target_directory = project_directory / PATH_TO_DATA_DIR_EARLY
    
    return target_directory

def give_selected_df(filename, late_hours):
    path_to_dir = give_dfs_directory(late_hours)
    dataframes = []
    
    path = Path(path_to_dir)
    for file in path.iterdir():
        if filename == file.name:
            df = give_df_from_csv_files(file)
            return df
    
    return None

def give_modified_df(filename, funct_to_modify, late_hours):
    df = give_selected_df(filename, late_hours)
    funct_to_modify(df, late_hours)
    return df

def give_modified_lines_stops_df(late_hours = False):
    return give_modified_df(LINE_STOPS_FILENAME, 
                            modify_line_stops_df, 
                            late_hours)
    
def give_modified_bus_stops_df(late_hours = False):
    return give_modified_df(BUS_STOPS_FILENAME, 
                            modify_bus_stops_df,
                            late_hours)

def give_modified_curr_positions_df(late_hours = False):
    return give_modified_df(CURR_POSITIONS_OF_BUSES_FILENAME, 
                            modify_curr_positions_of_buses_df,
                            late_hours)
    

def give_modified_time_tables_df(late_hours = False):
    return give_modified_df(TIME_TABLES_FILENAME, 
                            modify_time_tables_df,
                            late_hours)            
                




