from zero_sdk.config import Config
from zero_sdk.utils import from_json

conf_obj = from_json("../config.json")
config = Config()
config.from_object(conf_obj)
