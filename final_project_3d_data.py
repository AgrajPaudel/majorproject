import os
import pandas as pd

def create_data_cube(folder_path):
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Create an empty DataFrame to store the data
    data_cube = pd.DataFrame()

    for file in files:
        file_path = os.path.join(folder_path, file)
        bank_name = os.path.splitext(file)[0]

        # Read the CSV file into a pandas dataframe
        df = pd.read_csv(file_path, index_col=0)

        # Add a new column for the bank name
        df['Bank'] = bank_name

        # Append the dataframe to the data_cube
        data_cube = data_cube._append(df)

    return data_cube


