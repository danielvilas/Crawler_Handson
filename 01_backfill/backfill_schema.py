from datetime import date
from typing import Optional


class Category:
    url: str
    name: str


class Article:
    url: str
    date: date
    category: str
    newspaper: str

class MongoDB:
    """Persistent store for categories and article stubs."""

    def get_categories(self, newspaper: str) -> list[Category]:
        """Return the category list extracted in the previous (extract) step."""
        raise NotImplementedError

    def save(self, articles: list[Article]) -> None:
        """Persist a batch of article stubs."""
        raise NotImplementedError

    def mark_category_done(self, cat: Category) -> None:
        """Record that this category has been fully backfilled."""
        raise NotImplementedError

class Context:
    """
    Accumulates articles during a crawl session and flushes them to MongoDB.
    Also carries state shared between crawler iterations (e.g. last date seen).
    """

    def __init__(self, db: MongoDB) -> None:
        self.db = db
        self._buffer: list[Article] = []
        self.last_date: Optional[date] = None

    def store_articles(self, articles: list[Article]) -> None:
        """Buffer articles and persist them to the database."""
        self._buffer.extend(articles)
        if articles:
            self.last_date = articles[-1].date
        self.db.save(articles)

    def collected(self) -> list[Article]:
        return list(self._buffer)

class GeneralCrawler():
    """
    Orchestrates the backfill loop for any newspaper engine.

    1. Fetches the category list from MongoDB.
    2. For each category:
       a. Delegates to EngineCrawler to find the starting page.
       b. Pages through the API until the response is empty.
       c. Marks the category as done.

    Subclasses implement the engine-specific hooks:
      find_initial_page / get_page / extract_articles
    """

    def __init__(self, db: MongoDB, context: Context) -> None:
        self.db = db
        self.context = context

    def backfill(
        self,
        newspaper: str,
        start_date: date,
        end_date: date,
    ) -> list[Article]:

        categories = self.db.get_categories(newspaper)     

        for cat in categories:

            n = self.find_initial_page(cat, start_date, end_date)

            while True:
                articles = self.get_page(cat, n)          
                if not articles:                           
                    break
                filtered = self.extract_articles(          
                    articles, start_date, end_date
                )
                self.context.store_articles(filtered)      
                n += 1                                     

            self.db.mark_category_done(cat)               

        return self.context.collected

    def find_initial_page(
        self,
        cat: Category,
        start_date: date,
        end_date: date,
    ) -> int:
        """
        Scan forward until the page that starts the date window is found.
        Returns the page number where the main loop should begin.
        """
        pass

    def get_page(self, cat: Category, n: int) -> list[dict]:
        """
        Fetch raw items for page *n* of *cat* from the paginated API.
        Returns an empty list when there are no more pages.
        """

    def extract_articles(
        self,
        raw: list[dict],
        start_date: date,
        end_date: date,
    ) -> list[Article]:
        """
        Parse raw items into Article objects filtered to [start_date, end_date].
        """


class EngineCrawler(GeneralCrawler):
    """
    Engine-specific crawler.

    Inherits the backfill orchestration from GeneralCrawler and provides
    concrete implementations for page fetching and article extraction,
    which vary by newspaper engine (WordPress, bCube, Vocento, …).
    """


    def find_initial_page(
        self,
        cat: Category,
        start_date: date,
        end_date: date,
    ) -> int:
        """
        Walk pages until the start of the date window is located.
        Uses self.context to track the last date seen across iterations.
        """
        n = 1
        while not self._start_page_known(n):       
            raw = self.get_page(cat, n)             
            articles = self.extract_articles(      
                raw, start_date, end_date
            )
            self.context.store_articles(articles)   
            n = self._advance(n)                   
        return n                                   


    def get_page(self, cat: Category, n: int) -> list[dict]:
        """
        Fetch one page of raw article data from the paginated API.

        - page 1  → parse static HTML of the category URL
        - page n  → GET /webapi/module-pagination/?url=<cat>&page=<n>

        Returns [] when the response is empty (end of archive).
        """
        raise NotImplementedError   # ← replace with requests + BS4

   
    def extract_articles(
        self,
        raw: list[dict],
        start_date: date,
        end_date: date,
    ) -> list[Article]:
        """
        Parse raw dicts into Article objects and filter by date window.

        Typical implementation:
          - iterate items newest-first
          - skip if item.date > end_date  (too recent)
          - collect if item.date >= start_date
          - stop if item.date < start_date (past window)
        """
        raise NotImplementedError   # ← replace with BS4 parsing

   
    def _start_page_known(self, n: int) -> bool:
        """
        Return True once we know that page *n* is the right starting point.
        Implementations may use context.last_date or a fixed heuristic.
        """
        raise NotImplementedError

    def _advance(self, n: int) -> int:
        """
        Compute the next page to probe during the initial-page search.
        Default: linear increment. Override for binary search or other strategies.
        """
        return n + 1

