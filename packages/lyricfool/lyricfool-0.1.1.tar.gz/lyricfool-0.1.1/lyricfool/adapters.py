import re
import requests
from bs4 import BeautifulSoup as bs


class BaseAdapter:
    def __init__(self, url, spacer):
        self.url = url
        self.spacer = spacer

    def generate_url(self, artist, title):
        return self.url.format(artist=self.clean(artist), title=self.clean(title))

    def clean(self, text):
        return text.replace(' ', self.spacer)

    def request_page(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            r.raise_for_status()
        return bs(r.text, 'lxml')

    def __call__(self, artist, title):
        return self.get_lyrics(artist, title)

    def get_lyrics(self):
        raise Exception("BaseAdapter is abstract")


class AZLyricAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('http://www.azlyrics.com/lyrics/{artist}/{title}', '+')

    def get_lyrics(self, artist, title):
        url = self.generate_url(artist, title)
        soup = self.request_page(url)
        return soup.find("div", attrs={"class": None, "id": None}).get_text()


class GeniusAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('https://genius.com/{artist}-{title}-lyrics', '-')

    def get_lyrics(self, artist, title):
        url = self.generate_url(artist, title)
        return self.request_page(url).find('lyrics').text.strip()


class LyricsWikiaAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('http://lyrics.wikia.com/wiki/{artist}:{title}', '_')

    def get_lyrics(self, artist, title):
        url = self.generate_url(artist, title)
        page = self.request_page(url)
        lyrics = page.find("div", attrs={"class": "lyricbox"})
        refined = bs(re.sub(r'<br/>', '\n', str(lyrics)), 'lxml')
        return refined.get_text()


class MetroLyricsAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('http://www.metrolyrics.com/{title}-lyrics-{artist}.html', '-')

    def get_lyrics(self, artist, title):
        url = self.generate_url(artist, title)
        page = self.request_page(url)
        return '\n'.join([verse.get_text() for verse in page.find_all('p', class_='verse')])

    def clean(self, text):
        text = text.split(' ')
        if text[0].lower() == 'the':
            text.pop(0)
        return super().clean(' '.join(text))
