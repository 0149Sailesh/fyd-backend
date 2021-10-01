from dotenv import dotenv_values
import os


class Config:
    """Class containing all global configs"""

    def __init__(self):
        _dir_path = os.path.dirname(os.path.realpath(__file__))
        _path = _dir_path + "/../.env"
        config = dotenv_values(_path)
        self.PORT = int(config.get("PORT", 8000))
        self.PROJECT_NAME = config.get("PROJECT_NAME", "Wealth-A-Lot")
        self.DEBUG = config.get("DEBUG", "1") == "1"
        self.RELOAD = config.get("RELOAD", "1") == "1"
