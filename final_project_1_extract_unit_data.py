import pandas as pd

# Set display options to show all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def display_bank_quarter_data(datafile, bank, quarter):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for the specified bank and quarter
        result = df.loc[(slice(None), bank), quarter]
        print(result)
    except KeyError:
        print(f"Data not found for bank: {bank} and quarter: {quarter}")


def display_all_quarters_and_banks_for_variable(datafile, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all quarters and banks for the specified variable
        result = df.loc[(variable, slice(None)), :]
        print(result)
    except KeyError:
        print(f"Data not found for variable: {variable}")

def display_value_for_variable_bank_quarter(datafile, variable, bank, quarter):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for the specified variable, bank, and quarter
        result = df.loc[(variable, bank), quarter]
        print(result)
    except KeyError:
        print(f"Data not found for variable: {variable}, bank: {bank}, and quarter: {quarter}")

def display_all_banks_for_quarter_and_variable(datafile, quarter, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all banks for the specified quarter and variable
        result = df.loc[(variable, slice(None)), quarter]
        print(result)
    except KeyError:
        print(f"Data not found for quarter: {quarter} and variable: {variable}")

def display_all_quarters_for_bank_and_variable(datafile, bank, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all quarters for the specified bank and variable
        result = df.loc[(variable, bank), :]
        print(result)
    except KeyError:
        print(f"Data not found for bank: {bank} and variable: {variable}")


# Example: Call the function with the data cube file and specific bank and quarter
data_cube_file = '3d data/data_cube.csv'
bank_name = 'Citizen Bank'
variable_name = 'total assets'
quarter_name = 'Q1 2070'

# Call functions
display_value_for_variable_bank_quarter(data_cube_file, variable_name, bank_name, quarter_name)
display_all_banks_for_quarter_and_variable(data_cube_file, quarter_name, variable_name)
display_all_quarters_for_bank_and_variable(data_cube_file, bank_name, variable_name)
display_bank_quarter_data(data_cube_file, bank_name, quarter_name)
display_all_quarters_and_banks_for_variable(data_cube_file,variable_name)