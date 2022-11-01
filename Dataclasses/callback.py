from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json


@dataclass_json
@dataclass
class Callback:
    success: bool
    message: str = ""
    data: object = None

    def toJSON(self):
        callback_json = Callback(self.success, self.message, json.dumps(self.data))
        return callback_json.to_dict()
