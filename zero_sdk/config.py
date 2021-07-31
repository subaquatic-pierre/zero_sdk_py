import os
from pathlib import Path
from zero_sdk.utils import from_json

BASE_DIR = Path(__file__).resolve().parent.resolve().parent.resolve()
conf_path = os.path.join(BASE_DIR, "config.json")
conf_obj = from_json(conf_path)


class Config:
    def from_object(self, conf_obj):
        for key, val in conf_obj.items():
            self.__setattr__(key, val)

    def __str__(self):
        return f"The best"


config = Config()
config.from_object(conf_obj)
