import os
import pandas as pd
import re
from merge_row import merge_row

def remove_parentheses_and_contents(input_string):

    def keep_if_valid(match):
        content = match.group()

        # Check if the content inside parentheses contains only valid characters
        if re.match(r'^\([-0-9.,%]*\)$', content):
            return content[1:-1]   # Keep the valid content
        else:
            return ''  # Remove the parentheses and invalid content

    # Modify regex pattern to handle incomplete pairs at the beginning or end
    input_string = re.sub(r'\([^)]*\([^)]*\)[^)]*\)', '', input_string)

    result = re.sub(r'\([^)]*\)', keep_if_valid, input_string)

    index_of_first = result.find(')')
    index_of_open = result.find('(')

    if index_of_first < index_of_open:
        result = result[index_of_first + 1:]

    index_of_close = result.rfind(')')
    index_of_last = result.rfind('(')
    if index_of_last > index_of_close:
        result = result[:index_of_last]

    return result.strip()

def merge_files_in_folder(folder_path, output_file_name="merged_file.csv"):
    # Step 1: Read Data from Files
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]
    dataframes = [pd.read_csv(file) for file in file_paths]

    # Check if the column headers are the same in all CSV files
    first_column_headers = dataframes[0].columns.tolist()
    if not all(df.columns.tolist() == first_column_headers for df in dataframes):
        print("Column headers in CSV files are not identical:")
        for i, df in enumerate(dataframes):
            print(f"File {file_paths[i]}:")
            print(df.columns.tolist())
            print()
        raise ValueError("Column headers in CSV files must be identical.")

    # Print the column headers of the merged DataFrame
    print("Column headers of Merged DataFrame:")
    print(first_column_headers)
    print()

    # Step 2: Extract and Set Common Column Headers
    common_column_headers = first_column_headers
    common_column_headers.pop(0)
    # Print the common column headers
    print("Common Column Headers:")
    print(common_column_headers)
    print()

    # Step 2: Define Variables
    variables = [
        "reserves",
        "reserve and surplus",
        "debenture and bond",
        "borrowings",
        "deferred tax liabilities",
        "current tax liabilities",
        "loan and advances to bank and financial institutions",
        #"loans and advances to customers",
        "non-operating income",
        "non-operating expense",
        "non operating income/expense",
        "non operating income/expenses",
        # "income tax liability": "current tax liability + deferred tax liability",
        # "loan and advancements": "loan and advances to b/fis + loans and advances to customers",
        # "non-operating income - non-operating expense": "non operating income/expense",

        "deposits from customers",
        "deposits",
        "income tax liability",
        "other liabilities",
        "total assets",
        "loans and advances",
        "loan and advancements",
        "interest income",
        "interest expense",
        "net interest income",
        "net fee and commission income",
        "fee commission and discount",
        "fees commission and discount",
        "fees, commission and discount",
        "total operating income",
        "personnel expenses",
        "staff expenses",
        "operating profit",
        "non operating income/expense",
        "profit for the period",
        "net profit/loss",
        "capital fund to rwa",
        "non performing loan to total loan",
        "non-performing loan to total loan",
        "npl to total loan",
        "total loan loss provision to npl",
        "total loan loss provision to total npl",
        "cost of deposit",
        "cost of fund",
        "base rate",
        "net interest spread",
        "market share price",
        "market value per share",
        "return on equity",
        "return on total assets",
        "return on total net assets",
        "ccd ratio",
        "c/d ratio",
        "cd ratio",
        "credit to deposit ratio",
    ]

    # Print the resulting row headers
    print("Resulting Row Headers:")
    print(variables)
    print()

    # Create Empty DataFrame with Common Column Headers
    empty_df = pd.DataFrame(index=variables, columns=common_column_headers)

    # Step 4: Fill in Data
    for variable in variables:
        conflicting_files = []
        for i, df in enumerate(dataframes):
            if variable in df['Particulars'].apply(remove_parentheses_and_contents).str.lower().str.strip().values:
                print(variable)
                row_index = empty_df.index.get_loc(variable)
                for col in first_column_headers:
                    cell_value = \
                        df[df['Particulars'].apply(remove_parentheses_and_contents).str.lower().str.strip() == variable][
                            col].values.flatten()[0]
                    if pd.notna(cell_value):
                        if pd.notna(empty_df.at[variable, col]) and str(empty_df.at[variable, col]).strip() != str(
                                cell_value).strip():
                            conflicting_files.append((file_paths[i], col))
                            print(
                                f"Conflict in file {file_paths[i]}, column {col}: {empty_df.at[variable, col]} vs {cell_value}")
                        else:
                            if isinstance(cell_value, str):
                                print(cell_value)
                                empty_df.at[variable, col] = cell_value
                            else:
                                print(cell_value)
                                empty_df.at[variable, col] = str(cell_value)

        if conflicting_files:
            raise ValueError(f"Conflicting values for '{variable}' in columns of files: {conflicting_files}")

    # Step 5: Write to CSV without Extra Space before "Particulars"
    output_file_path = os.path.join(folder_path,folder_path+ output_file_name)
    empty_df.to_csv(output_file_path, index=True, header=True, sep=',')
    print(f"File '{output_file_path}' created.")
    merge_row(output_file_path)


# Example Usage
user_folder = input("Enter the folder path containing your files: ")
merge_files_in_folder(user_folder)
