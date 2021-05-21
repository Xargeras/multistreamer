import subprocess
from time import sleep


def run_rtsp_server():
    run_command = ['./rtsp-server/rtsp-simple-server', './rtsp-server/rtsp-simple-server.yml']
    server_uid = subprocess.Popen(run_command)
    try:
        while True:
            if server_uid.poll() is not None:
                server_uid = subprocess.Popen(run_command)
                sleep(2)
    except KeyboardInterrupt:
        server_uid.terminate()


if __name__ == '__main__':
    run_rtsp_server()
