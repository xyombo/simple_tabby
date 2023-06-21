
import getpass
import os
import socket
import select
import paramiko
import termios
import tty

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

import sys
from optparse import OptionParser

class SSH:

    def __init__(self,host,user,port,passwrd,private_key):
        self.host = host
        self.user = user
        self.port = port
        self.passwd = passwrd,
        self.private_key = private_key
    
    def open_shell(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host,
                           port=self.port,
                           username=self.user,
                           password=self.passwd[0],
                           key_filename=self.private_key
                           )
            print(f"\033[7m=> stabby login into {self.host}\033[0m\n")
            channel = client.invoke_shell(term='linux',width=1000,height=500)
            oldtty = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin)
            while True:
                readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
                if sys.stdin in readlist:
                    input_cmd = sys.stdin.read(1)
                    channel.sendall(input_cmd)
                if channel in readlist:
                    result = channel.recv(10485760) # max recv 10M btyes
                    if len(result) == 0:
                        break
                    sys.stdout.write(result.decode())
                    sys.stdout.flush()
        except Exception as err:
            print(str(err))
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            channel.close() 
            client.close()
            print(f"\033[7m\n<= stabby logout from {self.host} \033[0m\n")

    def open_tunnet(self,local_port,remote_port):
        import pyperclip
        pyperclip.copy(self.passwd[0])
        command = f"ssh -L {local_port}:127.0.0.1:{remote_port} {self.user}@{self.host}"
        print("-> run command :",command)
        i = os.system(command)

                            

class ForwardServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            print(
                "Incoming request to %s:%d failed: %s"
                % (self.chain_host, self.chain_port, repr(e))
            )
            return
        if chan is None:
            print(
                "Incoming request to %s:%d was rejected by the SSH server."
                % (self.chain_host, self.chain_port)
            )
            return

        print(
            "Connected!  Tunnel open %r -> %r -> %r"
            % (
                self.request.getpeername(),
                chan.getpeername(),
                (self.chain_host, self.chain_port),
            )
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        verbose("Tunnel closed from %r" % (peername,))
