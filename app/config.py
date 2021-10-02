from dotenv import dotenv_values
import os

_here = os.path.dirname(os.path.realpath(__file__))


class _Config:
    """Class containing all global configs"""

    def __init__(self):
        _path = _here + "/../.env"
        config = dotenv_values(_path)
        self.PORT = int(config.get("PORT", 8000))
        self.PROJECT_NAME = config.get("PROJECT_NAME", "Wealth-A-Lot")
        self.DEBUG = config.get("DEBUG", "1") == "1"
        self.RELOAD = config.get("RELOAD", "1") == "1"


class _Config_Keys:
    """Class for initializing Private and Public Key"""

    def __init__(self):
        _keyPath = _here + "/../keys/"
        try:
            with open(_keyPath + "public_key.pem", "rb") as f:
                self.PUBLIC_KEY = f.read()
            with open(_keyPath + "private_key.pem", "rb") as f:
                self.PRIVATE_KEY = f.read()
        except FileNotFoundError:
            raise Exception("Public and Private keys not found.")
        except Exception as e:
            print(f"Something went wrong while reading the keys, {e!r}")


class _Api_Keys:
    """Class for initializing API keys"""

    def __init__(self):
        _path = _here + "/../.env"
        config = dotenv_values(_path)
        self.CLIENT_API_KEY = config.get("CLIENT_API_KEY", "")
        self.AA_API_KEY = config.get("AA_API_KEY", "")


config = _Config()
keys = _Config_Keys()
api_keys = _Api_Keys()
