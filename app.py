from flask import Flask, request, jsonify, render_template
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    if scores['compound'] > 0.05:
        return 'positive'
    elif scores['compound'] < -0.05:
        return 'negative'
    else:
        return 'neutral'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentiment', methods=['POST'])
def get_sentiment():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    sentiment = analyze_sentiment(text)
    return jsonify({'sentiment': sentiment})

@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        color = request.args.get('color')
        storage = request.args.get('storage')
        rating = request.args.get('rating')

        query = """
        SELECT Title as "Review Title", Description as "Review Text", Color, `Storage Size`, `Verified Purchase`, Rating
        FROM reviews
        WHERE 1=1
        """
        params = []

        if color:
            query += " AND Color LIKE ?"
            params.append(f"%{color}%")
        if storage:
            query += " AND `Storage Size` LIKE ?"
            params.append(f"%{storage}%")
        if rating:
            query += " AND Rating = ?"
            params.append(float(rating))

        conn = sqlite3.connect('amazon_reviews.db')
        cursor = conn.cursor()

        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        reviews = [dict(zip(columns, row)) for row in cursor.fetchall()]

        
        for review in reviews:
            review['Sentiment'] = analyze_sentiment(review['Review Text'])

        conn.close()

        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)