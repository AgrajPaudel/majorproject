import os
import csv

def clean_data(value):
    # Function to clean data fields of single quotes and percent signs
    cleaned_value = value.replace(",", "").replace("%", "")
    cleaned_value= str(cleaned_value).replace('(',"").replace(')',"")
    return cleaned_value

def process_csv_file(file_path):
    # Function to process a CSV file
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Process data fields (excluding row and column headers)
    for i in range(1, len(data)):
        for j in range(1, len(data[i])):
            data[i][j] = clean_data(data[i][j])

    # Write the cleaned data back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def clean_csv_files_in_folder(folder_path):
    # Function to clean data fields in all CSV files in a folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            process_csv_file(file_path)
            print(f"Processed: {filename}")


