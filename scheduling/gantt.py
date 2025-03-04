import plotly.graph_objects as go  # type: ignore pylint: disable=import-error
import pandas as pd  # type: ignore pylint: disable=import-error
import toml  # type: ignore pylint: disable=import-error
from pprint import pprint
import datetime as dt

from typing import Dict, List, TypeVar, Type, Tuple


class TomlTime:
    def __init__(self, data: Dict | List) -> None:
        self.data = data
        self.TIME_ESTIMATE_KEYS = ["min", "est", "max"]
        self.priorityDict = {1: [], 2: [], 3: []}

    @classmethod
    def from_data(cls, data: Dict | List):
        return cls(data)

    @classmethod
    def from_filename(cls, filename: str, encoding: str = "utf-8"):
        with open(filename, "r", encoding=encoding) as f:
            return cls(toml.load(f))

    @classmethod
    def from_str(cls, dataStr: str):
        return cls(toml.loads(dataStr))

    def sum_project_hours(self, projectDict: Dict) -> float:
        if all(k in projectDict.keys() for k in self.TIME_ESTIMATE_KEYS):
            return self.three_point_estimate(
                mn=projectDict["min"], est=projectDict["est"], mx=projectDict["max"]
            )
        else:
            retSum = 0
            for t in projectDict["tasks"]:
                retSum += self.sum_project_hours(t)
            return retSum

    def data_to_str(self):
        def to_str_recurse(self, d):
            if all(k in dict.keys() for k in self.TIME_ESTIMATE_KEYS):
                return f"{d["name"]}: {d["est"]}"

    @staticmethod
    def three_point_estimate(mn: float, est: float, mx: float) -> float:
        return (mn + (4 * est) + mx) / 6

    def sort_tasks_priority(self, d):
        pass
        # TODO: clean up garbage
        # for key, val in enumerate(dict):
        #     if type(val) == list:
        #         for v in val:
        #             if all(k in v.keys() for k in self.TIME_ESTIMATE_KEYS):
        #                 self.priorityDict[v["priority"]].append(
        #                     (v["name"], self.sum_project_hours(v))
        #                 )
        #             else:
        #                 self.sort_tasks_priority(v["tasks"])
        #     elif type(val) == str:
        #         return
        #     else:
        #         if all(k in val.keys() for k in self.TIME_ESTIMATE_KEYS):
        #             self.priorityDict[val["priority"]].append(
        #                 (val["name"], self.sum_project_hours(val))
        #             )
        #         else:
        #             self.sort_tasks_priority(val["tasks"])


def total_time():
    q1_sched = TomlTime.from_filename("2025_q1.toml")
    sp_totals = [
        (subp["name"], round(q1_sched.sum_project_hours(subp), 2))
        for subp in q1_sched.data["shallow_profiler"]
    ]
    print(f"Shallow Profiler: {sp_totals}")
    sp_totalSum = 0
    for t in sp_totals:
        sp_totalSum += t[1]
    print(f"Shallow Profiler total: {round(sp_totalSum, 2)}\n")

    pv_totals = [
        (subp["name"], round(q1_sched.sum_project_hours(subp), 2))
        for subp in q1_sched.data["power_vault"]
    ]
    pv_IIB_totals = [
        # print(subsubp)
        (subsubp["name"], round(q1_sched.sum_project_hours(subsubp), 2))
        for subsubp in next(
            subp for subp in q1_sched.data["power_vault"] if subp["name"] == "IIB"
        )["tasks"]
    ]
    print(f"Power vault: {pv_totals}")
    pv_totalSum = 0
    for t in pv_totals:
        pv_totalSum += t[1]

    print(f"IIB: {pv_IIB_totals}")

    print(f"Power vault total: {round(pv_totalSum, 2)}")

    pprint(q1_sched.data)


def date_range(start: dt.date, end: dt.date):
    days = int((end - start).days)
    for n in range(days):
        yield start + dt.timedelta(n)


def draw_month_rect(fig, year, month, color):
    fig.add_vrect(
        x0=dt.datetime(year=year, month=month, day=1),
        x1=dt.datetime(
            year=(year if month < 12 else year + 1),
            month=(month + 1 if month < 12 else 1),
            day=1,
        )
        - dt.timedelta(microseconds=1),
        name=dt.datetime(year=year, month=month, day=1).strftime("%B"),
        opacity=0.2,
        fillcolor=color,
        showlegend=True,
        line_width=0,
    )


def draw_weekend_rects(fig, span):
    firstLegendFlag = True
    for day in date_range(*span):
        if day.weekday() == 5:  # is Saturday
            x0 = day.replace(hour=0, minute=0, second=0, microsecond=0)
            x1 = x0 + dt.timedelta(hours=48)
            x1 = span[1] if span[1] < x1 else x1
            # print(f"x0: {x0}, x1: {x1}")
            fig.add_vrect(
                x0=x0,
                x1=x1,
                opacity=0.5,
                name="Weekend",
                fillcolor="gray",
                legendgroup="weekend",
                showlegend=firstLegendFlag,
                line_width=0,
            )
            firstLegendFlag = False


def quarter_gantt():
    monthColor = {
        1: "lightskyblue",
        2: "plum",
        3: "lightgreen",
        4: "coral",
        5: "gold",
        6: "aqua",
        7: "steelblue",
        8: "darkgoldenrod",
        9: "forestgreen",
        10: "#FF6000",
        11: "saddlebrown",
        12: "slateblue",
    }
    year = 2025
    s1_span = [
        dt.datetime(year=year, month=1, day=1),
        dt.datetime(year=year, month=6, day=30, hour=23, minute=59, second=59),
    ]
    year_span = [
        dt.datetime(year=year, month=1, day=1),
        dt.datetime(year=year, month=12, day=31, hour=23, minute=59, second=59),
    ]

    fig = go.Figure()
    for month in [i + 1 for i in range(5)]:
        draw_month_rect(fig, 2025, month, monthColor[month])
    draw_weekend_rects(fig, s1_span)

    fig.add_trace(go.Scatter(x=[dt.datetime.now()], y=[4], name="dot"))

    fig.update_layout(xaxis=dict(range=s1_span))
    fig.show()


def make_prio_list():
    q1_sched = TomlTime.from_filename("2025_q1.toml")
    pprint(q1_sched.data)
    q1_sched.sort_tasks_priority(q1_sched.data)
    pprint(q1_sched.priorityDict)


def main():
    # quarter_gantt()
    # make_prio_list()
    total_time()


if __name__ == "__main__":
    main()
