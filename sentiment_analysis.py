import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    if scores['compound'] > 0.05:
        return 'positive'
    elif scores['compound'] < -0.05:
        return 'negative'
    else:
        return 'neutral'
    
def analyze_reviews(reviews):
    sentiments = [analyze_sentiment(text) for text in reviews['Description']]
    reviews['Sentiment'] = sentiments
    return reviews


if __name__=='__main__':
    conn = sqlite3.connect('amazon_reviews.db')
    df = pd.read_sql_query("SELECT * FROM reviews", conn)
    df_with_sentiment = analyze_reviews(df)
    df_with_sentiment.to_csv('amazon_reviews.csv')
    engine = create_engine('sqlite:///amazon_reviews.db')
    df_with_sentiment.to_sql('reviews', engine, if_exists='replace', index=False)
    



