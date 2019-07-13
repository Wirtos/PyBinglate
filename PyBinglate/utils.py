import requests
import bs4
from pprint import pprint

def get_latest_supported_languages():
    r = requests.get('https://www.bing.com/translator/?setlang=en')
    return {el['value']: el.text for el in bs4.BeautifulSoup(r.text, 'lxml').find('select', {"id": 'tta_srcsl'})}

if __name__ == '__main__':
    pprint(get_latest_supported_languages())