# coding: utf-8

# import sys

import logbook

logbook.set_datetime_format('local')
logger = logbook.Logger('sbackup2')


def define_log():
    # logbook.StreamHandler(sys.stdout).push_application()
    logbook.SyslogHandler().push_application()
