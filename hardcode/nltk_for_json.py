import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re







synonyms = []



wordnet_lemmatizer = WordNetLemmatizer()

# Tokenize the input string
input_string = input('Enter data')
tokens = nltk.word_tokenize(input_string)

# Lemmatize each token to find the root form
lemmatized = [wordnet_lemmatizer.lemmatize(token) for token in tokens]

for lemmat in lemmatized:
    for syn in wordnet.synsets(lemmat):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())


print(set(synonyms))
