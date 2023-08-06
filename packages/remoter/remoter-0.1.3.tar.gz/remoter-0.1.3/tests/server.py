"""
Inspired by https://github.com/carletes/mock-ssh-server
"""
import logging
import os
import select
import socket
import subprocess
import threading

from queue import Queue

import paramiko


SERVER_KEY_PATH = os.path.join(os.path.dirname(__file__), "server-key")


class Handler(paramiko.ServerInterface):

    log = logging.getLogger(__name__)

    def __init__(self, server, client_conn):
        self.server = server
        self.thread = None
        self.command_queues = {}
        client, _ = client_conn
        self.transport = t = paramiko.Transport(client)
        t.add_server_key(paramiko.RSAKey(filename=SERVER_KEY_PATH))

    def run(self):
        self.transport.start_server(server=self)
        while True:
            channel = self.transport.accept()
            if channel is None:
                break
            self.command_queues[channel.get_id()] = Queue()
            t = threading.Thread(target=self.handle_client, args=(channel,))
            t.setDaemon(True)
            t.start()

    def handle_client(self, channel):
        try:
            command = self.command_queues[channel.get_id()].get(block=True)
            self.log.debug("Executing %s", command)
            p = subprocess.Popen(command, shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            channel.sendall(stdout)
            channel.sendall_stderr(stderr)
            channel.send_exit_status(p.returncode)
        except Exception:
            self.log.error("Error handling client (channel: %s)", channel,
                           exc_info=True)
        finally:
            channel.close()

    def check_channel_exec_request(self, channel, command):
        self.command_queues.setdefault(channel.get_id(), Queue()).put(command)
        return True

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'test':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


class Server(object):

    host = "127.0.0.1"

    log = logging.getLogger(__name__)

    def __init__(self):
        self._socket = None
        self._thread = None

    def __enter__(self):
        self._socket = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, 9876))
        s.listen(1)
        self._thread = t = threading.Thread(target=self._run)
        t.setDaemon(True)
        t.start()
        return self

    def _run(self):
        sock = self._socket
        while sock.fileno() > 0:
            self.log.debug("Waiting for incoming connections ...")
            rlist, _, _ = select.select([sock], [], [], 1.0)
            if rlist:
                try:
                    conn, addr = sock.accept()
                except OSError:
                    pass
                else:
                    self.log.debug("... got connection %s from %s", conn, addr)
                    handler = Handler(self, (conn, addr))
                    t = threading.Thread(target=handler.run)
                    t.setDaemon(True)
                    t.start()

    def __exit__(self, *exc_info):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
        except Exception:
            pass
        self._socket = None
        self._thread = None
