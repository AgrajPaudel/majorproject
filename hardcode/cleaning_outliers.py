import csv
import os
import re

def clean_data(value):
    # Remove anything other than %, ,, ., numbers, and space
    value = re.sub(r'[^0-9%,. ]', '', value)

    # If there is a space, only consider the value before the space
    if ' ' in value:
        value = value.split(' ')[0]

    return value

def process_csv(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(file)
                with open(file_path, 'r') as csv_input, open(file_path + '.temp', 'w', newline='') as csv_output:
                    reader = csv.reader(csv_input)
                    writer = csv.writer(csv_output)

                    # Process header row
                    header = next(reader)
                    writer.writerow(header)

                    for row in reader:
                        try:
                            cleaned_row = [row[0]]  # First column remains unchanged

                            for value in row[1:]:
                                # Clean data based on specified conditions
                                cleaned_value = clean_data(value)
                                cleaned_row.append(cleaned_value)

                            # Write the cleaned row to the temporary output file
                            writer.writerow(cleaned_row)

                        except IndexError:
                            print(f"IndexError in file {file}: Skipping row {row}")

                # Replace the original file with the cleaned data
                os.replace(file_path + '.temp', file_path)

if __name__ == "__main__":
    input_folder_path = '.best'  # Replace with your input folder path

    process_csv(input_folder_path)
