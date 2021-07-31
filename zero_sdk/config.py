from zero_sdk.utils import from_json

conf_obj = from_json("../config.json")


class Config:
    def from_object(self, conf_obj):
        for key, val in conf_obj.items():
            self.__setattr__(key, val)


config = Config.from_object(conf_obj)
