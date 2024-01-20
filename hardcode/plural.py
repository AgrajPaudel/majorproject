import spacy
import inflect

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def combine_lists(list1, list2):
    # Ensure both lists are of the same length
    if len(list1) != len(list2):
        raise ValueError("Input lists must be of the same length")

    # Use zip to combine elements from both lists
    combined_list = [[word1, word2] for word1, word2 in zip(list1, list2)]

    return combined_list

def make_singular_plural_list(input_string):
    # Process the input string
    doc = nlp(input_string)

    # Create an inflect engine
    p = inflect.engine()

    # Create a list of processed tokens
    processed_tokens = []

    # Iterate over each token in the processed doc
    for token in doc:
        # Check if the token contains a dash
        if ' ' in token.text:
            print('space')
        elif token.tag_ == 'NNS':
            # Convert plural to singular
            processed_tokens.append(p.singular_noun(token.text) or token.lemma_)
        elif token.tag_ == 'NN':
            # Convert singular to plural
            processed_tokens.append(p.plural_noun(token.text) or token.text + 's')
        else:
            processed_tokens.append(token.text)

    return processed_tokens

from itertools import product

def generate_combinations(word_lists):
    # Generate all possible combinations of words
    word_combinations = product(*word_lists)

    # Join the combinations to form modified strings
    modified_strings = [' '.join(combination) for combination in word_combinations]

    return modified_strings

def jargoner(input_string):
    print('input_string',input_string)
    dash_string=[]
    if '-' in input_string or '/' in input_string or ':' in input_string or ',' in input_string or '"' in input_string:
        dash_string.append(input_string)
    else:
        # Example usage:
        inputstring = input_string
        list1 = inputstring.split()

        x = make_singular_plural_list(inputstring)
        print(list1)
        print(x)

        result = combine_lists(list1, x)

        # Generate all possible combinations
        result_strings = generate_combinations(result)

        # Print the modified strings
        print("Modified Strings:")
        for result_string in result_strings:
            print(result_string)
        return result_strings



    print('dash string:',dash_string)
    return []


