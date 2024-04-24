import argparse
import tk_file_select as tkf  # type: ignore pylint: disable=import-error


def myArgParse():
    """Argparse implementation for [MODULE]"""
    parser = argparse.ArgumentParser(description="MODULE DESCRIPTION")
    parser.add_argument(
        "-i",
        "--infiles",
        nargs="*",
        help="input files for [DESCRIPTION]",
    )

    args = parser.parse_args()

    if args.infiles is None:
        tkFile = tkf.TkFileSelect()
        args.infiles = tkFile.get_files()

    return args


if __name__ == "__main__":
    print(str(myArgParse()))
