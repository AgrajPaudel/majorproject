import re
from final_project_removeparenthesiscontent import  remove_parentheses_and_contents

def find_content_after_string(file_path, search_string):
    search_string=search_string.lower()
    search_string=search_string.replace('*','')
    search_string = search_string.replace('(%)', '')
    search_string = search_string.replace('%', '')
    x='Rs.'
    search_string = search_string.replace(x.lower(), '')
    search_string=remove_parentheses_and_contents(search_string)
    search_string = search_string.replace('-', '')
    search_string_processed = search_string.replace(' ', '')  # Remove spaces from the search string


    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:

            line = line.strip()  # Remove leading/trailing whitespaces

            line=line.replace('*', '')
            line=line.replace(',','')
            line = line.replace('(%)', '')
            line = line.replace('%', '')
            line = remove_parentheses_and_contents(line)
            line = line.replace('-', '')
            line=line.lower()

            if search_string_processed in line.replace(' ', ''):
                print('found')
                index = line.replace(' ', '').find(search_string_processed)

                found_content = line[index + len(search_string):].strip()
                print('found_content=',found_content)
                found_content=remove_parentheses_and_contents(found_content)

                return found_content
    return ''  # If the search string is not found in any line

