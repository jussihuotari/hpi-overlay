"""
Parse Wordpress posts export XML. 
"""
REQUIRES = ['lxml']

from my.config import wordpress as config # type: ignore[attr-defined]
from my.core import get_files #, Stats #, Res

from datetime import datetime
from pathlib import Path
from lxml import etree # type: ignore
from lxml.etree import Element # type: ignore
from typing import Iterator, NamedTuple, Optional, List

class Post(NamedTuple):
    post_id: int
    title: str
    link: str
    created_at: datetime
    updated_at: datetime
    text: str

def _parse_date(d: str) -> datetime:
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

def _parse_post(item: Element) -> Post:
    title = item.findtext('title')
    #print(f"Parsing post '{title}', modified: {item.findtext('{*}post_modified_gmt')}.")
    return Post(
            post_id = item.findtext('{*}post_id'),
            title = item.findtext('title'), # or: tree.xpath('//item/title')[0].text
            link = item.findtext('link'),
            created_at = _parse_date(item.findtext('{*}post_date_gmt')),
            updated_at = _parse_date(item.findtext('{*}post_modified_gmt')),
            text = item.findtext('{*}encoded') # or: etree.parse(str(get_files(config.export_path)[-1])).xpath('/rss/channel/item/content:encoded', namespaces=tree.getroot().nsmap
            )

def posts() -> Iterator[Post]:
    file = get_files(config.export_path)[-1] # Latest export
    tree = etree.parse(str(file))
    items = tree.xpath("//item")
    for item in items:
        yield _parse_post(item)

