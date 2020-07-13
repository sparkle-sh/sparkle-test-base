import dataclasses
import enum


class DeviceType(enum.Enum):
    SWITCHABLE = 1
    SENSOR = 2


@dataclasses.dataclass
class Device(object):
    dtype: DeviceType
    name: str
    description: str

    def serialize(self) -> dict:
        return {
            "type": self.dtype.value,
            "name": self.name,
            "description": self.description
        }
