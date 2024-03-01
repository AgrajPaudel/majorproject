import pandas as pd
import numpy as np



def display_all_quarters_for_variable(datafile, variable):
    try:
        # Read the data cube CSV file
        df = pd.read_csv(datafile, index_col=0)

        # Use loc to access data for all quarters for the specified variable
        result = df.loc[variable, :]

        # Remove empty data
        result = result.apply(lambda x: np.nan if pd.isna(x) or str(x).strip() == '' else x)

        # Convert string data to numeric
        result = result.apply(pd.to_numeric, errors='coerce')

        # Remove non-numeric and data containing '-'
        result = result.replace(['-', ''], np.nan).dropna()

        # Create a dictionary for each instance
        result_dict = [{"quarter": quarter, "value": str(value)} for quarter, value in result.items()]

        # Print and return the JSON-like result
        return result_dict

    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {datafile}")
    except KeyError:
        print(f"Data not found for variable: {variable}")

def get_values_for_quarter(datafile, quarter):
    try:
        # Read the data cube CSV file
        df = pd.read_csv(datafile, index_col=0)

        # Use loc to access data for the specified variable and quarter
        result = df.loc[:, quarter]

        # Handle numeric values directly
        if pd.api.types.is_numeric_dtype(result):
            # Convert to dictionary with variable as key and value as value
            result_dict = result.to_dict()
        else:

            # Remove empty data
            if str(result).strip() == '' or str(result).strip() == '-' or pd.isna(str(result)):
                result = np.nan

            print(result)
            # Convert string data to numeric
            result = pd.to_numeric(result, errors='coerce')

            # Convert to dictionary with variable as key and value as value
            result_dict = result.to_dict()

        # Convert to a list of dictionaries
        result_list = [{"variable": variable, "value": str(value)} for variable, value in result_dict.items()]


        return result_list
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {datafile}")
    except KeyError:
        print(f"Data not found for quarter: {quarter}")
        return np.nan

#print(get_values_for_quarter(datafile='D:/python tesseract/z outp/z output/merged_file.csv',quarter='Q1 2072'))
#print(display_all_quarters_for_variable(datafile='D:/python tesseract/z outp/z output/merged_file.csv',variable='reserves'))

