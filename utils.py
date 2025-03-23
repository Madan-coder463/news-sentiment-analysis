import requests
from bs4 import BeautifulSoup
import streamlit as st
import matplotlib.pyplot as plt
import json
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from gtts import gTTS
import os
from googletrans import Translator


# SENTIMENT ANALYSIS

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    
    # Return sentiment category based on compound score
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def fetch_news_with_sentiment(company_name, num_articles=10, num_topics=5):
    """
    Fetches news articles and performs sentiment analysis on them.
    :param company_name: Name of the company to search for.
    :param num_articles: Number of articles to fetch.
    :return: JSON with news details (title, link, summary, sentiment).
    """
    search_url = f'https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch news"}
    
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')[:num_articles]
    
    news_data = []
    summaries = []

    for item in items:
        description = item.description.text if item.description else "No summary available"
        summary = BeautifulSoup(description, "html.parser").get_text()  # Clean the HTML tags
        
        summaries.append(summary)
    # Extract topics using TF-IDF
    topics = extract_topics(summaries, num_topics)

    for idx, item in enumerate(items):
        title = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        description = item.description.text if item.description else "No summary available"

        
        summary = BeautifulSoup(description, "html.parser").get_text()  # Clean HTML
        
        sentiment = analyze_sentiment(summary)

        # Extract topics using TF-IDF
        topics = extract_topics(summaries, num_topics)
        
        news_data.append({
            "title": title,
            "link": link,
            "published_date": pub_date,
            "summary": summary,
            "sentiment": sentiment,
            "topics": topics[idx]  # Add the extracted topics
        })

         # Perform comparative sentiment analysis
    comparative_analysis = compare_sentiment(news_data)
    
    return json.dumps({
        "company": company_name,
        "articles": news_data,
        "comparative_analysis": comparative_analysis
    }, indent=4)

def extract_topics(summaries, num_topics=5):
    """
    Extracts topics from the list of article summaries using TF-IDF.
    :param summaries: List of cleaned article summaries.
    :param num_topics: Number of top topics to extract.
    :return: List of topics.
    """
    # Create the TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english', max_features=10)
    
    # Fit and transform the summaries to get TF-IDF scores
    tfidf_matrix = tfidf.fit_transform(summaries)
    
    # Get the feature names (terms)
    feature_names = tfidf.get_feature_names_out()
    
    # Extract top terms for each article
    topics = []
    for i in range(len(summaries)):
        # Get the indices of the highest scoring terms for this article
        scores = tfidf_matrix[i].toarray().flatten()
        top_indices = scores.argsort()[-num_topics:][::-1]
        
        # Get the corresponding terms (topics) for the top indices
        top_terms = [feature_names[idx] for idx in top_indices]
        topics.append(top_terms)
    
    return topics

## COMPARATIVE SENTIMENT ANALYSIS

def compare_sentiment(news_data):
    sentiment_counts = Counter(article['sentiment'] for article in news_data)

    """
    Perform comparative sentiment analysis across the articles.
    :param news_data: List of news articles with sentiment analysis.
    :return: A structured comparison of sentiments and coverage differences.
    """
    
    # Get comparisons of articles with contrasting sentiments
    coverage_differences = []
    for i in range(len(news_data)):
        for j in range(i + 1, len(news_data)):
            # Compare articles with different sentiments
            article_i = news_data[i]
            article_j = news_data[j]
            
            if article_i['sentiment'] != article_j['sentiment']:
                # Correctly generate the keys for article topics
                comparison = {
                    "Comparison": f"Article {i+1} ({article_i['sentiment']}) vs Article {j+1} ({article_j['sentiment']})",
                    "Impact": f"Article {i+1} focuses on positive aspects, while Article {j+1} highlights challenges or risks.",
                    "Key Themes": {
                        f"Article {i+1} Topics": article_i['topics'],  # Dynamically create the key
                        f"Article {j+1} Topics": article_j['topics']  # Dynamically create the key
                    }
                }
                coverage_differences.append(comparison)

    sentiment_distribution = dict(sentiment_counts)

    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences
    }



## TEXT-TO-SPEECH

# Function to generate Hindi TTS
def generate_hindi_tts(text, filename="summary.mp3"):
    # Step 1: Translate the concatenated text from English to Hindi
    from googletrans import Translator
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi').text
    
    # Ensure the summaries folder exists
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    
    # Step 2: Convert the translated Hindi text to speech
    file_path = f'summaries/{filename}'
    from gtts import gTTS
    tts = gTTS(translated_text, lang='hi')
    tts.save(file_path)
    print(f"Generated Hindi speech file: {file_path}")
    return file_path

def get_sentiment_distribution(news_data):
    """
    Calculates the sentiment distribution (positive, negative, neutral).
    :param news_data: List of news articles.
    :return: Dictionary with sentiment distribution.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    
    for article in news_data:
        sentiment = article['sentiment']
        sentiment_counts[sentiment] += 1
    
    return sentiment_counts

def plot_sentiment_distribution(sentiment_distribution):
    """
    Plots a pie chart showing the sentiment distribution.
    :param sentiment_distribution: Dictionary with sentiment distribution.
    """
    labels = sentiment_distribution.keys()
    sizes = sentiment_distribution.values()
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'red', 'grey'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)



## COMBINING EVERYTHING
def fetch_news_complete(company_name, num_articles=10):
    # Fetch news with sentiment
    news_json = fetch_news_with_sentiment(company_name, num_articles)
    news_data = json.loads(news_json)["articles"]
    
    # Compare sentiment
    sentiment_report = compare_sentiment(news_data)

    comparative_analysis = compare_sentiment(news_data)
    
    # Generate TTS for the report
    tts_filename = generate_hindi_tts(f"Sentiment analysis for {company_name} completed.")
    
    return {
        "news_data": news_data,
        "sentiment_report": sentiment_report,
        "comparative_analysis": comparative_analysis,
        "tts_file": tts_filename
    }

# Example usage
if __name__ == "__main__":
    company = "Tesla"
    result = fetch_news_complete(company)
    print(result)
