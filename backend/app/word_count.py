import spacy
from collections import Counter
import string

from mongo.models import Platform

nlp = spacy.load('en_core_web_sm')

def extract_top_adjectives(reviews, top_n=5):
    adj_counts = {
        'Talabat': Counter(),
        'Twitter': Counter(),
        'Elmenus': Counter()
    }
    
    review_dict = {
        'Talabat': {},
        'Twitter': {},
        'Elmenus': {}
    }
    
    for platform, review_set in reviews.items():
        for text in review_set:
            doc = nlp(text.lower())  
            
            filtered_tokens = [token for token in doc if token.text not in string.punctuation and not token.is_space]
            
            negation = False
            negation_words = {"not", "no", "n't"}

            for token in filtered_tokens:
                if token.pos_ == 'ADJ':
                    if negation:
                        adj_counts[platform][token.lemma_] -= 1
                        if token.lemma_ not in review_dict[platform]:
                            review_dict[platform][token.lemma_] = [text]
                        else:
                            review_dict[platform][token.lemma_].append(text)
                    else:
                        adj_counts[platform][token.lemma_] += 1
                        if token.lemma_ not in review_dict[platform]:
                            review_dict[platform][token.lemma_] = [text]
                        else:
                            review_dict[platform][token.lemma_].append(text)
                
                if token.text in negation_words:
                    negation = True
                elif token.dep_ == 'neg':
                    negation = True
                elif token.pos_ == 'VERB' and token.lemma_ == 'be' and token.head.dep_ == 'neg':
                    negation = True
                else:
                    negation = False
    
    # Sorting desc    
    top_adjectives = {}
    for platform, counts in adj_counts.items():
        top_adjectives[platform] = counts.most_common(top_n)

    return top_adjectives, review_dict

def format_result(adjectives_counts, review_dict):
    result = {}
    
    # Collecting all unique adjectives from all platforms
    all_adjectives = set()
    for platform, adjectives in adjectives_counts.items():
        for adj, count in adjectives:
            if count > 0:  # Exclude negative counts
                all_adjectives.add(adj)
    
    for adj in all_adjectives:
        result[adj] = {platform.value: {"count": 0, "reviews": []} for platform in Platform}
    
    for platform, adjectives in adjectives_counts.items():
        for adj, count in adjectives:
            if count > 0:  # Exclude negative counts
                result[adj][platform]["count"] = count
                result[adj][platform]["reviews"] = review_dict[platform].get(adj, [])
    
    return result

# EXAMPLE
reviews = {
    "Talabat": [
        "food was pretty bad",
        "service was good",
        "delivery was quick and food was fresh"
    ],
    "Twitter": [
        "satisfied with their speed",
        "drinks were made bad",
        "not happy with the service"
    ],
    "Elmenus": [
        "price was not good",
        "the menu variety was excellent",
        "not satisfied with the taste"
    ]
}

#top_adjectives, review_dict = extract_top_adjectives(reviews, top_n=5)

# RETURN THIS
#formatted_result = format_result(top_adjectives, review_dict)

#print(formatted_result)
