from requests import get
from bs4 import BeautifulSoup
import os
from configparser import ConfigParser
import subprocess
from urllib.parse import quote



config = ConfigParser()
config.read('env.ini')

LYRICS_OUTPUT = config.get('OUTPUT', 'LYRICS')
WAV_OUTPUT = config.get('RECORDING', 'WAV_OUTPUT')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"6.8.9"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

class Google():
    def __init__(self,) -> None:
        
        self.url = 'https://www.google.com/search?q='
        self.header = headers  # Headers(os="linux", headers=True).generate()
        self.song_title = None
        self.song_search_url = None
        self.lyrics = None

        self.save_lyrics_dirs = LYRICS_OUTPUT
        
    def recognize_song(self):
        self.song_title = os.popen(f'songrec recognize {WAV_OUTPUT}').read()
        # print(self.song_title )
    
    def searchSong(self):
        lyric_div_tag = None
        song_title_url = f'{self.song_title} lyrics'
        self.song_search_url = f'{self.url }{song_title_url}'
        # print(self.song_search_url)
        r = get(self.song_search_url, headers=self.header)
        if r.status_code == 200:
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            for s in ['Z1hOCe', 'WbKHeb']:
                lyric_div = soup.find_all("div", {"class": s}) # WbKHeb
                # print(lyric_div)
                if len(lyric_div) == 0:
                    pass
                else:
                    lyric_div_tag = remove_tags(lyric_div[0])
                    break
        else:
            return f'Error in request. Status code: {r.status_code}\n URL: {self.song_search_url}'
        # print(lyric_div_tag)
        self.lyrics = lyric_div_tag

    def save_lyrics(self):
        create_folder(self.save_lyrics_dirs)
        filename = f'{quote(self.song_title.strip())}.txt'
        if not os.path.exists(f"{self.save_lyrics_dirs}/{filename}"):
            f = open(f"{self.save_lyrics_dirs}/{filename}", "w")
            f.write(f"{self.lyrics}")
            f.close()
            print(f"{self.song_title.strip()}.txt has been successfully saved.")
            send_notification('Lyric is Downloaded', self.song_title.strip())
        else:
            print(f"{self.song_title.strip()}.txt already exists in the folder. Skipping save.")

def remove_tags(soup):

    for div in soup.find_all("div", {'class':'lyrics-to'}): 
        div.decompose()
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    lyrics_Text = '\n'.join(soup.stripped_strings)
    return lyrics_Text

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def send_notification(title, message):
    command = ['notify-send', title, message]
    subprocess.run(command)