import os
import re
import pandas as pd
from python_line_searcher import solver
from pdf2image import convert_from_path
import cv2
from PIL import Image
import pytesseract
from txttotxt import  txt_splitter
from delete_temp_tables import  delete_files
from checkingoverflow import var
import time

def remove_parentheses_and_contents(input_string):
    def keep_if_valid(match):
        content = match.group()
        # Check if the content inside parentheses contains only valid characters
        if re.match(r'^\([-0-9.,%]*\)$', content):
            return content[1:-1]   # Keep the valid content
        else:
            return ''  # Remove the parentheses and invalid content

    result = re.sub(r'\([^)]*\)', keep_if_valid, input_string)
    return result.strip()


def load_bank_data_variables(bank_data_files):
    bank_data_variables = []
    for bank_data_file in bank_data_files:
        print(bank_data_file)
        df_bank = pd.read_csv(bank_data_file, index_col=0)
        bank_data_variables.append(set(df_bank.index))
    return bank_data_variables


def load_bank_data_variablesforstring(bank_data_files):
    bank_data_variables = []
    print(bank_data_files)
    df_bank = pd.read_csv(bank_data_files, index_col=0)
    bank_data_variables.append(set(df_bank.index))
    return bank_data_variables

def count_variable_matches(bank_data_variables, text_files,bank_data_files):
    match_counts = {}

    for text_file in text_files:
        index = 0
        for variables in bank_data_variables:
            matched_variables = set()
            with open(os.path.join('', text_file), 'r', encoding='utf-8') as infile:
                for line in infile:
                    line_str = str(line)
                    line_str=remove_parentheses_and_contents(line_str)
                    for variable in variables:
                        if variable not in matched_variables and str(variable) in line_str and variable != 'nan':
                            matched_variables.add(variable)
                            break
            match_counts[(text_file, bank_data_files[index], str(variables))] = len(matched_variables)
            index=index+1

    return match_counts


def filter_highest_match_counts(match_counts):
    highest_matches = {}

    for key, count in match_counts.items():
        text_file, bank_file, bank_data = key
        if (bank_file, text_file) not in highest_matches or count > highest_matches[(bank_file)][0]:
            if bank_file in highest_matches and count>highest_matches[(bank_file)][0]:
                highest_matches[(bank_file)] = (count, bank_data,text_file)
            elif bank_file not in highest_matches:
                highest_matches[(bank_file)] = (count, bank_data,text_file)

    return highest_matches


def extract_data_from_highest_matches(highest_match_counts):
    data_list = []
    for bank_file,  text_file in highest_match_counts.items():
        data_list.append([bank_file, text_file[2]])
    return data_list



def checker(bank_data_files, text_files,quarter,pdf_path,pdf_file):
    bank_data_variables = load_bank_data_variables(bank_data_files)

    print("Bank Data Variables:")
    for index, variables in enumerate(bank_data_variables):
        modified_variables = []
        for variable in variables:
            modified_variable = remove_parentheses_and_contents(str(variable))
            modified_variables.append(modified_variable)
        bank_data_variables[index] = modified_variables
        print(f"File {index + 1} count: {len(bank_data_variables[index])}")
        print(f"File {index + 1} variables: {bank_data_variables[index]}")

    print("Text files =", text_files)

    found_variables_count = []
    unfound_variables_count = []

    for text_file in text_files:
        # Create a temporary file for output
        temp_file = os.path.join('', text_file + '.temp')

        with open(os.path.join('', text_file), 'r', encoding='utf-8') as infile, open(temp_file, 'w',
                                                                                        encoding='utf-8') as outfile:
            for line in infile:
                line_str = str(line)
                line_str = remove_parentheses_and_contents(line_str)

                found = False
                last_alpha_index = -1  # Initialize the last_alpha_index
                for variables in bank_data_variables:
                    matched_variables = set()
                    for variable in variables:
                        if variable not in matched_variables and str(variable) in line_str and variable != 'nan':
                            found = True
                            found_variables_count.append(variable)
                            matched_variables.add(variable)
                            # Update last_alpha_index only if a match is found in the line
                            last_alpha_index = max(last_alpha_index, line_str.find(variable))
                            break
                    if found:
                        break

                if not found:
                    unfound_variables_count.append(line)

                if found:
                    # Find the sequence following the matched variable that doesn't contain alphabets, spaces only, and stops at the first space

                    last_alpha = line_str[last_alpha_index:]
                    sequence_match = re.finditer(r'[^A-Za-z*&/@#!^?()\s]+ ', last_alpha)
                    for match in sequence_match:
                        sequence = match.group(0).strip()
                        if sequence and len(sequence)<4 and (',' in sequence or '.' in sequence):
                            print(f"invalid - {len(sequence)}")
                        elif sequence and len(sequence)<4 and (char in sequence for char in '0123456789-'):
                            print(f"Found in line: {variable} - Sequence: {sequence} -- {len(sequence)}")
                            break
                        elif sequence and len(sequence)>=4 and not ('.' in sequence or '%' in sequence or ',' in sequence):
                            print(f"invalid --- {len(sequence)}")
                        else:
                            print(f"Found in line: {variable} - Sequence: {sequence} ---- {len(sequence)}")
                            break


                    # Write the line to the temporary file
                    outfile.write(line)

        os.remove(temp_file)

    print("Found Variables Count:")
    for variable in found_variables_count:
        print(variable)

    print("Unfound Variables Count:")
    for line in unfound_variables_count:
        print(line)

    # Count variable matches for all combinations of CSV and text files
    match_counts = count_variable_matches(bank_data_variables, text_files,bank_data_files)
    print("Variable Matches:")

    for (bank_file,text_file,data),count in match_counts.items():
        print(f"Bank File : {bank_file} - Text file={text_file}, count={count}")
    print(match_counts)
    highest_match_counts = filter_highest_match_counts(match_counts)


    print("Highest Match Counts:")
    empty=0
    for (bank_file), count in highest_match_counts.items():
        print(f"Bank File: {bank_file} - Match Count: {count}")
        if(count[0]==0):
            empty=empty+1




    # Extract data from highest_match_counts
    data_list = extract_data_from_highest_matches(highest_match_counts)


    # Print the data list
    for data in data_list:
        bank_file, text_file = data
        print(f"Bank File: {bank_file}, Text File: {text_file}")

    if empty==len(data_list):
        manual_input(bank_data_files,quarter,pdf_path,pdf_file)
    else:
        compare_highest_matches(data_list,bank_data_files,quarter)

    return text_files


