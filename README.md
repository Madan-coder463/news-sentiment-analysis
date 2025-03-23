# News Sentiment Analysis and TTS Application

This application performs **sentiment analysis** and generates **text-to-speech (TTS)** audio in **Hindi** for news articles about a given company. It consists of a **Streamlit frontend** for interacting with users and a **Flask backend** to handle sentiment analysis and TTS generation.

### Table of Contents:
1. [Project Setup](#project-setup)
2. [Model Details](#model-details)
3. [API Development](#api-development)
4. [API Usage](#api-usage)
5. [Assumptions & Limitations](#assumptions-limitations)

---

## Project Setup

### Prerequisites:
- **Python**: Version 3.8 or higher.
- **Flask**: For the backend API.
- **Streamlit**: For the frontend.
- **Additional Libraries**: For sentiment analysis, topic extraction, TTS generation, etc.

### Steps to Install and Run the Application:

1. **Clone the Repository**:
   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/news-sentiment-analysis.git
   cd news-sentiment-analysis
   ```

2. **Set up a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Dependencies**:
   Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask API**:
   In the `api.py` directory, start the Flask server:
   ```bash
   python api.py
   ```
   By default, the Flask API runs on `http://127.0.0.1:5000`.

5. **Run the Streamlit App**:
   In the `app.py` directory, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**:
   Once the app is running, open your browser and go to `http://localhost:8501` to interact with the frontend.

---

## Model Details

### 1. **Summarization**:
   The **summarization** of the articles is done using the raw description field from the **Google News RSS Feed**. We also extract detailed content from the article itself using **newspaper3k** for more accurate summaries.

### 2. **Sentiment Analysis**:
   The **sentiment analysis** is performed using the **VADER** (Valence Aware Dictionary and sEntiment Reasoner) model. This model classifies the sentiment of each article as:
   - **Positive**
   - **Negative**
   - **Neutral**

   **VADER** is ideal for analyzing social media and short news articles, which is why it was chosen for this task.

### 3. **Text-to-Speech (TTS)**:
   The **Text-to-Speech (TTS)** is generated using **Google TTS (gTTS)**, which converts the sentiment analysis report into speech in **Hindi**.

   The steps for TTS generation are:
   1. The summaries of all news articles are concatenated.
   2. The concatenated text is translated into **Hindi** using **Google Translate**.
   3. The translated text is converted to audio in **Hindi** using **gTTS**.

---

## API Development

### 1. **Flask API**:
   The **Flask API** is responsible for:
   - Fetching news articles related to a specific company.
   - Performing **sentiment analysis** on each article.
   - Generating a **TTS audio** file summarizing the sentiment report.
   - Performing **comparative sentiment analysis** to highlight coverage differences.

   The API is accessible at `http://127.0.0.1:5000/fetch_news`.

#### **Flask Routes**:
   - `/fetch_news`: 
     - **Method**: `GET`
     - **Parameters**:
       - `company_name`: The name of the company to search for (e.g., "Tesla").
     - **Response**:
       - `news_data`: A list of articles with their title, summary, sentiment, and topics.
       - `comparative_analysis`: A breakdown of sentiment distribution and coverage differences.
       - `tts_file`: Path to the generated TTS audio file.

   Example:
   ```bash
   curl "http://127.0.0.1:5000/fetch_news?company_name=Tesla"
   ```

### 2. **Postman**:
   You can test the **Flask API** using **Postman**:
   - Set the method to `GET`.
   - URL: `http://127.0.0.1:5000/fetch_news?company_name=Tesla`
   - Hit **Send** to get the JSON response with news articles, sentiment analysis, and TTS file.

---

## API Usage

### 1. **Third-Party APIs**:
   The project uses the following third-party APIs and libraries:
   - **Google News RSS Feed**: For fetching the latest news articles related to a specific company.
   - **Google Translate** (via **googletrans**): For translating the concatenated article summaries into **Hindi**.
   - **gTTS**: For converting the translated text into **Hindi TTS**.
   - **VADER Sentiment Analysis**: For classifying the sentiment of news articles.

   These APIs are integrated as follows:
   - **Google News RSS**: Fetches the articles in XML format, which is parsed to get the article titles and summaries.
   - **googletrans**: Translates the concatenated summaries of the articles into Hindi.
   - **gTTS**: Converts the Hindi text into speech and saves it as an MP3 file.
   - **VADER**: Classifies the sentiment of the articles into positive, negative, or neutral.

---

## Assumptions & Limitations

### Assumptions:
1. **Article Availability**: It is assumed that news articles fetched from the **Google News RSS Feed** contain enough content for sentiment analysis and summarization.
2. **Hindi TTS**: It assumes that the **Google TTS** library will work properly with the generated text, especially for non-English languages like **Hindi**.
3. **API Limits**: The application assumes that external APIs like **Google News** and **Google Translate** don’t have significant usage restrictions for this scale.

### Limitations:
1. **Limited Coverage**: The **Google News RSS Feed** might not always contain the latest articles or cover all news sources.
2. **Sentiment Analysis Accuracy**: **VADER** sentiment analysis works well for social media and shorter texts but might not be perfect for all types of news articles.
3. **Text-to-Speech Quality**: The generated TTS may not have the best **pronunciation** in **Hindi**, and **gTTS** may have limitations in how it handles long texts.
4. **API Rate Limiting**: Some external APIs, like **Google Translate**, may have rate limits that could affect performance if too many requests are made in a short time.

---

### Conclusion

This project integrates **news sentiment analysis**, **comparative sentiment analysis**, and **Hindi TTS generation** into a seamless web application. By using **Streamlit** for the frontend and **Flask** for the backend, it provides an interactive way to explore news articles, analyze sentiment, and generate a TTS report in **Hindi**.

### **GitHub Description**:
This repository contains a **News Sentiment Analysis** application built with **Streamlit** and **Flask**. It fetches news articles for a specified company, performs **sentiment analysis**, and generates a **Hindi TTS** report summarizing the findings. The project also includes a **comparative sentiment analysis** feature that compares the sentiment between different articles and highlights coverage differences.

---

This **README** should provide a clear and thorough explanation of your project and guide users on how to set up, run, and interact with your application. Let me know if you need further changes or additions!
