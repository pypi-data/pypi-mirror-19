# coding: utf-8

import json
import socket
import datetime


class TaskConf:
    def __init__(self, path):
        with open(path) as f:
            self.conf = json.load(f)

    def get_tasks(self):
        return self.conf.get('tasks', [])

    @property
    def options(self):
        return self.conf.get('options', {})

    @staticmethod
    def db_list(task):
        dbs = []

        for item in task.get('db', []):
            dbs.append(item)

        return dbs

    @staticmethod
    def fd_list(task):
        fds = []

        for item in task.get('fd', []):
            fds.append(item)

        return fds

    @staticmethod
    def fd_exclude(task):
        return task.get('fd_exclude', [])

    @property
    def get_tar_file(self):
        options = self.options
        dt = datetime.datetime.now()
        d = {
            'host_name': socket.gethostname(),
            'year': dt.strftime('%Y'),
            'month': dt.strftime('%m'),
            'day': dt.strftime('%d'),
            'hour': dt.strftime('%H'),
            'minutes': dt.strftime('%M'),
            'seconds': dt.strftime('%S'),
        }
        try:
            file_name = options['tar_file']
        except KeyError:
            file_name = '{host_name}_{year}_{month}_{day}__{hour}_{minutes}' \
                        '_{seconds}.tar.bz2'

        return file_name.format(**d)
