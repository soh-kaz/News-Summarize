from langgraph.graph import StateGraph, START, END
import os
from newsapi import NewsApiClient
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser


from typing import TypedDict, Literal



# Optional: Keep dotenv for local development, but not required for Docker
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if present (for local development)
except ImportError:
    pass  # Skip if python-dotenv is not installed

#Create State for LangGraph
class NewsState(TypedDict):
    
    topic: str
    sentiment: str
    summarize: str
    news: str
    fetchCount: int
    concise: str
    

#Initialize NewsAPI model
news_api_key = os.getenv("NEWSAPI_KEY")
newsapi = NewsApiClient(api_key=news_api_key)

#Initialize LLM Model
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
model = ChatOpenAI()



#Fetch News from NewsApi
def fetch_news(state: NewsState):   
    try:
        topic = state['topic']
        # /v2/top-headlines
        response = newsapi.get_everything(q=topic,                          
                                          language='en',
                                          page=1,
                                          page_size=50)
        
        if response['status'] == 'ok' and response['totalResults'] > 0:       
            
            
            docs = ""
            
            articles = response.get('articles', [])
            for idx, article in enumerate(articles):
                docs += f"""
                
                Author: {article['author']}
                Title: {article['title']}
                Published At: {article['publishedAt']}
                Content: {article['content']}
                URL: {article['url']}
                
                """
                
            
            # print(docs)
            state['news'] = ""
            fetchCount = state['fetchCount']
            return {'news': docs, 'fetchCount': (fetchCount+1)}
        
        else:
            print("No Data Found")
            return {'news': ''}
        
    except Exception as e:
        print("Error while fetching news from newsapi.org api -> ", e, state)
        return {'news': ''}
        
#Summarize
def collect_summarize(state: NewsState):
    
    docs = state['news']
    prompt = f"I need a complete summary of the topic {state['topic']} from the following data {state['news']}"
    result = model.invoke(prompt).content
    
    # state['summarize'] = result
    return {'summarize': result}

#Find Sentiment
def find_sentiment(state: NewsState):
    
    summarize = state['summarize']
    prompt = PromptTemplate.from_template(
        "Provide a JSON object with key 'sentiment' and value should be any one of ['positive', 'negative'] for a article summary. {summarize_news}",
    )
    partial_prompt = prompt.partial(summarize_news=summarize)
    
    parser = JsonOutputParser()
    
    chain = partial_prompt | model | parser
    result = chain.invoke({})
    # state['sentiment'] = result
    
    return {'sentiment': result['sentiment']}

def checkSentimentCondition(state: NewsState) -> Literal["concise_report", "fetch_news"]:
    # print(state['sentiment'], state['fetchCount'])
    if state['sentiment'] == 'positive' or state['sentiment'] == 'mixed':
        return "concise_report"
    
    else:    
        if state['fetchCount'] <= 2:
            return "fetch_news"
        else:
            return "concise_report"

#Concise Report
def concise_report(state: NewsState):
    # print("I'm in now Concise Report Node")
    
    summarize = state['summarize']
    prompt = f"""Generate Concise report based on article/news summary {summarize}.
    Note:
    - Generate a Concise report with atleast 2 sentences from {summarize}
    - Mention maximum 8 URL at bottom in bullet points from {state['news']}:
    """
    result = model.invoke(prompt).content
    
    
    return {'concise': result}


#LangGraph graph
graph = StateGraph(NewsState)

#Create Nodes
graph.add_node("fetch_news", fetch_news)
graph.add_node("collect_summarize", collect_summarize)
graph.add_node("find_sentiment", find_sentiment)
graph.add_node("concise_report", concise_report)


#Create Edges
graph.add_edge(START, "fetch_news")
graph.add_edge("fetch_news", "collect_summarize")
graph.add_edge("collect_summarize", "find_sentiment")
graph.add_conditional_edges("find_sentiment", checkSentimentCondition)
# graph.add_edge("find_sentiment", "concise_report")
# graph.add_edge("find_sentiment", "fetch_news")
graph.add_edge("concise_report", END)

#Create Conditional Edge for Sentiment Check
    #If Sentiment is Negative again start all the process

#Compile
workflow = graph.compile()

# from IPython.display import Image
# Image(workflow.get_graph().draw_mermaid_png())



st.title("News Summary and Sentiment Analysis Application")

#Execute
topic = st.text_input("Enter a topic name:")
# Add a Submit button
if st.button("Submit"):
    if topic.strip() == "":
        st.error("Please enter a topic before submitting.")
    else:

        initial_state = {
            'topic': topic,
            'fetchCount': 0
        }
        
        with st.spinner("Analyzing topic..."):
            final_state = workflow.invoke(initial_state)
        

        #Color Codes
        GREEN = "\033[92m"
        RESET = "\033[0m"
        
        st.markdown("### 📊 Results")
        st.markdown("---------------------------------------")
        st.success(f"**Topic**: {final_state['topic']}")
        st.info(f"**Total Retry Count**: {final_state['fetchCount']} out of 3")
        st.warning(f"**Sentiment**: {final_state['sentiment']}")

        st.markdown("---------------------------------------")
        st.markdown("### 📝 Concise Report")
        st.write(final_state['concise'])

        # print("="*100)
        # print(f"{GREEN}Topic{RESET} : ", final_state['topic'])
        # print(f"{GREEN}Total Retry Count{RESET} : ", final_state['fetchCount'], " out of 3")
        # print(f"{GREEN}Sentiment{RESET} : ", final_state['sentiment'])

        # print("="*100)
        # print(f"{GREEN}Concise Report{RESET} : ")
        # print(final_state['concise'])




# Footer with name and links
st.markdown("------------------------------------------------------------------------------")
st.markdown("### 👤 Author & Repositories")
st.markdown("**Name:** [soh-kaz](https://github.com/soh-kaz)")
st.markdown("**GitHub:** [github.com/soh-kaz](https://github.com/soh-kaz)")
st.markdown("**Docker Hub:** [hub.docker.com/r/aghasuhail96](https://hub.docker.com/r/aghasuhail96)")