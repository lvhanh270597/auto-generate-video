import os
from configparser import ConfigParser

config = ConfigParser()
configFile = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'hale.ini'
)
config.read(configFile)