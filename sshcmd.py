#!/usr/bin/python
import paramiko
import os
import json


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


# requires a JSON file in the same directory with format:
# { passwords: { "<user>": "<password>" } }

password = ""

if os.path.exists('resources/passwords.json'):
    json_data = open('resources/passwords.json')
    data = json.load(json_data)
    password = data["passwords"]["yiannisk"]
    json_data.close()

ssh_command('10.0.2.15', 'yiannisk', password, 'id')
