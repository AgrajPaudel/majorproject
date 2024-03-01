import pandas as pd
from final_project_create_model_using_knn import get_nearest_datasets
import numpy as np
from final_project_4d_z_score import get_values_for_variable_bank_quarter
from final_project_create_model_using_knn import load_knn_model




def get_column_data(filename, knnfile):
    result_dict = {}  # Initialize the dictionary to store the results
    knn_model, all_values, all_indices = load_knn_model(knnfile)
    # Read the CSV file
    df = pd.read_csv(filename, index_col=0)




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

        nearest_dataset=get_nearest_datasets(knn_model, np.array(column_array), all_values, all_indices)

        # Format the nearest datasets as per the desired JSON structure
        result_dict[column] = {}
        for i, (dataset, distance) in enumerate(nearest_dataset, start=1):
            result_dict[column][f"{i}st data"] = {
                'bank': dataset[0],
                'quarter': dataset[1],
                'distance': distance
            }
    return result_dict


