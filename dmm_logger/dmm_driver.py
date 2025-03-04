import pyvisa
import toml
from pprint import pprint


class DMM_Driver:
    def __init__(self, configFile: str = "config.toml") -> None:
        with open(configFile, mode="r", encoding="utf-8") as f:
            config = toml.load(f)
        self.dmmAddr = config["dmm"]["ip"]
        self.dmmTimeout = config["dmm"]["timeout"]

        self.rm = pyvisa.ResourceManager("@py")

        self.dmm = self.rm.open_resource(
            f"TCPIP::{self.dmmAddr}::inst0::INSTR",
            read_termination=config["dmm"]["read_termination"],
            write_termination=config["dmm"]["write_termination"],
        )
        print(config["dmm"]["read_termination"])

    def __enter__(self):
        return self

    def close(self):
        if self.dmm is not None:
            self.dmm.close()
        self.rm.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def measure_resistance(self, ohmRange: int, resolution: float = None) -> float:
        queryStr = f"MEAS:RES? {ohmRange}"
        if resolution is not None:
            queryStr += f", {resolution}"
        # pprint(queryStr)
        try:
            return float(self.dmm.query(queryStr))
        except pyvisa.errors.VisaIOError:
            self.print_dmm_err()

    def configure_resistance(self, ohmRange: int, resolution: float = None) -> None:
        queryStr = f"MEAS:RES? {ohmRange}"
        if resolution is not None:
            queryStr += f", {resolution}"
        try:
            return float(self.dmm.query(queryStr))
        except pyvisa.errors.VisaIOError:
            self.print_dmm_err()

    def print_dmm_err(self) -> None:
        print(f"DMM error: {self.dmm.query("SYST:ERR?")}")
