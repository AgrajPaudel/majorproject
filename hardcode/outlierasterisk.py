import pandas as pd
import os
# Load the CSV file





def outliercleaning(file_path):
    try:
        data = pd.read_csv(file_path)
        if len(data.columns) != 0:
            print(data.columns)
            for column in data.columns:
                data[column] = data[column].apply(
                    lambda x: str(x) + '*' if pd.notna(x) and isinstance(x, str) and len(str(x)) == 1 else x)
        else:
            print('empty file ' + file_path)

        #x = file_path.strip('.csv')

        data.to_csv(file_path, index=False)
    except        pd.errors.EmptyDataError:
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
        outliercleaning(pdf_path)
        print('work done in : '+pdf_path)








