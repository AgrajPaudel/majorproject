import re

def remove_numbers_and_symbols(input_str):
    # Use regular expression to remove numeric values and symbols between them
    result_str = re.sub(r'\b\d+\b|[,.\d]+', '', input_str)
    # Remove extra whitespaces resulting from the removal
    result_str = ' '.join(result_str.split())
    return result_str.strip()


