from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, error
import os
from configparser import ConfigParser
from modules.google import send_notification

config = ConfigParser()
config.read('env.ini')

MP3_OUTPUT = config.get('OUTPUT', 'MP3')

class YoutubeMp3():
    def __init__(self, song_title) -> None:
        self.song_title = song_title
        self.video_link = None
        self.mp3_path = None
    
    def youtube_search(self):
        videosSearch = VideosSearch(self.song_title, limit=2)
        results = videosSearch.result()
        if results and 'result' in results and results['result']:
            self.video_link = results['result'][0]['link']
        else:
            print(f"No match for the song: {self.song_title}")
    
    def download_mp3(self):
        if not self.video_link:
            print("No video link found. Skipping download.")
            return
        
        try:
            # Ensure output directory exists
            os.makedirs(MP3_OUTPUT, exist_ok=True)

            # Define the MP3 path with video_title.mp3
            video_title = self.song_title.strip()
            self.mp3_path = os.path.join(MP3_OUTPUT, f"{video_title}.mp3")

            # Check if the file already exists
            if os.path.exists(self.mp3_path):
                print(f"File '{self.mp3_path}' already exists. Skipping download.")
                return

            # Download the YouTube video
            yt = YouTube(self.video_link)
            audio_stream = yt.streams.filter(only_audio=True).first()

            if audio_stream:
                # Download the audio stream
                video_download_path = audio_stream.download(output_path=MP3_OUTPUT)

                # Convert to MP3
                AudioSegment.from_file(video_download_path).export(self.mp3_path, format='mp3')

                # Remove the original file
                os.remove(video_download_path)

                # Add metadata
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

                print(f'Successfully downloaded and converted to {self.mp3_path}')
                send_notification('Song is Downloaded', video_title)
            else:
                print("No audio stream found in the video.")
        except Exception as e:
            print(f'An error occurred: {e}')
    
    def add_lyrics(self, lyrics):
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
    
    def run(self):
        self.youtube_search()
        self.download_mp3()


