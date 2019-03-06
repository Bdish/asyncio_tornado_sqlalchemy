import logging
from configparser import ConfigParser
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

configFile = ConfigParser()
configFile.read('config.ini')
config = configFile

logging.basicConfig(filename=config.get("async_log", "logfile"), level=logging.DEBUG, \
                    format='[%(asctime)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S %z')