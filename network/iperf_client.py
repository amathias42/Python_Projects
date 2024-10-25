import subprocess
import re
from pprint import pprint

serverAddr = "10.1.1.35"
serverPort = "5201"

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
