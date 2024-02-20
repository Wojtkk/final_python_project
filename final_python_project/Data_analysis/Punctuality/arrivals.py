""" 
In this module from data with positions of vehicles we want to extract
times of arrivals at bus stops.

We need such data to analyse punctuality.

Idea of handling arrivals is like that: 
if data is updated after 10 s and 10 s is actually
shortest time bus can spend on bus stop than if bus arrives at bus stop
than we will have its position when its standing there in our data.
"""

import pandas as pd

from Data_reading.modifying_dfs import Aliases as als

from Helpers.positions import distance_between_two_points_in_km
from Helpers.dataframe_support import divide_on_dfs_by_given_column

from Data_reading.reading import give_modified_lines_stops_df
from Data_reading.reading import give_modified_bus_stops_df
from Data_reading.reading import give_modified_curr_positions_df
from Data_reading.reading import give_modified_time_tables_df

BUS_STOP_RANGE_IN_KM = 0.015

INF = 1000000000

NORTH_COORDS = (52.37124014293236, 20.9833612220712)
WEST_COORDS = (52.232228462386196, 20.789954779824953)

def group_df_by_vehicles(df):
    return divide_on_dfs_by_given_column(df, als.VEHICLE_NUMBER.value)

def group_by_line(df):
    return divide_on_dfs_by_given_column(df, als.LINE.value)

def df_line_stops_with_coords(line_stops_df, bus_stops_df):
    joined_df = pd.merge(line_stops_df, bus_stops_df, on = als.BUS_STOP_ID.value)
    return joined_df


def calc_arrival_times(single_line_stops, single_veh_positions):
    """ 
    we return Dataframe with columns:
    (line, veh_number, time, lat, lon, bus_stop_id)
    every row of such Dataframe 
    corresponds to one arrival of specific vehicle at bus stop

    argument 'single_line_stops' is Dataframe with 
    bus stops on which this vehicle may stop
    'single_veh_positions' is Dataframe with positions of specific vehicle
    
    we calculate distance of both bus stops and positions from some another point
    and then we sort them by this distance
    and then we iterate through sorted and for elements being neighbours 
    on this list we check if they are really that close 
    so we can say that vehicle arrived on bus stop
    """
    def give_stops_and_lines_list(line_stops, veh_positions):
        lst = []
        for i, elem in line_stops.iterrows():
            row = (elem[als.LAT.value],
                   elem[als.LON.value],
                   elem[als.BUS_STOP_ID.value])
            lst.append(row)
            
        for i, elem in veh_positions.iterrows():
            row = (elem[als.LAT.value],
                   elem[als.LON.value],
                   elem[als.TIME.value])
            lst.append(row)
        
        return lst
    
    def calc_stops_and_positions(rel_point, line_stops, veh_positions):
        stops_and_positions = give_stops_and_lines_list(line_stops, veh_positions)
        for i, elem in enumerate(stops_and_positions):
            elem_coords = (elem[0], elem[1])
            d = distance_between_two_points_in_km(rel_point, (elem_coords))
            stops_and_positions[i] = (elem[0], elem[1], elem[2], d)
            
        stops_and_positions = sorted(stops_and_positions, key = lambda x: x[3])
        return stops_and_positions
        
    def collect_arrivals_data(stops_and_positions, vehicle_num, line_num):
        arrival_data = []
        for i, elem in enumerate(stops_and_positions):
            is_bus = isinstance(elem[2], int)
            
            if i - 1 > 0:
                prev = stops_and_positions[i - 1]
                is_opposite = is_bus != isinstance(prev[2], int)
                if not is_opposite:
                    continue
                
                coords1 = (elem[0], elem[1])
                coords2 = (prev[0], prev[1])
                d = distance_between_two_points_in_km(coords1, coords2)
                if d < BUS_STOP_RANGE_IN_KM:
                    time = elem[2] if not is_bus else prev[2] 
                    coords = coords1 if is_bus else coords2
                    bus_stop_id = elem[2] if is_bus else prev[2]
                    row = [line_num,
                           vehicle_num,
                           time,
                           coords[0],
                           coords[1],
                           bus_stop_id]
                    arrival_data.append(row)
                    
        if len(arrival_data) == 0:
            return None
        else:
            return arrival_data
                
    def calc_with_rel_point(rel_point, line_stops, veh_positions):
        lst = calc_stops_and_positions(rel_point, line_stops, veh_positions)
        veh_num = veh_positions[als.VEHICLE_NUMBER.value].iloc[0]
        line_num = veh_positions[als.LINE.value].iloc[0]
        return collect_arrivals_data(lst, veh_num, line_num)
    
    def concatenate_if_not_none(lst, element):
        if element is not None:
            lst += element
            
    cols = [als.LINE.value, als.VEHICLE_NUMBER.value, als.TIME.value, 
            als.LAT.value, als.LON.value, als.BUS_STOP_ID.value]
    arrivals_data = []
    
    rel_points = [NORTH_COORDS, WEST_COORDS]
    for p in rel_points:
        arrivals = calc_with_rel_point(p, single_line_stops, single_veh_positions)
        concatenate_if_not_none(arrivals_data, arrivals)
     
    if len(arrivals_data) > 0:
        dfs = pd.DataFrame(arrivals_data, columns = cols)
        return dfs
    else:
        return None

def give_df_with_arrivals(df_with_positions, lines_stops_df, bus_stops_df):
    """ 
    in this function we divide data for every vehicle so we can use function
    'calc_arrival_times(...)' and then we return Dataframe with arrivals
    which is concatenated DataFrames from function 'calc_arrival_times(...)'
    for every vehicle
    """
    dfs_positions_of_vehicle = group_df_by_vehicles(df_with_positions)
    
    df_of_line_stops = df_line_stops_with_coords(lines_stops_df, bus_stops_df)
    
    dict_of_bus_stops_for_lines = group_by_line(df_of_line_stops)
    
    arrival_dfs = []
    iter = 0
    for single_veh_positions in dfs_positions_of_vehicle.values():
        iter += 1
        
        line = single_veh_positions[als.LINE.value].iloc[0]
        if line not in dict_of_bus_stops_for_lines.keys():
            continue
        
        single_line_stops = dict_of_bus_stops_for_lines[line]
        
        veh_arrivals_df = calc_arrival_times(single_line_stops, single_veh_positions)
        if veh_arrivals_df is not None:
            arrival_dfs.append(veh_arrivals_df)
        
    concatenated_df = pd.concat(arrival_dfs, ignore_index=True)
    
    columns_to_consider = [als.VEHICLE_NUMBER.value, als.BUS_STOP_ID.value]
    df_no_duplicates = concatenated_df.drop_duplicates(subset=columns_to_consider)
    return df_no_duplicates

if __name__ == '__main__':
    pos_df = give_modified_curr_positions_df()
    lines_df = give_modified_lines_stops_df()
    
    bus_stops_df = give_modified_bus_stops_df()
    
    df_to_vis = give_df_with_arrivals(pos_df, lines_df, bus_stops_df)
    len(df_to_vis)
    
    points_and_values = [(r[als.LAT.value], r[als.LON.value], 0.5) for index, r in df_to_vis.iterrows()]   
    from Helpers.visualization import plot_points_on_map
    plot_points_on_map(points_and_values)   
    
    
    