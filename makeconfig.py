# makeconfig.py
# This script generates secret keys, unique node IDs, and sets other configuration variables

from uuid import uuid4
import json


class Config:
    def __init__(self):
        self._key = str(uuid4()).replace('-', '')
        self._nodeid = str(uuid4()).replace('-', '')
        self._debug = True
        self._host = "localhost"
        self._nodename = "mynode"
        self._nodetype = "full"

    def as_json(self):
        return json.dumps(self.__dict__)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self):
        self._key = str(uuid4()).replace('-', '')

    @property
    def nodeid(self):
        return self._nodeid

    @nodeid.setter
    def nodeid(self, value):
        self._nodeid = value


    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if type(value) != bool:
            print("Debug mode must be a boolean value")
        else:
            self._debug = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def nodename(self):
        return self._nodename

    @nodename.setter
    def nodename(self, value):
        self._nodename = value

    @property
    def nodetype(self):
        return self._nodetype

    @nodetype.setter
    def nodetype(self, value):
        self._nodetype = value


if __name__ == "__main__":
    config = Config()
    with open("./config.json", mode="w") as f:
        print(config.as_json(), file=f)
