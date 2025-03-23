import streamlit as st
import requests
import os
import matplotlib.pyplot as plt
from utils import generate_hindi_tts, get_sentiment_distribution, plot_sentiment_distribution

# Add custom CSS to improve the look of the app
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit UI
def main():
    st.title("News Sentiment Analysis and TTS in Hindi")

    # Create a container for the initial input
    with st.container():
        st.subheader("Step 1: Input Company Name and Fetch News")
        company_name = st.text_input("Enter Company Name:", "Tesla")

        # Add filters for sentiment, topics, and keywords
        sentiment_filter = st.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])
        topics_filter = st.text_input("Filter by Topics (comma-separated)")
        keyword_filter = st.text_input("Filter by Keywords")

        # Create a button to fetch and analyze the news
        if st.button("Fetch News and Analyze", help="Click to fetch news articles and analyze sentiment"):
            # Add a progress bar to show the process of fetching data
            progress_bar = st.progress(0)
            with st.spinner(f"Fetching news for {company_name}..."):
                # Only update progress once
                progress_bar.progress(100)

                try:

                    
                        
                    # Make a GET request to the Flask API
                    response = requests.get(f'http://127.0.0.1:5000/fetch_news', params={'company_name': company_name})
                    data = response.json()

                    # Check for errors in the response
                    if 'error' in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        # Create a new container to display the fetched news
                        with st.container():
                            st.subheader(f"News Articles for {company_name}")
                            all_summaries = ""  # Initialize an empty string to hold all summaries

                            # Loop through articles and display relevant information
                            for article in data["news_data"]:
                                st.write(f"**Title:** {article['title']}")
                                st.write(f"**Published on:** {article['published_date']}")
                                st.write(f"**Summary:** {article['summary']}")
                                st.write(f"**Sentiment:** {article['sentiment']}")
                                st.write(f"**Topics:** {', '.join(article['topics'])}")
                                st.write("---")

                                # Concatenate all article summaries
                                all_summaries += article['summary'] + "\n\n-----\n\n"  # Adding separator between articles

                            # Generate Hindi TTS for all the summaries combined
                            st.subheader("Play Sentiment Report Audio in Hindi")
                            tts_filename = generate_hindi_tts(all_summaries)  # Pass the concatenated summaries
                            if os.path.exists(tts_filename):
                                st.audio(tts_filename)

                            # Create a container for the comparative sentiment analysis
                            with st.container():
                                st.subheader("Coverage Differences (Comparative Sentiment Analysis)")
                                comparative_analysis = data.get("comparative_analysis", None)

                                if comparative_analysis:
                                    st.write(f"Sentiment Distribution: {comparative_analysis['Sentiment Distribution']}")

                                    if comparative_analysis["Coverage Differences"]:
                                        for comparison in comparative_analysis["Coverage Differences"]:
                                            st.write(f"**{comparison['Comparison']}**")
                                            st.write(f"Impact: {comparison['Impact']}")

                                            # Dynamically access the topic keys (e.g., 'Article 1 Topics')
                                            article_1_key = f"Article 1 Topics"
                                            article_2_key = f"Article 2 Topics"

                                            # Safely access topics, ensuring keys exist
                                            article_1_topics = comparison['Key Themes'].get(article_1_key, [])
                                            article_2_topics = comparison['Key Themes'].get(article_2_key, [])

                                            st.write(f"Key Themes - Article 1: {', '.join(article_1_topics)}")
                                            st.write(f"Key Themes - Article 2: {', '.join(article_2_topics)}")
                                            st.write("---")

                                else:
                                    st.warning("No comparative sentiment analysis available.")

                            # Visualization using Matplotlib
                            sentiment_distribution = get_sentiment_distribution(data["news_data"])
                            with st.container():
                                st.subheader("Sentiment Distribution Visualization")
                                plot_sentiment_distribution(sentiment_distribution)

                except Exception as e:
                    st.error(f"Failed to fetch data: {str(e)}")

if __name__ == "__main__":
    main()
