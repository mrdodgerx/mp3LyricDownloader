from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
import os
from configparser import ConfigParser
from modules.google import send_notification

config = ConfigParser()
config.read('env.ini')

MP3_OUTPUT = config.get('OUTPUT', 'MP3')

class YoutubeMp3():
    def __init__(self, song_title) -> None:
        self.song_title = song_title
        self.video_link = ''
    
    def youtube_search(self):
        # print(self.song_title)
        videosSearch = VideosSearch(self.song_title, limit = 2)
        results = videosSearch.result()
        # print(results)
        if results:
            self.video_link = results["result"][0]["link"]

    def download_mp3(self):
        if self.video_link:
            try:
                # Create output directory if it doesn't exist
                if not os.path.exists(MP3_OUTPUT):
                    os.makedirs(MP3_OUTPUT)

                # Define the MP3 path with video_title.mp3
                video_title = self.song_title.strip()
                mp3_path = os.path.join(MP3_OUTPUT, f"{video_title}.mp3")

                # Check if the file already exists
                if os.path.exists(mp3_path):
                    print(f"File '{mp3_path}' already exists. Skipping download.")
                    return

                # Download the YouTube video
                yt = YouTube(self.video_link)
                audio_stream = yt.streams.filter(only_audio=True).first()

                if audio_stream:
                    # Set the download path
                    video_download_path = audio_stream.download(output_path=MP3_OUTPUT)

                    # Convert to MP3
                    AudioSegment.from_file(video_download_path).export(mp3_path, format='mp3')

                    # Optionally, remove the original file
                    os.remove(video_download_path)

                    print(f'Successfully downloaded and converted to {mp3_path}')
                    send_notification('Song is Downloaded', video_title)

            except Exception as e:
                print(f'An error occurred: {e}')
    
    def run(self):
        self.youtube_search()
        self.download_mp3()

