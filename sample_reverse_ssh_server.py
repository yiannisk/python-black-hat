#!/usr/bin/python
import socket
import paramiko
import threading
import sys
import os
import json

host_key = paramiko.RSAKey(filename='resources/test_rsa.key')


class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        try:
            if os.path.exists('resources/passwords.json'):
                json_data = open('resources/passwords.json')

                data = json.load(json_data)
                password = data["passwords"][username]

                json_data.close()

                if password == password:
                    return paramiko.AUTH_SUCCESSFUL
        except:
            pass

        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)

    print '[+] Listening for connection...'
    client, addr = sock.accept()

except Exception, e:
    print '[-] Listen failed: ' + str(e)
    sys.exit(1)

print '[+] Got a connection!'

try:
    sess = paramiko.Transport(client)
    sess.add_server_key(host_key)

    server = Server()

    try:
        sess.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed.'

    chan = sess.accept(20)
    print '[+] Authenticated!'
    print chan.recv(1024)

    chan.send('Welcome to ssh')

    while True:
        try:
            command = raw_input("Enter command: ").strip('\n')

            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                sess.close()
                raise Exception('exit')

        except KeyboardInterrupt:
            sess.close()

except Exception, e:
    print '[-] Caught exception: ' + str(e)

    try:
        sess.close()
    except:
        pass

    sys.exit(1)
