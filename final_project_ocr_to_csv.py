import final_project_dictionary as dictionary
from final_project_removeparenthesiscontent import remove_parentheses_and_contents
from final_project_singular_maker import make_singular
import os
from final_project_find_content_after import find_content_after_string
from final_project_change_filetype import process_files_in_folder
from final_project_remove_line_numbers import remove_numbers_and_symbols
import pandas as pd
from final_project_number_sequence_comma_dot import convert_numerical_sequence
from final_project_sequenceinsameline import find_sequence
from final_project_remove_forenumber import remove_numeric_prefix


def extract_from_ocr_to_csv(pdf_path, output_folder, txtfile_name):
    print('extraction')
    print(txtfile_name)
    print(output_folder)
    process_files_in_folder(output_folder)
    # Get the filename without the '.txt' part
    filename = os.path.splitext(os.path.basename(txtfile_name))[0]
    print(filename)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=["Particulars"])

    # If CSV file exists, load it
    csv_file_path = os.path.join(output_folder, f"{filename}.csv")
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)

    # Keep track of lines where matches are found
    matched_line_indices = set()

    # Check if the filename column already exists
    filename_column_exists = filename in df.columns

    # Iterate through the variables in the dictionary
    for left_side, right_side_list in dictionary.variables.items():
        # Process left side
        left_side_original = left_side  # Store the original variable name
        left_side_processed = make_singular(
            remove_parentheses_and_contents(left_side.strip("*-").replace("&", "and").replace(" ", "")))

        # Process right sides outside the loop
        right_sides_processed = [
            make_singular(remove_parentheses_and_contents(right_side.strip("*-").replace("&", "and").replace(" ", "")))
            for right_side in right_side_list]
        print(right_sides_processed)

        # Iterate through the lines of the text file
        with open(txtfile_name, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

            for line_num, line in enumerate(lines[1:], start=1):  # Exclude the first line from processing
                # Skip lines that have already been matched
                if line_num in matched_line_indices:
                    continue

                line_str = remove_parentheses_and_contents(line.replace("&", "and"))
                line_str = line_str.replace('*', '')
                line_str = line_str.replace(':', '')
                line_str = line_str.replace('%', '')
                line_str = remove_numeric_prefix(line_str)
                original_line = line_str
                line_str = line_str.replace('-', '')
                line_str = remove_numbers_and_symbols(line_str)

                line_str = line_str.replace(" ", "")
                line_str = line_str.replace("(", "")
                line_str = line_str.replace(")", "")
                line_str = line_str.strip()

                line_str_processed = make_singular(line_str)
                print(line_str_processed.lower())
                # Check if the processed left side matches any processed right side in the list
                if any(right_side_processed.lower() == line_str_processed.lower() for right_side_processed in
                       right_sides_processed):
                    print(line_str_processed.lower(), 'is given as ....')
                    # Update the set of matched line indices
                    matched_line_indices.add(line_num)

                    try:
                        check = remove_numbers_and_symbols(original_line)
                        check = remove_parentheses_and_contents(check)
                        print('original line=', check)
                        check = check.strip()
                        content = find_content_after_string(txtfile_name, check)
                        sequence = find_sequence(content)
                        sequence = convert_numerical_sequence(sequence)
                        sequence = str(sequence).replace('%','')
                        sequence = str(sequence).replace(',', '')
                        df = df._append({"Particulars": left_side_original, filename: sequence},
                                       ignore_index=True)

                    except IndexError:
                        print("Line not found.")

    # Print list of variables not found
    not_found_variables = set(dictionary.variables.keys()) - set(df["Particulars"])
    print("Variables not found:", not_found_variables)

    # Append not found variables to the DataFrame
    for not_found_variable in not_found_variables:
        df = df._append({"Particulars": not_found_variable, filename: "-"}, ignore_index=True)

    # Save the DataFrame to a CSV file in the specified folder
    df.to_csv(csv_file_path, index=False)

    print("Ocr complete")
