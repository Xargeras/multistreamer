import subprocess
from time import sleep


def run_youtube_broadcaster():
    youtube_url = 'rtmp://a.rtmp.youtube.com/live2'
    key = '95hb-4hcj-5fpa-1063-4ws6'
    input_url = 'rtsp://localhost:8554/mystream'
    broadcaster_uid = subprocess.Popen(['ffmpeg', '-i', input_url, '-f', 'flv', f'{youtube_url}/{key}'])
    try:
        while True:
            if broadcaster_uid.poll() is not None:
                broadcaster_uid = subprocess.Popen(['ffmpeg', '-i', input_url, '-f', 'flv', f'{youtube_url}/{key}'])
                sleep(2)
    except KeyboardInterrupt:
        broadcaster_uid.terminate()


if __name__ == '__main__':
    run_youtube_broadcaster()
