from pyarabic import araby
from spacy.lang.ar.stop_words import STOP_WORDS
from string import punctuation
from nltk import ISRIStemmer
import re


stopwords = list(STOP_WORDS)
punct = list(punctuation)
stemmer = ISRIStemmer()

def clean_arabic_text(sentence):
    tokens = araby.tokenize(sentence)
    
    cleaned_tokens = []
    for token in tokens:
        token = re.sub("[إأآا]", "ا", token)
        token = re.sub("ى", "ي", token)
        token = re.sub("ة", "ه", token)
        token = re.sub("[\W\d]", "", token)
        # removes harakat and any small letters or marks
        token = araby.strip_diacritics(token)
        # removes tatweel
        token = araby.strip_tatweel(token)
        token = stemmer.stem(token)
        if token in stopwords or token in punct or len(token) == 1:
            token = ''

        if token != '':
            cleaned_tokens.append(token)
        
    return cleaned_tokens

        
    
    
    