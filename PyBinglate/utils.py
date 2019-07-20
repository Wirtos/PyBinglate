from pprint import pprint
from typing import Sequence
import re


def _list_lstrip(s: str, args: Sequence[str]) -> str:
    match = re.finditer(r'|'.join(re.escape(i) for i in args), s)
    start = 0
    for i in match:
        if i.span()[0] == start:
            start = i.span()[1]
        else:
            break
    return s[start:]


def _list_rstrip(s: str, args: Sequence[str]) -> str:
    match = re.finditer(r'|'.join(re.escape(i[::-1]) for i in args), s[::-1])
    end = 0
    for i in match:
        if i.span()[0] == end:
            end = i.span()[1]
        else:
            break
    return s[:-end] if end != 0 else s


def _list_strip(s: str, args: Sequence[str]) -> str:
    return _list_rstrip(_list_lstrip(s, args), args)


def get_latest_supported_languages():
    import requests
    import bs4
    import lxml
    r = requests.get('https://www.bing.com/translator/?setlang=en')
    return {el['value']: el.text for el in bs4.BeautifulSoup(r.text, 'lxml').find('select', {"id": 'tta_srcsl'})}


if __name__ == '__main__':
    pprint(get_latest_supported_languages())
