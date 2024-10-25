import math


class Component:
    def __init__(self, value, unit) -> None:
        self.SCALES = {
            "p": 10**-12,
            "n": 10**-9,
            "u": 10**-6,
            "m": 10**-3,
            "": 1,
            "k": 10**3,
            "M": 10**6,
            "G": 10**9,
        }
        self.SCALES_TO_STR = {v: k for k, v in self.SCALES.items()}
        self.UNIT_TYPES = ("F", "H")

        if not self.validate_unit(unit):
            raise ValueError(
                f"Invalid unit: should be string combination of any 1 character from the scale list ({self.SCALES.keys()}) and any 1 character from the unit type list ({self.UNIT_TYPES})"
            )

        self.type = unit[-1]
        self.scale = self.SCALES[unit[0]]
        self.inputValue = value
        self.value = self.inputValue * self.scale

    def __str__(self) -> str:
        return f"{self.inputValue} {self.SCALES_TO_STR[self.scale]}{self.type}"

    def validate_unit(self, unit):
        if type(unit) is not str:
            return False
        if len(unit) != 2:
            return False
        if unit[-1] not in self.UNIT_TYPES:
            return False
        if unit[:-1] not in self.SCALES:
            return False
        return True

    def to_X(self, freq):
        if self.type == "H":
            return self.value * 2 * math.pi * freq
        elif self.type == "F":
            return -1 / (self.value * 2 * math.pi * freq)

    def X_to_str(self, x, freq):
        if x > 0:
            val = x / (2 * math.pi * freq)
            scale = 10 ** (3 * math.floor(math.log10(abs(val)) / 3))
            scaleChar = self.SCALES_TO_STR[scale]
            return f"{val / scale:3.1f} {scaleChar}H"
        elif x < 0:
            val = -1 / (x * 2 * math.pi * freq)
            scale = 10 ** (3 * math.floor(math.log10(abs(val)) / 3))
            scaleChar = self.SCALES_TO_STR[scale]
            return f"{val / scale:3.1f} {scaleChar}F"
        else:
            return "0"

    def z_match(self, freq, target=0):
        if type(target) is Component:
            target = target.to_X(freq)

        return self.X_to_str(target - self.to_X(freq), freq)
