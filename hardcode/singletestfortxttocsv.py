from file_operations import bank_file_maker
import os
import re
import pandas as pd
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


def update_csv_from_txt(bankfile_list, txt_folder, condition_phrases, user_input_column):
    txt_files = [f for f in os.listdir(txt_folder) if f.lower().endswith(('.txt'))]
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
                    condition_phrase=condition_phrases[3]
                condition_phrase=condition_phrase.lower()
                pattern = re.compile(r'\b' + re.escape(condition_phrase) + r'\b')
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



#yaha issue cha
                                    # If the loop finishes without finding a suitable line, print a message
                                    while not line_below:

                                     # Move to the next line
                                        #yeta halne try
                                        line_num += 1
                                        line_below = lines[line_num].strip()
                                        print('bwlooooo', line_below)

                                     # Check if the line below contains alphabets
                                    if any(char.isalpha() for char in line_below):
                                        print("Line below contains alphabets. Ignored.")
                                        # Stop searching once a line with alphabets is found
                                        # Check if the line below contains a numerical sequence
                                    elif any(char.isdigit() or char =='-' for char in line_below):
                                        # Store the line with a numerical sequence in the CSV
                                        df.at[variables.index(found_variable), user_input_column] = line_below
                                        print('line num===', line_below)
                                          # Stop searching once a suitable line is found

                                except IndexError:
                                    print("Line below not found.")

            os.remove(temp_file)
            # Save the updated DataFrame back to CSV files
        df.to_csv(csv_file_path, index=False)


bankfile_list=bank_file_maker()
update_csv_from_txt(bankfile_list, 'z output',
                    ['CONDENSED STATEMENT OF FINANCIAL POSITION', 'CONDENSED STATEMENT OF PROFIT OR LOSS',
                     'Ratios as per NRB Directive', 'CONDENSED STATEMENT OF CASH FLOWS'], ' Q4 2079')

