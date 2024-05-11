from youtubesearchpython import VideosSearch
from pytube import YouTube
import os
from configparser import ConfigParser

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
            yt = YouTube(self.video_link)
            video_title = self.song_title.strip()
            audio_stream = yt.streams.filter(only_audio=True).first()

            if audio_stream:
                mp3_file = f'{video_title}.mp3'
                if not os.path.exists(os.path.join(MP3_OUTPUT, mp3_file)):
                    out_file = audio_stream.download(output_path=MP3_OUTPUT, filename=video_title)
                    # save the file with .mp3 extension
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    print(f'{video_title} has been successfully downloaded.')
                else:
                    print(f'{mp3_file} already exists in the folder. Skipping download.')
            else:
                print('No audio stream available for download.')
    
    def run(self):
        self.youtube_search()
        self.download_mp3()

