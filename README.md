# iPhone 12 Review Analysis

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)

## Introduction

This project is a comprehensive solution for scraping, analyzing, and serving iPhone 12 reviews from Amazon. It includes web scraping capabilities, sentiment analysis, and a Flask-based API for interacting with the collected data.

The main components of the project are:
1. Web scraping script to collect iPhone 12 reviews from Amazon
2. Sentiment analysis of the collected reviews
3. API endpoints for retrieving reviews and performing sentiment analysis
4. A simple frontend for interacting with the API

## Features

- **Web Scraping**: Collects reviews, ratings, and other metadata from Amazon's iPhone 12 product page.
- **Sentiment Analysis**: Analyzes the sentiment of reviews using NLTK and TextBlob.
- **Keyword Analysis**: Identifies the most impactful positive and negative keywords in the reviews.
- **RESTful API**: Provides endpoints for retrieving reviews and performing sentiment analysis on new text.
- **Database Storage**: Stores collected reviews in an SQLite database for easy access and management.
- **Simple Frontend**: Includes a basic HTML interface for interacting with the API.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/charans2702/Amazon-ReviewRetrival-and-SentimentAnalysis.git
   cd Amazon_Scrapper
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download NLTK data:
   ```
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

## Usage

1. Run the web scraping script:
   ```
   python Amazon_Scrapper.py
   ```
   This will collect reviews and save them to the `amazon_reviews.db` SQLite database.

2. Perform sentiment analysis on the collected reviews:
   ```
   python sentiment_analysis.py
   ```

3. Start the Flask API:
   ```
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

4. Open `index.html` in a web browser to use the frontend interface.

## API Endpoints

1. **Sentiment Analysis**
   - URL: `/sentiment`
   - Method: POST
   - Data Params: `{ "text": "Review text here" }`
   - Success Response: `{ "sentiment": "positive" }`

2. **Review Retrieval**
   - URL: `/reviews`
   - Method: GET
   - URL Params: 
     - `color` (optional)
     - `storage` (optional)
     - `rating` (optional)
   - Success Response: Array of review objects

## Technologies Used

- Python 3.x
- BeautifulSoup4 for web scraping
- NLTK and TextBlob for sentiment analysis
- Flask for API development
- SQLite for database storage
- Pandas for data manipulation
- Scikit-learn for TF-IDF vectorization

