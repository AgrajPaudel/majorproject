import pandas as pd
import json
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
        # Convert each item to a JSON-style entry
        result_json = [{'variable': str(variable), 'value': str(value)} for (variable, _), value in result.items()]
        return result_json
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
        return result
    except KeyError:
        print(f"Data not found for variable: {variable}, bank: {bank}, and quarter: {quarter}")

def display_all_banks_for_quarter_and_variable(datafile, quarter, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all banks for the specified quarter and variable
        result = df.loc[(variable, slice(None)), quarter]

        # Convert the result to a JSON-like format
        result_json = [{"bank": bank, "value": str(value)} for (variable, bank), value in result.items()]

        # Print and return the JSON-like result

        return result_json

    except KeyError:
        print(f"Data not found for quarter: {quarter} and variable: {variable}")



def display_all_quarters_for_bank_and_variable(datafile, bank, variable):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for all quarters for the specified bank and variable
        result = df.loc[(variable, bank), :]

        # Convert the result to a JSON-like format
        result_json = [{"quarter": idx, "value": str(value)} for idx, value in result.items()]

        return result_json

    except KeyError:
        print(f"Data not found for bank: {bank} and variable: {variable}")


#print(display_value_for_variable_bank_quarter(datafile='D:/python tesseract/3d data/data_cube.csv',variable='reserves',quarter='Q3 2078',bank='Civil Bank'))