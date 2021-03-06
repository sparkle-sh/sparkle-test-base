from typing import List
import dataclasses
import enum


class DeviceType(enum.Enum):
    SWITCHABLE = 0
    SENSOR = 1


class Datasheet(object):
    def serialize(self) -> dict:
        raise NotImplementedError


@dataclasses.dataclass
class SwitchableDeviceDatasheet(Datasheet):
    states: List[int] = dataclasses.field(default_factory=list)

    def serialize(self) -> dict:
        return {
            "states": self.states
        }


@dataclasses.dataclass
class SensorDeviceDatasheet(Datasheet):
    labels: List[str] = dataclasses.field(default_factory=list)

    def serialize(self) -> dict:
        return {
            "labels": self.labels
        }


@dataclasses.dataclass
class Device(object):
    dtype: DeviceType = DeviceType.SWITCHABLE
    name: str = 'example_name'
    description: str = 'example_description'
    datasheet: Datasheet = SwitchableDeviceDatasheet([0, 1])

    def serialize(self) -> dict:
        return {
            "type": self.dtype.value,
            "name": self.name,
            "description": self.description,
            "datasheet": self.datasheet.serialize()
        }
