# -*- coding: utf-8 -*-
import os

from paramiko.client import SSHClient, AutoAddPolicy
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .exceptions import DuplicateServerConfiguration


class Config(object):
    DEFAULT_FILENAME = 'remoter.yml'

    def __init__(self, filename=None):
        self.filename = filename or self.DEFAULT_FILENAME
        self.client = self._setup_client()
        self.conf = self._load()
        self.validate()

    def _open(self):
        with open(os.path.abspath(self.filename), mode='r') as conf:
            read_data = conf.read()
        return read_data

    def _load(self):
        data = self._open()
        return load(data, Loader=Loader)

    def _setup_client(self):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        return client

    def validate(self):
        server_section_names, tasks_section_names = [], []
        for serv_name, serv_conf in self.conf.get('servers').items():
            server_section_names.append(serv_name)
        for serv_name, tasks_list in self.conf.get('tasks').items():
            tasks_section_names.append(serv_name)
        # TODO: needs better solution
        if len(set(server_section_names)) != len(server_section_names):
            first_duplicate = [x for x in server_section_names if x not in list(set(server_section_names))][0]
            raise DuplicateServerConfiguration('authentication', first_duplicate)
        if len(set(tasks_section_names)) != len(tasks_section_names):
            first_duplicate = [x for x in tasks_section_names if x not in list(set(tasks_section_names))][0]
            raise DuplicateServerConfiguration('tasks', first_duplicate)

    def run(self):
        output = b''
        for serv_name, tasks_list in self.conf.get('tasks').items():
            serv_conf = self.conf.get('servers').get(serv_name)
            self.client.connect(
                hostname=serv_conf.get('host'),
                port=serv_conf.get('port'),
                username=serv_conf.get('username'),
                password=serv_conf.get('password')
            )
            for task in tasks_list:
                stdin, stdout, stderr = self.client.exec_command(task)
                latest_stdout = stdout.read() if stdout else b''
                latest_stderr = stderr.read() if stderr else b''
                output += latest_stdout + latest_stderr
            self.client.close()
        return output.decode('utf-8')
