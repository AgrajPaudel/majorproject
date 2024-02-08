import pandas as pd
import numpy as np

def calculate_values_and_update_csv(csv_file_path):
    # Function to calculate the value based on the specified formula
    def calculate_value(data, variable, formula):
        if variable not in data.index or pd.isna(data.at[variable]):
            # Calculate the value using the provided formula
            try:
                calculated_value = eval(formula, globals(), data.to_dict())
            except:
                calculated_value = 0

            # Add a new row with the calculated value for the specified variable
            new_row = pd.Series([calculated_value] + [np.nan] * (data.shape[1] - 1), index=data.columns, name=variable)
            data = data._append(new_row)

        return data

    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path, index_col=0)

    # Define the formulas for the calculations
    formulas = {
        'income tax liability': 'current tax liabilities + deferred tax liabilities',
        'net interest income': 'interest income - interest expense',
        'non operating income expense': 'non operating income - non operating expense',
        'loan and advancements': 'loans and advances to customers + loan and advances to b/fis'
    }

    # Iterate through the formulas and calculate the values
    for result_variable, formula in formulas.items():
        # Calculate the value for each variable
        data = calculate_value(data, result_variable, formula)

    # Save the updated DataFrame back to the CSV file
    data.to_csv(csv_file_path)

