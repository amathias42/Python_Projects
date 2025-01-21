import subprocess
import re
from pprint import pprint

import paramiko

serverAddr = "10.1.1.61"
server = "miso-pi-1"
serverPort = "5201"

ssh = paramiko.SSHClient()
ssh.connect(server, username="spv", password="#power!2024Vault")
ssh_in, ssh_out, ssh_err = ssh.exec_command(f"iperf3 -s -p {serverPort}")

iperfClientCommandFields = [
    "iperf3",
    "-c",
    serverAddr,
    "-p",
    serverPort,
    "-t",
    "5",
    "-i",
    "0.25",
    # "-J",
    # "--json-stream", only iperf3.17 which is only supported on Oracular Oriole
    "--forceflush",  # provides ability to read output after every 1s
    "--bidir",
]

iperfClient = subprocess.Popen(
    iperfClientCommandFields, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

for line in iperfClient.stdout:
    # print(line)

    l = list(
        filter(
            lambda x: x != "",
            re.split(r"\s", str(re.search(r"(?<=b').*(?=\\n')", str(line)).group())),
        )
    )
    print(f"{l[1]}")

for line in iperfClient.stderr:
    print(line)


# Need to forceflush to get output in real time from subprocess
