import pandas as pd
from pathlib import Path

CSV = 'csv'

def give_df_from_csv_files(path_to_file):
    df = pd.read_csv(path_to_file)
    return df

def give_dataframes_with_filenames_from_csv_files_from_dir(path_to_dir):
    dataframes = {}
    
    path = Path(path_to_dir)
    for file in path.iterdir():
        if file.suffix == f'.{CSV}':
            df = give_df_from_csv_files(file)
            dataframes[file.name] = df
    
    return dataframes

def give_dataframes_from_right_folder():
    project_directory = Path(__file__).resolve().parent.parent
    target_directory = project_directory / 'Data_collecting/for_data'
    
    dict_of_dataframes = give_dataframes_with_filenames_from_csv_files_from_dir(target_directory)
    return dict_of_dataframes

# dict_df = give_dataframes_from_right_folder()
