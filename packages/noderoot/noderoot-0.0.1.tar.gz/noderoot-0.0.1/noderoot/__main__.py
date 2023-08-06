#!/usr/bin/python2.7

import sys
import os, os.path
import argparse
import log
import paramiko
import socket
import time
import signal
from ssh_helpers import *

log.setup('noderoot', '/var/log')
logger = log.get(__name__)
default_mounts = [ 'var/tmp', 'run', 'dev', 'proc', 'sys', 'dev/pts' ]
do_run = True

def can_run():
    global do_run
    return do_run

def signal_handler(signal, frame):
    global do_run
    logger.info('Ctrl-C caught')

    # Ctrl-C pressed more then once!
    if do_run == False:
        sys.exit(1)

    do_run = False

def bring_down_target(ssh, nfs_share, address, local_directory, local_user, local_password, remote_directory, remote_user, remote_password, mounts):
    for m_src in reversed(mounts):
        m_dest = os.path.join(remote_directory, m_src)
        if safe_umount_ssh(ssh, m_dest) == False:
            return False
    
    if safe_umount_ssh(ssh, remote_directory) == False:
        return False

    nfs_share.bringdown()

    return True

def bring_up_target(ssh, nfs_share, address, local_directory, local_user, local_password, remote_directory, remote_user, remote_password, mounts):
    mkdirs_ssh(ssh, remote_directory)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('gmail.com',80))
    this_address = s.getsockname()[0]

    nfs_share.bringup()

    nfs_cmd = 'mount -t nfs -o rw,intr,noatime,actimeo=60,vers=4,fsc {0}:{1} {2}'.format(this_address, local_directory, remote_directory)
    retcode, _, stdout, stderr = run_ssh_command(ssh, nfs_cmd)
    if retcode != 0:
        logger.info('Failed: {0}'.format(nfs_cmd))
        return False

    time.sleep(2)
    for m_src in mounts:
        m_dest = os.path.join(remote_directory, m_src)
        m_cmd = 'mount --bind /{0} {1}'.format(m_src, m_dest)
        logger.info(m_cmd)
        mkdirs_ssh(ssh, m_dest)
        retcode, _, stdout, stderr = run_ssh_command(ssh, m_cmd)
        if retcode != 0:
            logger.info("Failed: {0}".format(m_cmd))

    return True

def on_start(a):
    signal.signal(signal.SIGINT, signal_handler)

    ssh = get_ssh_connection(a.remote_address, a.remote_user, a.remote_password)
    nfs_share = NFSShare(a.remote_address, a.remote_dir, 'rw,no_root_squash,subtree_check,sync')

    if bring_down_target(ssh, nfs_share, a.remote_address, a.local_dir, a.local_user, a.local_password, a.remote_dir, a.remote_user, a.remote_password, a.extra_mounts) == False:
        ssh.close()
        sys.exit(1)

    exit_code = 1 
    if bring_up_target(ssh, nfs_share, a.remote_address, a.local_dir, a.local_user, a.local_password, a.remote_dir, a.remote_user, a.remote_password, a.extra_mounts) == True:
        seperator = str('-' * 20)
        logger.info(seperator)
        if a.command:
            exit_code = chroot_ssh_command(ssh, a.remote_dir, a.command, can_run)
        else:
            logger.info('Mounts up, use Ctrl+C to bring down')
            while do_run:
                time.sleep(0.1)
        logger.info(seperator)

    bring_down_target(ssh, nfs_share, a.remote_address, a.local_dir, a.local_user, a.local_password, a.remote_dir, a.remote_user, a.remote_password, a.extra_mounts)
    ssh.close()
    sys.exit(exit_code)

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

	parser = argparse.ArgumentParser(description='Supports chrooting into a folder and using a real CPU located on a network as the CPU')
	parser.add_argument('--command', help='Command to run when chrooting.', required=False)
	parser.add_argument('--local-dir', help='Root filesystem to chroot into.', required=True)
	parser.add_argument('--local-user', help='Local user for remote machine to connect via', required=True)
	parser.add_argument('--local-password', help='Local password for remote machine to connect with, if not specified SSH wil try SSH key if available', required=False)
	parser.add_argument('--remote-user', help='User to SSH into the target machine for setup reasons', required=True)
	parser.add_argument('--remote-password', help='Password for SSH, if not specified SSH wil try SSH key if available, if not it will prompt for password', required=False)
	parser.add_argument('--remote-address', help='Address of target machine.', required=True)
	parser.add_argument('--remote-dir', help='Directory to mount the root file system in on the target.', required=True)
	parser.add_argument('--extra-mounts', help='Extra 1:1 bind mounts to bringup, ie /proc, /sys, /dev. Can be specified multiple times.', action='append', default=default_mounts, required=False)

	parser.set_defaults(func=on_start)
	args = parser.parse_args()
	args.func(args)

if __name__ == "__main__":
    main()
