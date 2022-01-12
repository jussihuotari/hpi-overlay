"""
Parse Evernote export that has been converted to markup using
https://github.com/wormi4ok/evernote2md
"""

from my.config import evernote_md as config # type: ignore[attr-defined]
from my.core import get_files #, Stats #, Res

import re
from datetime import datetime
from pathlib import Path
from typing import Iterator, NamedTuple, Optional, List

class Heading(NamedTuple):
    title: str
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]]

# https://stackoverflow.com/questions/44287623/a-way-to-subclass-namedtuple-for-purposes-of-typechecking
class Note(NamedTuple):
    heading: Heading
    text_md: str
    text_preproc: str

def _parse_date(d: str) -> datetime:
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S %z")

def _parse_heading(raw: str) -> NamedTuple:
    fields = {}
    for row in raw.split('\n'):
        a = row.split(': ', 1)
        if len(a) > 1:
            fields[a[0]] = a[1].strip("'")
    heading = Heading(
            title = fields["title"], # if title in fields else ""
            created_at = _parse_date(fields["date"]),
            updated_at = _parse_date(fields["updated_at"]),
            tags = fields["tags"] if "tags" in fields else None
            )
    return heading

def _preprocess_md(markup: str) -> str:
    """
    Simple preprocessing to remove formatting, links, images. Downcase letters
    and handle some emojis. The preprocessed text can be input to e.g. Fasttext
    for generating word vectors and calculating document similarities.

    Inspired by https://github.com/facebookresearch/fastText/blob/main/wikifil.pl
    """
    # Remove images
    re_images = re.compile(r'!\[.+\]\(.+\)')
    markup = re_images.sub("", markup)
    # Remove links
    re_links = re.compile(r'\[(.+)\]\(.+\)')
    markup = re_links.sub(r'\1', markup)
    re_https = re.compile(r'https?')
    markup = re_https.sub('', markup)
    # Currency (120€) and points (88p) and such (180°)
    # issues with eg. 2020-05
    re_euro = re.compile(r'\s\d+([^\d])\W')
    markup = re_euro.sub(r' nro\1 ', markup)
    # Remove punctuation, this removes also aren't -> aren t. Good or bad?
    re_punct = re.compile(r'[!"#$%&\'’•()*+,-./:;<=>?@\[\]^_`{|}~\\]')
    markup = re_punct.sub(' ', markup)
    # Numbers to words
    # https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
    markup = (markup.replace('1', ' one ').
            replace('2', ' two ').
            replace('3', ' three ' ).
            replace('4', ' four ' ).
            replace('5', ' five ' ).
            replace('6', ' six ' ).
            replace('7', ' seven ' ).
            replace('8', ' eight ' ).
            replace('9', ' nine ' ).
            replace('0', ' zero ' ))
    # Remove linefeeds and whitespace
    markup = " ".join(markup.split())

    return markup.lower()

def _iter_notes() -> Iterator[Note]:
    for path in Path(config.export_path).glob('*.md'):
        #print(f"Reading {path}")
        raw = path.read_text(errors="ignore")
        raw_head,content = raw.split("\n\n---\n\n", 1)
        heading = _parse_heading(raw_head)
        yield Note(
                heading = heading,
                text_md = content,
                text_preproc = _preprocess_md(content)
                )

def get_notes() -> List[Note]:
    return list(sorted(_iter_notes(), key=lambda b: b.heading.created_at)) #, reverse=True))

