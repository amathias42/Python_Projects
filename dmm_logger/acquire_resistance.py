import datetime as dt
import pyvisa  # type: ignore pylint: disable=import-error

from dmm_driver import DMM_Driver

resList = []
with DMM_Driver() as dmm:
    try:
        print("Measuring Resistance...")
        while True:
            now = dt.datetime.now(dt.UTC)
            res = dmm.measure_resistance(100, 0.00015)
            resList.append(f"{now.strftime("%b-%d-%Y_T_%H:%M:%S.%f")}, {res}\n")
    except (KeyboardInterrupt, pyvisa.errors.VisaIOError):
        print("Stopping")

with open("instron_res_run_4.csv", mode="w", encoding="utf-8") as f:
    for r in resList:
        f.write(r)
