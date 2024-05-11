import sounddevice as sd
from scipy.io.wavfile import write
from configparser import ConfigParser

from modules.google import Google
from modules.youtube import YoutubeMp3
# from modules.musicmatch import MusicMatch
import time

config = ConfigParser()
config.sections()
config.read('env.ini')

FS = config.getint('RECORDING', 'FS')
SECONDS = config.getint('RECORDING', 'SECONDS')
CHANNELS =config.getint('RECORDING', 'CHANNELS')
WAV_OUTPUT = config.get('RECORDING', 'WAV_OUTPUT')

def record_wav():
    wav_record = sd.rec(int(SECONDS * FS), samplerate=FS, channels=CHANNELS)
    sd.wait()  # Wait until recording is finished
    write(WAV_OUTPUT, FS, wav_record)  # Save as WAV file 


if __name__ == "__main__":
    while True:
        record_wav()
        g = Google()
        g.recognize_song()
        if g.song_title:
            # print(g.song_title)
            y = YoutubeMp3(g.song_title.strip())
            y.run()
            g.searchSong()
            if g.lyrics:
                g.save_lyrics()
        time.sleep(3)

