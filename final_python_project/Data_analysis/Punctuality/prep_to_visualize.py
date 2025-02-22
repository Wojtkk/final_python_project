""" 
In this module we are preparing data regarding punctuality so
it can be ploted conveniently.
"""

import pandas as pd 

from Data_reading.modifying_dfs import Aliases as als

def most_delayed_bus_stops_data(delay_by_bus_stop_df, bus_stops_df, how_many=20):
    df = delay_by_bus_stop_df.merge(bus_stops_df, on = als.BUS_STOP_ID.value)
    
    df = df.sort_values(by=als.DELAY.value, ascending=False)
    df = df.head(how_many)
    
    return df[[als.PLACE.value, als.DELAY.value]]  

def shortest_expected_waiting_bus_stops(expected_by_bus_stop_df, bus_stops_df, how_many=20):
    df = expected_by_bus_stop_df.merge(bus_stops_df, on = als.BUS_STOP_ID.value)
    
    df = df.sort_values(by=als.EXPECTED_WAITING.value, ascending=True)
    df = df.head(how_many)
    return df[[als.PLACE.value, als.EXPECTED_WAITING.value]]


 
def bus_stops_to_plot_on_map_where_better_random_time(expected_by_bus_stop_df,
                                                      delay_by_bus_stop_df,
                                                      bus_stops_df,
                                                      planning_delay = 4):
    """ 
    in this function we verify hypothesis:
    are there any bus stops where at certain hours if we will do the following:
    select random line from this bus stop, and go according to the time table

    then we will loose more time because of 'planning_delay' than just
    walk on this bus stop at random time and then wait on this line 
    as long as we need

    Maybe buses are so out of schedule, that there is no use 
    in checking time tables at certain bus stops??

    if such bus stops exist function give us data to plot them on map
    """
    df = expected_by_bus_stop_df.merge(delay_by_bus_stop_df, on = als.BUS_STOP_ID.value)
    df = df.merge(bus_stops_df, on = als.BUS_STOP_ID.value)
    
    df = df[df[als.DELAY.value] + planning_delay > df[als.EXPECTED_WAITING.value]]
    
    data_to_plot = []
    for _, row in df.iterrows():
        lat = row[als.LAT.value]
        lon = row[als.LON.value]
        
        if row[als.DELAY.value] + planning_delay > row[als.EXPECTED_WAITING.value]:
            value = 1
        else:
            value = 0.5

        data_to_plot.append([lat, lon, value])

    return data_to_plot
        