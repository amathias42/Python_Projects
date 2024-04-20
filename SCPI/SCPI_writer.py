import sys
from time import sleep

sys.path.append("../utils")
import tk_file_select as tkf  # type: ignore pylint: disable=import-error wrong-import-position

import pyvisa  # type: ignore pylint: disable=import-error
import argparse


def openOnlyIntsrument(baud_rate, write_termination="\r\n", read_termination="\r\n"):
    rm = pyvisa.ResourceManager()
    return rm.open_resource(
        rm.list_resources()[0],
        baud_rate=baud_rate,
    )


def getCommandListFromFile(fileName):
    with open(fileName, mode="r", encoding="utf-8") as cmdFile:
        return cmdFile.read().splitlines()


def sendCommandList(instrument, cmdList):
    for cmd in cmdList:
        sleep(0.2)
        print(cmd)
        if cmd.find("?") == -1:
            instrument.write(cmd)
        else:
            print(instrument.query(cmd))


def myArgParse():
    """Argparse implementation"""
    parser = argparse.ArgumentParser(description="SCPI command reader & sender")
    parser.add_argument(
        "-i",
        "--infile",
        nargs="*",
        help="input text file with SCPI commands",
    )

    args = parser.parse_args()

    if args.infile is None:
        tkFile = tkf.TkFileSelect()
        args.infile = tkFile.get_files()

    return args


def main():

    args = myArgParse()

    inst = openOnlyIntsrument(baud_rate=57600)

    for file in args.infile:
        sendCommandList(inst, getCommandListFromFile(file))

        inst.close()


if __name__ == "__main__":
    main()
