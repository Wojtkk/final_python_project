from Data_reading.modifying_dfs import Aliases as als
import datetime

import pandas as pd

INF = 100000

def dict_of_dfs_by_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

def give_minutes_between_two_timestamps(t1, t2):
    diff = t2 - t1
    return diff.total_seconds() / 60

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
    for scheduled_time in time_table_for_line:
        first_time_after = give_minutes_between_two_timestamps(scheduled_time, end)
        
        for real_arrive_times in list_of_arrival_times:
            single_delay = give_minutes_between_two_timestamps(scheduled_time, real_arrive_times)
            if single_delay >= -1:
                first_time_after = min(first_time_after, single_delay, 0)
            
        delay_sum += first_time_after
        
    return delay_sum
        
def dict_with_time_only(dict_of_arrivals_by_line):
    new_dict = {}
    for line, arrivals_time_df in dict_of_arrivals_by_line.items():
        time_list = arrivals_time_df[als.TIME.value].tolist()
        new_dict[line] = time_list
        
    return new_dict
    

# this function is supposed to give dataframe in format:
# (bus_stop_id, expected_waiting)
# expected waiting is for given bus stop is defined this way:
# we randomly select line and then go to given bus stop 
# time we wait is first vehicle of selected line which will appear after we arrive 
# how we are going to calculate it for the given bus stop?
# we will take average of expected time for every line and then for line:
# for line we will take general time interval, and then we will sum up 
# probability of appearing in given minute on bus stop (for every minute the same)
# and amount of time we are going to wait (time to neaarest vehicle of this line)
# so it is going to be eaasy formula:

def give_df_with_expected_waiting_time_on_bus_stop(arrivals_df, bus_positions_df):
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

# this function is supposed to give dataframe in format:
# (bus_stop_id, average_delay, bus_stop_lat, bus_stop_lon)
# formula will be average of all delays:
# for given bus stop we want to have the following:
# for every time table time of arrival of line we want to have first arrival after it (or minute earlier)
# then difference between these two times is delay, we take average of them

def get_delays_data(dict_of_arrivals, dict_of_time_tables, time_interval):
    for bus_stop_id, arrive_df in dict_of_arrivals.items():
        if bus_stop_id not in dict_of_time_tables.keys(): # to erase
            continue 
        else:
            time_table_on_this_bus_stop_df = dict_of_time_tables[bus_stop_id]
        
        dict_time_table_line = dict_of_dfs_by_column(time_table_on_this_bus_stop_df,
                                                     als.LINE.value)
        dict_time_only = dict_with_time_only(dict_time_table_line)
        
        
        dict_of_arrivals_by_line = dict_of_dfs_by_column(arrive_df, als.LINE.value)
        dict_time_only = dict_with_time_only(dict_of_arrivals_by_line)
        
        sum_delays = 0
        counter = 0
        result_df_data = []
        for line, list_of_arrival_times in dict_time_only.items():
            if line not in dict_time_table_line.keys():
                continue
            time_table_for_line = dict_time_only[line]
            print(time_table_for_line)
            sum_delays = calc_delays(list_of_arrival_times, time_table_for_line, time_interval)
            
            counter += len(list_of_arrival_times)
         
        if counter != 0:
            avg_delay = sum_delays / counter 
        else:
            avg_delay = 0
                
        coords = (arrive_df[als.LAT.value].iloc[0], 
                  arrive_df[als.LON.value].iloc[0])
        result_df_data.append([bus_stop_id, avg_delay, coords[0], coords[1]])

    return result_df_data

def give_df_with_avg_delay_on_bus_stop(arrivals_df, time_tables_df):
    dict_of_arrivals = dict_of_dfs_by_column(arrivals_df, als.BUS_STOP_ID.value)
    dict_of_time_tables = dict_of_dfs_by_column(time_tables_df, als.BUS_STOP_ID.value)
    
    time_interval = give_general_time_interval(arrivals_df)
    cols = [als.BUS_STOP_ID.value, als.DELAY.value, als.LAT, als.LON]
    result_df_data = get_delays_data(dict_of_arrivals, dict_of_time_tables, time_interval)
        
    df = pd.DataFrame(result_df_data, columns = cols)      
    return df
        
    
    