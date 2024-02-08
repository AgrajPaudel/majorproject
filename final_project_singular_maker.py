import spacy

# Load the English language model
nlp = spacy.load('D:/python tesseract/venv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.7.0')

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


