import re

def convert_numerical_sequence(input_str):
    # Check if input_str is None or empty
    if input_str is None or not input_str:
        return input_str

    # Check if the sequence has more than three digits after a dot or more than one dot
    if input_str.count('.') > 1 or re.search(r'\.\d{3,}', input_str):
        # Replace dots with commas for the entire sequence
        converted_sequence = input_str.replace('.', ',')
        return converted_sequence
    else:
        return input_str
