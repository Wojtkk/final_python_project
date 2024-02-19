""" 
What we do in this module is modifying each DataFrame we have.

We set our names of column, names are declared in 'Aliases' class.
Its convenient to have some structured naming of columns.

Also we erase out of time range data and data with coordinates 
out of Warsaw and near Warsaw area.

We also convert number of bus stops group and num of bus stop 
into single: 'BUS_STOP_ID'.

These things make further work much easier.
"""

import pandas as pd
from enum import Enum

EARLY_HOUR = 10

LATE_HOUR = 15

DEFAULT_DATE = '1900-01-01'
SPECIFIC_DATE = '18-02-2024'

MAX_NUM_OF_BUS_STOP = 1000

class Aliases(Enum):
    BUS_STOP_NUM = 'bus_stop_num'
    BUS_STOP_GROUP_NUM = 'bus_stop_group'
    BUS_STOP_ID = 'bus_stop_id'
    STREET_ID = 'street_id'
    PLACE = 'place'

    LINE = 'line'
    DIRECTION = 'direction'
    ROUTE = 'route'

    VEHICLE_NUMBER = 'vehicle_num'
    TIME = 'time'

    DISTANCE = 'distance'
    LON = 'lon'
    LAT = 'lat'
    
    DELAY = 'delay'
    EXPECTED_WAITING = 'expected_waiting'
    
    OVERSPEED_PERCENTAGE = 'overspeed_percentage'
    SPEED = 'speed'

def modify_dataframe(df, columns_to_drop, 
                     columns_renames_dict, late_hours = False):
    def drop_given_columns(df, columns_to_drop):
        df.drop(columns = columns_to_drop, axis = 1, inplace = True)
        
    def rename_given_columns(df, columns_renames_dict):
        df.rename(columns = columns_renames_dict, inplace = True)
    
    def remove_bus_depots_data(df):
        def bus_stop_is_bus_depot(bus_stop_group_num):
            return isinstance(bus_stop_group_num, str) and bus_stop_group_num[0] == 'R'
                
        if Aliases.BUS_STOP_GROUP_NUM.value in df.columns:
            depot_indices = df[df[Aliases.BUS_STOP_GROUP_NUM.value].apply(bus_stop_is_bus_depot)].index
            df = df.drop(depot_indices, inplace = True)
    
    def convert_time_format_if_possible(df):
        if Aliases.TIME.value in df.columns:
            df[Aliases.TIME.value] = pd.to_datetime(df[Aliases.TIME.value],
                                                    errors = 'coerce')
            df = df.dropna(subset=[Aliases.TIME.value])
    
    def delete_out_of_time_range(df, late_hours):
        if Aliases.TIME.value in df.columns:
            hour = LATE_HOUR if late_hours else EARLY_HOUR

            HOUR_STR = 'hour'
            DATE_STR = 'date'
            df[HOUR_STR] = df[Aliases.TIME.value].dt.hour
            df[DATE_STR] = df[Aliases.TIME.value].dt.date
    
            df.drop(df[~((df[HOUR_STR] == hour) 
                        & ((df[DATE_STR] ==  pd.to_datetime(SPECIFIC_DATE).date()) 
                        | (df[DATE_STR] == pd.to_datetime(DEFAULT_DATE).date())))].index, 
                        inplace=True)
            df.drop(columns=[HOUR_STR, DATE_STR], inplace=True)
    
    def add_bus_stop_id_column_if_possible(df):
        def mapping_on_bus_stops_id(num_of_group, num_of_bus_stop):
            return num_of_group * (MAX_NUM_OF_BUS_STOP + 1) + num_of_bus_stop
        
        cols = df.columns
        if Aliases.BUS_STOP_GROUP_NUM.value in cols and Aliases.BUS_STOP_GROUP_NUM.value in cols:
            df[Aliases.BUS_STOP_ID.value] = ""
            for i, row in df.iterrows():
                num_of_group = int(row[Aliases.BUS_STOP_GROUP_NUM.value])
                num_of_bus_stop = int(row[Aliases.BUS_STOP_NUM.value])
                
                bus_stop_id = mapping_on_bus_stops_id(num_of_group, num_of_bus_stop)
                
                df.at[i, Aliases.BUS_STOP_ID.value] = bus_stop_id
                
            unnecessary_cols_now = {Aliases.BUS_STOP_GROUP_NUM.value, 
                                    Aliases.BUS_STOP_NUM.value}
            drop_given_columns(df, unnecessary_cols_now)

    drop_given_columns(df, columns_to_drop)
    rename_given_columns(df, columns_renames_dict)
    remove_bus_depots_data(df)
    convert_time_format_if_possible(df)
    delete_out_of_time_range(df, late_hours)
    add_bus_stop_id_column_if_possible(df)

def modify_line_stops_df(df, late_hours = False):
    """ 
    original columns:
    odleglosc, ulica_id, nr_zespolu, typ, nr_przystanku, line 
    """
    to_drop = {'typ'}

    renames = {'odleglosc' : Aliases.DISTANCE.value,
              'ulica_id' : Aliases.STREET_ID.value,
              'nr_przystanku' : Aliases.BUS_STOP_NUM.value,
              'nr_zespolu' : Aliases.BUS_STOP_GROUP_NUM.value}  
       
    modify_dataframe(df, to_drop, renames, late_hours)       
    
def modify_bus_stops_df(df, late_hours = False):
    """
    original columns:
    zespol, slupek, nazwa_zespolu, id_ulicy, szer_geo, 
    dlug_geo, kierunek, obowiazuje_od
    """
    to_drop = {'obowiazuje_od'}
    
    renames = {'zespol' : Aliases.BUS_STOP_GROUP_NUM.value,
                'slupek' : Aliases.BUS_STOP_NUM.value,
                'id_ulicy' : Aliases.STREET_ID.value,
                'szer_geo' : Aliases.LAT.value,
                'dlug_geo' : Aliases.LON.value,
                'kierunek' : Aliases.DIRECTION.value,
                'nazwa_zespolu' : Aliases.PLACE.value}
    
    modify_dataframe(df, to_drop, renames, late_hours)  

def modify_curr_positions_of_buses_df(df, late_hours = False):
    """
    original columns:
    Lines, Lon, VehicleNumber, Time, Lat, Brigade
    print(late_hours)
    to_drop = {'Brigade'}
    """
    renames = {'Lines' : Aliases.LINE.value,
               'Lon' : Aliases.LON.value,
               'VehicleNumber' : Aliases.VEHICLE_NUMBER.value,
               'Time' : Aliases.TIME.value,
               'Lat' : Aliases.LAT.value}
    
    modify_dataframe(df, to_drop, renames, late_hours)

def modify_time_tables_df(df, late_hours = False):
    """
    original columns:
    line, nr_przystanku, nr_zespolu,symbol_2,
    symbol_1, brygada, kierunek, trasa, czas
    """
    to_drop = {'symbol_2', 'symbol_1', 'brygada', 'trasa'}
    
    renames = {'kierunek' : Aliases.DIRECTION.value,
               'czas' : Aliases.TIME.value,
               'nr_przystanku' : Aliases.BUS_STOP_NUM.value,
               'nr_zespolu': Aliases.BUS_STOP_GROUP_NUM.value}
    
    modify_dataframe(df, to_drop, renames, late_hours)
