# SCPI Command Interface Script

## Description

This Python script can read in plain text files containing a list of SCPI commands and then send those commands to an instrument which communicates over SCPI. Right now it is only configured for a network with 1 instrument accessible.

## Setup

- Download & install python - preferably the version in `version.txt` - [Python Download](https://www.python.org/downloads/)
- (Optional) create a venv for the project directory - [Python venv docs](https://docs.python.org/3/library/venv.html)
- Command Line: `pip install -r requirements.txt`

## Usage

Connect to your instrument via usb or serial and run `python SCPI_writer.py` with the optional command arguments:

- `-i` or `--infile` `[list of input text file(s)]` containing SCPI commands to be read in. If not provided, a file selection dialog will appear
- `-b` or `--baud` `[instrument baud rate] (default = 115200)`
- `-w` or `--writeTerm` `[termination character(s) for writing SCPI commands] (default = '\r\n')` - see instrument manual
- `-r` or `--readTerm` `[termination character(s) for reading SCPI commands] (default = None)` - see instrument manual
