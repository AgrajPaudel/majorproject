from file_operations import bank_file_maker
import os
import re
import pandas as pd
import chardet
from chardet.universaldetector import UniversalDetector

import shutil


import spacy


def detect_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
    detector.close()

    # Return the detected encoding or a default encoding (e.g., 'utf-8')
    return detector.result['encoding'] or 'utf-8'


def convert_to_utf8(file_path, source_encoding):
    with open(file_path, 'r', encoding=source_encoding, errors='replace') as infile:
        content = infile.read()

    with open(file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            source_encoding = detect_encoding(file_path)

            if source_encoding.lower() != 'utf-8':
                print(f"Converting {filename} from {source_encoding} to UTF-8.")
                convert_to_utf8(file_path, source_encoding)
            else:
                print(f"{filename} is already in UTF-8.")

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


def find_content_after_string(file_path, search_string):
    search_string=search_string.lower()
    search_string=search_string.replace('*','')
    search_string=search_string.replace('-', '')
    search_string = search_string.replace('(%)', '')
    search_string = search_string.replace('%', '')
    x='Rs.'
    search_string = search_string.replace(x.lower(), '')
    search_string=remove_parentheses_and_contents(search_string)
    search_string_processed = search_string.replace(' ', '')  # Remove spaces from the search string

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            line=line.replace('*', '')
            line=line.replace('-', '')
            line = line.replace('(%)', '')
            line = line.replace('%', '')
            line = remove_parentheses_and_contents(line)
            line=line.lower()
            if search_string_processed in line.replace(' ', ''):

                index = line.replace(' ', '').find(search_string_processed)

                found_content = line[index + len(search_string):].strip()

                found_content=remove_parentheses_and_contents(found_content)

                return found_content
    return ''  # If the search string is not found in any line





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

def find_sequence(string):
    string=string.replace(':','')

    print('string=',string)
    sequence_match = re.finditer(r'[0-9.,%)(]+', string.strip())
    matches = [match.group() for match in sequence_match]
    print("Matches found:", matches[0])
    sequence=matches[0]


    if  dash_searcher(sequence) == False and (sequence!='(%)' and sequence!='()' and sequence!='%' and sequence!='.') :

        return sequence

def dash_searcher(string):
    first = False
    second = False
    dash = False

    for x in string:
        if x == '-' or x.lower() in 'abcdefghijklmnopqrstuvwxyz':
            dash = True
        elif x == '(':
            first = True
        elif x == ')':
            second = True

    if dash == True and (first == True or second == True):
        return True
    elif (second == True and first == False) or (first == True and second == False):
        return True
    else:
        return False


def update_single_page_pdfs(bankfile_list, txt_folder):
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
        user_input_column=' '+txt_file.strip('.txt')
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
                line_str=line_str.strip()
                line_str=line_str.replace('*','')
                line_str=line_str.replace('-','')
                line_str=line_str.replace(':','')
                line_str = line_str.replace("&", "and")

                # Check if any variable is in the line
                for variable, no_parenthesis_variable in zip(variables, no_parenthesis_csv_list):

                    singular_csv_data = make_singular(no_parenthesis_variable)
                    singular_csv_data=singular_csv_data.replace('*','')
                    singular_csv_data=singular_csv_data.replace('-', '')
                    singular_data = make_singular(line_str)
                    singular_csv_data=singular_csv_data.replace(' ','')
                    singular_data=singular_data.replace(' ','')
                    if singular_csv_data.lower() in singular_data.lower():
                        found_variable = variable
                        print(f"Found variable: {found_variable}")
                        print(line_str)

                        try:
                            content=find_content_after_string(txt_path,no_parenthesis_variable)
                            print('content=',content)
                            sequence=find_sequence(content)
                            print('sequence=',sequence)
                            df.at[variables.index(found_variable),user_input_column]=sequence





                        except IndexError:
                            print("Line not found.")

        os.remove(temp_file)
        df.to_csv(bankfile_list[4], index=False)
        # Save the updated DataFrame back to CSV files




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



bankfile_list=bank_file_maker()
current_dir = os.getcwd()
# List all files in the current directory

path=os.path.join(current_dir,'z output')
files_show = os.listdir(path)
# Iterate over all PDF files




files=[file for file in files_show if file.lower().endswith('.txt')]
print(files)
process_files_in_folder('z output')
update_single_page_pdfs(bankfile_list,'z output')










delete_directory_contents('z output')