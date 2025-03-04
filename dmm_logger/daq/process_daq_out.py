import datetime as dt
import re
import pandas as pd  # type: ignore pylint: disable=import-error
import numpy as np  # type: ignore pylint: disable=import-error

# import plotly.express as px  # type: ignore pylint: disable=import-error
import plotly.graph_objects as go  # type: ignore pylint: disable=import-error
from plotly.subplots import make_subplots

LOAD_COLOR = "orangered"
DISPLACEMENT_COLOR = "dodgerblue"
RESISTANCE_COLOR = "green"


def timestamp_daq_output(daq_list):
    outList = []
    latest_ts = None
    oldest_ts = None
    section = []
    stepList = []
    for i in reversed(daq_list):
        if i[1] == "'":
            i = re.sub(r"['\(\)]", "", i).strip()[:-1]
            if latest_ts is None:
                latest_ts = dt.datetime.strptime(i, "%b-%d-%Y_T_%H:%M:%S.%f")
            else:
                oldest_ts = dt.datetime.strptime(i, "%b-%d-%Y_T_%H:%M:%S.%f")
                step = (latest_ts - oldest_ts) / len(section)
                # print(f"step: {step}, len: {len(section)}")
                stepList.append(step)
                for iv, v in enumerate(section):
                    outList.append((latest_ts - (iv * step), v))
                section = []
                latest_ts = oldest_ts
        else:
            section.append(re.sub(r"[\n]", "", i)[:-1])
    step = sum(stepList, dt.timedelta()) / len(stepList)
    for iv, v in enumerate(section):
        # print(iv, v)
        outList.append((oldest_ts - (iv * step), v))
    outList.reverse()
    for i, t in enumerate(outList):
        outList[i] = t[0], *t[1].split(", ")
    return outList


def make_strain_plot(instronFile, resistanceFile, outfile, title):
    with open(instronFile, "r", encoding="utf-8") as inf:
        lines = inf.readlines()

    resdf = pd.read_csv(
        resistanceFile,
        delimiter=",",
        names=("time", "resistance"),
        dtype="string",
    )
    resdf["time"] = pd.to_datetime(resdf["time"], format="%b-%d-%Y_T_%H:%M:%S.%f")
    resdf["resistance"] = resdf["resistance"].astype(float)
    ## Measured offset
    resdf["time"] = resdf["time"] - dt.timedelta(seconds=1.1)

    outL = timestamp_daq_output(lines)
    df = pd.DataFrame(outL, columns=("time", "ch0_volt", "ch1_volt"))
    df[["ch0_volt", "ch1_volt"]] = df[["ch0_volt", "ch1_volt"]].astype(float)

    # Process Data
    df["ch0_volt"] = df["ch0_volt"] * 100
    df["ch0_volt"] = df["ch0_volt"].rolling(window=5).max()
    df["ch1_volt"] = df["ch1_volt"].rolling(window=5).max()
    df_dec = df.set_index(df["time"]).resample("10ms").max()

    df = df_dec

    resdf["resistance"] = resdf["resistance"].apply(lambda x: 100 if x > 100 else x)
    if test == 1:
        resdf["time"] = resdf["time"] - dt.timedelta(seconds=1)

        startTime = np.datetime64(
            dt.datetime(
                year=2025,
                month=3,
                day=4,
                hour=18,
                minute=46,
                second=30,
            )
        )

        resdf = resdf[resdf["time"] > startTime]
        df = df[df["time"] > startTime]

    # resdf["resistance"] = resdf["resistance"].rolling(window=50).max()
    # resdf_dec = resdf.set_index(resdf["time"]).resample("50ms").max()
    # resdf['dec_time']
    # print((resdf.iloc[:200]).to_string())

    # resdf = resdf_dec

    # print(df)

    # line_plot = px.line(df, x="time", y=df.columns[1:3])
    # scatter_plot = px.scatter(df, x="time", y=df.columns[1:3])

    # line_plot.show()
    # scatter_plot.show()

    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ch0_volt"],
            name="Load",
            yaxis="y1",
            line=dict(color=LOAD_COLOR),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ch1_volt"],
            name="Displacement",
            yaxis="y2",
            line=dict(color=DISPLACEMENT_COLOR),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=resdf["time"],
            y=resdf["resistance"],
            name="Resistance",
            yaxis="y3",
            line=dict(color=RESISTANCE_COLOR),
        )
    )

    fig.update_layout(
        title=title,
        xaxis=dict(title="Time (UTC)"),
        yaxis1=dict(
            title=dict(text="Load (lbs)", font=dict(color=LOAD_COLOR)),
            tickfont=dict(color=LOAD_COLOR),
            range=[-100, 850],
        ),
        yaxis2=dict(
            title=dict(text="Displacement (in)", font=dict(color=DISPLACEMENT_COLOR)),
            anchor="free",
            overlaying="y",
            side="left",
            # position=0.1,
            autoshift=True,
            tickfont=dict(color=DISPLACEMENT_COLOR),
            range=[-1, 8.5],
        ),
        yaxis3=dict(
            title=dict(text="Resistance(Ohms)", font=dict(color=RESISTANCE_COLOR)),
            anchor="x",
            overlaying="y",
            side="right",
            tickfont=dict(color=RESISTANCE_COLOR),
            range=[-10, 85],
        ),
        # width=1600,
        # height=900,
    )

    fig.update_yaxes(
        # rangemode="tozero",
        scaleanchor="y1",
        scaleratio=100,
        constraintoward="bottom",
        secondary_y=False,
    )

    fig.update_yaxes(
        # rangemode="tozero",
        scaleanchor="y2",
        scaleratio=1,
        constraintoward="bottom",
        secondary_y=True,
    )

    fig.update_yaxes(
        # rangemode="tozero",
        scaleanchor="y3",
        scaleratio=10,
        constraintoward="bottom",
        secondary_y=True,
    )

    fig.write_html(f"{outfile}.html")
    fig.write_image(f"{outfile}.png")


for test in [1, 2, 3]:

    make_strain_plot(
        instronFile=f"daq/data/instron_run_{test}.txt",
        resistanceFile=f"instron_res_run_{test}.csv",
        outfile=f"plots/Cable_strain_test_{test}",
        title=f"Cable strain test {test}",
    )

make_strain_plot(
    instronFile="daq/data/instron_test.txt",
    resistanceFile="testing_instron_res.csv",
    outfile="plots/Instron_test",
    title="Instron Test",
)
