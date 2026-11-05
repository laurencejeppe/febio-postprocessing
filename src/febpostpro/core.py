
import numpy as np
import pandas as pd

import febpostpro.vis as vis

def read_output_file_to_dataframe(file_path) -> dict[str, pd.DataFrame]:
    """
    Reads a FEBio output file and returns the data as a pandas DataFrame.

    Parameters:
    file_path (str): The path to the FEBio output file.

    Returns:
    dict[str, pd.DataFrame]: A dictionary of output points mapped to pandas DataFrames containing the output data.
    """
    with open(file_path, 'r') as file:
        # Parse the whole file
        lines = file.readlines()
    
    # Evaluate the format of the output file and extract relevant data
    step_0 = lines[0].strip().split(' = ')
    time_0 = lines[1].strip().split(' = ')
    data_0 = lines[2].strip().split(' = ')[-1].split(';')
    data_len = len(data_0)
    output_dict = {}
    data_point_count = 0
    while True:
        output_point = lines[3+data_point_count].strip().split(' ')[0]
        if output_point[0] == '*':
            break
        output_dict[output_point] = pd.DataFrame(columns=[step_0[0], time_0[0]] + data_0)
        data_point_count += 1

    struct_length = 3 + data_point_count

    num_steps = int(len(lines) / struct_length)

    for step in range(num_steps):
        step_n = int(lines[step * struct_length].strip().split(' = ')[-1])
        time_n = float(lines[step * struct_length + 1].strip().split(' = ')[-1])
        for data_point in range(data_point_count):
            data_line = lines[step * struct_length + 3 + data_point].strip().split(' ')
            output_dict[data_line[0]].loc[step] = [step_n, time_n] + [float(x) for x in data_line[1:]]

    return output_dict

def output_df_to_csv(dataframe: pd.DataFrame, output_dir: str, name: str = "output_data") -> None:
    """
    Saves the output data from a FEBio output file to CSV files.

    Parameters:
    dataframe (pd.DataFrame): The pandas DataFrame containing the output data.
    output_dir (str): The directory where the CSV files will be saved.
    name (str, optional): The name of the CSV file. If not provided, a default name will be used.
    """
    csv_file_path = f"{output_dir}/{name}.csv"
    dataframe.to_csv(csv_file_path, index=False)