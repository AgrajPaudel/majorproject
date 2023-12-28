import re

def remove_parentheses_and_contents(input_string):
    def keep_if_valid(match):


        content = match.group()
        print("content="+str(content))

        # Check if the content inside parentheses contains only valid characters
        if re.match(r'^\([0-9.,%]*\)$', content) and '-' not in str(content) :
            print('contesadnt='+content)
            return content[1:-1]   # Keep the valid content
        else:
            return ''  # Remove the parentheses and invalid content

    result = re.sub(r'\([^)]*\)', keep_if_valid, input_string)
    return result.strip()

import re

def find_sequence(string):
    sequence_match = re.finditer(r'[0-9.,%)(]+', string)
    for match in sequence_match:
        sequence = match.group(0).strip()

        # If the sequence doesn't contain any alphanumeric characters


        if  dash_searcher(sequence) == False and (sequence!='(%)' and sequence!='()' and sequence!='%' and sequence!='.') :
            print(sequence)
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


def find_content_after_string(file_path, search_string):
    search_string=search_string.lower()
    search_string_processed = search_string.replace(' ', '')  # Remove spaces from the search string
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_stripped = line.strip()  # Remove leading/trailing whitespaces
            line = remove_parentheses_and_contents(line)
            print("removed "+line)
            line=line.lower()
            if search_string_processed in line.replace(' ', ''):
                index = line.replace(' ', '').find(search_string_processed)
                found_content = line_stripped[index + len(search_string)-1:].strip()
                found_content=remove_parentheses_and_contents(found_content)
                return found_content
    return ''  # If the search string is not found in any line


def solver(file_path,search_word):



    result = find_content_after_string(file_path, search_word)
    sequence=find_sequence(result)
    print(f"Content found after '{search_word}': '{result}'")
    print(sequence)
    return sequence


solver('Q1 2073.txt','Total Capital and liabilities')