from math import floor
import pandas as pd

from speed import give_dataframe_of_coords_with_line_and_speed
from Helpers.positions import get_distance_between_two_points_in_km

MIN_NUM_OF_MEASUREMENTS = 10
R_IN_KM = 0.15

from Data_reading.modifying_dfs import Aliases as als
from speed import SPEED_LIMIT, MAX_MEASURED_SPEED

def dict_of_dfs_by_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def give_sector_indexes(lower_left_coords, point_coords):
    def give_in_which_part(start_coords, p_coords):
        partial_dist = get_distance_between_two_points_in_km(start_coords, p_coords)
        index = partial_dist // R_IN_KM
        return int(index)
    
    our_point = (lower_left_coords[0], point_coords[1])
    column_index = give_in_which_part(lower_left_coords, our_point)
    
    our_point = (point_coords[0], lower_left_coords[1])
    row_index = give_in_which_part(lower_left_coords, our_point)
    return (column_index, row_index)   

def init_sectors_2d_data(area_coords, elem = None):
    rows_num = give_sector_indexes(area_coords[0], area_coords[1])[1] + 1
    cols_num = give_sector_indexes(area_coords[0], area_coords[1])[0] + 1
    
    row = [elem] * cols_num
    arr_2d = []
    for i in range(rows_num):
        arr_2d.append(row)
        
    return arr_2d

def give_overspeed_df_by_sector(speed_measurements_df, area_coords):    
    lower_left_coords = area_coords[0]
    upper_right_coords = area_coords[1]
    
    sectors_2d_list = init_sectors_2d_data(area_coords, elem = (0, 0))
    
    for i, measurement in speed_measurements_df.iterrows():
        speed = measurement[als.SPEED.value]
        point_coords = (measurement[als.LAT.value], measurement[als.LON.value])
        
        i, j = give_sector_indexes(lower_left_coords, point_coords)
        
        if SPEED_LIMIT < speed < MAX_MEASURED_SPEED:
            is_overspeed = 1
        elif speed < MAX_MEASURED_SPEED:
            is_overspeed = 0
            
        x = sectors_2d_list[i][j][0] + is_overspeed
        y = sectors_2d_list[i][j][1] + 1
        new_tuple = (x, y)
        sectors_2d_list[i][j] = new_tuple
        
    return sectors_2d_list

def get_area_coords(bus_stop_df, speed_df):
    lat = als.LAT.value
    lon = als.LON.value
    df1 = bus_stop_df
    df2 = speed_df
    min_lat = min(df1[lat].min(), df2[lat].min())
    max_lat = max(df1[lat].max(), df2[lat].max()) 
    
    min_lon = min(df1[lon].min(), df2[lon].min())
    max_lon = max(df1[lon].max(), df2[lon].max())
    left_lower = (min_lat, min_lon)
    right_upper = (max_lat, max_lon) 
    return (left_lower, right_upper)

# in this function we want to calculate df: (bus_stop_id, place, percent_of_overspeed)
def give_overspeed_percentage_around_bus_stops_df(bus_stops_df, speed_measurements_df):
    area_coords = get_area_coords(bus_stops_df, speed_measurements_df)
    overspeed_in_sectors = give_overspeed_df_by_sector(speed_measurements_df, area_coords)
    
    cols = [als.BUS_STOP_ID.value, als.PLACE.value, als.OVERSPEED_PERCENTAGE.value]
    df_data = []
    for i, bus in bus_stops_df.iterrows():
        lat = bus[als.LAT.value]
        lon = bus[als.LON.value]
        
        lower_left_coords = area_coords[0]
        row, col = give_sector_indexes(lower_left_coords, (lat, lon))
        sum = overspeed_in_sectors[col][row][0]
        counter = overspeed_in_sectors[col][row][1]
        avg = sum / counter if counter != 0 and counter >= MIN_NUM_OF_MEASUREMENTS else 0
        
        
        id = bus[als.BUS_STOP_ID.value]
        place = bus[als.PLACE.value]
        df_data.append([id, place, avg])
        
    result_df = pd.DataFrame(df_data, columns = cols)
    return result_df
    
# in this function we want to calculate df: 
# (group_name, avg_percent_of_overspeed_in_group_name)
def give_places_with_overspeed_percent_df(bus_stops_df, speed_measurements_df):
    bus_stop_overspeed_df = give_overspeed_percentage_around_bus_stops_df(bus_stops_df, 
                                                                        speed_measurements_df)
    overspeed_by_place_dict = dict_of_dfs_by_column(bus_stop_overspeed_df, als.PLACE.value)
    
    cols = [als.PLACE.value, als.OVERSPEED_PERCENTAGE.value]
    data_for_df = []
    for place, df_overspeed_percent in overspeed_by_place_dict.items():
        avg = df_overspeed_percent[als.OVERSPEED_PERCENTAGE.value].mean(skipna=True)
        print(avg)
        row = [place, avg]
        data_for_df.append(row)
        
    df = pd.DataFrame(data_for_df, columns = cols)
    return df

def give_fastest_places(bus_stops_df, speed_measurements_df, how_many = 30):
    df = give_places_with_overspeed_percent_df(bus_stops_df, speed_measurements_df)
    df = df.sort_values(by = als.OVERSPEED_PERCENTAGE.value, ascending = False)
    return df.head(how_many)
        
if __name__ == '__main__':
    from speed import give_dataframe_of_coords_with_line_and_speed
    from Data_reading.reading import give_modified_bus_stops_df
    from Data_reading.reading import give_modified_curr_positions_df
    
    positions = give_modified_curr_positions_df()
    
    speed = give_dataframe_of_coords_with_line_and_speed(positions)
    bus_stops = give_modified_bus_stops_df()
    
    print(give_fastest_places(bus_stops, speed))
        
    
    