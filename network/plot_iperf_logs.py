import pandas as pd
from pprint import pprint
import re

import plotly.express as px
import plotly.graph_objects as go


class IperfFileReader:

    def __init__(self, filePath):
        self.STR_TO_SCALES = {"": 1, "k": 10**3, "m": 10**6, "g": 10**9, "t": 10**12}
        self.SCALES_TO_STR = {v: k for k, v in self.STR_TO_SCALES.items()}

        with open(filePath, mode="r", encoding="utf-8") as f:
            self.fileLines = f.readlines()

    def parseFile(self):
        self.fileLines = self.fileLines[
            1:
        ]  # don't care about initial "connecting" header
        summaryDict = {0: [], 1: [], 2: []}
        splitInd = 0

        for line in self.fileLines:
            if splitInd == 2:
                break
            if line[0] != "[":
                splitInd += 1
            else:
                summaryDict[splitInd].append(line)

        headerAndTicks = summaryDict[0]
        summary = summaryDict[1]
        # pprint(summaryDict)
        for i in range(len(headerAndTicks)):
            if headerAndTicks[i][:5] == "[ ID]":
                header = headerAndTicks[:i]
                ticks = headerAndTicks[i:]

        ticksDF = self.dataframifyLineList(ticks, "Cwnd")
        summDF = self.dataframifyLineList(summary, "Role")
        t = ticksDF.loc[137]["Transfer"]
        # print(t)
        # print(self.scaleData(t))
        ticksDF["Interval"] = (
            ticksDF["Interval"].str.split("-", expand=True)[0].astype(float)
        )
        ticksDF["Bitrate"] = ticksDF.apply(
            lambda x: self.scaleData((x["Bitrate"], x["Bitrate Units"])), axis=1
        )
        # print(ticksDF)
        # print(summDF)
        ticksRX = ticksDF[ticksDF["Role"] == "RX-C"]
        ticksRX.reset_index(drop=True, inplace=True)
        ticksTX = ticksDF[ticksDF["Role"] == "TX-C"]
        ticksTX.reset_index(drop=True, inplace=True)
        # print(ticksRX)
        # print(ticksTX)
        return ticksRX, ticksTX

    def dataframifyLineList(self, lineList, lastField):

        splitSumm = []
        splitCombSumm = []
        for l in lineList:
            splitSumm.append(list(filter(lambda x: x != "" and x != "[", l.split(" "))))
        for l in splitSumm:
            if re.search(r"^\d", l[0]) is not None:
                lComb = [
                    *self.parseIDMode(l[0]),
                    l[1],
                    l[2],
                    l[3],
                    l[4],
                    l[5],
                    l[6],
                    l[7] if len(l) > 8 else None,
                    (
                        (l[8], l[9])
                        if len(l) > 9
                        else (
                            l[8].strip()
                            if len(l) > 8
                            else l[7].strip() if l[7].strip() != "" else None
                        )
                    ),
                ]
                splitCombSumm.append(lComb)
            else:
                appendL = [
                    *self.parseIDMode(l[0]),
                    "Interval",
                    "Interval Units",
                    "Transfer",
                    "Transfer Units",
                    "Bitrate",
                    "Bitrate Units",
                    "Retr",
                    l[-1].strip(),
                ]
                if len(appendL) == 6:
                    appendL.append("Mode")
                splitCombSumm.append(appendL)

        return pd.DataFrame(splitCombSumm[1:], columns=splitCombSumm[0])

    def parseIDMode(self, idMode):
        groups = re.match(r"^(.*)\]\[(.*)\]", idMode).groups()
        return [groups[0], groups[1]]

    def scaleData(self, dataTup):
        val, scale = dataTup
        scaleStr = re.match(r"(.*)(?=[Bb])", scale).groups()[0].lower()
        return float(val) * self.STR_TO_SCALES[scaleStr]


fr_ambient = IperfFileReader("logs/estimated_extraneous_coupling.txt")
fr_sw_shield = IperfFileReader("logs/shielding_sw_couple.txt")
fr_sw = IperfFileReader("logs/saltwater_comms.txt")

fr_ambient_dfs = fr_ambient.parseFile()
fr_sw_shield_dfs = fr_sw_shield.parseFile()
fr_sw_dfs = fr_sw.parseFile()


def addTraceToFig(fig, df, name, color):
    fig.add_trace(
        go.Scatter(
            x=df["Interval"],
            y=df["Bitrate"],
            name=name,
            line=dict(color=color),
        )
    )


fig = go.Figure()

addTraceToFig(fig, fr_ambient_dfs[0], "Ambient TX-to-RX", "salmon")
addTraceToFig(fig, fr_ambient_dfs[1], "Ambient RX-to-TX", "crimson")
addTraceToFig(
    fig, fr_sw_shield_dfs[0], "Shield Coupling Through Saltwater TX-to-RX", "gold"
)
addTraceToFig(
    fig, fr_sw_shield_dfs[1], "Shield Coupling Through Saltwater RX-to-TX", "orange"
)
addTraceToFig(fig, fr_sw_dfs[0], "Full Saltwater TX-to-RX", "royalBlue")
addTraceToFig(fig, fr_sw_dfs[1], "Full Saltwater RX-to-TX", "steelBlue")


fig.update_layout(
    title="Saltwater G.hn Comms Data Rate testing",
    xaxis_title="Time (s)",
    yaxis_title="Bitrate (bits/sec)",
)
# fig.write_html("saltwater_ghn_comms.html")
# fig.write_image("saltwater_ghn_comms.png", width=1500, height=750)
fig.show()
