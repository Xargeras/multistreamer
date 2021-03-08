import subprocess
from time import sleep


def run_rtsp_server():
    server_uid = subprocess.Popen(['docker', 'run', '--rm', '--network=host', 'aler9/rtsp-simple-server'])
    try:
        while True:
            if server_uid.poll() is not None:
                server_uid = subprocess.Popen(['docker', 'run', '--rm', '--network=host', 'aler9/rtsp-simple-server'])
                sleep(2)
    except KeyboardInterrupt:
        server_uid.terminate()


if __name__ == '__main__':
    run_rtsp_server()
