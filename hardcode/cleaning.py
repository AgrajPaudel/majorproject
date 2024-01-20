import pandas as pd
import os
# Load the CSV file



    # Function to delete specific rows based on condition
def delete_rows(dataframe):
    rows_to_delete = []

    # Find rows with very few data points and mark them for deletion
    for index, row in dataframe.iterrows():
        data_count = row.count()
        if data_count <= 1:
            rows_to_delete.append(index)

    # Delete rows marked for deletion
    dataframe.drop(rows_to_delete, inplace=True)




# Function to delete entirely empty columns
def delete_empty_columns(dataframe):
    empty_cols = dataframe.columns[dataframe.isnull().all()]
    dataframe.drop(empty_cols, axis=1, inplace=True)

def deleteemptyrowsandcolumns(file_path):

    df = pd.read_csv(file_path)




    # Count initial empty instances
    initial_empty_spaces = df.isnull().sum().sum()
    initial_dashes = df.apply(lambda x: x.astype(str).str.count('-')).sum().sum()
    initial_data = df.count().sum() - initial_empty_spaces - initial_dashes

    # Delete rows with few data points
    delete_rows(df)

    # Delete entirely empty columns
    delete_empty_columns(df)


    df.to_csv(file_path,index=False)




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
        deleteemptyrowsandcolumns(pdf_path)
        print('work done in : '+pdf_path)








