import yaml
import os
from source.singleton import singleton

FILE = os.path.abspath(__file__)
CURDIR = os.path.dirname(FILE)
DEFAULT_CONFIG = os.path.join(CURDIR, "config.yml")


@singleton
class Config:
    def __init__(self, filename=DEFAULT_CONFIG) -> None:
        self.data = self.load(filename)
        self.isvalid()  # ensure we have a valid config in file.

    def __str__(self):
        return str(self.data)

    @property
    def dateformat(self):
        return self.data["global"]["date-format"]

    @property
    def currency(self):
        return self.data["global"]["currency"]

    @property
    def amountdisplaystyle(self):
        return self.data["global"]["amount-display-style"]

    @property
    def amountdecimalplaces(self):
        return self.data["global"]["amount-decimal-places"]

    @property
    def decimalsinhrformat(self):
        return self.data["global"]["amount-decimal-places-in-human-readable-format"]

    def load(self, filename):
        try:
            with open(filename, "r") as config_file:
                config = yaml.safe_load(config_file)
                return config
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return None

    def isvalid(self):
        assert self.amountdecimalplaces in [
            0,
            2,
        ], "Number of decimal places can only be 0 or 2"
        assert self.amountdisplaystyle in [
            "comma-separated",
            "human-readable",
        ], "amount display style can be either comma separated or human-readable"
        assert self.decimalsinhrformat in [
            0,
            1,
            2,
        ], "Number of decimal places in human readable format can either be 0, 1 or 2"


if __name__ == "__main__":
    config = Config()
    print(config.amountdecimalplaces)
    print(config.currency)

    config2 = Config()

    print(config is config2)
