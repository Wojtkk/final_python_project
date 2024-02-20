""" 
In this module we analyse two parameters of punctuality of buses -
average waiting time and expected waiting time on bus, which
is part of my own analysis and try to predict how long are 
we going to wait on bus if we dont check time table.
"""

from Data_reading.modifying_dfs import Aliases as als
import datetime

import pandas as pd

INF = 100000

TO_EARLY_TIME = -1

def dict_of_dfs_by_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def give_minutes_between_two_timestamps(t1, t2):
    hour1, minute1 = t1.hour, t1.minute
    hour2, minute2 = t2.hour, t2.minute
    
    diff_minutes = abs((hour2 - hour1) * 60 + (minute2 - minute1))
    return diff_minutes

def give_general_time_interval(bus_positions_df):
    min_time = min(bus_positions_df[als.TIME.value])
    max_time = max(bus_positions_df[als.TIME.value])
    return min_time, max_time

def calculate_expected_waiting_time(general_time_interval, line_arrives_time):
    start = general_time_interval[0]
    end = general_time_interval[1]
    times = [start] + line_arrives_time + [end]
    integral = 0
    for i in range(len(times) - 1):
        diff = give_minutes_between_two_timestamps(times[i], times[i+1])
        integral += diff * diff / 2
        
    interval_length = give_minutes_between_two_timestamps(start, end)
    expected_delay = integral / interval_length
    return expected_delay
        

def calc_delays(list_of_arrival_times, time_table_for_line, time_interval):
    end = time_interval[1]
    delay_sum = 0
    counter = 0
    for scheduled_time in time_table_for_line:
        first_time_after = give_minutes_between_two_timestamps(scheduled_time, end)
        
        some_arrival = False
        for real_arrive_time in list_of_arrival_times:
            single_delay = give_minutes_between_two_timestamps(scheduled_time, real_arrive_time)
            if single_delay > TO_EARLY_TIME:
                first_time_after = min(first_time_after, single_delay)
                some_arrival = True
                
        if some_arrival:
            delay_sum += first_time_after
            counter += 1
        
    return delay_sum / counter if counter != 0 else 0
        
def dict_with_time_only(dict_of_arrivals_by_line):
    new_dict = {}
    for line, arrivals_time_df in dict_of_arrivals_by_line.items():
        time_list = arrivals_time_df[als.TIME.value].tolist()
        new_dict[line] = time_list
        
    return new_dict
    

def give_df_with_expected_waiting_time_on_bus_stop(arrivals_df, bus_positions_df):
    """
    This function generates a DataFrame in the format:
    (bus_stop_id, expected_waiting, lat, lon), where the expected_waiting
    for a given bus stop is calculated based on the arrival times
    of vehicles.

    Expected waiting time for a bus stop is defined as follows:
    - Randomly select a bus line.
    - The expected waiting time is the time until the arrival of the
      next vehicle on that line after reaching the bus stop.

    The expected waiting time for each bus stop is calculated by
    averaging the expected waiting times for every line that serves
    that bus stop.

    The calculation involves summing up the probability of a vehicle
    arriving at the bus stop in a given minute and the time it takes
    to reach the nearest vehicle of that line.
    """
    dict_of_arrivals = dict_of_dfs_by_column(arrivals_df, als.BUS_STOP_ID.value)

    cols = [als.BUS_STOP_ID.value, als.EXPECTED_WAITING.value, als.LAT, als.LON]
    df_data = []

    time_interval = give_general_time_interval(arrivals_df)
    for bus_stop_id, arrive_df in dict_of_arrivals.items():
        dict_of_arrivals_by_line = dict_of_dfs_by_column(arrive_df, als.LINE.value)
        dict_time_only = dict_with_time_only(dict_of_arrivals_by_line)
        
        sum_of_expected = 0
        for line, list_of_arrival_times in dict_time_only.items():
            sum_of_expected += calculate_expected_waiting_time(time_interval,
                                                               list_of_arrival_times)
            
        num_of_lines = len(dict_time_only)
        final_expected = sum_of_expected / num_of_lines
        
        coords = (arrive_df[als.LAT.value].iloc[0], 
                  arrive_df[als.LON.value].iloc[0])
        df_data.append([bus_stop_id, final_expected, coords[0], coords[1]])
        
    df = pd.DataFrame(df_data, columns = cols)      
    return df

def get_delays_data(dict_of_arrivals, dict_of_time_tables, time_interval):
    result_df_data = []
    for bus_stop_id, arrive_df in dict_of_arrivals.items():
        if bus_stop_id not in dict_of_time_tables.keys(): # to erase
            continue 
        
        time_table_on_this_bus_stop_df = dict_of_time_tables[bus_stop_id]
        
        dict_time_table_line = dict_of_dfs_by_column(time_table_on_this_bus_stop_df,
                                                     als.LINE.value)
        dict_time_only_time_table = dict_with_time_only(dict_time_table_line)
        
        
        dict_of_arrivals_by_line = dict_of_dfs_by_column(arrive_df, als.LINE.value)
        dict_time_only_real_arrives = dict_with_time_only(dict_of_arrivals_by_line)
        
        sum_delays = 0
        counter = 0
        for line, list_of_arrival_times in dict_time_only_real_arrives.items():
            if line not in dict_time_table_line.keys():
                continue
            
            time_table_for_line = dict_time_only_time_table[line]
            sum_delays += calc_delays(list_of_arrival_times, time_table_for_line, time_interval)
            
        size = len(dict_time_only_real_arrives.items())
        if size != 0:
            avg_delay = sum_delays / size
        else:
            avg_delay = 0
            
        coords = (arrive_df[als.LAT.value].iloc[0], 
                  arrive_df[als.LON.value].iloc[0])
        result_df_data.append([bus_stop_id, avg_delay, coords[0], coords[1]])

    return result_df_data

def give_df_with_avg_delay_on_bus_stop(arrivals_df, time_tables_df):
    """ 
    this function is supposed to give dataframe in format:
    (bus_stop_id, average_delay, bus_stop_lat, bus_stop_lon)
    average delay on bus stop is just average delay of every scheduled
    arrival on this bus stop
    """
    dict_of_arrivals = dict_of_dfs_by_column(arrivals_df, als.BUS_STOP_ID.value)
    dict_of_time_tables = dict_of_dfs_by_column(time_tables_df, als.BUS_STOP_ID.value)
    
    time_interval = give_general_time_interval(arrivals_df)
    cols = [als.BUS_STOP_ID.value, als.DELAY.value, als.LAT, als.LON]
    result_df_data = get_delays_data(dict_of_arrivals, dict_of_time_tables, time_interval)
        
    df = pd.DataFrame(result_df_data, columns = cols)      
    return df
        
    
    