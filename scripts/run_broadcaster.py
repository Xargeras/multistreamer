import subprocess
import sys
from time import sleep


def run_broadcaster():
    input_url = sys.argv[1]
    output_url = sys.argv[2]
    key = sys.argv[3]
    bitrate = sys.argv[4]
    run_command = ['ffmpeg', '-i', input_url, '-b:v', bitrate + 'k', '-vcodec', 'libx264', '-f', 'flv', f'{output_url}/{key}']
    broadcaster_uid = subprocess.Popen(run_command)
    try:
        while True:
            if broadcaster_uid.poll() is not None:
                broadcaster_uid = subprocess.Popen(run_command)
                sleep(2)
    except KeyboardInterrupt:
        broadcaster_uid.terminate()


if __name__ == '__main__':
    run_broadcaster()
