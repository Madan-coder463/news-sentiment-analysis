from flask import Flask, request, jsonify
from utils import fetch_news_complete, generate_hindi_tts  # Import your functions
import os
# from utils import compare_sentiment

app = Flask(__name__)

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    # Get the company name from the query parameter
    company_name = request.args.get('company_name', default='Tesla', type=str)
    # sentiment_filter = request.args.get('sentiment', default=None, type=str)
    # topics_filter = request.args.get('topics', default=None, type=str)
    # keyword_filter = request.args.get('keywords', default=None, type=str)
    
    # Fetch news and process the data
    try:
        result = fetch_news_complete(company_name)

        # Apply filters if necessary
        # if sentiment_filter:
        #     result["news_data"] = [article for article in result["news_data"] if article['sentiment'] == sentiment_filter]
        # if topics_filter:
        #     result["news_data"] = [article for article in result["news_data"] if topics_filter.lower() in [topic.lower() for topic in article['topics']]]
        # if keyword_filter:
        #     result["news_data"] = [article for article in result["news_data"] if keyword_filter.lower() in article['summary'].lower()]
        
        # Perform comparative sentiment analysis
        # comparative_analysis = compare_sentiment(result["news_data"])

        # Extract audio file path for Hindi TTS
        tts_filename = result["tts_file"]

        print("Fetched Data: ", result)  # Print to check if data is correct
        
        # Return the news data and audio file path
        return jsonify({
            'company': company_name,
            'news_data': result["news_data"],
            'comparative_analysis': result["comparative_analysis"],
            'tts_file': tts_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Ensure the folder for saving audio files exists
    if not os.path.exists('summaries'):
        os.makedirs('summaries')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
