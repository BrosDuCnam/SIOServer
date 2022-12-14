from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
from Utils.vector import Vector


@dataclass
class ThrowData:
    object_name: str
    location: Vector
    velocity: Vector

    def __init__(self, data: object):
        self.object_name = data["object_name"]
        self.location = data["location"]
        self.velocity = data["velocity"]

    def __init__(self):
        self.object_name = ""
        self.location = Vector(0, 0, 0)
        self.velocity = Vector(0, 0, 0)

    def toJSON(self):
        throwdata_json = ThrowDataJSON(self)
        return throwdata_json.to_dict()

    @staticmethod
    def get_random():
        data = ThrowData()
        data.object_name = ""
        data.location = Vector.random3D()
        data.velocity = Vector.random3D() * 1000
        return data


@dataclass_json
@dataclass
class ThrowDataJSON:
    object_name: str
    location: tuple
    velocity: tuple

    def __init__(self, data: ThrowData):
        self.object_name = data.object_name
        self.location = data.location.values
        self.velocity = data.velocity.values
