import re

def remove_numeric_prefix(line):
    # Define a regular expression pattern to match numeric prefix after an optional alphabet and before the decimal point
    pattern = re.compile(r'^[a-zA-Z]*\.\d+(\.\d+)?(?=[^a-zA-Z0-9,.%])|^\d+(\.\d+)?(?=[^a-zA-Z0-9,.%])|[a-zA-Z]+\.')

    # Use the pattern to find and replace the numeric prefix
    line_without_numeric_prefix = pattern.sub('', line)

    return line_without_numeric_prefix

# Example usage:
line_with_alphabets = "1.1  total assets 1213123131 2131312"
line_with_mixed_alphabets = "a.a total assets 12345645353"
line_with_only_alphabets = "a. total assets 12345645353"
line_without_alphabets = "1234567890"

result_with_alphabets = remove_numeric_prefix(line_with_alphabets)
result_with_mixed_alphabets = remove_numeric_prefix(line_with_mixed_alphabets)
result_with_only_alphabets = remove_numeric_prefix(line_with_only_alphabets)
result_without_alphabets = remove_numeric_prefix(line_without_alphabets)

print(result_with_alphabets)
print(result_with_mixed_alphabets)
print(result_with_only_alphabets)
print(result_without_alphabets)
