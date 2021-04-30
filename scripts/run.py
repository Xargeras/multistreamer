import subprocess
from signal import SIGINT


class Server:
    __instance = None
    server_uid = None
    broadcasts = {}
    RTSP = 1
    RTMP = 2
    host = 'localhost'
    rtsp_url = f'rtsp://{host}:8554'
    rtmp_url = f'rtmp://{host}'

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

    def start_broadcast(self, id, internal_url, output_url, key, type):
        if type == self.RTMP:
            url = self.rtmp_url
        else:
            url = self.rtsp_url
        input_url = f'{url}/{internal_url}'
        self.broadcasts[id] = subprocess.Popen(['python3', 'scripts/run_broadcaster.py', input_url, output_url, key])

    def stop_broadcast(self, id):
        self.broadcasts[id].send_signal(SIGINT)
        self.broadcasts.pop(id)

    def is_broadcast_online_list(self, broadcast_list):
        return any(self.is_broadcast_online(broadcast.id) for broadcast in broadcast_list)

    def start_broadcast_list(self, broadcast_list, key, type):
        for broadcast in broadcast_list:
            if not self.is_broadcast_online(broadcast):
                self.start_broadcast(broadcast.id, key, broadcast.url, broadcast.key, type)

    def stop_broadcast_list(self, broadcast_list):
        for broadcast in broadcast_list:
            if self.is_broadcast_online(broadcast.id):
                self.stop_broadcast(broadcast.id)

    def get_url(self, type):
        if type == self.RTMP:
            return self.rtmp_url
        else:
            return self.rtsp_url
