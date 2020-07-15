import dataclasses
import enum


class DeviceType(enum.Enum):
    SWITCHABLE = 1
    SENSOR = 2


class Datasheet(object):
    def serialize(self) -> dict:
        raise NotImplementedError


@dataclasses.dataclass
class SwitchableDeviceDatasheet(Datasheet):
    states: []

    def serialize(self) -> dict:
        return {
            "states": self.states
        }


@dataclasses.dataclass
class SensorDeviceDatasheet(Datasheet):
    labels: []

    def serialize(self) -> dict:
        return {
            "labels": self.labels
        }


@dataclasses.dataclass
class Device(object):
    dtype: DeviceType = DeviceType.SWITCHABLE
    name: str = 'example_name'
    description: str = 'example_description'
    datasheet: Datasheet = SwitchableDeviceDatasheet()

    def serialize(self) -> dict:
        return {
            "type": self.dtype.value,
            "name": self.name,
            "description": self.description,
            "datasheet":  self.datasheet.serialize()
        }
