import json
import logging
import os
import runpy
import socket
import subprocess

BUFFER_SIZE = 255
ENCODING = "utf-8"

log = logging.getLogger(__name__)


class Config:
    def __init__(self, filepath):
        attrs = runpy.run_path(filepath)
        for setting, setting_value in attrs.items():
            if setting.isupper():
                setattr(self, setting, setting_value)

    @staticmethod
    def store(filepath, **kwargs):
        with open(filepath, "w") as f:
            for k, v in kwargs.items():
                f.write('{} = {}\n'.format(k, repr(v)))



class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)


def daemon(server_address, execute, condition=lambda: True):
    ss = Socket()
    ss.bind(server_address)
    ss.listen(1)
    try:
        while condition():
            log.debug("SERVER: waiting for a connection...")
            sc, ad = ss.accept()
            log.debug("SERVER: connection from %s", ad)
            request = bytes()
            while True:
                log.debug("SERVER: receiving...")
                data = sc.recv(BUFFER_SIZE)
                log.debug("SERVER: received %s", data)
                if not data:
                    log.debug("SERVER: no more data to receive")
                    break
                request += data
            response = execute(request.decode(ENCODING))
            log.debug("SERVER: sending '%s' ...", response)
            sc.sendall(response.encode(ENCODING))
            log.debug("SERVER: sent")
            log.debug("SERVER: closing client socket...")
            sc.close()
            log.debug("SERVER: closed client socket")
    finally:
        log.debug("SERVER: closing server socket...")
        ss.close()
        log.debug("SERVER: closed server socket")


def client(server_address, request):
    ss = Socket()
    try:
        log.debug("CLIENT: connecting '%s' ...", server_address)
        ss.connect(server_address)
        log.debug("CLIENT: connected")
        log.debug("CLIENT: sending '%s' ...", request)
        ss.sendall(request.encode(ENCODING))
        ss.shutdown(socket.SHUT_WR)
        log.debug("CLIENT: sent")
        response = bytes()
        while True:
            log.debug("CLIENT: receiving...")
            data = ss.recv(BUFFER_SIZE)
            log.debug("CLIENT: received %s", data)
            if not data:
                log.debug("CLIENT: no more data to receive")
                break
            response += data
        return response.decode(ENCODING)
    finally:
        log.debug("CLIENT: closing...")
        ss.close()
        log.debug("CLIENT: closed")


def executor(exe_path, command):
    exe_name, args = json.loads(command)
    log.debug("executor %s %s", exe_name, " ".join(args))
    cmd = [os.path.join(exe_path, exe_name)]
    cmd.extend(args)
    try:
        out = subprocess.check_output(cmd, cwd=exe_path)
        returncode = 0
    except subprocess.CalledProcessError as cpe:
        out = cpe.output
        returncode = cpe.returncode
    return json.dumps({"stdout": out.decode(ENCODING), "returncode": returncode})


class Proxy:
    def __init__(self, host, port, client=client):
        self.server_address = (host, port)
        self.client = client

    def run(self, executable_name, *args):
        result = self.client(self.server_address, json.dumps([executable_name, args]))
        return json.loads(result)
