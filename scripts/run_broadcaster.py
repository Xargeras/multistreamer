import subprocess
import sys
from time import sleep


def run_broadcaster():
    input_url = sys.argv[0]
    output_url = sys.argv[2]
    key = sys.argv[3]
    broadcaster_uid = subprocess.Popen(['ffmpeg', '-i', input_url, '-f', 'flv', f'{output_url}/{key}'])
    try:
        while True:
            if broadcaster_uid.poll() is not None:
                broadcaster_uid = subprocess.Popen(['ffmpeg', '-i', input_url, '-f', 'flv', f'{output_url}/{key}'])
                sleep(2)
    except KeyboardInterrupt:
        broadcaster_uid.terminate()


if __name__ == '__main__':
    run_broadcaster()
