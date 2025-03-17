import asyncio
from apify import Actor
from src.tools import search_news, extract_news_summary
from src.prompts import NEWSLETTER_TEMPLATE, REFINEMENT_TEMPLATE, ENTERTAINMENT_TEMPLATE
from src.models import Newsletter
from langchain_openai import ChatOpenAI

#  Initialize OpenAI LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)


async def generate_newsletter(topic: str):
    """Creates an AI-generated newsletter on a given topic."""
    Actor.log.info(f"📝 Generating newsletter for: {topic}")

    #  Step 1: Fetch latest news
    articles = search_news(topic)

    #  Step 2: Extract structured summary
    news_summary = extract_news_summary(articles)

    #  Ensure all articles have a summary (fixes missing field issue)
    for article in articles:
        if "summary" not in article or not article["summary"]:
            article["summary"] = "Summary not available."

    #  Step 3: Generate newsletter using LLM
    response = NEWSLETTER_TEMPLATE | llm
    newsletter_content = response.invoke({"user_input": topic}).content

    #  Step 4: Apply Refinements
    refined_content = REFINEMENT_TEMPLATE | llm
    newsletter_content = refined_content.invoke({
        "current_content": newsletter_content,
        "refinement_instructions": "Make it concise and engaging while ensuring factual accuracy."
    }).content

    #  Step 5: Apply Entertainment Enhancements
    final_content = ENTERTAINMENT_TEMPLATE | llm
    newsletter_content = final_content.invoke({
        "current_content": newsletter_content
    }).content

    #  Step 6: Save & return newsletter
    newsletter = Newsletter(topic=topic, news_summary=news_summary, articles=articles)
    with open("newsletter.md", "w", encoding="utf-8") as f:
        f.write(newsletter_content)

    Actor.log.info(" Newsletter saved as `newsletter.md`!")
    return newsletter_content

async def main():
    """Runs the AI Newsletter Generator workflow."""
    async with Actor:
        actor_input = await Actor.get_input() or {}
        Actor.log.info(f"📥 Received input: {actor_input}")

        #  Extract user query
        topic = actor_input.get("topic", "Latest AI News")

        #  Generate Newsletter
        newsletter_content = await generate_newsletter(topic)
        Actor.log.info(f" Newsletter Generation Completed.")

        #  Save Final Report
        await Actor.set_value("newsletter.md", newsletter_content)

        #  Push data to Apify dataset
        await Actor.push_data({"topic": topic, "newsletter": newsletter_content})

if __name__ == "__main__":
    asyncio.run(main())
