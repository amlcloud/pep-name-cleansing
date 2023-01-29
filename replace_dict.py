# THIS DICTIONARY IS USED TO REPLACE ALL THE TITLE WORDS
# PRESENT IN THE PROVIDED NAMES SUCH AS Mr., Ms., Mrs., Honourable, etc.

word_ref = {
    # For now we can assume these titles only occur in the first part
    # of the string
    r'\s*mr\.\s+': "",
    r'\s*mr\s+' : "",
    r'\s*Mr\.\s+' : "",
    r'\s*Mr\s+' : "",
    r'\s*ms\.\s+': "",
    r'\s*ms\s+' : "",
    r'\s*Ms\.\s+' : "",
    r'\s*Ms\s+' : "",
    r'\s*Mrs\.\s+' : "",
    r'\s*Mrs\s+' : "",
    # For these, need to separate cases where
    # title is at start or in the middle of the string
    r'\d+': "",
    r'^\s*the\s+|^\s*The\s+': "",
    r'\s*the\s+|\s*The\s+' : " ",
    r'^\s*hon\s+|^\s*Hon\s+' : "",
    r'\s*hon\s+|\s*Hon\s+' : " ",
    r'^\s*hon\.\s+|^\s*Hon\.\s+' : "",
    r'\s*hon\.\s+|\s*Hon\.\s+' : " ",
    r'^\s*honourable\s+|^\s*Honourable\s+': "",
    r'\s*honourable\s+|\s*Honourable\s+': " ",
    r'^\s*Senator\s+|^\s*senator\s+': "",
    r'\s*Senator\s+|\s*senator\s+' : " ",
    r'^\s*President\s+|^\s*president\s+': "",
    r'\s*President\s+|\s*president\s+' : " ",
    r'^\s*Vice\s+|^\s*vice\s+': "",
    r'\s*Vice\s+|\s*vice\s+' : " ",
    # These titles appear as a word, so can remove them as is
    # "Honourable" : "",
    r'Prime Minister|prime Minister|Prime minister|prime minister' : "",
    r'Air Marshal|air Marshal|Air marshal|air marshal' : "",
    "AO" : "",
    "AC" : "",
    # "King" : "",
    # "king" : "",
    # "Queen" : "",
    # "queen": ""
}