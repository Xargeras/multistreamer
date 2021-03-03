import subprocess
from signal import SIGINT


class Server:
    __instance = None
    server_uid = None
    url = 'rtsp://localhost:8554'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        pass

    def is_server_online(self):
        if not self.server_uid:
            return False
        return self.server_uid.poll() is None

    def start_server(self):
        self.server_uid = subprocess.Popen(['python3', 'scripts/run_rtsp_server.py'])

    def stop_server(self):
        self.server_uid.send_signal(SIGINT)

    def start_broadcast(self, internal_url, key):
        youtube_url = 'rtmp://a.rtmp.youtube.com/live2'
        input_url = f'{self.url}/{internal_url}'
        self.youtube_uid = subprocess.Popen(['python3', 'scripts/run_broadcaster.py', input_url, youtube_url, key])

    def stop_broadcast(self):
        self.youtube_uid.send_signal(SIGINT)