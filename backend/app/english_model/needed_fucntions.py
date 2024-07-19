import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


nlp = spacy.load("en_core_web_sm")
stopwords = list(STOP_WORDS)
punct = list(punctuation)

def text_data_cleaning(sentence, stopwords=stopwords, punct=punct, nlp=nlp):
    doc = nlp(sentence)
    
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
    
    cleaned_tokens = []
    for token in tokens:
        if (token not in stopwords and token not in punct) or token == 'not' :
            cleaned_tokens.append(token)
    return cleaned_tokens


