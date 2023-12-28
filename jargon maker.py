import os
import pandas as pd
import json

def get_cumulative_variable_list(folder_path):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.csv')]

    # Initialize an empty set to store unique variables
    unique_variables = set()

    # Iterate over each CSV file
    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, csv_file)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Extract variables from the first column and add them to the set
        variables = set(df.iloc[:, 0])
        unique_variables.update(variables)

    # Convert the set of unique variables to a list
    cumulative_variable_list = list(unique_variables)

    return cumulative_variable_list


def generate_jargon_file(jargon_path,folder_path):
    # Get the cumulative list of variables
    cumulative_variables = get_cumulative_variable_list(folder_path)

    # Create a list of jargons
    jargons = []

    # Iterate over each variable and create a jargon entry
    for variable in cumulative_variables:
        jargon_entry = {
            "head": variable,
            "pattern": [[]]  # You can customize this part based on your requirements
        }
        jargons.append(jargon_entry)

    # Create a dictionary for the jargon file
    jargon_file_data = {
        "jargons": jargons
    }

    # Save the jargon file to a JSON file
    jargon_file_path = "jargons.json"  # You can change the file name as needed
    with open(jargon_file_path, 'w', encoding='utf-8') as jargon_file:
        json.dump(jargon_file_data, jargon_file, ensure_ascii=False, indent=4)

    print(f"Jargon file saved to {jargon_file_path}.")


# Example usage:
folder_name = ".templates"  # Replace with the actual folder name
folder_path = os.path.join(os.getcwd(), folder_name)
cumulative_variables = get_cumulative_variable_list(folder_path)
jargon_path=os.getcwd()
generate_jargon_file(jargon_path,folder_path)




# Print the cumulative list of variables
print("Cumulative List of Variables:")
index=0
for variable in cumulative_variables:
    print(variable)
    index=index+1
    print(index)
