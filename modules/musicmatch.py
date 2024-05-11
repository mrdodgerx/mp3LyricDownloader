from requests import get
import urllib.parse
from bs4 import BeautifulSoup
import os
from configparser import ConfigParser
from modules.google import create_folder

config = ConfigParser()
config.sections()
config.read('env.ini')

LYRICS_OUTPUT = config.get('OUTPUT', 'LYRICS')
WAV_OUTPUT = config.get('RECORDING', 'WAV_OUTPUT')

headers = {
    'authority': 'www.musixmatch.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
}

class MusicMatch():
    def __init__(self) -> None:
        self.url = 'https://www.musixmatch.com'
        self.header = headers
        self.song_title = None
        self.song_url = None
        self.song_search_url = None

    def read_record_wav(self):
        self.song_title = os.popen(f'songrec recognize {WAV_OUTPUT}').read()

    def searchSong(self):
        song_title_url = urllib.parse.quote(self.song_title)
        url = f'{self.url }/search/{song_title_url}'
        # print(url)
        r = get(url, headers=self.header)
        if r.status_code == 200:
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            pageResult = soup.find_all("div", {"class": "box-style-plain"})
            if len(pageResult) == 0:
                print('Result Not Found')
            else:
                resultUrl = pageResult[0].find_all('a', href=True)
                # print(resultUrl)
                for i, a in enumerate(resultUrl):
                    if i == 0:
                        self.song_search_url = f"{self.url }{a['href']}"
                        # print("WHAT IS THIS ", self.song_search_url)
        else:
            print(f'Error in request. Status code: {r.status_code}\n URL: {url}')
        return

    def get_lyrics(self):
        if self.song_search_url:
            r = get(self.song_search_url.replace('/add',''), headers=self.header)
            if r.status_code == 200:
                # print(r.text)
                soup = BeautifulSoup(r.text, 'html.parser')
                lyricResult = soup.find_all("div", {"class": "mxm-lyrics"})
                # print(len(lyricResult))
                if len(lyricResult) <=1:
                    print('Lyrics Not Found')
                else:
                    # print(lyricResult[1])
                    return remove_tags(lyricResult[1])
            if r.status_code == 404:
                self.get_lyrics()
            else:
                print(f'Error in request. Status code: {r.status_code}\n URL: {self.song_search_url}')
            return
        return
    
    def run(self):
        self.read_record_wav()
        self.searchSong()
        print(self.song_title)
        print(self.song_search_url)
        print(self.get_lyrics())

def remove_tags(soup):

    for div in soup.find_all("div", {'class':'lyrics-to'}): 
        div.decompose()
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    lyrics_Text = ' '.join(soup.stripped_strings)
    # return data by retrieving the tag content
    splitStr = ['Informar de un problema Writer(s):', 'Report a problem Writer(s):']
    rStr = ''
    for s in splitStr:
        if len(lyrics_Text.split(s))>0:
                rStr = lyrics_Text.split(s)[0]
    return rStr