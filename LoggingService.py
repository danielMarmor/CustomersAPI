import logging
from datetime import datetime
from configparser import ConfigParser
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# singelton
class CustomersLogger:
    _instance = None

    def __init__(self):
        raise Exception('Cannot Init FlightsLogger')

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.Logger = cls.create_logger(cls)
        return cls._instance

    def create_logger(self):
        for handler in logging.root.handlers:
            logging.root.removeHandler(handler)
        # CONFIG
        config_file_name = 'config.conf'
        config_file_location = os.path.join(ROOT_DIR, config_file_name)
        config = ConfigParser()
        config.read(config_file_location)
        log_level = config['logging']['log_level']
        log_file_name = config['logging']['log_file_name']
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # NEW
        logger = logging.getLogger('FlightsLogger')
        logger.setLevel(log_level)
        log_file_location = os.path.join(ROOT_DIR, log_file_name)
        # FILE HANDLER
        file_handler = logging.FileHandler(log_file_location)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger





