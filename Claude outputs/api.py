from fastapi import FastAPI
from pymongo import MongoClient

from article_model import Article, ArticleRepository

app  = FastAPI()
db   = MongoClient("mongodb://root:example@localhost:27017/")["news_db"]
repo = ArticleRepository(database=db)


@app.get("/articles", response_model=list[Article])
def list_articles(np_name: str = None, limit: int = 10):
    """Return articles, optionally filtered by newspaper name."""
    q = {}
    if np_name:
        q["np_name"] = np_name
    return list(repo.find_by(q))


@app.get("/articles/{np_name}/count")
def count(np_name: str):
    """Count articles for a given newspaper without loading them all."""
    return {
        "np_name": np_name,
        "count": db["articles"].count_documents({"np_name": np_name}),
    }
