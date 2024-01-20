import pandas as pd

def process_and_save_csv(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Iterate through columns in forward order
    print("Forward Order:")
    for col in df.columns:
        is_empty = df[col].isnull().all()
        print(f"Column: {col}, Empty: {is_empty}")

        # Delete empty columns
        if is_empty:
            df = df.drop(columns=col)
        elif not is_empty and col!='Particulars':
            break

    # Iterate through columns in reverse order
    print("\nReverse Order:")
    for col in reversed(df.columns):
        is_empty = df[col].isnull().all()
        print(f"Column: {col}, Empty: {is_empty}")

        # Delete empty columns
        if is_empty:
            df = df.drop(columns=col)
        elif not is_empty and col != 'Particulars':
            break

    # Display the updated DataFrame
    print("\nUpdated DataFrame:")
    print(df)

    # Save the updated DataFrame to a new CSV file
    updated_csv_path = 'updated_' + csv_path
    df.to_csv(updated_csv_path, index=False)
    print(f"\nUpdated DataFrame saved to '{updated_csv_path}'.")

# Example usage
csv_file_path = 'sunrisemerged_file_final.csv'  # Replace with the path to your CSV file
process_and_save_csv(csv_file_path)
