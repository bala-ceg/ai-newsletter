from pydantic import BaseModel
from typing import List

class NewsArticle(BaseModel):
    title: str
    url: str
    summary: str

class Newsletter(BaseModel):
    topic: str
    news_summary: str
    articles: List[NewsArticle]
