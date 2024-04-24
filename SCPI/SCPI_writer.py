from time import sleep
import pyvisa  # type: ignore pylint: disable=import-error
import argparse
import tk_file_select as tkf  # type: ignore pylint: disable=import-error wrong-import-position


def openOnlyIntsrument(baud_rate, write_termination="\r\n", read_termination=None):
    """opens and returns the first pyvisa resource seen. Unreliable selection if connected to more than 1 instrument."""
    rm = pyvisa.ResourceManager("@py")
    return rm.open_resource(
        rm.list_resources()[0],
        baud_rate=baud_rate,
        write_termination=write_termination,
        read_termination=read_termination,
    )


def getCommandListFromFile(fileName):
    """reads in plain text file of SCPI commands each on their own line"""
    with open(fileName, mode="r", encoding="utf-8") as cmdFile:
        return cmdFile.read().splitlines()


def sendCommandList(instrument, cmdList):
    """sends SCPI commands in @param-cmdList to @param-instrument with 200ms delay
    to account for slower processing of older instruments.
    If command contains '?': will query the instrument and print the result to console
    """
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
    parser.add_argument(
        "-b",
        "--baud",
        nargs="?",
        help="serial baud rate of SCPI instrument - default = 115200",
        default=115200,
    )
    parser.add_argument(
        "-w",
        "--writeTerm",
        nargs="?",
        help="termination characters for writing an SCPI command - default = '\\r\\n'",
        default="\r\n",
    )
    parser.add_argument(
        "-r",
        "--readTerm",
        nargs="?",
        help="termination characters for reading an SCPI command - default = None",
        default=None,
    )

    args = parser.parse_args()

    if args.infile is None:
        tkFile = tkf.TkFileSelect()
        args.infile = tkFile.get_files()

    return args


def main():

    args = myArgParse()

    inst = openOnlyIntsrument(
        baud_rate=args.baud,
        write_termination=args.writeTerm,
        read_termination=args.readTerm,
    )

    for file in args.infile:
        sendCommandList(inst, getCommandListFromFile(file))

    inst.close()


if __name__ == "__main__":
    main()
