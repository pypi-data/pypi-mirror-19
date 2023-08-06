#!/usr/bin/python2.7

import log
import paramiko
import time
import os
import select


def get_ssh_connection(address, user, password=None):
    logger = log.get(__name__)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(address, username=user, password=password)
    logger.info('Connecting to: {0}@{1}'.format(user, address))
    
    return ssh

def run_ssh_command(client, command):
    logger = log.get(__name__)
    stdin, stdout, stderr = client.exec_command(command)
    retcode = stdout.channel.recv_exit_status()
    logger.info(command)
    logger.info('retcode: {0}'.format(retcode))
    logger.debug(stdout)
    logger.debug(stderr)

    return retcode, stdin, stdout, stderr

def chroot_ssh_command(client, directory, command, can_run):
    logger = log.get(__name__)
    chroot_cmd = 'chroot {0} {1}'.format(directory, command)

    logger.info(chroot_cmd)
    channel = client.get_transport().open_session()
    channel.exec_command(chroot_cmd)
    while True:
        rl, wl, xl = select.select([channel], [], [], 0.1)
        if len(rl) > 0:
            msg = channel.recv(1024)
            msg = msg.strip()
            if msg:
                logger.info(msg)
            elif channel.exit_status_ready():
                break
        else:
            if channel.exit_status_ready():
                break

        if can_run() == False:
            return -255

    retcode = channel.recv_exit_status()
    logger.info('retcode: {0}'.format(retcode))

    return retcode

def send_file_ssh(client, source_file, dest_file):
    sftp = client.open_sftp()
    sftp.put(source_file, dest_file)

def mkdirs_ssh(client, path):
    logger = log.get(__name__)
    cmd = 'mkdir -p {0}'.format(path)
    retcode, _, stdout, stderr = run_ssh_command(client, cmd)
    if retcode != 0:
        logger.error("Failed: {0}".format(cmd))
        return False

    return True

def safe_umount_ssh(client, path):
    logger = log.get(__name__)
    cmd = 'mount | grep "on {0} type"'.format(path)
    _, _, stdout, stderr = run_ssh_command(client, cmd)

    instances = stdout.read().splitlines()
    logger.info('{0} mounted {1} times'.format(path, len(instances)))
    for instance in instances:
        cmd = 'umount {0} -l'.format(path)
        retcode, _, stdout, stderr = run_ssh_command(client, cmd)
        if retcode != 0:
            logger.error("Failed: {0}".format(cmd))
            return False

    return True

