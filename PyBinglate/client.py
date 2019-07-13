import requests
from typing import Sequence, Union
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


LANGUAGES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'auto-detect': 'Auto-Detect',
    'bg': 'Bulgarian',
    'bn-BD': 'Bangla',
    'bs-Latn': 'Bosnian (Latin)',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fil': 'Filipino',
    'fj': 'Fijian',
    'fr': 'French',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'ht': 'Haitian Creole',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mg': 'Malagasy',
    'ms': 'Malay (Latin)',
    'mt': 'Maltese',
    'mww': 'Hmong Daw',
    'nl': 'Dutch',
    'no': 'Norwegian Bokmål',
    'otq': 'Querétaro Otomi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sm': 'Samoan',
    'sr-Cyrl': 'Serbian (Cyrillic)',
    'sr-Latn': 'Serbian (Latin)',
    'sv': 'Swedish',
    'sw': 'Kiswahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tlh': 'Klingon',
    'to': 'Tongan',
    'tr': 'Turkish',
    'ty': 'Tahitian',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'yua': 'Yucatec Maya',
    'yue': 'Cantonese (Traditional)',
    'zh-Hans': 'Chinese Simplified',
    'zh-Hant': 'Chinese Traditional'
}

EMPTY_CHARS = (
    '\n', ' ', '\xa0', '\u180e', '\u2000',
    '\u2001', '\u2002', '\u2003',
    '\u2004', '\u2005', '\u2006',
    '\u2007', '\u2008', '\u2009',
    '\u200a', '\u200b', '\u202f',
    '\u205f', '\u2063', '\u3000',
    'ㅤ', '\ufeff'
)


class BingError(Exception):
    pass


error_messages = {
    400: BingError("Invalid input values [400]")
}


class BingTranslator:
    def __init__(self, timeout=10.0):
        """
        :param timeout: try to connect for x seconds without raising error
        """
        self._session = requests.session()
        self.timeout = timeout

    def detect_language(self, text: str) -> str:
        """
        :param str text:
        :return: str detected language from PyBinglate.LANGUAGES
        """

        return self._session.post('https://www.bing.com/ttranslatev3',
                                  data={'text': text, 'fromLang': 'auto-detect', 'to': 'en'}
                                  ).json()[0]['detectedLanguage']['language']

    def translate(self, text: str, dest: str, src: str = None, raw=False) -> Union[str, dict]:
        """
        :param str text:
        :param str dest: language from PyBinglate.LANGUAGES
        :param str src: (optional) language from PyBinglate.LANGUAGES
        :param bool raw: (optional) return dict of response instead of string translation
        :return str: translated string
        """
        src = None if src in ('auto', 'auto-detect', None) else src
        text = _list_strip(text, EMPTY_CHARS)

        if dest not in LANGUAGES:
            err = 'Invalid dest value: {}'.format(dest)
            raise ValueError(err)

        elif src not in LANGUAGES if src is not None else False:
            err = 'Invalid src value: {}'.format(src)
            raise ValueError(err)

        if not text:
            err = 'Text cannot be empty'
            raise ValueError(err)

        if src is not None:
            req = self._session.post('https://www.bing.com/ttranslatev3',
                                     data={'text': text, 'fromLang': src, 'to': dest}, timeout=self.timeout)
        else:
            req = self._session.post('https://www.bing.com/ttranslatev3',
                                     data={'text': text, 'fromLang': 'auto-detect', 'to': dest})

        resp = req.json()
        status_code = req.status_code
        if status_code != 200:
            msg = error_messages.get(status_code)
            raise msg if msg else BingError('Unknown error: [{}]'.format(status_code))
        return resp[0]['translations'][0]['text'] if not raw else resp
