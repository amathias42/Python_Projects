"""Python script to analyze csv files produced by o-scope"""

import sys
import os
import argparse
import pandas as pd
import plotly.graph_objects as go

sys.path.append("../utils")

import tk_file_select as tkf  # type: ignore pylint: disable=import-error wrong-import-position


def myArgParse():
    """Argparse implementation"""
    parser = argparse.ArgumentParser(description="Analyzing sandbox for o-scope plots")
    parser.add_argument(
        "-i", "--infile", nargs="*", help="input csv file(s) to analyze"
    )
    parser.add_argument(
        "-o", "--outdir", nargs="?", help="output directory to place graphs in"
    )

    args = parser.parse_args()

    if args.infile is None:
        tkFile = tkf.TkFileSelect()
        args.infile = tkFile.get_files()
    if args.outdir is not None and not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    return args


def readCSVs(args):
    """turn csv of o-scope data into dictionary of dataframes separated out by trace"""
    fileList = []

    if type(args.infile) is tuple or type(args.infile) is list:
        fileList = args.infile
    else:
        fileList = [args.infile]

    fileDict = {}
    for f in fileList:
        df = pd.read_csv(f, header=None)

        # All lines signifying the start of a new trace: "x-axis [Channel #]"
        headers = df[df[0].str.contains("x-axis")]

        dfDict = {}
        prevHeaderIndex = None
        prevHeader = None

        for h in headers.iterrows():

            if prevHeaderIndex is not None:
                subDF = df.iloc[prevHeaderIndex + 1 : h[0], :].reset_index(
                    drop=True
                )  # get section of df pertaining to 1 trace
                subDF = subDF.rename(
                    columns={0: subDF.iloc[0, 0], 1: subDF.iloc[0, 1]}
                ).drop(
                    index=0
                )  # move the unit descriptions from the first line to the column names
                dfDict[prevHeader] = subDF.astype(
                    float
                )  # add to df dictionary w/ trace name (1, 2, 3, 4, F1, etc.) as the key

            prevHeader = h[1][1]
            prevHeaderIndex = h[0]

        # Handle final trace
        subDF = df.iloc[prevHeaderIndex + 1 :, :].reset_index(drop=True)
        subDF = subDF.rename(columns={0: subDF.iloc[0, 0], 1: subDF.iloc[0, 1]}).drop(
            index=0
        )

        dfDict[prevHeader] = subDF.astype(float)
        fileDict[f] = dfDict

    return fileDict


def plotOverlay(
    args, dfList, x_axis, y_axis, title="", x_axis_title="", y_axis_title=""
):
    fig = go.Figure()
    hoverTemplate = "%{y} " + y_axis_title + "<br>%{x} " + x_axis_title
    for name, df in dfList:
        fig.add_trace(
            go.Scatter(
                x=df[x_axis], y=df[y_axis], name=name, hovertemplate=hoverTemplate
            )
        )

    fig.update_layout(title=title, xaxis_title=x_axis_title, yaxis_title=y_axis_title)
    if args.outdir is not None:
        outDir = args.outdir
    else:
        outDir = ""
    fig.write_html(outDir + title + ".html")


def main():
    args = myArgParse()
    fileDict = readCSVs(args)
    dfList = []
    for filename, dfs in fileDict.items():
        lastSlash = max(filename.rfind("\\") + 1, filename.rfind("/") + 1)
        dfList.append((filename[lastSlash : filename.rindex("fan") + 3], dfs["F1"]))
    plotOverlay(
        args,
        dfList,
        "Hertz",
        "dBV",
        title="Large Scale noise",
        x_axis_title="Hertz",
        y_axis_title="dBV",
    )

    # fft = dfDict["F1"]
    # print(fft.sort_values(by=["dBV"], ascending=False).head(10))


if __name__ == "__main__":
    main()
