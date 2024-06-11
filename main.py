import sounddevice as sd
from scipy.io.wavfile import write
from configparser import ConfigParser
import psutil
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

def is_ncmpcpp_running():
    """Check if ncmpcpp is running."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        # print(proc.info['name'])
        if proc.info['name'] == 'ncmpcpp' or proc.info['name'] == 'mopidy':
            return True
    return False


if __name__ == "__main__":
    while True:
        if is_ncmpcpp_running():
            print("ncmpcpp is running. Skipping recording...")
            time.sleep(3)  # Sleep for a while before checking again
            continue

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
                y.add_lyrics(g.lyrics)
        # Sleep for a while before the next iteration
        time.sleep(3)
