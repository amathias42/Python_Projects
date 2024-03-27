import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pint

ureg = pint.UnitRegistry()
R = 499e3  # 499kΩ
C = 0.1e-6  # 0.1µF

tRange = np.arange(500) * 0.001  # 0-500 ms
vRange = 2.45 * (1 - np.exp(-tRange / (R * C)))

fig = go.Figure(go.Scatter(x=tRange, y=vRange, name="OC Alarm RC charge", mode="lines"))
fig.update_layout(
    title="OC Alarm RC charge",
    xaxis_title="Time (s)",
    yaxis_title="Capacitor Voltage (V)",
)

st.write(fig)


# Fixed hardware OC alarm level
ureg.default_format = ".2f"

st.header("Hardware OC limit w/ 12V,1A load, 50mΩ sense resistor")


col1, col2 = st.columns(2)

with col1:
    st.image("./imgs/IIB_CH1_current_sense.png", caption="Current sense schematic")
    st.image(
        "./imgs/IIB_CH1_OC_hard_comparators.png",
        caption="Harware threshold comparators for OC alarm",
    )


Rsense = 50e-3 * ureg.ohm
col1.write("Rsense = " + str(Rsense))
ImaxLoad = 1 * ureg.amp
col1.write("ImaxLoad = " + str(ImaxLoad))


col2.image(
    "./imgs/IIB_current_sense_chip_app_note.png", caption="Current sense chip app note"
)


Vsense = Rsense * ImaxLoad
col1.write("Vsense = ImaxLoad * Rsense = " + str(Vsense.to("V")))
Rin = 100 * ureg.ohm
col1.write("Rin = " + str(Rin))
Iout = Vsense / Rin
col1.write("Iout = Vsense / Rin = " + str(Iout.to("mA")))
Rout = 9.09e3 * ureg.ohm
col1.write("Rout = " + str(Rout))
Vout = Iout * Rout
col1.write("Vout = CH1_CURRENT = Iout * Rout = " + str(Vout.to("V")))
R129 = 10e3 * ureg.ohm
R128 = 12.1e3 * ureg.ohm
Ch1_level_thresh = 5 * ureg.volt * (R128 / (R128 + R129))
col1.write("CH1_LEVEL_THRESHOLD = 5V * R128/(R128+R129) = " + str(Ch1_level_thresh))


col1.subheader("Current limit with hardware alarm:")

trip_Iout = Ch1_level_thresh / Rout
col1.write(
    "Iout that trips hardware OC alarm = CH1_LEVEL_THRESHOLD / Rout = trip_Iout = "
    + str(trip_Iout.to("mA"))
)
trip_Vsense = trip_Iout * Rin
col1.write(
    "Vsense that trips harware OC alarm = trip_Iout * Rin = trip_Vsense = "
    + str(trip_Vsense.to("V"))
)
trip_Iload = trip_Vsense / Rsense
col1.write(
    "Current that trips CH1_LEVEL_THRESHOLD = trip_Vsense / Rsense = "
    + str(trip_Iload.to("A"))
)
col2.image(
    "./imgs/IIB_CH1_OC_hard_thresh.png", caption="Hardware threshold set for OC alarm"
)
