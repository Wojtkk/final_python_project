import pandas as pd

LON_STR = 'lon'
LAT_STR = 'lat'

BUS_STOP_NUM_STR = 'bus_stop_num'
BUS_STOP_GROUP_NUM_STR = 'bus_stop_group'
BUS_STOP_ID_STR = 'bus_stop_id'
STREET_ID_STR = 'street_id'

LINE_STR = 'line'
DIRECTION_STR = 'direction'
ROUTE_STR = 'route'

VEHICLE_NUMBER_STR = 'vehicle_num'
TIME_STR = 'time'

DISTANCE_STR = 'distance'
LON_STR = 'lon'
LAT_STR = 'lat'

MAX_NUM_OF_BUS_STOP = 1000

def modify_dataframe(df, columns_to_drop, columns_renames_dict):
    def drop_given_columns(df, columns_to_drop):
        df.drop(columns = columns_to_drop, axis = 1, inplace = True)
        
    def rename_given_columns(df, columns_renames_dict):
        df.rename(columns = columns_renames_dict, inplace = True)
    
    def remove_bus_depots_data(df):
        def bus_stop_is_bus_depot(bus_stop_group_num):
            return isinstance(bus_stop_group_num, str) and bus_stop_group_num[0] == 'R'
                
        if BUS_STOP_GROUP_NUM_STR in df.columns:
            depot_indices = df[df[BUS_STOP_GROUP_NUM_STR].apply(bus_stop_is_bus_depot)].index
            df = df.drop(depot_indices, inplace = True)
    
    def convert_time_format_if_possible(df):
        if TIME_STR in df.columns:
            bad_midnight = '24:00:00'
            good_midnight = '23:59:59'
            
            def modify_midnight(time):
                if bad_midnight in time:
                    return time.replace(bad_midnight, good_midnight)
                return time
                    
            
            df[TIME_STR] = df[TIME_STR].apply(modify_midnight)
            
            df[TIME_STR] = pd.to_datetime(df[TIME_STR])
    
    def add_bus_stop_id_column_if_possible(df):
        def mapping_on_bus_stops_id(num_of_group, num_of_bus_stop):
            return num_of_group * (MAX_NUM_OF_BUS_STOP + 1) + num_of_bus_stop
        
        cols = df.columns
        if BUS_STOP_GROUP_NUM_STR in cols and BUS_STOP_NUM_STR in cols:
            df[BUS_STOP_ID_STR] = ""
            for i, row in df.iterrows():
                num_of_group = int(row[BUS_STOP_GROUP_NUM_STR])
                num_of_bus_stop = int(row[BUS_STOP_NUM_STR])
                
                bus_stop_id = mapping_on_bus_stops_id(num_of_group, num_of_bus_stop)
                
                df.at[i, BUS_STOP_ID_STR] = bus_stop_id
                
            unnecessary_cols_now = {BUS_STOP_GROUP_NUM_STR, BUS_STOP_NUM_STR}
            drop_given_columns(df, unnecessary_cols_now)

    drop_given_columns(df, columns_to_drop)
    
    rename_given_columns(df, columns_renames_dict)
    
    remove_bus_depots_data(df)
    
    convert_time_format_if_possible(df)
    
    add_bus_stop_id_column_if_possible(df)


def modify_stops_on_routes_df(df):
    # original columns:
    # odleglosc, ulica_id, nr_zespolu, typ, nr_przystanku, line 
    to_drop = {'nr_zespolu', 'typ'}

    renames = {'odleglosc' : DISTANCE_STR,
              'ulica_id' : STREET_ID_STR,
              'nr_przystanku' : BUS_STOP_ID_STR}  
       
    modify_dataframe(df, to_drop, renames)       
    
def modify_bus_stops_df(df):
    # original columns:
    # zespol, slupek, nazwa_zespolu, id_ulicy, szer_geo, dlug_geo, kierunek, obowiazuje_od
    to_drop = {'nazwa_zespolu', 'obowiazuje_od'}
    
    renames = {'zespol' : BUS_STOP_GROUP_NUM_STR,
                'slupek' : BUS_STOP_NUM_STR,
                'id_ulicy' : STREET_ID_STR,
                'szer_geo' : LAT_STR,
                'dlug_geo' : LON_STR,
                'kierunek' : DIRECTION_STR}
    
    modify_dataframe(df, to_drop, renames)  

def modify_curr_positions_of_buses_df(df):
    # original columns:
    # Lines, Lon, VehicleNumber, Time, Lat, Brigade
    to_drop = {'Brigade'}
    
    renames = {'Lines' : LINE_STR,
               'Lon' : LON_STR,
               'VehicleNumber' : VEHICLE_NUMBER_STR,
               'Time' : TIME_STR,
               'Lat' : LAT_STR}
    
    modify_dataframe(df, to_drop, renames)
    
def modify_time_tables_df(df):
    # original columns:
    # line,nr_przystanku,nr_zespolu,symbol_2,symbol_1,brygada,kierunek,trasa,czas
    to_drop = {'symbol_2', 'symbol_1', 'brygada', 'trasa'}
    
    renames = {'kierunek' : DIRECTION_STR,
               'czas' : TIME_STR,
               'nr_przystanku' : BUS_STOP_NUM_STR,
               'nr_zespolu': BUS_STOP_GROUP_NUM_STR}
    
    modify_dataframe(df, to_drop, renames)
