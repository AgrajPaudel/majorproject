import os
import pandas as pd


def remove_after_dot(input_float):
    # Convert input to string for processing
    input_string = str(input_float)

    # Check if the input contains a decimal point
    if '.' in input_string:
        # Split the string by the decimal point
        parts = input_string.split('.')

        # Return only the part before the decimal point as a float
        return float(parts[0])
    else:
        # If there is no decimal point, return the original input as a float
        return float(input_string)


def manage_denomination(folder_path):

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            check = False
            # Create the full path to the CSV file
            csv_file_path = os.path.join(folder_path, filename)

            # Read the CSV file into a pandas DataFrame, treating '-' as NaN
            df = pd.read_csv(csv_file_path, index_col=0, na_values='-')

            for column in df.columns:
                # Check if the value in 'total assets' row in the column has more than 10 digits
                total_assets_value = df.loc['total assets', column]
                for index in [
        "reserves", "debenture and bond", "borrowings", "deposits", "income tax liability", "other liabilities",
        "total assets", "loan and advancements", "interest income", "interest expense", "net interest income",
        "net fee and commission income", "total operating income", "staff expenses", "operating profit",
        "non operating income expense", "profit for the period"
    ]:
                    if len(str(remove_after_dot(pd.to_numeric(df.loc[index, column], errors='coerce'))))> 10:
                        check=True
                        break


                if check is True:
                    print(f"Denomination in '{filename}', converting to in 1000 for column '{column}'")

                    # Apply specific transformations only if 'total assets' value has more than 10 digits
                    for index in [
        "reserves", "debenture and bond", "borrowings", "deposits", "income tax liability", "other liabilities",
        "total assets", "loan and advancements", "interest income", "interest expense", "net interest income",
        "net fee and commission income", "total operating income", "staff expenses", "operating profit",
        "non operating income expense", "profit for the period", "current tax liabilities","loan and advances to b/fis","loans and advances to customers",
                        "deferred tax liabilities","non operating income","non operating expense",""
    ]:
                        numeric_value = pd.to_numeric(df.loc[index, column], errors='coerce')
                        print('numeric value =' ,numeric_value)
                        if numeric_value is not None:

                            df.loc[index, column] = numeric_value / 1000
                            print(df.loc[index, column])
            # Replace 0 values with empty strings
            df.replace('0.00', '', inplace=True)

            # Save the modified DataFrame back to the CSV file
            df.to_csv(csv_file_path, mode='w', header=True)

            print(f"The new ratios in '{filename}' have been calculated and stored below the existing ones in the CSV file.")

