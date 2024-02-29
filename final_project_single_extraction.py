import final_project_dictionary as dictionary
from final_project_removeparenthesiscontent import remove_parentheses_and_contents
from final_project_singular_maker import make_singular
from final_project_ocr_for_pdf import ocr_for_pdf
import os
from final_project_remove_forenumber import remove_numeric_prefix
import pandas as pd
import spacy

# Load the English language model
nlp = spacy.load('D:/python tesseract/venv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.7.0')


def extract_text_and_store_csv(txt_file, csv_folder, pdf_path):
    if_ocr=False
    # Get the filename without the '.txt' part
    filename = os.path.splitext(os.path.basename(txt_file))[0]

    # Create an empty DataFrame
    df = pd.DataFrame(columns=["Particulars"])

    # If CSV file exists, load it
    csv_file_path = os.path.join(csv_folder, f"{filename}.csv")
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
        right_sides_processed = [make_singular(
            remove_parentheses_and_contents(right_side.strip("*-").replace("&", "and").replace(" ", " "))) for
            right_side in right_side_list]


        # Iterate through the lines of the text file
        with open(txt_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

            for line_num, line in enumerate(lines[1:], start=1):  # Exclude the first line from processing
                # Skip lines that have already been matched
                if line_num in matched_line_indices:
                    continue
                line_str = remove_parentheses_and_contents(line.replace("&", "and"))
                line_str=line_str.lower()
                line_str = line_str.replace('-', '')
                line_str = remove_numeric_prefix(line_str)
                line_str = line_str.replace(" ", " ")
                line_str = line_str.strip()
                line_str_processed = make_singular(line_str)


                # Check if the processed left side matches any processed right side in the list
                if any(right_side_processed.lower() == line_str_processed.lower() for right_side_processed in
                       right_sides_processed):

                    # Update the set of matched line indices
                    matched_line_indices.add(line_num)

                    try:
                        # Get the line below
                        line_below = lines[line_num + 1].strip()
                        line_below_processed = line_below.strip()

                        while not line_below:
                            line_num += 1
                            line_below = lines[line_num].strip()


                        # Check if the line below contains alphabets
                        if any(char.isalpha() for char in line_below_processed):
                            print("Line below contains alphabets. Ignored.")
                        elif any(char.isdigit() or char == '-' or char == ' ' for char in line_below_processed):
                            # Check if the variable is already present in the DataFrame
                            existing_entry_indices = df.index[
                                df["Particulars"].str.lower() == left_side_processed.lower()].tolist()
                            if existing_entry_indices:
                                # Update existing entries
                                for existing_entry_index in existing_entry_indices:
                                    line_below_processed = line_below_processed.replace('%', '')
                                    line_below_processed = line_below_processed.replace(',', '')
                                    # Take the first part of the string before space
                                    line_below_processed = line_below_processed.split()[0]
                                    df.at[existing_entry_index, filename] = line_below_processed
                            else:
                                # Append the data to the DataFrame
                                # Take the first part of the string before space
                                line_below_processed = line_below_processed.split()[0]
                                df = df._append({"Particulars": left_side_original, filename: line_below_processed},
                                                ignore_index=True)

                                break


                    except IndexError:
                        print("Line below not found.")

    # Save the DataFrame to a CSV file in the specified folder
    df.to_csv(csv_file_path, index=False)


    not_found_variables = set(dictionary.variables.keys()) - set(df["Particulars"])


    # Check if any variables were found
    if not df.empty:
        print("Variables found. No need to execute OCR.")
    else:

        ocr_for_pdf(pdf_path=pdf_path, output_folder=csv_folder, filename=txt_file)
        if_ocr=True


    # Add not found variables to the DataFrame
    if if_ocr==False:
        not_found_df = pd.DataFrame({"Particulars": list(not_found_variables), filename: ['-'] * len(not_found_variables)})

        # Append not found variables to the CSV file
        with open(csv_file_path, 'a', newline='') as csvfile:
            not_found_df.to_csv(csvfile, index=False, header=False, mode='a')
