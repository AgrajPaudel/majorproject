
from file_operations import bank_file_maker
import os
import re
import pandas as pd

import fitz
from zpythonpdftotxtpagewise import extract_text_from_pdf
import shutil


import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")
def make_singular(input_string):


    # Process the input string
    doc = nlp(input_string)

    # Create a list of processed tokens
    processed_tokens = []

    # Iterate over each token in the processed doc
    for token in doc:
        # Check if the token is a plural noun
        if token.tag_ == 'NNS':
            # Convert plural to singular
            singular_form = token.lemma_
            processed_tokens.append(singular_form)
        else:
            processed_tokens.append(token.text)

    # Join the processed tokens to form the modified string
    modified_string = ' '.join(processed_tokens)

    return modified_string







bankfile_list=bank_file_maker()


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

    index_of_first=result.find(')')
    index_of_open=result.find('(')


    if index_of_first<index_of_open:
        result = result[index_of_first+1:]


    index_of_close = result.rfind(')')
    index_of_last = result.rfind('(')
    if index_of_last>index_of_close:

        result=result[:index_of_last]

    return result.strip()

# Define a key function to extract the numerical part from each file name
def extract_number(filename):
    match = re.search(r'_\d+', filename)
    return int(match.group()[1:]) if match else float('inf')

def update_csv_from_txt(bankfile_list, txt_folder, condition_phrases, user_input_column):
    txt_files = [f for f in os.listdir(txt_folder) if f.lower().endswith(('.txt'))]
    txt_files.sort(key=extract_number)
    print(txt_files)
    index=0
    # Iterate through each CSV file
    done_or_not=[]
    for x in bankfile_list:
        done_or_not.append(False)

    for index,csv_file_path in enumerate(bankfile_list):
        df=pd.read_csv(csv_file_path)
        variables = df.iloc[:, 0].tolist()
        no_parenthesis_csv_list = []

        print(variables)
        for variable in variables:
            nobracket=remove_parentheses_and_contents(variable)
            no_parenthesis_csv_list.append(nobracket)
        print(index)
        # Extract the CSV file name without extension
        for txt_file in txt_files:
            print('is currently used',txt_file)

            txt_path=os.path.join(txt_folder,txt_file)
            temp_file = os.path.join('',txt_path.strip('.txt') +'.temp')
            with open(os.path.join('', txt_path), 'r', encoding='utf-8') as infile, open(temp_file, 'w',
                                                                                          encoding='utf-8') as outfile:

                txt_content = infile.read()
                if(index<=3):
                    condition_phrase = condition_phrases[index]
                else:
                    break
                condition_phrase=condition_phrase.lower()
                pattern = re.compile(re.escape(condition_phrase) )
                if pattern.search(txt_content.lower()) and done_or_not[index]==False:
                    done_or_not[index]=True
                    print('caught')
                    lines = txt_content.split('\n')



                    for line_num, line in enumerate(lines):
                        line_str = str(line)
                        line_str = remove_parentheses_and_contents(line_str)
                        line_str=line_str.strip()
                        line_str = line_str.replace("&", "and")
                        line_str=line_str.replace(" ",'')
                        # Check if any variable is in the line
                        for variable, no_parenthesis_variable in zip(variables, no_parenthesis_csv_list):
                            no_parenthesis_variable=no_parenthesis_variable.replace(' ',"")
                            singular_csv_data=make_singular(no_parenthesis_variable)
                            singular_data=make_singular(line_str)
                            if singular_csv_data.lower() == singular_data.lower():
                                found_variable = variable
                                print(f"Found variable: {found_variable}")
                                print(line_str)

                                # Print the value of the line below the found line
                                try:
                                    line_below = lines[line_num + 1].strip()
                                    line_below=remove_parentheses_and_contents(line_below)

                                    # yaha issue cha
                                    # If the loop finishes without finding a suitable line, print a message
                                    while not line_below:
                                        # Move to the next line
                                        # yeta halne try
                                        line_num += 1
                                        line_below = lines[line_num].strip()
                                        print('bwlooooo', line_below)

                                    # Check if the line below contains alphabets
                                    if any(char.isalpha() for char in line_below):
                                        print("Line below contains alphabets. Ignored.")
                                        # Stop searching once a line with alphabets is found
                                        # Check if the line below contains a numerical sequence
                                    elif any(char.isdigit() or char == '-' for char in line_below):
                                        # Store the line with a numerical sequence in the CSV
                                        df.at[variables.index(found_variable), user_input_column] = line_below
                                        print('line num===', line_below)
                                        # Stop searching once a suitable line is found

                                except IndexError:
                                    print("Line below not found.")

            os.remove(temp_file)
            # Save the updated DataFrame back to CSV files
        df.to_csv(csv_file_path, index=False)

    if True not in done_or_not:
        update_single_page_pdfs(bankfile_list, txt_folder, user_input_column)

