# News Summary and Sentiment Analysis Application

## Overview
This application, built using **LangGraph**, **LangChain**, **Gemini**, **OpenAI model API**, and the **NewsAPI Python library**, fetches news articles based on a user-specified topic, generates a summary, and analyzes its sentiment. If the sentiment is negative, it retries up to three times to fetch new articles and generate a positive or mixed sentiment summary. Finally, it produces a concise report with up to eight relevant news article URLs.

## Features
- **Topic-Based News Fetching**: Users input a topic, and the system retrieves related news articles using the NewsAPI.
- **Summary Generation**: Generates a concise summary of fetched articles using advanced language models.
- **Sentiment Analysis**: Analyzes the sentiment of the summary and retries (up to 3 times) if the sentiment is negative.
- **Concise Report**: Outputs a report with the topic, retry count, sentiment, summary, and up to 8 relevant article URLs.
- **Technologies Used**: LangGraph, LangChain, Gemini, OpenAI API, NewsAPI Python library.

## Prerequisites
- Python 3.8+
- A NewsAPI key (obtain from [NewsAPI](https://newsapi.org/))
- OpenAI API key
- Gemini API key (if applicable)
- Docker (optional, for containerized deployment)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/soh-kaz/News-Summarize.git
   cd your-repo-name

2. **Set Up a Virtual Environment:**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables: Create a .env file in the project root and add:**
```bash
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage
1. **Run the Application:**
```bash
python app.py
```
 - Enter a topic (e.g., "cricket") when prompted.
 - The system will fetch news, generate a summary, analyze sentiment, and produce a report.

2. **Example Output:**
```text
Topic: cricket
Total Retry Count: 1 out of 3
Sentiment: positive
=========================================================================
Concise Report:
Cricket, a sport played between two teams of 11 players using a bat and ball, has seen various events with specific mentions of women's cricket, WTC finals, and The Hundred in England...

- https://www.bbc.co.uk/iplayer/episode/m002gbtf/womens-odi-cricket-2025-highlights-england-v-india-second-odi
- https://www.bbc.com/sport/cricket/articles/cwyrx6wkez5o
...
```

## Project Structure
```text
News-Summarize/
├── news.py                # Main application script
├── test.ipynb             # Main application Notebook
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not tracked)
├── Dockerfile             # Docker configuration
├── README.md              # README File

```

## Workflow
<img width="1050" height="1167" alt="image" src="https://github.com/user-attachments/assets/c45c3ab6-5d07-46c2-b61f-d839126f8d76" />

## Contributing
Contributions are welcome.
