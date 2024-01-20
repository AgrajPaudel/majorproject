import spacy
from itertools import product
import json
from plural import  jargoner
import re

# Load the English language model
nlp = spacy.load("en_core_web_sm")

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


# Read existing jargons from jargons.json file
with open('jargons.json', 'r', encoding='utf-8') as jargons_file:
    jargons_data = json.load(jargons_file)

# Iterate over each jargon in the original data and update with generated patterns
for jargon_data in jargons_data["jargons"]:
    head = jargon_data.get("head", "")
    print(head)
    head=remove_parentheses_and_contents(head)
    # Generate patterns from the head (only singular and plural forms)
    patterns = jargoner(head)

    # Update the jargon data with the generated patterns
    jargon_data["pattern"] = [patterns]

    # Print all the patterns created
    print(f"Head: {head}")
    print("Generated Patterns:")
    for pattern in patterns:
        print(f"- {pattern}")
    print("\n")

# Save the updated jargons_data back to jargons.json file
with open('jargons_updated.json', 'w', encoding='utf-8') as updated_jargons_file:
    json.dump(jargons_data, updated_jargons_file, ensure_ascii=False, indent=4)

print("Updated jargons saved to jargons.json.")
