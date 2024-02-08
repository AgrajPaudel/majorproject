import os
import pandas as pd

def combine_csv_files(input_folder, merged_csv_name):
    # Get a list of all CSV files in the input_folder
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()

    # Iterate through each CSV file and merge its data into the DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)

        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path, index_col=0)

        # Rename the columns to avoid conflicts in case of duplicate column names
        data.columns = [f"{col}" for col in data.columns]

        # Merge the data into the main DataFrame
        merged_data = pd.concat([merged_data, data], axis=1)

    # Save the merged DataFrame to a new CSV file
    merged_data.to_csv(os.path.join(input_folder,merged_csv_name))


