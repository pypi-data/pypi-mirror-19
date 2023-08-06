# coding: utf-8

import re
import os

import logbook

logbook.set_datetime_format('local')
logger = logbook.Logger('sbackup2')


def get_task_files(path):
    abs_path = os.path.abspath(path)
    items = os.listdir(abs_path)
    re_conf = re.compile('.+\.conf$')
    tasks = []

    for item in items:
        if re_conf.match(item):
            tasks.append(os.path.join(abs_path, item))

    return tasks
