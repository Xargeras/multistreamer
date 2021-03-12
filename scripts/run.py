import subprocess
from signal import SIGINT


class Server:
    __instance = None
    server_uid = None
    broadcasts = {}
    url = 'rtsp://localhost:8554'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if not Server.__instance:
            Server.__instance = Server()
        return Server.__instance

    def is_server_online(self):
        if not self.server_uid:
            return False
        return self.server_uid.poll() is None

    def start_server(self):
        self.server_uid = subprocess.Popen(['python3', 'scripts/run_rtsp_server.py'])

    def stop_server(self):
        self.server_uid.send_signal(SIGINT)

    def is_broadcast_online(self, id):
        uid = self.broadcasts.get(id, None)
        if not uid:
            return False
        return uid.poll() is None

    def start_broadcast(self, id, internal_url, output_url, key):
        input_url = f'{self.url}/{internal_url}'
        self.broadcasts[id] = subprocess.Popen(['python3', 'scripts/run_broadcaster.py', input_url, output_url, key])

    def stop_broadcast(self, id):
        self.broadcasts[id].send_signal(SIGINT)
        self.broadcasts.pop(id)
