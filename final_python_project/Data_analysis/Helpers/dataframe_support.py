import random
from Helpers.positions import calculate_time_in_sec_between_dates
import pandas as pd
""" 
In our project we frequently need to calculate something for every line
or for every bus stop.

Then its convenient to use such function which creates dictionary 
containing grouped dataframes.

Also if we want to make data smaller we can analyse only part of lines.
Thats why we have function give_dfs_contain_only_part_of_lines()
"""

from Data_reading.modifying_dfs import Aliases as als

def divide_on_dfs_by_given_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes

import random

def give_dfs_contain_part_of_column(dataframes_list, column_name, selected_values=None, how_many_values=10):
    # Assuming all dataframes have the same columns
    if column_name not in dataframes_list[0].columns:  
        return dataframes_list
    
    if selected_values is None:
        dict_of_values = {}
        for df in dataframes_list:
            values = df[column_name].unique()
            for value in values:
                if value in dict_of_values:
                    dict_of_values[value] += 1
                else: 
                    dict_of_values[value] = 1 

        how_many_dfs = len(dataframes_list)
        possible_to_select = []
        for val, counter in dict_of_values.items():
            if counter == how_many_dfs:
                possible_to_select.append(val)

        how_many_values = min(how_many_values, len(possible_to_select))
        selected_values = random.sample(possible_to_select, how_many_values)
    
    new_dataframes_list = []
    for df in dataframes_list:
        new_df = df[df[column_name].isin(selected_values)].copy()
        new_dataframes_list.append(new_df)
    
    return new_dataframes_list

def give_positions_from_a_few_minutes(positions_df, how_many_minutes=3):
    sorted_df = positions_df.sort_values(by=als.TIME.value, ascending=True)
    
    min_in_hours = 60
    how_many = int((how_many_minutes / min_in_hours) * len(sorted_df))
    
    return sorted_df.head(how_many)
    
                
            
        
        