import pandas as pd
import numpy as np
from final_project_zscore_calculator import calculate_z_score

# Set display options to show all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def display_all_quarters_and_banks_for_variable(datafile, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all quarters and banks for the specified variable
        result = df.loc[(variable, slice(None)), :]

        # Extract values from the result DataFrame
        values = result.values.flatten()

        # Convert all instances to numeric, remove non-numeric, empty, and '-'
        values = pd.to_numeric(values, errors='coerce')
        values = values[~np.isnan(values)]

        print(result)
        return values
    except KeyError:
        print(f"Data not found for variable: {variable}")


def display_all_quarters_for_bank_and_variable(datafile, bank, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all quarters for the specified bank and variable
        result = df.loc[(variable, bank), :]

        # Remove empty data
        result = result.apply(lambda x: np.nan if pd.isna(x) or str(x).strip() == '' else x)

        # Convert string data to numeric
        result = result.apply(pd.to_numeric, errors='coerce')

        # Remove non-numeric and data containing '-'
        result = result.replace(['-', ''], np.nan).dropna()

        # Extract values from the result DataFrame
        values = result.values.flatten()

        # Return the array of numerical data
        return values
    except KeyError:
        print(f"Data not found for bank: {bank} and variable: {variable}")


def display_all_banks_for_quarter_and_variable(datafile, quarter, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all banks for the specified quarter and variable
        result = df.loc[(variable, slice(None)), quarter]

        # Remove empty data
        result = result.apply(lambda x: np.nan if pd.isna(x) or str(x).strip() == '' else x)

        # Convert string data to numeric
        result = result.apply(pd.to_numeric, errors='coerce')

        # Remove non-numeric and data containing '-'
        result = result.replace(['-', ''], np.nan).dropna()

        # Extract values from the result DataFrame
        values = result.values.flatten()

        # Return the array of numerical data
        return values
    except KeyError:
        print(f"Data not found for quarter: {quarter} and variable: {variable}")


def calculate_z_scores(datafile):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    # Get the list of unique variables, banks, and quarters
    variables = df.index.get_level_values(0).unique()
    banks = df.index.get_level_values(1).unique()
    quarters = df.columns

    # Iterate through all data fields
    for variable in variables:
        for bank in banks:
            for quarter in quarters:
                try:
                    print(f"Variable: {variable}, Bank: {bank}, Quarter: {quarter}")
                    print(f"Old Line: {df.loc[variable].loc[bank, quarter]}")
                    value_to_check = df.loc[variable].loc[bank, quarter]

                    # Check if the value is empty, '-', or non-numeric
                    if pd.isna(value_to_check) or str(value_to_check).strip() == '' or not pd.to_numeric(value_to_check,
                                                                                                         errors='coerce'):
                        print("Skipping z-score calculation for non-numeric value.")
                        continue

                    array_of_all_variables = display_all_quarters_and_banks_for_variable(datafile, variable)
                    array_of_one_bank = display_all_quarters_for_bank_and_variable(datafile, bank=bank,
                                                                                   variable=variable)
                    array_of_one_quarter = display_all_banks_for_quarter_and_variable(datafile=datafile,
                                                                                      quarter=quarter,
                                                                                      variable=variable)

                    first_z_score = calculate_z_score(array=array_of_all_variables, value=pd.to_numeric(value_to_check))
                    second_z_score = calculate_z_score(array=array_of_one_quarter, value=pd.to_numeric(value_to_check))
                    third_z_score = calculate_z_score(array=array_of_one_bank, value=pd.to_numeric(value_to_check))

                    print(f"Z-Scores: {first_z_score}, {second_z_score}, {third_z_score}")
                    # Store z-scores in the DataFrame
                    df.at[(variable, bank), quarter] = f"{first_z_score:.6f} {second_z_score:.6f} {third_z_score:.6f}"



                except KeyError:
                    print(f"Data not found for Variable: {variable}, Bank: {bank}, Quarter: {quarter}")

    # Save the final DataFrame to a new CSV file
    df.to_csv('D:/python tesseract/z score/3d_zscore_table.csv')

# Example: Call the function with the data cube file
#data_cube_file = 'D:/python tesseract/3d data/data_cube.csv'

# Call the function to calculate and print z-scores
#calculate_z_scores(data_cube_file)
