""" 
In our project we frequently need to calculate something for every line
or for every bus stop.

Then its convenient to use such function which creates dictionary 
containing grouped dataframes.
"""

def divide_on_dfs_by_given_column(dataframe, column_name):
    grouped = dataframe.groupby(column_name)

    dataframes = {}
    for category, group_df in grouped:
        dataframes[category] = group_df 
        
    return dataframes