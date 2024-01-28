import pandas as pd
from pathlib import Path

from Data_collecting.data_convert import STOPS_ON_ROUTES_FILENAME
from Data_collecting.data_convert import BUS_STOPS_FILENAME
from Data_collecting.data_convert import CURR_POSITIONS_OF_BUSES_FILENAME
from Data_collecting.data_convert import TIME_TABLES_FILENAME

LON_STR = 'Lon'
LAT_STR = 'Lat'

CSV = 'csv'
DATA_COLLECTING_MODULE = Path('Data_collecting')
PATH_TO_DATA_DIR = DATA_COLLECTING_MODULE / 'for_data'

STOP_ID_STR = 'stop_id'
STREET_ID_STR = 'street_id'

LINE_STR = 'line'
DIRECTION_STR = 'direction'
ROUTE_STR = 'route'

VEHICLE_NUMBER_STR = 'vehicle_num'
TIME_STR = 'time'

DISTANCE_STR = 'distance'
LON_STR = 'lon'
LAT_STR = 'lat'

def give_df_from_csv_files(path_to_file):
    df = pd.read_csv(path_to_file)
    return df

def give_dfs_directory():
    project_directory = Path(__file__).resolve().parent
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


def modify_stops_on_routes_df(df):
    # original columns:
    # odleglosc, ulica_id, nr_zespolu, typ, nr_przystanku, line 
    df.drop(axis = 1,
            inplace = True,
            labels = {'nr_zespolu', 'typ'})
    
    df.rename(columns = {'odleglosc' : DISTANCE_STR,
                        'ulica_id' : STREET_ID_STR,
                        'nr_przystanku' : STOP_ID_STR},
                        inplace = True)
    
def modify_bus_stops_df(df):
    # original columns:
    # zespol, slupek, nazwa_zespolu, id_ulicy, szer_geo, dlug_geo, kierunek, obowiazuje_od
    df.drop(axis = 1,
            inplace = True,
            labels = {'zespol', 'nazwa_zespolu', 'obowiazuje_od', 'slupek'})
    
    df.rename(columns = {'id_ulicy' : STREET_ID_STR,
                        'szer_geo' : LAT_STR,
                        'dlug_geo' : LON_STR,
                        'kierunek' : DIRECTION_STR},
                        inplace = True)

def modify_curr_positions_of_buses_df(df):
    # original columns:
    # Lines, Lon, VehicleNumber, Time, Lat, Brigade
    df.drop(axis = 1,
            inplace = True,
            labels = {'Brigade'})
    
    df.rename(columns = {'Lines' : LINE_STR,
                        'Lon' : LON_STR,
                        'VehicleNumber' : VEHICLE_NUMBER_STR,
                        'Time' : TIME_STR,
                        'Lat' : LAT_STR},
                        inplace = True)
    
    df[TIME_STR] = pd.to_datetime(df[TIME_STR])
    
def modify_time_tables_df(df):
    # original columns:
    # line, symbol_2, symbol_1, brygada, kierunek, trasa, czas
    df.drop(axis = 1,
            inplace = True,
            labels = {'symbol_2', 'symbol_1', 'brygada'})
    
    df.rename(columns = {'kierunek' : DIRECTION_STR,
                         'trasa' : DIRECTION_STR,
                         'czas' : TIME_STR},
                        inplace = True)
    
    df[TIME_STR] = pd.to_datetime(dataframe[time_column_name])


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
                print(df)
                
                new_dfs_and_filenames.append((name, df))
                break 
            
    return new_dfs_and_filenames
                
                
if __name__ == '__main__':
    dfs = give_modified_dataframes_from_dir()
    for filename, df in dfs:
        print(f"DataFrame from file: {filename}")
        print(df.head())

        # Assuming TIME_STR is a column name
        if TIME_STR in df.columns:
            first_time_value = df.loc[0, TIME_STR]
            print(f"Value in the first row of {TIME_STR} column: {first_time_value}")
        else:
            print(f"{TIME_STR} column not found in DataFrame.")
    



