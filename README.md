..
# Music Recognition and Download Application

This application is built using Python and allows you to recognize music, search for lyrics, and download MP3 files.

## Requirements

- Python 3.x
- pip (Python package installer)
- Dependencies listed in `requirements.txt`
- SongRec: Install from [GitHub](https://github.com/marin-m/SongRec)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mrdodgerx/mp3LyricDownloader.git
    cd mp3LyricDownloader
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install SongRec: 
   Read SongRec to install

4. Create `env.ini`:

    ```ini
    [RECORDING]
    FS = 44100
    SECONDS = 10
    CHANNELS = 2
    WAV_OUTPUT = /tmp/output.wav

    [OUTPUT]
    LYRICS = /path/to/lyrics/output
    MP3 = /path/to/mp3/output
    ```

## Usage

Run the `main.py` script:

```bash
python main.py
