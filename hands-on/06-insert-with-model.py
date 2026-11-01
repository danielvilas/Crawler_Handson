# Step 6 – Insert and query articles using the typed model
# Run from the hands-on/ folder so article_model is importable
from pymongo import MongoClient
from datetime import datetime
from article_model import Article, ArticleRepository

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["news_db"]
repo = ArticleRepository(database=db)

# Pydantic validates every field before touching MongoDB
article = Article(
    title="El paro baja en noviembre",
    url="https://elpais.com/economia/paro.html",
    np_name="elpais",
    date=datetime(2024, 11, 1),
    tags=["economía", "trabajo"],
)
repo.save(article)
print(f"Inserted id: {article.id}")

# Query returns typed Article instances — no dict key access
for art in repo.find_by({"np_name": "elpais"}):
    print(art.date, art.title)
