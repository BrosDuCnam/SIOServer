from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
from Utils.vector import Vector


@dataclass_json
@dataclass
class ThrowData:
    object_name: str
    location: Vector
    velocity: Vector

    def __init__(self, data: object):
        self.object_name = data["object_name"]
        self.location = data["location"]
        self.velocity = data["velocity"]

    @staticmethod
    def get_random():
        data = ThrowData()
        data.object_name = ""
        data.location = Vector.random3D().normalize()
        data.velocity = Vector.random3D().normalize()
        return data
