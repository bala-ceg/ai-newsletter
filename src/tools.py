import json
from apify import Actor
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.prompts import NEWSLETTER_TEMPLATE, REFINEMENT_TEMPLATE, ENTERTAINMENT_TEMPLATE


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(TAVILY_API_KEY)

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

def search_news(topic: str) -> list:
    """Searches Tavily for latest news articles on a given topic."""
    Actor.log.info(f"🔍 Searching news for topic: {topic}")

    try:
        response = tavily_client.search(query=f"Latest news about {topic}", search_depth="basic", max_results=5)
        articles = response.get("results", [])
        
        if not articles:
            Actor.log.warning(f"⚠️ No news found for {topic}")
            return []
        
        Actor.log.info(f" Found {len(articles)} articles")
        return articles
    except Exception as e:
        Actor.log.error(f"❌ Tavily API error: {e}")
        return []


def extract_news_summary(articles: list) -> str:
    """Summarizes key insights from news articles using LLM."""
    if not articles:
        return "No relevant news found."

    summary_prompt = ChatPromptTemplate.from_template("""
        Summarize the following news articles in a clear and structured format.
        Ensure the key insights are extracted and **each article is properly cited** with inline Markdown hyperlinks.

        ### News Articles:
        {articles}

        **Format:** Provide a well-written summary for each article with key takeaways, followed by proper citations.
    """)

    response = summary_prompt | llm
    summary = response.invoke({"articles": json.dumps(articles, indent=2)}).content
    return summary if summary else "Failed to generate summary."
