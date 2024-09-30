from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import pandas as pd
import numpy as np
import sqlite3


def analyze_keywords(reviews):
    all_text = ' '.join(reviews['Description'])
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform([all_text])
    feature_names = vectorizer.get_feature_names_out()
    sentiments = [TextBlob(text).sentiment.polarity for text in reviews['Description']]
    word_sentiments = {word: [] for word in feature_names}
    for review, sentiment in zip(reviews['Description'], sentiments):
        words = set(review.lower().split())
        for word in words.intersection(feature_names):
            word_sentiments[word].append(sentiment)

    avg_sentiments = {word: np.mean(sents) if sents else 0 for word, sents in word_sentiments.items()}
    sorted_words = sorted(avg_sentiments.items(), key=lambda x: x[1])
    worst_keywords = sorted_words[:10]
    best_keywords = sorted_words[-10:][::-1]
    
    return best_keywords, worst_keywords


if __name__=='__main__':
    conn = sqlite3.connect('amazon_reviews.db')
    df = pd.read_sql_query("SELECT * FROM reviews", conn)
    best_keywords, worst_keywords = analyze_keywords(df)
    best_keyword=[]
    for i in range(len(best_keywords)):
        best_keyword.append(best_keywords[i][0])
    worst_keyword=[]
    for i in range(len(worst_keywords)):
        worst_keyword.append(worst_keywords[i][0])
    print("Best Keywords:", best_keyword)
    print("Worst Keywords:", worst_keyword)

