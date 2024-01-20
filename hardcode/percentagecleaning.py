import pandas as pd

import os
from pdftotxt import txtmaker
from file_operations import bank_file_maker
from checkingfromcsvtotxt import  checker
from checkingoverflow import variable as v
import time

import pandas as pd
import os


def process_csv(file_path):
    try:
        data = pd.read_csv(file_path)

        # Calculate the threshold for empty cells (40% or more)
        threshold = int(0.5 * len(data.columns))

        # Remove rows that have fewer than the threshold non-empty cells
        data.dropna(thresh=threshold, inplace=True)

        # Remove the '.jpg' columns and process the data
        for column in data.columns:
            if column.endswith('.jpg') or column.endswith('.JPG'):
                col_name_no_jpg = column.replace('.jpg', '').replace('.JPG', '')
                if col_name_no_jpg in data.columns:
                    data[col_name_no_jpg] = data[col_name_no_jpg].combine_first(data[column])
                else:
                    data.rename(columns={column: col_name_no_jpg}, inplace=True)

        jpg_columns = [col for col in data.columns if col.endswith('.jpg') or col.endswith('.JPG')]
        data.drop(jpg_columns, axis=1, inplace=True)

        # Save the modified CSV with the removed rows
        data.to_csv(file_path, index=False)
        print('Modified CSV file saved at:', file_path)
    except  pd.errors.EmptyDataError:
        print("The provided CSV file is empty or doesn't contain any data.")



parent_folder = 'z test for cleaning'

# Get a list of subfolders in the parent folder
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# Loop through each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Get a list of pdf file paths in the subfolder
    pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.csv'))]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(subfolder_path, pdf_file)
        x=pdf_file.strip('.csv')
        print(pdf_file)  # name of file
        print(subfolder_path)  # before file
        print(pdf_path)# fullpath
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
        process_csv(pdf_path,)
        print('work done in : '+pdf_path)

















