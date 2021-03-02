import subprocess
from signal import SIGINT


def main():
    server_uid = subprocess.Popen(['python3', 'run_rtsp_server.py'])
    youtube_uid = subprocess.Popen(['python3', 'run_broadcaster.py'])

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server_uid.send_signal(SIGINT)
        youtube_uid.send_signal(SIGINT)


if __name__ == '__main__':
    main()
