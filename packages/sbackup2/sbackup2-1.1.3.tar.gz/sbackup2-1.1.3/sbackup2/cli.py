# coding: utf-8

import os

import click
import logbook

import sbackup2.log
import sbackup2.conf
import sbackup2.task
import sbackup2.utils

logbook.set_datetime_format('local')
logger = logbook.Logger('sbackup2')

log_syslog = click.option(
    '--syslog', help='send message to syslog', is_flag=True, default=False)


@click.group()
@log_syslog
def cli(syslog):
    if syslog:
        sbackup2.log.define_log()


@cli.command()
@click.option('--task-file', help='Use only this the task file')
@click.option('--not-rm-tmp', help='delete temp directory', is_flag=True,
              default=False)
def backup(task_file, not_rm_tmp):
    logger.info('start work')

    if task_file:
        tasks_file = [os.path.abspath(task_file)]
    else:
        tasks_file = sbackup2.utils.get_task_files('/etc/sbackup2.d')

    # обрабатываем список файлов
    for task_full_path in tasks_file:
        logger.info('task file: {}'.format(task_full_path))
        task_conf = sbackup2.conf.TaskConf(task_full_path)
        tasks = task_conf.get_tasks()
        task_process = sbackup2.task.Task(
            task_conf.get_tar_file, task_conf.options)
        fd = []

        # обработка задачи
        for task in tasks:
            # обрабатываем список задач для DB
            for db_type, db_name in task_conf.db_list(task):
                logger.info('create dump file of DB \'{}\''.format(db_name))

                if task_process.db_task(db_type, db_name):
                    logger.info('add dump \'{}\' to list of back up'.format(
                        db_name))
                    fd.append(task_process.last_dump)
                else:
                    logger.error(
                        'dump file of DB \'{}\' was not created'.format(
                            db_name))

            # обработка файлов
            for item in task_conf.fd_list(task):
                logger.info('add \'{}\' to list of back up'.format(item))
                fd.append(item)

        # создание TAR файла
        if fd:
            logger.info('compress files')

            if not task_process.create_tar(fd):
                logger.error('compressed is failure')
                continue
        else:
            logger.warning('task(s) not found')
            continue

        logger.info('sending TAR file to remote host')

        if not task_process.send_tar():
            logger.error('TAR file was not send to remote host')

        if not_rm_tmp is False:
            logger.info('deleting tmp directory {}'.format(
                task_process.tmp_dir))
            task_process.remove_tmp_dir()

    logger.info('stop work')
