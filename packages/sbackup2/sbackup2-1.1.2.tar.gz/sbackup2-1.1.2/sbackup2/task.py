# coding: utf-8

import os
import shutil
import tempfile
import subprocess

import logbook

logbook.set_datetime_format('local')
logger = logbook.Logger('sbackup2')


class Task:
    def __init__(self, tar_file, options,
                 tmp_dir=tempfile.mkdtemp(prefix='sbackup2_')):
        self.tmp_dir = tmp_dir
        self.tar_file = os.path.join(tmp_dir, tar_file)
        self.last_dump = None
        self.options = options

    def db_task(self, db_type, db_name):
        if db_type == 'mysql':
            return self.mysql_dump(db_name)

        elif db_type == 'psql':
            pass
        else:
            return False

        return True

    def create_tar(self, fd, exclude=None):
        command = 'tar jcf {}'.format(self.tar_file)

        for item in fd:
            command += ' {}'.format(item)

        if exclude:
            for item in exclude:
                command += ' --exclude {}'.format(item)

        return sub_process(command)

    def send_tar(self):
        sftp_file_ask = file_asks(
            self.tmp_dir, self.tar_file, self.options['sftp_remote_dir'])
        options = self.options.copy()
        options.update({'sftp_conf': sftp_file_ask})

        command = 'sshpass -p {sftp_password} sftp {sftp_options} ' \
                  '-b {sftp_conf} {sftp_user}@{sftp_host}'.format(**options)

        try:
            return sub_process(command)
        finally:
            os.remove(sftp_file_ask)

    def remove_tmp_dir(self):
        shutil.rmtree(self.tmp_dir)

    def mysql_dump(self, db):
        self.last_dump = os.path.join(self.tmp_dir, db) + '.sql'
        command = 'mysqldump {db} > {dump_file}'.format(
            db=db, dump_file=self.last_dump)

        return sub_process(command)


def sub_process(command):
    r = subprocess.call(
        command, shell=True, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    if r:
        return False

    return True


def file_asks(tmp_dir, archive, backup_dir):
    f = os.path.join(tmp_dir, 'sftp_command')

    with open(f, 'w') as file:
        file.write('cd {}\n'.format(backup_dir))
        file.write('put {}\n'.format(archive))
        file.write('quit\n')

    return f
