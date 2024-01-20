import re

def find_sequence(string):
    string=string.replace(':','')

    print('string=',string)
    sequence_match = re.finditer(r'[0-9.,%)(]+', string.strip())
    matches = [match.group() for match in sequence_match]
    print("Matches found:", matches[0])
    sequence=matches[0]


    if  dash_searcher(sequence) == False and (sequence!='(%)' and sequence!='()' and sequence!='%' and sequence!='.') :

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

