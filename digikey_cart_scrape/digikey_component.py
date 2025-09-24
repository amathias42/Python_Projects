from dataclasses import dataclass


@dataclass
class DigikeyComponent:
    lineNumber: int
    partNumber: str
    link: str
    description: str
    quantity: int
    unitPrice: float

    def to_dict(self):
        return {
            "lineNumber": self.lineNumber,
            "partNumber": self.partNumber,
            "link": self.link,
            "description": self.description,
            "quantity": self.quantity,
            "unitPrice": self.unitPrice,
        }

    @classmethod
    def from_dict(cls, d):

        return cls(
            d["lineNumber"],
            d["partNumber"],
            d["link"],
            d["description"],
            d["quantity"],
            d["unitPrice"],
        )
