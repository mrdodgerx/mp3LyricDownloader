import os
from typing import Optional
from configparser import ConfigParser
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, error

from modules.google import send_notification

config = ConfigParser()
config.read('env.ini')

MP3_OUTPUT = config.get('OUTPUT', 'MP3')

class YoutubeMp3:
    def __init__(self, song_title: str):
        self.song_title = song_title
        self.video_link: Optional[str] = None
        self.mp3_path: Optional[str] = None

    def youtube_search(self) -> None:
        try:
            videos_search = VideosSearch(self.song_title, limit=2)
            results = videos_search.result()
            if results and 'result' in results and results['result']:
                self.video_link = results['result'][0]['link']
            else:
                print(f"No match found for the song: {self.song_title}")
        except Exception as e:
            print(f"An error occurred during YouTube search: {e}")

    def download_mp3(self) -> None:
        if not self.video_link:
            print("No video link found. Skipping download.")
            return

        try:
            os.makedirs(MP3_OUTPUT, exist_ok=True)
            video_title = self.song_title.strip()
            self.mp3_path = os.path.join(MP3_OUTPUT, f"{video_title}.mp3")

            if os.path.exists(self.mp3_path):
                print(f"File '{self.mp3_path}' already exists. Skipping download.")
                return

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(MP3_OUTPUT, f"{video_title}.%(ext)s"),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_link])

            self._add_metadata(video_title)
            print(f'Successfully downloaded and converted to {self.mp3_path}')
            send_notification('Song Downloaded', video_title)
        except Exception as e:
            print(f'An error occurred during download: {e}')

    def _add_metadata(self, video_title: str) -> None:
        try:
            audio = EasyID3(self.mp3_path)
            title_artist = video_title.split(' - ')
            if len(title_artist) > 1:
                audio['title'] = title_artist[1].strip()
                audio['artist'] = title_artist[0].strip()
            else:
                audio['title'] = video_title
                audio['artist'] = 'Unknown Artist'
            audio['genre'] = 'YouTube'
            audio.save()
        except Exception as e:
            print(f'Failed to add metadata: {e}')

    def add_lyrics(self, lyrics: str) -> None:
        if not self.mp3_path or not os.path.exists(self.mp3_path):
            print(f"MP3 file does not exist: {self.mp3_path}")
            return

        try:
            audio = ID3(self.mp3_path)
            audio.add(USLT(encoding=3, lang='eng', desc='Lyrics', text=lyrics))
            audio.save()
            print(f'Lyrics added to {self.mp3_path}')
        except error as e:
            print(f'Failed to add lyrics: {e}')

    def run(self) -> None:
        self.youtube_search()
        self.download_mp3()

# Example usage (commented out)
# if __name__ == "__main__":
#     song_title = "Owl City - Fireflies"
#     youtube_mp3 = YoutubeMp3(song_title)
#     youtube_mp3.run()
#     lyrics = "You would not believe your eyes, if ten million fireflies..."
#     youtube_mp3.add_lyrics(lyrics)
