"""
Parse the Goodreads data export.

Inspired by: 

* https://github.com/karlicoss/goodrexport/blob/master/src/goodrexport/dal.py
* https://github.com/karlicoss/exporthelpers
"""

from my.config import goodreads_export as config # type: ignore[attr-defined]
from my.core import get_files #, Stats #, Res

from csv import DictReader
from datetime import datetime
from typing import Iterator, NamedTuple, Optional, List

def _parse_date(d1: str, d2: str) -> datetime:
    d = d1 if d1 else d2
    return datetime.strptime(d, "%Y/%m/%d")

def _parse_year_published(d: str) -> int:
    return int(d) if d else -1

class Book(NamedTuple):
    book_id: str
    title: str
    author: str
    rating: int
    review: Optional[str]
    isbn13: Optional[str]
    publisher: str
    publication_year: int
    date_read: datetime

def _iter_books() -> Iterator[Book]:
    source_file = max(get_files(config.export_path, glob='*.csv'))
    with source_file.open() as f:
        for row in DictReader(f):
            yield Book(
                    book_id = row["Book Id"],
                    title = row["Title"],
                    author = row["Author"],
                    rating = int(row["My Rating"]),
                    review = row["My Review"],
                    isbn13 = row["ISBN13"].replace('=','').strip('"'),
                    publisher = row["Publisher"],
                    publication_year = _parse_year_published(row["Year Published"]),
                    date_read = _parse_date(row["Date Read"], row["Date Added"])
                    )

def get_books() -> List[Book]:
    return list(sorted(_iter_books(), key=lambda b: b.date_read)) #, reverse=True))