def update_single_page_pdfs(bankfile_list, txt_folder, user_input_column):
    txt_files = [f for f in os.listdir(txt_folder) if f.lower().endswith(('.txt'))]
    print(txt_files)
    index = 0


    df = pd.read_csv(bankfile_list[4])
    variables = df.iloc[:, 0].tolist()
    no_parenthesis_csv_list = []



    print(variables)
    for variable in variables:
        nobracket = remove_parentheses_and_contents(variable)
        no_parenthesis_csv_list.append(nobracket)
    print(index)
    # Extract the CSV file name without extension
    for txt_file in txt_files:
        print('is currently used', txt_file)

        txt_path = os.path.join(txt_folder, txt_file)
        temp_file = os.path.join('', txt_path.strip('.txt') + '.temp')
        with open(os.path.join('', txt_path), 'r', encoding='utf-8') as infile, open(temp_file, 'w',
                                                                                     encoding='utf-8') as outfile:

            txt_content = infile.read()




            print('caught')
            lines = txt_content.split('\n')

            for line_num, line in enumerate(lines):
                line_str = str(line)

                line_str = remove_parentheses_and_contents(line_str)
                line_str = line_str.strip()
                line_str = line_str.replace("&", "and")
                # Check if any variable is in the line
                for variable, no_parenthesis_variable in zip(variables, no_parenthesis_csv_list):
                    singular_csv_data = make_singular(no_parenthesis_variable)
                    singular_data = make_singular(line_str)
                    if singular_csv_data.lower() in singular_data.lower():
                        found_variable = variable
                        print(f"Found variable: {found_variable}")
                        print(line_str)

                        try:
                            line_below = lines[line_num + 1].strip()
                            line_below = remove_parentheses_and_contents(line_below)
                            # yaha issue cha
                            # If the loop finishes without finding a suitable line, print a message
                            while not line_below:
                                # Move to the next line
                                # yeta halne try
                                line_num += 1
                                line_below = lines[line_num].strip()
                                print('bwlooooo', line_below)

                            # Check if the line below contains alphabets
                            if any(char.isalpha() for char in line_below):
                                print("Line below contains alphabets. Ignored.")
                                # Stop searching once a line with alphabets is found
                                # Check if the line below contains a numerical sequence
                            elif any(char.isdigit() or char == '-' for char in line_below):
                                # Store the line with a numerical sequence in the CSV
                                df.at[variables.index(found_variable), user_input_column] = line_below
                                print('line num===', line_below)
                                # Stop searching once a suitable line is found

                        except IndexError:
                            print("Line below not found.")

        os.remove(temp_file)
        # Save the updated DataFrame back to CSV files
    df.to_csv(bankfile_list[4], index=False)



def delete_directory_contents(directory_path):
    try:
        # Iterate over all files and subdirectories in the given directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Check if the item is a file or directory
            if os.path.isfile(item_path):
                # If it's a file, delete it
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                # If it's a directory, delete it recursively
                shutil.rmtree(item_path)

        print(f"Contents of {directory_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting contents of {directory_path}: {e}")


def rename_pdf_for_ocr(pdf_path):
    base_name = os.path.basename(pdf_path)
    file_name, file_extension = os.path.splitext(base_name)
    ocr_pdf_path = f"{file_name} ocr{file_extension}"
    os.rename(pdf_path, ocr_pdf_path)
    return ocr_pdf_path

current_dir = os.getcwd()
# List all files in the current directory
files = os.listdir(current_dir)
# Filter PDF files
pdf_files = [file for file in files if file.lower().endswith('.pdf')]

# Iterate over all PDF files
for pdf_file_name in pdf_files:
    delete_directory_contents('z output')

    pdf_file_path = os.path.join(current_dir, pdf_file_name)
    pdf_file_name=pdf_file_name.lower()
    user_input_column = ' ' + pdf_file_name.strip('.pdf')
    content = extract_text_from_pdf(pdf_file_path, 'z output/')

    if not content.strip():  # Check if the extracted text is empty
        # Rename the PDF file to include "ocr" in the filename
        pdf_file_path = rename_pdf_for_ocr(pdf_file_path)

    # Check the number of pages in the PDF
    with open(pdf_file_path, 'rb') as pdf_file:
        # Check the number of pages in the PDF using PyMuPDF (fitz)
        pdf_document = fitz.open(pdf_file_path)
        num_pages = pdf_document.page_count

        if num_pages > 4:
            # Call update_csv_from_txt for PDFs with more than 4 pages
            update_csv_from_txt(bankfile_list, 'z output', ['STATEMENT OF FINANCIAL POSITION','STATEMENT OF PROFIT OR LOSS','Ratios as per NRB Directive','STATEMENT OF CASH FLOW'], user_input_column)
        else:
            # Call update_single_page_pdfs for PDFs with 4 or fewer pages
            update_single_page_pdfs(bankfile_list, 'z output', user_input_column)




