import pandas as pd

def merge_csv_files(file1_path, file2_path, output_path):
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1_path, index_col=0)
    df2 = pd.read_csv(file2_path, index_col=0)

    # Check if the columns (quarters/years) are the same in both files
    if not df1.columns.equals(df2.columns):
        raise ValueError("Columns (quarters/years) are not identical in both files.")

    # Identify common variables
    common_variables = df1.index.intersection(df2.index)

    # Merge the data for common variables
    merged_df = pd.DataFrame(index=common_variables, columns=df1.columns)

    for variable in common_variables:
        for quarter in df1.columns:
            value_file1 = df1.loc[variable, quarter]
            value_file2 = df2.loc[variable, quarter]

            # Handle merging conditions
            if pd.notna(value_file1) and pd.isna(value_file2):
                merged_df.loc[variable, quarter] = value_file1
            elif pd.isna(value_file1) and pd.notna(value_file2):
                merged_df.loc[variable, quarter] = value_file2
            elif pd.isna(value_file1) and pd.isna(value_file2):
                merged_df.loc[variable, quarter] = pd.NA
            elif value_file1 == value_file2:
                merged_df.loc[variable, quarter] = value_file1
            else:
                # Use the value from file2 in case of conflict
                merged_df.loc[variable, quarter] = value_file2

    # Concatenate data for variables present only in one file
    unique_variables_df1 = df1.drop(common_variables)
    unique_variables_df2 = df2.drop(common_variables)
    merged_df = pd.concat([merged_df, unique_variables_df1, unique_variables_df2])

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv(output_path)

    print("Merge successful. Merged data saved to", output_path)

    return output_path

# Example usage
file1_path = "everestocrdata5.csv"
file2_path = "Everestdata5.csv"
output_path = "Everestmerged.csv"

try:
    merged_file_path = merge_csv_files(file1_path, file2_path, output_path)
except ValueError as e:
    print(f"Error: {e}")
