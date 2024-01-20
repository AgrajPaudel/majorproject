import pandas as pd
import numpy as np
from final_project_4d_z_score import get_values_for_variable_bank_quarter
# Convert the output to JSON format
import json

def calculate_rms_distance(array1, array2):
    # Calculate the squared differences for valid values (not NaN)
    squared_diff = np.square(array1 - array2)
    # Mask NaN values in either array
    valid_mask = ~np.isnan(array1) & ~np.isnan(array2)
    # Calculate the mean of squared differences for valid values
    mean_squared_diff = np.nanmean(squared_diff[valid_mask])
    # Take the square root to get the rms distance
    rms_distance = np.sqrt(mean_squared_diff)
    return rms_distance


def get_column_data(filename, datafile):
    result_dict = {}  # Initialize the dictionary to store the results

    # Read the CSV file
    df = pd.read_csv(filename, index_col=0)
    df_file = pd.read_csv(datafile, index_col=[0, 'Bank'])
    # Get the list of unique variables, banks, and quarters
    variables = df_file.index.get_level_values(0).unique()
    banks = df_file.index.get_level_values(1).unique()
    quarters = df_file.columns

    # Define the required variables
    required_variables = [
        "capital fund to rwa",
        "non performing loan to total loan",
        "total loan loss provision to npl",
        "cost of fund",
        "base rate",
        "net interest spread",
        "return on equity",
        "return on total assets",
        "credit to deposit ratio",
        "debt ratio",
        "return on investment",
        "net profit margin",
    ]

    # Iterate through each column
    for column in df.columns:
        column_array = [0] * len(required_variables)

        # Iterate through each row and populate the array
        for index, value in df[column].items():
            # Check if the variable is required
            if index in required_variables:
                var_index = required_variables.index(index)
                # Convert value to numeric, if possible
                numeric_value = pd.to_numeric(value, errors='coerce')
                column_array[var_index] = numeric_value

        # Initialize variables to track the 3 lowest distances
        lowest_distances = [float('inf')] * 3
        lowest_quarters = [''] * 3
        lowest_banks = [''] * 3

        result_dict[column] = {}  # Initialize the result dictionary for the current column

        for bank in banks:
            for quarter in quarters:
                value_of_variables = []
                for variable in required_variables:
                    value_of_variables.append(get_values_for_variable_bank_quarter(datafile=datafile,
                                                                                  variable=variable,
                                                                                  quarter=quarter,
                                                                                  bank=bank))

                # Calculate the rms distance
                rms_distance = calculate_rms_distance(np.array(column_array), np.array(value_of_variables))
                # Check if the distance is smaller than any in the list
                for i in range(3):
                    if rms_distance < lowest_distances[i]:
                        lowest_distances.insert(i, rms_distance)
                        lowest_distances = lowest_distances[:3]
                        lowest_quarters.insert(i, quarter)
                        lowest_quarters = lowest_quarters[:3]
                        lowest_banks.insert(i, bank)
                        lowest_banks = lowest_banks[:3]
                        break

        # Add the 3 lowest distances with their quarters and banks to the result dictionary
        result_dict[column] = {f"{i+1}st data": {
            'Distance': lowest_distances[i],
            'Quarter': lowest_quarters[i],
            'Bank': lowest_banks[i]
        } for i in range(3)}

    return result_dict