################################################################
def compare_highest_matches(data_list,bank_data_files,quarter):

    big_data=[]
    index1=0
    for data in data_list:
        bank_file, text_file= data
        medium_data=[]
        big_data.append(medium_data)

        # Load CSV data for the bank_file
        df_bank = pd.read_csv(bank_file, index_col=0)


        bank_data_variables = load_bank_data_variablesforstring(bank_file)
        print("Bank Data Variables:")
        print(bank_data_variables)

        for index, variables in enumerate(bank_data_variables):
            modified_variables = []
            for variable in variables:
                modified_variable = remove_parentheses_and_contents(str(variable))
                modified_variables.append(modified_variable)
            bank_data_variables[index] = modified_variables


        # Load text data for the text_file
        with open(os.path.join('', text_file), 'r', encoding='utf-8') as infile:
            matched_variables = set()
            for line in infile:
                line_str = str(line)
                line_str = remove_parentheses_and_contents(line_str)
                found = False
                for variables in bank_data_variables:
                    variables=sorted(variables, key=len,reverse=True)
                    for variable in variables:
                        if variable not in matched_variables and variable != 'nan':
                            found = True
                            matched_variables.add(variable)
                            break
                    if found:
                        break



                print(f"matched variable ={matched_variables}")
                print(line_str)
                if found:
                    sequence=solver(text_file,variable)
                    small_data = []
                    small_data.append(variable)
                    small_data.append(sequence)
                    big_data[index1].append(small_data)


        index1=index1+1

    for data in big_data:
        print(data)

    copy_data_to_bank_data(big_data,bank_data_files,quarter)



def manual_input(bank_data_files,quarter,pdf_path,pdf_file):
    quarter_year_input = quarter
    #edit here
    file = os.path.join(pdf_path, pdf_file)
    print('manualinput='+file)
    pages = convert_from_path(os.path.join(file))
    for i, page in enumerate(pages):
        image_path = os.path.join(pdf_path, f'{i + 1}.png')  # Output image file names as 1.png, 2.png, etc.
        page.save(image_path, 'PNG')

        # Get a list of image file paths in the subfolder
    image_files = [f for f in os.listdir(pdf_path) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort the image file paths numerically
    image_files.sort(key=lambda x: int(x.split('.')[0]))

    # Output file path for the subfolder
    txtfile=pdf_file.strip('.pdf')
    output_file = os.path.join(pdf_path, f'{txtfile}.txt')

    with open(output_file, 'w', encoding='utf-8') as output_txt:
        for image_file in image_files:
            image_path = os.path.join(pdf_path, image_file)
            # Read the image using OpenCV for preprocessing
            img = cv2.imread(image_path)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to convert to black and white
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # Use dilation and erosion to enhance text regions
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            dilate = cv2.dilate(thresh, kernel, iterations=1)
            erode = cv2.erode(dilate, kernel, iterations=1)
            text = pytesseract.image_to_string(Image.open(image_path), lang='eng', config='--psm 6')
            output_txt.write(text)
            output_txt.write("\n" + "-" * 78 + "\n")  # Add a line of dashes to separate the content

    outputfiles=txt_splitter(output_file,pdf_path,f'{txtfile}.txt')
    time.sleep(3)
    x = checker(bank_data_files, outputfiles, quarter, pdf_path, pdf_file)

    var()



###################################################


def copy_data_to_bank_data(pdf_data_list, bank_data_files,quarter):
    quarter_year_input = quarter

    # Extract the quarter+year column name
    column_name = " " + quarter_year_input.strip().upper()

    for bank_data_file, data_list in zip(bank_data_files, pdf_data_list):
        df1 = pd.read_csv(bank_data_file, index_col=0)
        csv_list=df1.index.to_list()
        no_parenthesis_csv_list=[]
        index=0
        for item in csv_list:
            no_parenthesis_csv_list.append(remove_parentheses_and_contents(str(csv_list[index])))
            index=index+1
        data_list = sorted(data_list, key=lambda x: len(x[0]), reverse=True)
        print(data_list)
        print(len(data_list))
        print(no_parenthesis_csv_list)
        print(len(no_parenthesis_csv_list))

        for variable, data in data_list:

            variable_exists = variable in no_parenthesis_csv_list




            if variable_exists:
                index_of_list = no_parenthesis_csv_list.index(variable)
                df1.at[csv_list[index_of_list], column_name] = data
                df1.to_csv(bank_data_file, index=True)
                print(f"Data copied to {bank_data_file} for {variable} in {column_name}")
            elif not variable_exists:
                print(f"No matching variable found for {bank_data_file} in {column_name}")
            else:
                print(f"Data for {variable} in {column_name} already exists in {bank_data_file}")





