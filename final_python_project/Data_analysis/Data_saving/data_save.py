""" 
Module for saving data.

We get dataframes with 'give_all_dataframes_and_their_titles()'
and create specified foler and save DataFrames there
if it already exist we raise an error
(prevention from overwritting downloaded data)
"""

import requests
from pathlib import Path
from data_convert import give_all_dataframes_and_their_titles

def save_df_to_csv_file(df, path):
    df.to_csv(path, index=False, sep=',', encoding='utf-8')

def save_all_dataframes_we_need_to_save(name_of_folder_to_save_in):
    folder = Path(__file__).parent / Path(name_of_folder_to_save_in)

    if not folder.exists():
        folder.mkdir(parents=True)
    else:
        raise ValueError("Directory with such name already exist!")

    titles_and_dataframes = give_all_dataframes_and_their_titles()
    for _, (filename, dataframe) in enumerate(titles_and_dataframes):
        path = folder.joinpath(filename)
        try:
            save_df_to_csv_file(dataframe, path)
        except Exception as e:
            print(f"Error saving {filename}: {e}")

if __name__ == "__main__":
    save_all_dataframes_we_need_to_save('for_timetables_v2')
