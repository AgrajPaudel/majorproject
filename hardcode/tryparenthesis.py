import re

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

