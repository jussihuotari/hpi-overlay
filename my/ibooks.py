"""
Apple iBooks annotations. Read the iBooks' annotations database using
https://github.com/jussihuotari/pinotate

I wonder if it would be possible to extract reading progress events from the
database, similar to https://github.com/karlicoss/kobuddy
"""
REQUIRES = ['pinotate']

from my.config import ibooks as config # type: ignore[attr-defined]
from pinotate.core import IBooksWorker # type: ignore
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, NamedTuple, Optional, List

# Typed copy of https://github.com/jussihuotari/pinotate/blob/master/core/highlight.py
class Highlight(NamedTuple):
    text: str
    heading: str
    created: datetime
    chapter: int
    ref_in_chapter: int

class Book(NamedTuple):
    author: str
    title: str
    highlights: List[Highlight]

def _parse_date(seconds_since_ref_date: int) -> datetime:
    reference_date = datetime(2001, 1, 1, 0, 0, 0)
    delta_since_reference = timedelta(seconds=seconds_since_ref_date)
    utc = (reference_date + delta_since_reference)
    return utc

def _iter_books() -> Iterator[Book]:
    worker = IBooksWorker()
    for (author, title) in worker.titles():
        aid = worker.asset_id(title)
        data = worker.highlights(aid)
        #print(f"Processing book '{title}', {aid}.")
        highlights = [Highlight(d.text, d.heading, _parse_date(d.created), d.chapter, d.ref_in_chapter) for d in data]
        if len(highlights):
            yield Book(author = author, title = title, highlights = highlights)

def books() -> List[Book]:
    return list(sorted(_iter_books(), key=lambda b: (b.author, b.title)))

