# Step 5 – Article model with Pydantic + pydantic-mongo
# pip install pydantic-mongo pymongo
from pydantic_mongo import AbstractRepository, ObjectIdField
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Article(BaseModel):
    id: ObjectIdField = None
    title: str
    url: str
    np_name: str
    date: datetime
    body: Optional[str] = None
    tags: list[str] = []


class ArticleRepository(AbstractRepository[Article]):
    class Meta:
        collection_name = "articles"
