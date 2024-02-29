import os
import pandas as pd


def add_and_store_in_folder(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Create the full path to the CSV file
            csv_file_path = os.path.join(folder_path, filename)

            # Read the CSV file into a pandas DataFrame, treating '-' as NaN
            df = pd.read_csv(csv_file_path, index_col=0, na_values='-')

            # Ensure the specified row headers are present in the DataFrame
            if 'loan and advancements' not in df.index or 'loan and advances to b/fis' not in df.index or 'loans and advances to customers' not in df.index:
                print(f"One or more specified row headers not found in '{filename}'. Skipping.")
                continue

            # Convert values to numeric and fill NaN with 0 for each row individually
            df.loc['loan and advancements'] = pd.to_numeric(df.loc['loan and advancements'], errors='coerce').fillna(0)
            df.loc['loan and advances to b/fis'] = pd.to_numeric(df.loc['loan and advances to b/fis'],
                                                                 errors='coerce').fillna(0)
            df.loc['loans and advances to customers'] = pd.to_numeric(df.loc['loans and advances to customers'],
                                                                      errors='coerce').fillna(0)

            # Add the numeric values and store the result in the target row
            df.loc['loan and advancements'] += df.loc['loan and advances to b/fis'] + df.loc[
                'loans and advances to customers']

            # Non operating income expense addition
            df.loc['non operating income expense'] = pd.to_numeric(df.loc['non operating income expense'],
                                                                   errors='coerce').fillna(0)
            df.loc['non operating income'] = pd.to_numeric(df.loc['non operating income'], errors='coerce').fillna(0)
            df.loc['non operating expense'] = pd.to_numeric(df.loc['non operating expense'], errors='coerce').fillna(0)
            df.loc['non operating income expense'] += df.loc['non operating income'] - df.loc[
                'non operating expense'] + df.loc['non operating income expense']

            # Income tax liability addition
            df.loc['income tax liability'] = pd.to_numeric(df.loc['income tax liability'], errors='coerce').fillna(0)
            df.loc['current tax liabilities'] = pd.to_numeric(df.loc['current tax liabilities'],
                                                              errors='coerce').fillna(0)
            df.loc['deferred tax liabilities'] = pd.to_numeric(df.loc['deferred tax liabilities'],
                                                               errors='coerce').fillna(0)
            df.loc['income tax liability'] += df.loc['current tax liabilities'] + df.loc['deferred tax liabilities'] + \
                                              df.loc['income tax liability']

            # Ratios calculation and handling division by zero

            # List of ratio calculations
            ratio_calculations = [
                ('debt ratio', 'borrowings', 'total assets'),
                ('interest income to assets ratio', 'interest income', 'total assets'),
                ('interest income margin', 'net interest income', 'total assets'),
                ('return on investment', 'profit for the period', 'total assets'),
                ('commission to operating income', 'net fee and commission income', 'total operating income'),
                ('staff expense to income ratio', 'staff expenses', 'total operating income'),
                ('net profit margin', 'profit for the period', 'total operating income'),
                ('income tax portion of operating profit', 'income tax liability', 'profit for the period'),
                ('loan to deposit ratio', 'loan and advancements', 'deposits')
            ]

            for ratio_name, numerator_col, denominator_col in ratio_calculations:
                numerator = pd.to_numeric(df.loc[numerator_col], errors='coerce').fillna(0)
                denominator = pd.to_numeric(df.loc[denominator_col], errors='coerce').fillna(0)  # Replace 0 with 1 to avoid division by zero

                # Calculate ratio and handle division by zero for each column
                if denominator is not 0:
                    ratio = (numerator / denominator) * 100
                else:
                    ratio=0

                # Apply the calculation for each column separately
                for col in ratio.index:
                    value = ratio[col]
                    df.loc[ratio_name, col] = '-' if pd.isna(value) or value == float('inf') or value == float(
                        '-inf') or (
                                                             denominator[col] == 0 and numerator[
                                                         col] == 0) else f'{value:.2f}'

            # Replace 0 values with empty strings
            df.replace('0.00', '', inplace=True)

            # Save the modified DataFrame back to the CSV file
            df.to_csv(csv_file_path, mode='w', header=True)

            print(
                f"The new ratios in '{filename}' have been calculated, multiplied by 100, and stored below the existing ones in the CSV file.")
