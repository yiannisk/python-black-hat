#!/usr/bin/python
# import threading
import paramiko
import subprocess
import os


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    if os.path.exists("~/.ssh/known_hosts"):
        client.load_host_keys('~/.ssh/known_hosts')

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)

    return


ssh_command('10.0.2.15', 'yiannisk', '1k@r@d1m@s', 'id')