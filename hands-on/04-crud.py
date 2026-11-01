"""Step 4 – Read & insert with pymongo.
pip install pymongo
python 04-crud.py
"""
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://root:example@localhost:27017/")
col = client["news_db"]["articles"]

# INSERT
result = col.insert_one({
    "title"  : "Artículo de prueba",
    "url"    : "https://example.com/test",
    "np_name": "example",
    "date"   : datetime.now(),
    "body"   : "Contenido del artículo...",
})
print("Inserted id:", result.inserted_id)

# READ – only elpais articles, 5 max
print("\nelpais articles:")
for art in col.find({"np_name": "elpais"}, {"title": 1, "date": 1, "_id": 0}).limit(5):
    print(" ", art["date"].date(), "–", art["title"])

print("\nTotal docs:", col.count_documents({}))
